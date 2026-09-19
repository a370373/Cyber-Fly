from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
import base64

import numpy as np


class MessageType(str, Enum):
    FRAME = "frame"
    EVENT = "event"
    ACTION = "action"


@dataclass
class FrameMessage:
    width: int
    height: int
    channels: int
    pixels: bytes

    type: MessageType = MessageType.FRAME

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "width": self.width,
            "height": self.height,
            "channels": self.channels,
            "pixels": base64.b64encode(self.pixels).decode("ascii"),
        }

    def encode(self) -> bytes:
        return json.dumps(self.to_dict(), separators=(",", ":")).encode()


@dataclass
class EventMessage:
    event: str
    data: dict

    type: MessageType = MessageType.EVENT

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "event": self.event,
            "data": self.data,
        }

    def encode(self) -> bytes:
        return json.dumps(self.to_dict(), separators=(",", ":")).encode()


@dataclass
class ActionMessage:
    action: str
    parameters: dict

    type: MessageType = MessageType.ACTION

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "action": self.action,
            "parameters": self.parameters,
        }

    def encode(self) -> bytes:
        return json.dumps(self.to_dict(), separators=(",", ":")).encode()


def decode_message(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))


def frame_from_array(pixels: np.ndarray) -> FrameMessage:
    pixels = np.asarray(pixels)

    if pixels.ndim == 2:
        channels = 1
    elif pixels.ndim == 3:
        channels = pixels.shape[2]
    else:
        raise ValueError("frame must be a 2-D or 3-D array")

    height, width = pixels.shape[:2]

    return FrameMessage(
        width=int(width),
        height=int(height),
        channels=int(channels),
        pixels=np.ascontiguousarray(pixels).tobytes(),
    )
