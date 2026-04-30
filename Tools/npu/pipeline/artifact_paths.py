from __future__ import annotations

from pathlib import PurePosixPath

from .config import DEFAULT_ALLOWED_ARTIFACT_PREFIXES


def normalize_repo_relative_path(path: str) -> str:
    """Normalize a generated artifact path to a safe POSIX-style repo path."""

    normalized = path.replace("\\", "/").strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return str(PurePosixPath(normalized))


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
