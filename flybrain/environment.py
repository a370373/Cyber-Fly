from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


@dataclass
class ScreenFrame:
    """A normalized screen frame supplied by an external environment."""

    pixels: np.ndarray
    width: int
    height: int
    channels: int


class ScreenEnvironment(ABC):
    """Interface for external screen-based environments."""

    @abstractmethod
    def capture(self) -> ScreenFrame:
        """Capture one current screen frame."""
        raise NotImplementedError
