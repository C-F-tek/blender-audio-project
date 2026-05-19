"""Profile loading and heap command construction."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from .io_utils import now_stamp, read_json
from .models import CLI_FLAG_KEYS, CLI_VALUE_KEYS, DEFAULT_PROFILE, PROFILE_FILE, LauncherConfig


def resolve_project_python(repo_root: Path, explicit: str = "") -> str:
    if explicit:
        return str(Path(explicit).resolve())
    for candidate in (
        repo_root / ".venv" / "Scripts" / "python.exe",
        repo_root / "venv" / "Scripts" / "python.exe",
        repo_root / ".venv314" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate.resolve())
    return sys.executable


def load_profiles(repo_root: Path, profiles_file: Path | None = None) -> dict[str, Any]:
    path = profiles_file or repo_root / PROFILE_FILE
    if not path.is_absolute():
        path = repo_root / path
    return read_json(path)


def profile_names(repo_root: Path) -> list[str]:
    profiles = load_profiles(repo_root).get("profiles", {})
    return sorted(profiles) if isinstance(profiles, dict) else []


def select_profile(repo_root: Path, name: str, profiles_file: Path | None = None) -> dict[str, Any]:
    doc = load_profiles(repo_root, profiles_file)
    profiles = doc.get("profiles") if isinstance(doc.get("profiles"), dict) else {}
    selected = name or str(doc.get("default_profile") or DEFAULT_PROFILE)
    profile = profiles.get(selected)
    if not isinstance(profile, dict):
        raise SystemExit(f"unknown profile '{selected}'. Available: {', '.join(sorted(profiles))}")
    result = dict(profile)
    result["profile_name"] = selected
    return result


def resolve_config(config: LauncherConfig) -> LauncherConfig:
    repo_root = config.repo_root.resolve()
    request_file = config.request_file
    if not request_file.is_absolute():
        request_file = repo_root / request_file
    intermediate_root = config.intermediate_root
    if not intermediate_root.is_absolute():
        intermediate_root = repo_root / intermediate_root
    final_root = config.final_root
    if not final_root.is_absolute():
        final_root = repo_root / final_root
    return LauncherConfig(
        repo_root=repo_root,
        request_file=request_file.resolve(strict=False),
        intermediate_root=intermediate_root.resolve(strict=False),
        final_root=final_root.resolve(strict=False),
        profile_name=config.profile_name,
        python_exe=resolve_project_python(repo_root, config.python_exe),
        stamp=config.stamp or now_stamp(),
        revision_context=config.revision_context,
        profiles_file=config.profiles_file,
        profile_overrides=dict(config.profile_overrides or {}),
    )


def run_dir_for(config: LauncherConfig) -> Path:
    return config.intermediate_root / f"heap_context_closure_{config.stamp}"


def build_heap_command(config: LauncherConfig) -> list[str]:
    cfg = resolve_config(config)
    profile = select_profile(cfg.repo_root, cfg.profile_name, cfg.profiles_file)
    for key, value in (cfg.profile_overrides or {}).items():
        if value not in ("", None):
            profile[key] = value
    revision_context = cfg.revision_context or str(
        profile.get("revision_context_mode") or "auto_latest"
    )
    command = [
        cfg.python_exe,
        "-m",
        "Tools.ai",
        "heap_context_closure",
        "--repo-root",
        ".",
        "--python-exe",
        cfg.python_exe,
        "--request-file",
        str(cfg.request_file),
        "--stamp",
        cfg.stamp,
        "--output-dir",
        str(run_dir_for(cfg)),
        "--documents-root",
        str(cfg.final_root),
        "--revision-context",
        revision_context,
    ]
    for key, flag in CLI_VALUE_KEYS.items():
        if key in profile and profile[key] not in ("", None):
            command.extend([flag, str(profile[key])])
    for key, flag in CLI_FLAG_KEYS.items():
        if bool(profile.get(key)):
            command.append(flag)
    return command
