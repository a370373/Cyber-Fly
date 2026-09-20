from __future__ import annotations

import numpy as np

from .environment import ScreenFrame


class ScreenVision:
    """Provide complete screen frames to the fly's visual system."""

    def __init__(self):
        pass

    def frame(self, screen: ScreenFrame) -> np.ndarray:
        """Return the complete RGB/RGBA screen as normalized float32 data."""

        pixels = np.asarray(screen.pixels)

        if pixels.ndim == 2:
            pixels = pixels[..., None]

        if pixels.ndim != 3:
            raise ValueError(
                "ScreenFrame.pixels must be a 2-D grayscale "
                "or 3-D RGB/RGBA array"
            )

        if pixels.shape[2] not in (1, 3, 4):
            raise ValueError(
                f"unsupported channel count: {pixels.shape[2]}"
            )

        pixels = pixels.astype(np.float32, copy=False)

        if pixels.size == 0:
            return pixels

        if float(np.nanmax(pixels)) > 1.0:
            pixels /= 255.0

        return np.clip(pixels, 0.0, 1.0)
