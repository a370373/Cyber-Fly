from __future__ import annotations

import numpy as np

from .brain import FlyBrain
from .environment import ScreenFrame
from .eyes import Eyes
from .screen_vision import ScreenVision


class ScreenProcessor:
    """Connect a screen environment to the fly's visual system and brain."""

    def __init__(self, brain: FlyBrain):
        self.brain = brain
        self.eyes = Eyes(brain.azimuth)
        self.vision = ScreenVision()

    def step(self, frame: ScreenFrame) -> np.ndarray:
        blobs = self.vision.detect(frame)
        eye_drive = self.eyes.drive(blobs)
        return self.brain.step(eye_drive)
