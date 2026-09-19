from __future__ import annotations

import numpy as np

from .brain import FlyBrain
from .environment import ScreenFrame
from .screen_processor import ScreenProcessor
from .motor import Action, MotorDecoder


class CyberFly:
    """Complete Cyber-Fly loop: vision -> MaleCNS -> motor action."""

    def __init__(self):
        self.brain = FlyBrain()
        self.visual = ScreenProcessor(self.brain)
        self.motor = MotorDecoder(self.brain)

    def step(self, frame: ScreenFrame) -> tuple[np.ndarray, Action]:
        fired = self.visual.step(frame)
        action = self.motor.decode(fired)
        return fired, action

    def observe(self, frame: ScreenFrame):
        fired = self.visual.step(frame)
        activity, action = self.motor.observe(fired)
        return fired, activity, action
