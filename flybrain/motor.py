from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class ActionType(str, Enum):
    NONE = "none"

    # Pointer / touch actions
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    LONG_PRESS = "long_press"
    RELEASE = "release"
    SWIPE = "swipe"
    LONG_PRESS_DRAG = "long_press_drag"

    # Abstract movement
    MOVE_FORWARD = "move_forward"
    MOVE_BACKWARD = "move_backward"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"

    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"

    ESCAPE_LEFT = "escape_left"
    ESCAPE_RIGHT = "escape_right"

    ATTACK_LEFT = "attack_left"
    ATTACK_RIGHT = "attack_right"

    # Generic input
    KEY_PRESS = "key_press"
    KEY_RELEASE = "key_release"

    SCROLL_UP = "scroll_up"
    SCROLL_DOWN = "scroll_down"


@dataclass
class Action:
    type: ActionType = ActionType.NONE

    x: float = 0.0
    y: float = 0.0
    x2: float = 0.0
    y2: float = 0.0

    duration: float = 0.0

    # Optional abstract input name.
    # Bridge decides how this is implemented.
    key: str | None = None


@dataclass
class ActionCombo:
    actions: list[Action] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return len(self.actions) == 0


class MotorDecoder:
    """
    Convert MaleCNS motor-group activity into platform-independent actions.

    The decoder does NOT know Android, PC, games, keyboards, or mouse APIs.
    Those mappings belong to external Bridges.

    Motor groups:
        forward_L / forward_R
        steer_L / steer_R
        escape_L / escape_R
        backward_L / backward_R
        punch_L / punch_R
        kick_L / kick_R
    """

    GROUPS = (
        "forward_L",
        "forward_R",
        "steer_L",
        "steer_R",
        "escape_L",
        "escape_R",
        "backward_L",
        "backward_R",
        "punch_L",
        "punch_R",
        "kick_L",
        "kick_R",
    )

    def __init__(self, brain, threshold: int = 1):
        self.brain = brain
        self.threshold = max(1, int(threshold))

        self.motor_groups = {
            name: np.asarray(
                getattr(brain, f"_group_{name}", []),
                dtype=np.int32,
            )
            for name in self.GROUPS
        }

        # Fallback to brain.groups.
        if not any(len(v) for v in self.motor_groups.values()):
            for name in self.GROUPS:
                try:
                    idx = brain.groups[name]
                    self.motor_groups[name] = np.asarray(
                        idx,
                        dtype=np.int32,
                    )
                except (KeyError, TypeError, AttributeError):
                    self.motor_groups[name] = np.empty(0, dtype=np.int32)

        self._pressed = False

    def _activity(self, fired):
        fired = np.asarray(fired, dtype=np.int32)

        if fired.size == 0:
            return {name: 0 for name in self.GROUPS}

        fired_set = set(int(x) for x in fired)

        return {
            name: sum(
                int(i) in fired_set
                for i in indices
            )
            for name, indices in self.motor_groups.items()
        }

    def _active(self, activity, name):
        return activity[name] >= self.threshold

    def decode(self, fired) -> Action:
        """
        Preserve the original single-action API.

        For multiple simultaneous motor groups use decode_combo().
        """

        combo = self.decode_combo(fired)

        if combo.empty:
            return Action()

        return combo.actions[0]

    def decode_combo(self, fired) -> ActionCombo:
        """
        Decode all active motor groups.

        Multiple groups are preserved instead of being discarded.
        """

        activity = self._activity(fired)
        actions: list[Action] = []

        forward_l = self._active(activity, "forward_L")
        forward_r = self._active(activity, "forward_R")

        steer_l = self._active(activity, "steer_L")
        steer_r = self._active(activity, "steer_R")

        escape_l = self._active(activity, "escape_L")
        escape_r = self._active(activity, "escape_R")

        backward_l = self._active(activity, "backward_L")
        backward_r = self._active(activity, "backward_R")

        punch_l = self._active(activity, "punch_L")
        punch_r = self._active(activity, "punch_R")

        kick_l = self._active(activity, "kick_L")
        kick_r = self._active(activity, "kick_R")

        # ------------------------------------------------------------
        # Movement
        # ------------------------------------------------------------

        if forward_l or forward_r:
            actions.append(
                Action(
                    type=ActionType.MOVE_FORWARD,
                    x=0.50,
                    y=0.50,
                )
            )

        if backward_l or backward_r:
            actions.append(
                Action(
                    type=ActionType.MOVE_BACKWARD,
                    x=0.50,
                    y=0.50,
                )
            )

        if forward_l and not forward_r:
            actions.append(
                Action(
                    type=ActionType.MOVE_LEFT,
                    x=0.25,
                    y=0.50,
                )
            )

        if forward_r and not forward_l:
            actions.append(
                Action(
                    type=ActionType.MOVE_RIGHT,
                    x=0.75,
                    y=0.50,
                )
            )

        # ------------------------------------------------------------
        # Steering
        # ------------------------------------------------------------

        if steer_l:
            actions.append(
                Action(
                    type=ActionType.TURN_LEFT,
                    x=0.35,
                    y=0.50,
                )
            )

        if steer_r:
            actions.append(
                Action(
                    type=ActionType.TURN_RIGHT,
                    x=0.65,
                    y=0.50,
                )
            )

        # ------------------------------------------------------------
        # Escape
        # ------------------------------------------------------------

        if escape_l:
            actions.append(
                Action(
                    type=ActionType.ESCAPE_LEFT,
                    x=0.25,
                    y=0.50,
                )
            )

        if escape_r:
            actions.append(
                Action(
                    type=ActionType.ESCAPE_RIGHT,
                    x=0.75,
                    y=0.50,
                )
            )

        # ------------------------------------------------------------
        # Punch
        #
        # Preserve existing behavior:
        #   one side  -> CLICK
        #   both sides -> DOUBLE_CLICK
        # ------------------------------------------------------------

        if punch_l and punch_r:
            actions.append(
                Action(
                    type=ActionType.DOUBLE_CLICK,
                    x=0.50,
                    y=0.50,
                )
            )

        elif punch_l:
            actions.append(
                Action(
                    type=ActionType.CLICK,
                    x=0.35,
                    y=0.50,
                )
            )

        elif punch_r:
            actions.append(
                Action(
                    type=ActionType.CLICK,
                    x=0.65,
                    y=0.50,
                )
            )

        # Also expose the abstract attack direction.
        if punch_l:
            actions.append(
                Action(
                    type=ActionType.ATTACK_LEFT,
                    x=0.35,
                    y=0.50,
                )
            )

        if punch_r:
            actions.append(
                Action(
                    type=ActionType.ATTACK_RIGHT,
                    x=0.65,
                    y=0.50,
                )
            )

        # ------------------------------------------------------------
        # Kick / dragging
        #
        # Preserve existing behavior:
        #   kick side -> SWIPE
        #   both sides -> LONG_PRESS_DRAG
        # ------------------------------------------------------------

        if kick_l and kick_r:
            actions.append(
                Action(
                    type=ActionType.LONG_PRESS_DRAG,
                    x=0.30,
                    y=0.50,
                    x2=0.70,
                    y2=0.50,
                    duration=0.80,
                )
            )

        elif kick_l:
            actions.append(
                Action(
                    type=ActionType.SWIPE,
                    x=0.50,
                    y=0.50,
                    x2=0.20,
                    y2=0.50,
                    duration=0.30,
                )
            )

        elif kick_r:
            actions.append(
                Action(
                    type=ActionType.SWIPE,
                    x=0.50,
                    y=0.50,
                    x2=0.80,
                    y2=0.50,
                    duration=0.30,
                )
            )

        # ------------------------------------------------------------
        # Long press / release state
        #
        # A sustained motor state can be interpreted by the Bridge as
        # a long press. The actual physical implementation remains
        # Bridge-specific.
        # ------------------------------------------------------------

        pointer_active = (
            punch_l
            or punch_r
            or kick_l
            or kick_r
        )

        if pointer_active and not self._pressed:
            actions.append(
                Action(
                    type=ActionType.LONG_PRESS,
                    x=0.50,
                    y=0.50,
                    duration=0.50,
                )
            )
            self._pressed = True

        elif not pointer_active and self._pressed:
            actions.append(
                Action(
                    type=ActionType.RELEASE,
                    x=0.50,
                    y=0.50,
                )
            )
            self._pressed = False

        return ActionCombo(actions)

    def observe(self, fired):
        """
        Return complete motor activity plus all decoded actions.
        """

        activity = self._activity(fired)
        combo = self.decode_combo(fired)

        return activity, combo

    def active_groups(self, fired):
        """
        Return only currently active MaleCNS motor groups.
        """

        activity = self._activity(fired)

        return {
            name: count
            for name, count in activity.items()
            if count >= self.threshold
        }
