"""Profile loading for the canonical IA-Carmine operator product run."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROFILE_FILE = Path("ia_carmine/runtime/run/profiles/heap_runtime_launcher_profiles.json")
PROFILE_RUNTIME_ROUTE = "heap_context_closure"
PROFILE_REQUEST_FLAG = "--request-file"
PROFILE_DEST_OVERRIDES = {
    "revision_context_mode": "revision_context",
}
PROFILE_METADATA_KEYS = {
    "description",
    "profile_name",
    "universe_roles",
    "block_pointer_protocol",
}


def load_profiles(repo_root: Path, profiles_file: Path | None = None) -> dict[str, Any]:
    path = profiles_file or (repo_root / PROFILE_FILE)
    if not path.is_absolute():
        path = repo_root / path
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise SystemExit(f"profile file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"profile file is not valid JSON: {path}: {exc}") from exc
    return data if isinstance(data, dict) else {}


def profile_names(repo_root: Path, profiles_file: Path | None = None) -> list[str]:
    profiles = load_profiles(repo_root, profiles_file).get("profiles", {})
    return sorted(profiles) if isinstance(profiles, dict) else []


def select_profile(
    repo_root: Path,
    name: str = "",
    profiles_file: Path | None = None,
) -> dict[str, Any]:
    if not name:
        raise SystemExit("profile selection must be explicit; pass --profile <name>")
    doc = load_profiles(repo_root, profiles_file)
    profiles = doc.get("profiles") if isinstance(doc.get("profiles"), dict) else {}
    selected = str(name)
    profile = profiles.get(selected)
    if not isinstance(profile, dict):
        available = ", ".join(sorted(profiles)) or "<none>"
        raise SystemExit(f"unknown profile '{selected}'. Available: {available}")
    result = dict(profile)
    result["profile_name"] = selected
    return result


def apply_profile_to_args(
    args: Any,
    repo_root: Path,
    provided_dests: set[str],
) -> None:
    profile_name = str(getattr(args, "profile", "") or "")
    if not profile_name:
        return
    raw_profiles_file = str(getattr(args, "profiles_file", "") or "")
    profiles_file = Path(raw_profiles_file) if raw_profiles_file else None
    profile = select_profile(repo_root, profile_name, profiles_file)
    applied: dict[str, str] = {}
    for key, value in profile.items():
        if key in PROFILE_METADATA_KEYS:
            continue
        dest = PROFILE_DEST_OVERRIDES.get(key, key)
        if dest in provided_dests or not hasattr(args, dest) or value is None:
            continue
        setattr(args, dest, value)
        applied[dest] = f"profile:{profile_name}"
    setattr(args, "_profile_name", profile_name)
    setattr(args, "_profile_applied_fields", applied)
