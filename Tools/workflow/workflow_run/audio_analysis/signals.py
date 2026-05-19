"""Signal-processing helpers for WAV-derived animation curves."""

from __future__ import annotations

import numpy as np


def moving_average(values: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return values
    kernel = np.ones(window, dtype=np.float64) / window
    return np.convolve(values, kernel, mode="same")


def robust_normalize(
    values: np.ndarray,
    floor_percentile: float = 5.0,
    ceil_percentile: float = 99.0,
) -> np.ndarray:
    lo = np.percentile(values, floor_percentile)
    hi = np.percentile(values, ceil_percentile)
    if hi - lo < 1e-12:
        return np.zeros_like(values)
    normalized = (values - lo) / (hi - lo)
    return np.clip(normalized, 0.0, 1.0)


def compress_curve(values: np.ndarray, gamma: float = 0.8) -> np.ndarray:
    return np.power(np.clip(values, 0.0, 1.0), gamma)


def band_envelope_from_stft(
    magnitude: np.ndarray,
    freqs: np.ndarray,
    fmin: float,
    fmax: float,
) -> np.ndarray:
    mask = (freqs >= fmin) & (freqs < fmax)
    if not np.any(mask):
        return np.zeros(magnitude.shape[1], dtype=np.float64)
    return np.mean(magnitude[mask, :], axis=0)


def resample_to_fps(
    times: np.ndarray,
    values: np.ndarray,
    fps: float,
    duration: float,
) -> tuple[np.ndarray, np.ndarray]:
    target_times = np.arange(0, duration, 1.0 / fps)
    target_values = np.interp(target_times, times, values)
    return target_times, target_values
