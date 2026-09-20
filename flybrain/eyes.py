"""Full-frame visual encoding for the MaleCNS visual input.

The environment provides a complete RGB/RGBA frame.  The visual encoder
projects that frame onto the 6,006 MaleCNS photoreceptor inputs using the
photoreceptors' azimuth positions.

The encoder keeps the full frame as its input instead of first detecting
objects or converting the scene into hand-defined blobs.
"""

from __future__ import annotations

import numpy as np


BACKGROUND = 0.9


def _normalize_frame(pixels: np.ndarray) -> np.ndarray:
    pixels = np.asarray(pixels)

    if pixels.ndim == 2:
        pixels = pixels[..., None]

    if pixels.ndim != 3:
        raise ValueError(
            "visual frame must be a 2-D grayscale or 3-D RGB/RGBA array"
        )

    if pixels.shape[2] == 1:
        pixels = np.repeat(pixels, 3, axis=2)
    elif pixels.shape[2] >= 3:
        pixels = pixels[..., :3]
    else:
        raise ValueError("unsupported channel count")

    pixels = pixels.astype(np.float32, copy=False)

    if pixels.size == 0:
        return np.empty((0, 0, 3), dtype=np.float32)

    maximum = float(np.nanmax(pixels))
    if maximum > 1.0:
        pixels /= 255.0

    return np.clip(pixels, 0.0, 1.0)


class Eyes:
    """Encode a complete visual frame into MaleCNS photoreceptor input."""

    def __init__(self, azimuth: np.ndarray):
        self.azimuth = np.asarray(azimuth, dtype=np.float32)
        self.previous: np.ndarray | None = None

    def _horizontal_projection(self, frame: np.ndarray) -> np.ndarray:
        """Project the complete 2-D frame onto the fly's panoramic axis."""

        if frame.size == 0:
            return np.zeros(len(self.azimuth), dtype=np.float32)

        height, width, _ = frame.shape

        # Full RGB input is converted to luminance only at the final
        # photoreceptor encoding stage.  The entire frame participates.
        luminance = (
            0.2126 * frame[..., 0]
            + 0.7152 * frame[..., 1]
            + 0.0722 * frame[..., 2]
        )

        # Average vertically so every horizontal position receives
        # information from the complete screen column.
        profile = luminance.mean(axis=0)

        x = ((self.azimuth + 1.0) * 0.5) * max(width - 1, 0)

        left = np.floor(x).astype(np.int32)
        right = np.minimum(left + 1, max(width - 1, 0))
        weight = x - left

        values = (
            profile[left] * (1.0 - weight)
            + profile[right] * weight
        )

        return np.clip(values, 0.0, 1.0).astype(np.float32)

    def drive(self, frame: np.ndarray) -> np.ndarray:
        """Encode a complete RGB/RGBA frame into 6006 visual inputs."""

        pixels = _normalize_frame(frame)

        if pixels.size == 0:
            return np.zeros(len(self.azimuth), dtype=np.float32)

        lum = self._horizontal_projection(pixels)

        if self.previous is None:
            change = np.zeros_like(lum)
        else:
            change = np.abs(lum - self.previous)

        self.previous = lum.copy()

        # Preserve the original fly.ai temporal-response behavior while
        # removing the Blob-based object detector.
        return np.clip(
            0.45 * lum + 1.6 * change,
            0.0,
            1.0,
        ).astype(np.float32)


# Kept for compatibility with existing experiments/imports.
ENCODER = {
    "loom_gain": 10.0,
    "loom_size": 0.0,
    "chase_base": 0.6,
    "chase_gain": 0.2,
    "threat_max": 0.8,
    "shot_gain": 10.0,
    "cap": 0.8,
}

CHANNELS = {
    "loom": ["LPLC2"],
    "threat": ["LC4"],
    "shot": ["LPLC1"],
    "chase": ["LC10a"],
}


class FeatureDetectors:
    """Optional identified-neuron visual shortcut retained for compatibility."""

    def __init__(self, brain, **encoder):
        unknown = set(encoder) - set(ENCODER)
        if unknown:
            raise ValueError(
                f"unknown encoder parameters: {sorted(unknown)}"
            )

        self.p = {
            k: np.asarray(encoder.get(k, v), np.float32)
            for k, v in ENCODER.items()
        }

        self.cells = {
            ch: {s: brain.cells(types, s) for s in "LR"}
            for ch, types in CHANNELS.items()
        }

        self.previous: dict = {}
        self.last = {
            f"{ch}{s}": 0.0
            for ch in CHANNELS
            for s in "LR"
        }

    @property
    def loom(self):
        return self.cells["loom"]

    @property
    def chase(self):
        return self.cells["chase"]

    def inject(self, opp=None, shots=(), threat: float = 0.0) -> list:
        p = self.p
        drive = {
            key: np.float32(0.0)
            for key in self.last
        }
        seen = {}

        def angle_and_growth(key, dx, size):
            angle = size / max(abs(dx), 8.0)
            seen[key] = angle
            return angle, max(
                0.0,
                angle - self.previous.get(key, angle),
            )

        if opp is not None:
            dx, size = opp
            s = "L" if dx < 0 else "R"

            angle, growth = angle_and_growth(
                "opp",
                dx,
                size,
            )

            drive[f"loom{s}"] = np.clip(
                growth * p["loom_gain"]
                + angle * p["loom_size"],
                0,
                p["cap"],
            )

            drive[f"chase{s}"] = np.clip(
                p["chase_base"]
                + p["chase_gain"] * angle,
                0,
                p["cap"],
            )

            drive[f"threat{s}"] = (
                p["threat_max"]
                * np.float32(np.clip(threat, 0, 1))
            )

        for key, dx, size in shots:
            s = "L" if dx < 0 else "R"

            _, growth = angle_and_growth(
                key,
                dx,
                size,
            )

            drive[f"shot{s}"] = np.maximum(
                drive[f"shot{s}"],
                np.clip(
                    growth * p["shot_gain"],
                    0,
                    p["cap"],
                ),
            )

        self.previous = seen
        self.last = {
            key: float(np.mean(amount))
            for key, amount in drive.items()
        }

        return [
            (
                self.cells[key[:-1]][key[-1]],
                amount,
            )
            for key, amount in drive.items()
            if np.any(amount > 0)
        ]
