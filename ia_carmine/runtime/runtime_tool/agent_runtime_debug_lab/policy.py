"""Policy and request validation for agent_runtime_debug_lab."""

from __future__ import annotations

from pathlib import Path
from typing import Any

ALLOWED_OPERATION_TYPES = {
    "python_compile",
    "python_script",
    "powershell_parse",
    "git_diff_check",
    "git_status_short",
    "validation_report_contract",
    "json_report_probe",
}
FORBIDDEN_OPERATION_TYPES = {
    "free_shell",
    "git_commit",
    "git_push",
    "git_merge",
    "git_reset",
    "git_clean",
    "patch_apply",
    "pip_install",
    "uv_add",
    "npm_install",
    "terraform_apply",
    "terraform_destroy",
    "blender_run",
    "ffmpeg_run",
    "provider_run",
    "ollama_run",
    "openvino_run",
}
SOURCE_PREFIXES = (
    "ia_carmine/",
    "Tools/validation/",
    "Tools/docs/",
    "Tools/workflow/",
    "docs/",
    "Scripting/",
)
EXECUTABLE_PYTHON_PREFIXES = (
    "ia_carmine/",
    "Tools/validation/",
    "Tools/docs/",
)
DENY_PREFIXES = (
    ".git/",
    "output/",
    "renders/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
)
DENY_SUFFIXES = (
    ".db",
    ".sqlite",
    ".sqlite3",
    ".sqlite-wal",
    ".sqlite-shm",
)
PROVIDER_RUNTIME_TOKENS = (
    "ollama",
    "openvino",
    "provider_probe",
    "run_local_provider_probe",
    "run_npu",
    "run_ollama",
    "blender",
    "ffmpeg",
)
OUTPUT_PREFIX = "output/validation/"
MAX_OPERATION_TIMEOUT_SECONDS = 600


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def normalize_repo_path(repo_root: Path, raw_path: Any) -> tuple[str, str | None]:
    if not isinstance(raw_path, str) or not raw_path.strip():
        return "", "path must be a non-empty string"
    raw = raw_path.strip().replace("\\", "/")
    path = Path(raw)
    candidate = path if path.is_absolute() else repo_root / path
    try:
        relative = candidate.resolve(strict=False).relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return raw, "path escapes repository root"
    if not relative:
        return relative, "empty repository-relative path"
    if relative.startswith("../") or "/../" in relative:
        return relative, "path traversal is forbidden"
    return relative, None


def is_forbidden_path(path: str) -> str | None:
    lower = path.lower()
    for prefix in DENY_PREFIXES:
        if lower.startswith(prefix.lower()):
            return f"path prefix is forbidden: {prefix}"
    for suffix in DENY_SUFFIXES:
        if lower.endswith(suffix):
            return f"path suffix is forbidden: {suffix}"
    return None


def validate_source_path(
    repo_root: Path, raw_path: Any, *, suffix: str | None = None
) -> tuple[str, str | None]:
    path, error = normalize_repo_path(repo_root, raw_path)
    if error:
        return path, error
    forbidden = is_forbidden_path(path)
    if forbidden:
        return path, forbidden
    if not any(path.startswith(prefix) for prefix in SOURCE_PREFIXES):
        return path, "path is outside allowed source prefixes"
    if suffix and not path.endswith(suffix):
        return path, f"path must end with {suffix}"
    if not (repo_root / path).exists():
        return path, "path does not exist"
    return path, None


def validate_python_script(repo_root: Path, raw_path: Any) -> tuple[str, str | None]:
    path, error = validate_source_path(repo_root, raw_path, suffix=".py")
    if error:
        return path, error
    if not any(path.startswith(prefix) for prefix in EXECUTABLE_PYTHON_PREFIXES):
        return path, "python_script path is outside executable Python prefixes"
    lower = path.lower()
    if any(token in lower for token in PROVIDER_RUNTIME_TOKENS):
        return path, "python_script appears to target provider/application runtime"
    return path, None


def validate_output_path(
    repo_root: Path, raw_path: Any, *, required_suffix: str | None = None
) -> tuple[str, str | None]:
    path, error = normalize_repo_path(repo_root, raw_path)
    if error:
        return path, error
    if not path.startswith(OUTPUT_PREFIX):
        return path, "output path must be under output/validation/"
    if required_suffix and not path.endswith(required_suffix):
        return path, f"output path must end with {required_suffix}"
    return path, None


def validate_string_args(args: Any) -> tuple[list[str], str | None]:
    if args is None:
        return [], None
    if not isinstance(args, list):
        return [], "args must be a list of strings"
    out: list[str] = []
    for item in args:
        if not isinstance(item, str):
            return [], "args must contain only strings"
        lowered = item.lower()
        if any(
            token in lowered
            for token in (
                "git push",
                "git merge",
                "pip install",
                "ffmpeg",
                "blender",
                "ollama",
            )
        ):
            return [], f"argument contains forbidden runtime/write token: {item}"
        out.append(item)
    return out, None


def operation_timeout(raw_value: Any, default_timeout: int) -> int:
    if raw_value is None:
        return min(default_timeout, MAX_OPERATION_TIMEOUT_SECONDS)
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        return min(default_timeout, MAX_OPERATION_TIMEOUT_SECONDS)
    return max(1, min(value, MAX_OPERATION_TIMEOUT_SECONDS))


def validate_request(request: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if request.get("kind") != "agent_runtime_debug_lab_request":
        errors.append("kind must be agent_runtime_debug_lab_request")
    if request.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    operations = request.get("operations")
    if not isinstance(operations, list) or not operations:
        errors.append("operations must be a non-empty list")
    return errors
