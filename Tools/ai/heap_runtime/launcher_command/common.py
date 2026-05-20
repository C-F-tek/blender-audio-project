"""Shared helpers for heap runtime launcher command generation."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_PROFILE_FILE = "Tools/ai/run/profiles/heap_runtime_launcher_profiles.json"
REQUIRED_COMPOSER_JSON = "heap_final_proposal_composer.json"
PROFILE_TO_CLI: dict[str, tuple[str, str]] = {
    "budget_minutes": ("--budget-minutes", "value"),
    "max_iterations": ("--max-iterations", "value"),
    "min_runtime_rounds": ("--min-runtime-rounds", "value"),
    "min_proposal_iterations": ("--min-proposal-iterations", "value"),
    "max_rounds": ("--max-rounds", "value"),
    "max_provider_revisions": ("--max-provider-revisions", "value"),
    "timeout_seconds": ("--timeout-seconds", "value"),
    "preflight_timeout_seconds": ("--preflight-timeout-seconds", "value"),
    "npu_device_workload_seconds": ("--npu-device-workload-seconds", "value"),
    "npu_device_workload_iterations": ("--npu-device-workload-iterations", "value"),
    "startup_max_memory_chars": ("--startup-max-memory-chars", "value"),
    "startup_max_context_files": ("--startup-max-context-files", "value"),
    "startup_scan_context_files": ("--startup-scan-context-files", "value"),
    "startup_max_chars_per_file": ("--startup-max-chars-per-file", "value"),
    "context_document_count": ("--context-document-count", "value"),
    "context_document_preview_chars": ("--context-document-preview-chars", "value"),
    "semantic_code_chunk_limit": ("--semantic-code-chunk-limit", "value"),
    "semantic_code_chunk_preview_chars": ("--semantic-code-chunk-preview-chars", "value"),
    "semantic_evidence_chunk_limit": ("--semantic-evidence-chunk-limit", "value"),
    "memory_search_limit": ("--memory-search-limit", "value"),
    "tool_catalog_limit": ("--tool-catalog-limit", "value"),
    "revision_context_max_tasks": ("--revision-context-max-tasks", "value"),
    "documents_root": ("--documents-root", "value"),
    "output_dir": ("--output-dir", "value"),
    "stamp": ("--stamp", "value"),
    "allow_provider_generation": ("--allow-provider-generation", "flag"),
    "operator_intent": ("--operator-intent", "flag"),
    "skip_preflight": ("--skip-preflight", "flag"),
    "skip_startup_reload": ("--skip-startup-reload", "flag"),
    "strict_startup_reload": ("--strict-startup-reload", "flag"),
    "no_documents": ("--no-documents", "flag"),
}
EXTERNAL_METADATA_KEYS = (
    "revision_context_mode",
    "revision_context_max_tasks",
    "universe_enabled",
    "universe_roles",
    "universe_max_steps",
    "universe_stop_condition",
    "block_pointer_protocol",
    "max_blocks_per_step",
    "max_block_chars",
    "max_revision_depth",
    "allow_backrefinement",
    "allow_forward_pointers",
    "require_resume_pointer",
    "require_refines_pointer",
)

def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit(f"JSON profile file must contain an object: {path}")
    return data

def read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}

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

def ps_quote(value: Any) -> str:
    text = str(value)
    return '"' + text.replace("`", "``").replace('"', '`"') + '"'

def normalize_provider_flags(profile: dict[str, Any]) -> dict[str, Any]:
    result = dict(profile)
    if result.get("allow_provider_generation") is True:
        result["operator_intent"] = True
    return result

def choose_profile(profile_doc: dict[str, Any], profile_name: str) -> dict[str, Any]:
    profiles = profile_doc.get("profiles") if isinstance(profile_doc.get("profiles"), dict) else {}
    selected = profile_name or str(profile_doc.get("default_profile") or "")
    profile = profiles.get(selected)
    if not isinstance(profile, dict):
        raise SystemExit(f"unknown profile '{selected}'. Available: {', '.join(sorted(profiles))}")
    result = dict(profile)
    result["profile_name"] = selected
    return normalize_provider_flags(result)

def apply_overrides(profile: dict[str, Any], overrides: list[str]) -> dict[str, Any]:
    result = dict(profile)
    for override in overrides:
        if "=" not in override:
            raise SystemExit(f"invalid override: {override}; expected key=value")
        key, value = override.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value.lower() in {"true", "false"}:
            result[key] = value.lower() == "true"
        else:
            try:
                result[key] = int(value)
            except ValueError:
                try:
                    result[key] = float(value)
                except ValueError:
                    if value.startswith("[") or value.startswith("{"):
                        try:
                            result[key] = json.loads(value)
                            continue
                        except json.JSONDecodeError:
                            pass
                    result[key] = value
    return normalize_provider_flags(result)

def profile_cli_keys(profile: dict[str, Any]) -> list[str]:
    return [key for key in profile if key in PROFILE_TO_CLI]

def profile_external_metadata(profile: dict[str, Any]) -> dict[str, Any]:
    return {key: profile[key] for key in EXTERNAL_METADATA_KEYS if key in profile}
