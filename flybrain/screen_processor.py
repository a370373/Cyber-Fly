from __future__ import annotations

import numpy as np

from .brain import FlyBrain
from .environment import ScreenFrame
from .eyes import Eyes
from .screen_vision import ScreenVision


class ScreenProcessor:
    """Connect a complete screen frame to the fly's visual system."""

    def __init__(self, brain: FlyBrain):
        self.brain = brain
        self.eyes = Eyes(brain.azimuth)
        self.vision = ScreenVision()

    def step(self, frame: ScreenFrame) -> np.ndarray:
        """Process the complete screen through the fly's visual system."""

        pixels = self.vision.frame(frame)
        eye_drive = self.eyes.drive(pixels)

        return self.brain.step(eye_drive)
