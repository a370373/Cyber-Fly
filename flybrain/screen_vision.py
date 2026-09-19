from __future__ import annotations

import numpy as np

from .environment import ScreenFrame
from .eyes import Blob


class ScreenVision:
    """Convert arbitrary RGB/RGBA screen frames into horizontal visual blobs."""

    def __init__(
        self,
        threshold: float = 0.20,
        horizontal_bins: int = 64,
    ):
        self.threshold = float(np.clip(threshold, 0.0, 1.0))
        self.horizontal_bins = max(8, int(horizontal_bins))

    def _normalize(self, frame: ScreenFrame) -> np.ndarray:
        pixels = np.asarray(frame.pixels)

        if pixels.ndim == 3:
            if pixels.shape[2] >= 3:
                pixels = pixels[..., :3].mean(axis=2)
            elif pixels.shape[2] == 1:
                pixels = pixels[..., 0]
            else:
                raise ValueError("unsupported channel count")

        if pixels.ndim != 2:
            raise ValueError(
                "ScreenFrame.pixels must be a 2-D grayscale or 3-D RGB/RGBA array"
            )

        pixels = pixels.astype(np.float32, copy=False)

        if pixels.size == 0:
            return np.empty((0, 0), dtype=np.float32)

        if float(np.nanmax(pixels)) > 1.0:
            pixels /= 255.0

        return np.clip(pixels, 0.0, 1.0)

    def detect(self, frame: ScreenFrame) -> list[Blob]:
        """Convert a complete screen into horizontally distributed visual blobs."""

        pixels = self._normalize(frame)

        if pixels.size == 0:
            return []

        height, width = pixels.shape

        if width <= 0 or height <= 0:
            return []

        darkness = 1.0 - pixels
        profile = darkness.mean(axis=0)

        bins = min(self.horizontal_bins, width)
        edges = np.linspace(0, width, bins + 1, dtype=np.int32)

        blobs: list[Blob] = []

        for i in range(bins):
            x0 = int(edges[i])
            x1 = int(edges[i + 1])

            if x1 <= x0:
                continue

            strength = float(profile[x0:x1].mean())

            if strength < self.threshold:
                continue

            center_px = (x0 + x1 - 1) * 0.5

            center = (
                2.0 * center_px / max(width - 1, 1)
            ) - 1.0

            half_width = (
                max(1.0, x1 - x0) / max(width, 1)
            ) * 0.5

            blobs.append(
                Blob(
                    center=float(np.clip(center, -1.0, 1.0)),
                    half_width=float(np.clip(half_width, 0.01, 1.0)),
                    darkness=float(np.clip(strength, 0.0, 1.0)),
                )
            )

        return blobs
