#!/usr/bin/env python3

import base64
import json
import socket
import struct
import time
from pathlib import Path

import numpy as np

from flybrain.brain import FlyBrain
from flybrain.motor import MotorDecoder
from flybrain.environment import ScreenFrame
from flybrain.screen_processor import ScreenProcessor
from flybrain.communication import (
    CommunicationChannel,
    CyberFlyGateway,
    FrameMessage,
    EventMessage,
)


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
FLY_DATA = PROJECT_ROOT / "fly-data"

HOST = "127.0.0.1"
PORT = 8765

# Maximum single TCP message payload.
# Prevents malformed clients from allocating unlimited memory.
MAX_MESSAGE_SIZE = 16 * 1024 * 1024


# ============================================================
# TCP framing
# ============================================================

def recv_exact(sock: socket.socket, size: int) -> bytes:
    """
    Receive exactly `size` bytes from a TCP socket.

    TCP is a byte stream, so one recv() does not necessarily
    correspond to one complete message.
    """
    data = bytearray()

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError("peer disconnected")

        data.extend(chunk)

    return bytes(data)


def recv_message(sock: socket.socket) -> dict:
    """
    Receive one length-prefixed JSON message.

    Format:

        4 bytes  : big-endian payload length
        N bytes  : UTF-8 JSON payload
    """
    header = recv_exact(sock, 4)

    size = struct.unpack("!I", header)[0]

    if size <= 0:
        raise ValueError("invalid message size")

    if size > MAX_MESSAGE_SIZE:
        raise ValueError(
            f"message too large: {size} bytes"
        )

    payload = recv_exact(sock, size)

    return json.loads(payload.decode("utf-8"))


def send_message(sock: socket.socket, message: bytes) -> None:
    """
    Send one length-prefixed message.
    """
    if len(message) > MAX_MESSAGE_SIZE:
        raise ValueError(
            f"message too large: {len(message)} bytes"
        )

    header = struct.pack("!I", len(message))

    sock.sendall(header + message)


# ============================================================
# Cyber-Fly Runtime
# ============================================================

