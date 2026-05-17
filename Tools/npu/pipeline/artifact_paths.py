from __future__ import annotations

from pathlib import Path, PurePosixPath

from .config import DEFAULT_ALLOWED_ARTIFACT_PREFIXES, slugify_track_stem


def normalize_repo_relative_path(path: str) -> str:
    """Normalize a generated artifact path to a safe POSIX-style repo path."""

    normalized = path.replace("\\", "/").strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return str(PurePosixPath(normalized))


def repo_relative_path(path: str | Path, *, repo_root: str | Path | None = None) -> str:
    """Return a normalized repo-relative path when a repo root is available."""

    if repo_root is not None:
        try:
            root = Path(repo_root).resolve()
            candidate = Path(path)
            if not candidate.is_absolute():
                candidate = root / candidate
            relative = candidate.resolve().relative_to(root)
            return normalize_repo_relative_path(relative.as_posix())
        except (OSError, ValueError):
            pass
    return normalize_repo_relative_path(str(path))


def is_allowed_generated_artifact_path(
    path: str,
    *,
    allowed_prefixes: tuple[str, ...] = DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
) -> bool:
    """Return True when a path is inside an allowed generated-artifact prefix."""

    normalized = normalize_repo_relative_path(path)
    if normalized.startswith("../") or normalized == "..":
        return False
    return any(normalized.startswith(prefix) for prefix in allowed_prefixes)


def validate_generated_artifact_paths(
    paths: list[str],
    *,
    allowed_prefixes: tuple[str, ...] = DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
) -> dict[str, object]:
    """Validate generated artifact destinations without touching the filesystem."""

    normalized = [normalize_repo_relative_path(path) for path in paths]
    invalid = [
        path
        for path in normalized
        if not is_allowed_generated_artifact_path(
            path,
            allowed_prefixes=allowed_prefixes,
        )
    ]
    return {
        "ok": not invalid,
        "allowed_prefixes": list(allowed_prefixes),
        "paths": normalized,
        "invalid_paths": invalid,
    }


def dual_ai_legacy_runtime_output_paths(track_stem: str) -> tuple[str, ...]:
    """Return exact legacy output paths owned by the dual-AI runtime."""

    return (
        f"output/{track_stem}_dual_ai_scene_plan.json",
        f"output/{track_stem}_ollama_music_insights.json",
        f"output/{track_stem}_ai_implementation_draft.json",
        f"indexAI/scene_scripts/{slugify_track_stem(track_stem)}_scene_builder_candidate.py",
        "Tools/npu/context_artifacts/dual_ai_blender_agent_brief.md",
        "Tools/npu/context_artifacts/ollama_music_insights.md",
        "Tools/npu/context_artifacts/npu_dual_ai_technical_notes.md",
        "Tools/npu/npu_preflight_report.json",
        "Tools/npu/context_artifacts/generated_implementation_notes.md",
        "Tools/npu/context_artifacts/npu_dual_ai_implementation_notes.md",
    )


def is_allowed_legacy_runtime_output_path(
    path: str | Path,
    *,
    repo_root: str | Path,
    track_stem: str,
) -> bool:
    """Return True when a path is an exact legacy dual-AI runtime output."""

    normalized = repo_relative_path(path, repo_root=repo_root)
    allowed = {
        normalize_repo_relative_path(item)
        for item in dual_ai_legacy_runtime_output_paths(track_stem)
    }
    return normalized in allowed


def validate_legacy_runtime_output_paths(
    paths: list[str | Path],
    *,
    repo_root: str | Path,
    track_stem: str,
) -> dict[str, object]:
    """Validate exact legacy runtime outputs without allowing broad source prefixes."""

    normalized = [repo_relative_path(path, repo_root=repo_root) for path in paths]
    allowed = tuple(
        normalize_repo_relative_path(path)
        for path in dual_ai_legacy_runtime_output_paths(track_stem)
    )
    invalid = [path for path in normalized if path not in allowed]
    return {
        "ok": not invalid,
        "track_stem": track_stem,
        "allowed_exact_paths": list(allowed),
        "paths": normalized,
        "invalid_paths": invalid,
    }
