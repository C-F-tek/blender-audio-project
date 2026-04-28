"""Audio mapping template.

This module converts compact audio-analysis data into visual control values.
Keep JSON field assumptions documented in inputs/input_schema.json.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class VisualControls:
    """Normalized control values used by scene modules."""

    low_energy: float = 0.0
    mid_energy: float = 0.0
    high_energy: float = 0.0
    beat_strength: float = 0.0
    onset_strength: float = 0.0
    section_intensity: float = 0.0


def clamp01(value: float) -> float:
    """Clamp a numeric value to the 0..1 range."""

    return max(0.0, min(1.0, float(value)))


def controls_from_summary(summary: Mapping[str, Any] | None) -> VisualControls:
    """Build visual controls from a compact track summary.

    The expected schema is intentionally conservative. Extend this function
    after documenting real fields in inputs/input_schema.json.
    """

    if not summary:
        return VisualControls()

    bands = summary.get("bands", {}) if isinstance(summary, Mapping) else {}
    rhythm = summary.get("rhythm", {}) if isinstance(summary, Mapping) else {}

    return VisualControls(
        low_energy=clamp01(bands.get("low", 0.0) if isinstance(bands, Mapping) else 0.0),
        mid_energy=clamp01(bands.get("mid", 0.0) if isinstance(bands, Mapping) else 0.0),
        high_energy=clamp01(bands.get("high", 0.0) if isinstance(bands, Mapping) else 0.0),
        beat_strength=clamp01(rhythm.get("beat_strength", 0.0) if isinstance(rhythm, Mapping) else 0.0),
        onset_strength=clamp01(rhythm.get("onset_strength", 0.0) if isinstance(rhythm, Mapping) else 0.0),
        section_intensity=clamp01(summary.get("section_intensity", 0.0)),
    )
