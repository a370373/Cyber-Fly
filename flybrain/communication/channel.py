from __future__ import annotations

from collections import deque
from typing import Any


class CommunicationChannel:
    """
    Generic bidirectional communication boundary.

    Bridge -> Cyber-Fly:
        frame / event

    Cyber-Fly -> Bridge:
        action
    """

    def __init__(self) -> None:
        self._incoming = deque()
        self._outgoing = deque()

    def send_to_core(self, message: Any) -> None:
        self._incoming.append(message)

    def receive_from_bridge(self) -> Any | None:
        if not self._incoming:
            return None
        return self._incoming.popleft()

    def send_to_bridge(self, message: Any) -> None:
        self._outgoing.append(message)

    def receive_from_core(self) -> Any | None:
        if not self._outgoing:
            return None
        return self._outgoing.popleft()

    def incoming_count(self) -> int:
        return len(self._incoming)

    def outgoing_count(self) -> int:
        return len(self._outgoing)