class CyberFlyRuntime:
    """
    Persistent Cyber-Fly runtime.

    Android Bridge
        ↓
    localhost TCP
        ↓
    Communication Layer
        ↓
    Screen Vision
        ↓
    Eyes
        ↓
    MaleCNS
        ↓
    Motor Decoder
        ↓
    Communication Layer
        ↓
    localhost TCP
        ↓
    Android Bridge
    """

    def __init__(self):
        print("========================================")
        print("          🧠 Cyber-Fly Runtime")
        print("========================================")

        if not FLY_DATA.is_dir():
            raise FileNotFoundError(
                f"Cyber-Fly data directory not found: {FLY_DATA}"
            )

        if not (FLY_DATA / "brain.npz").is_file():
            raise FileNotFoundError(
                f"Missing brain.npz: {FLY_DATA / 'brain.npz'}"
            )

        if not (FLY_DATA / "weights.npz").is_file():
            raise FileNotFoundError(
                f"Missing weights.npz: {FLY_DATA / 'weights.npz'}"
            )

        print(f"data             : {FLY_DATA}")

        # ----------------------------------------------------
        # Core
        # ----------------------------------------------------

        self.brain = FlyBrain(data=FLY_DATA)

        # ----------------------------------------------------
        # Vision → MaleCNS
        # ----------------------------------------------------

        self.screen = ScreenProcessor(self.brain)

        # ----------------------------------------------------
        # MaleCNS → abstract motor actions
        # ----------------------------------------------------

        self.motor = MotorDecoder(self.brain)

        # ----------------------------------------------------
        # Platform-independent Communication Layer
        # ----------------------------------------------------

        self.channel = CommunicationChannel()
        self.gateway = CyberFlyGateway(self.channel)

        self.running = True

        print(f"neurons          : {self.brain.n}")
        print(f"visual receptors : {len(self.brain.visual)}")
        print("motor groups     : 12")
        print("communication    : READY")
        print("vision           : READY")
        print("motor            : READY")
        print(f"tcp server       : {HOST}:{PORT}")
        print("runtime          : READY")
        print()
        print(
            "[WAIT] Cyber-Fly is waiting for Android Bridge..."
        )

    # ========================================================
    # Frame conversion
    # ========================================================

    @staticmethod
    def _frame_message_from_dict(data: dict) -> FrameMessage:
        """
        Convert a network JSON object into the existing
        platform-independent FrameMessage.
        """

        if data.get("type") != "frame":
            raise ValueError("message is not a frame")

        width = int(data["width"])
        height = int(data["height"])
        channels = int(data["channels"])

        if width <= 0 or height <= 0:
            raise ValueError("invalid frame dimensions")

        if channels <= 0:
            raise ValueError("invalid channel count")

        pixels_b64 = data.get("pixels")

        if not isinstance(pixels_b64, str):
            raise ValueError("frame pixels must be base64 string")

        pixels = base64.b64decode(
            pixels_b64,
            validate=True,
        )

        expected = width * height * channels

        if len(pixels) != expected:
            raise ValueError(
                "invalid frame payload: "
                f"expected {expected} bytes, "
                f"got {len(pixels)}"
            )

        return FrameMessage(
            width=width,
            height=height,
            channels=channels,
            pixels=pixels,
        )

    @staticmethod
    def _frame_to_screen_frame(
        message: FrameMessage,
    ) -> ScreenFrame:
        """
        Convert FrameMessage into ScreenFrame.
        """

        pixels = np.frombuffer(
            message.pixels,
            dtype=np.uint8,
        )

        expected = (
            message.width
            * message.height
            * message.channels
        )

        if pixels.size != expected:
            raise ValueError(
                f"invalid frame payload: "
                f"expected {expected} bytes, "
                f"got {pixels.size}"
            )

        if message.channels == 1:
            shape = (
                message.height,
                message.width,
            )
        else:
            shape = (
                message.height,
                message.width,
                message.channels,
            )

        pixels = pixels.reshape(shape)

        return ScreenFrame(
            pixels=pixels,
            width=message.width,
            height=message.height,
            channels=message.channels,
        )

    # ========================================================
    # Action serialization
    # ========================================================

    @staticmethod
    def _action_parameters(action) -> dict:
        return {
            "x": float(action.x),
            "y": float(action.y),
            "x2": float(action.x2),
            "y2": float(action.y2),
            "duration": float(action.duration),
            "key": action.key,
        }

    # ========================================================
    # Core processing
    # ========================================================

    def _process_frame(
        self,
        message: FrameMessage,
    ):
        """
        One complete:

        Frame
          ↓
        Vision
          ↓
        MaleCNS
          ↓
        Motor
          ↓
        Action
        """

        frame = self._frame_to_screen_frame(message)

        # Screen → Eyes → MaleCNS
        fired = self.screen.step(frame)

        # MaleCNS → Motor
        action = self.motor.decode(fired)

        if action is None:
            return

        # Motor → Communication Layer
        self.gateway.send_action(
            action.type.value,
            self._action_parameters(action),
        )

        print(
            f"[ACTION] {action.type.value}"
        )

    # ========================================================
    # Incoming message handling
    # ========================================================

    def _process_network_message(
        self,
        data: dict,
    ):
        message_type = data.get("type")

        if message_type == "frame":

            message = self._frame_message_from_dict(data)

            print(
                f"[FRAME] "
                f"{message.width}x{message.height} "
                f"channels={message.channels}"
            )

            self._process_frame(message)

        elif message_type == "event":

            event = str(data.get("event", "unknown"))

            event_data = data.get("data", {})

            message = EventMessage(
                event=event,
                data=dict(event_data),
            )

            print(
                f"[EVENT] {message.event}"
            )

            self._process_event(message)

        else:
            raise ValueError(
                f"unsupported message type: {message_type}"
            )

    def _process_event(
        self,
        message: EventMessage,
    ):
        """
        Handle environment events.

        Events currently do not directly modify MaleCNS.
        This keeps the protocol ready for future extensions.
        """

        print(
            f"[EVENT] {message.event}"
        )

    # ========================================================
    # Action output
    # ========================================================

    def _send_pending_actions(
        self,
        client: socket.socket,
    ):
        """
        Send every ActionMessage generated by the Core.
        """

        while True:

            action = self.gateway.receive_bridge_action()

            if action is None:
                break

            send_message(
                client,
                action.encode(),
            )

            print(
                f"[SEND] {action.action}"
            )

    # ========================================================
    # TCP server
    # ========================================================

    def _serve_client(
        self,
        client: socket.socket,
        address,
    ):
        print()
        print(
            f"[BRIDGE] connected: {address}"
        )
        print(
            "[BRIDGE] realtime communication active"
        )

        try:

            while self.running:

                data = recv_message(client)

                try:

                    self._process_network_message(
                        data
                    )

                    # Send any resulting actions
                    # immediately after processing
                    # the frame/event.
                    self._send_pending_actions(
                        client
                    )

                except Exception as exc:

                    print(
                        f"[ERROR] message processing failed: "
                        f"{exc}"
                    )

                    error = {
                        "type": "event",
                        "event": "error",
                        "data": {
                            "message": str(exc),
                        },
                    }

                    send_message(
                        client,
                        json.dumps(
                            error,
                            separators=(",", ":"),
                        ).encode("utf-8"),
                    )

        except ConnectionError:

            print(
                "[BRIDGE] disconnected"
            )

        except Exception as exc:

            print(
                f"[TCP ERROR] {exc}"
            )

        finally:

            try:
                client.close()
            except Exception:
                pass

            print(
                "[WAIT] waiting for Android Bridge..."
            )

    def run(self):
        """
        Start localhost TCP server and wait indefinitely
        for an Android Bridge connection.
        """

        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )

        server.bind(
            (HOST, PORT)
        )

        server.listen(1)

        print(
            f"[TCP] listening on "
            f"{HOST}:{PORT}"
        )

        try:

            while self.running:

                client, address = server.accept()

                self._serve_client(
                    client,
                    address,
                )

        except KeyboardInterrupt:

            print()
            print(
                "[STOP] Cyber-Fly stopped."
            )

        finally:

            self.running = False

            try:
                server.close()
            except Exception:
                pass


# ============================================================
# Entry point
# ============================================================

def main():

    runtime = CyberFlyRuntime()

    runtime.run()


if __name__ == "__main__":
    main()
