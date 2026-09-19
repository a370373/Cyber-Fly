from __future__ import annotations

import numpy as np

from .channel import CommunicationChannel
from .protocol import (
    ActionMessage,
    EventMessage,
    FrameMessage,
    MessageType,
)


class CyberFlyGateway:
    """
    Communication boundary between Cyber-Fly Core and external Bridges.

    External world -> Frame/Event -> Cyber-Fly
    Cyber-Fly -> Action -> External world

    This layer does not know Android, Windows, Linux, games,
    Accessibility APIs, or any platform-specific implementation.
    """

    def __init__(self, channel: CommunicationChannel):
        self.channel = channel

    def receive_frame(
        self,
        pixels: np.ndarray,
    ) -> None:
        pixels = np.asarray(pixels)

        if pixels.ndim not in (2, 3):
            raise ValueError(
                "frame must be a 2-D grayscale or 3-D color array"
            )

        if pixels.ndim == 2:
            channels = 1
        else:
            channels = pixels.shape[2]

        height, width = pixels.shape[:2]

        message = FrameMessage(
            width=int(width),
            height=int(height),
            channels=int(channels),
            pixels=np.ascontiguousarray(pixels).tobytes(),
        )

        self.channel.send_to_core(message)

    def receive_event(
        self,
        event: str,
        data: dict | None = None,
    ) -> None:
        message = EventMessage(
            event=str(event),
            data={} if data is None else dict(data),
        )

        self.channel.send_to_core(message)

    def send_action(
        self,
        action: str,
        parameters: dict | None = None,
    ) -> None:
        message = ActionMessage(
            action=str(action),
            parameters={} if parameters is None else dict(parameters),
        )

        self.channel.send_to_bridge(message)

    def receive_core_message(self):
        return self.channel.receive_from_bridge()

    def receive_bridge_action(self):
        return self.channel.receive_from_core()

    def pending_input(self) -> int:
        return self.channel.incoming_count()

    def pending_actions(self) -> int:
        return self.channel.outgoing_count()
