from __future__ import annotations

from typing import Any


def sample_music_context_fixture() -> dict[str, Any]:
    """Return a deterministic compact music context for tests and dry-runs."""

    return {
        "analysis_summary": {
            "duration_sec": 60.0,
            "fps": 30,
            "estimated_bpm": 120.0,
        },
        "track_summary": {
            "title": "Fixture Track",
            "estimated_tempo_bpm": 120.0,
        },
        "scene_summaries": [
            {
                "name": "fixture_intro",
                "start_sec": 0.0,
                "end_sec": 15.0,
            }
        ],
        "segments": [
            {
                "index": 1,
                "start_sec": 0.0,
                "end_sec": 8.0,
                "dominant_band": "low",
                "intensity": "medium",
                "intensity_score": 0.55,
                "controls": {"low": 0.7, "mid": 0.35, "high": 0.2},
                "top_events": list(range(12)),
            },
            {
                "index": 2,
                "start_sec": 8.0,
                "end_sec": 16.0,
                "dominant_band": "mid",
                "intensity": "high",
                "intensity_score": 0.82,
                "controls": {"low": 0.4, "mid": 0.85, "high": 0.55},
                "top_events": list(range(12, 20)),
            },
        ],
    }


def sample_implementation_draft_fixture() -> dict[str, Any]:
    """Return a deterministic valid implementation draft contract fixture."""

    return {
        "implementation_kind": "new_blender_scene_script_from_json",
        "safety": {"requires_manual_review": True, "runtime_execution": False},
        "reference_files": ["Scripting/v61b/materials.py"],
        "proposed_files": [
            {
                "file": "indexAI/scene_scripts/fixture_candidate.py",
                "purpose": "review-only generated script candidate",
            }
        ],
        "implementation_plan": [
            "validate helper contracts",
            "review generated artifact destination",
        ],
    }


def sample_provider_request_fixture() -> dict[str, Any]:
    """Return a provider request payload without executing any provider."""

    return {
        "provider": "ollama",
        "model": "fixture-model",
        "prompt": "fixture prompt",
        "max_tokens": 128,
        "metadata": {"fixture": True, "executed": False},
    }
