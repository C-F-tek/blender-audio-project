"""Shared helpers for the report-only runtime tool broker."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from ia_carmine._shared.file_backed_transport import write_text_artifact
from ia_carmine._shared.agent_runtime_tool_broker_execution import TimedCommandResult

DEFAULT_OUTPUT = "output/validation/agent_runtime_tool_broker.json"
DEFAULT_MARKDOWN = "output/validation/agent_runtime_tool_broker.md"
SAFE_ID_RE = re.compile(r"[^A-Za-z0-9_.-]+")


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    allowed_args: tuple[str, ...]
    builder: Callable[[Path, Path, str, dict[str, Any]], tuple[list[str], dict[str, Any]]]
    input_schema: dict[str, Any] | None = None
    categories: tuple[str, ...] = ()
    broker_only: bool = False


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def execute_debug_lab_in_process(
    *,
    repo_root: Path,
    request_args: dict[str, Any],
    outputs: dict[str, str],
    timeout_seconds: int,
) -> TimedCommandResult:
    started_at = now_iso()
    started = perf_counter()
    request = request_args.get("request_json")
    if not isinstance(request, dict):
        return TimedCommandResult(
            returncode=2,
            stdout_tail="",
            stderr_tail="",
            error="agent_runtime_debug_lab in-process execution requires request_json object",
            started_at=started_at,
            finished_at=now_iso(),
            elapsed_seconds=round(max(0.0, perf_counter() - started), 3),
        )
    try:
        from ia_carmine.runtime.runtime_tool.agent_runtime_debug_lab.reporting import (
            render_markdown as render_debug_lab_markdown,
            write_reports as write_debug_lab_reports,
        )
        from ia_carmine.runtime.runtime_tool.agent_runtime_debug_lab.runner import run_request

        report = run_request(
            repo_root=repo_root,
            request=request,
            timeout_seconds=timeout_seconds,
            tail_chars=int(request_args.get("tail_chars") or 4000),
        )
        write_debug_lab_reports(
            repo_root=repo_root,
            output=outputs["json_report"],
            markdown_output=outputs["markdown_report"],
            report=report,
            markdown=render_debug_lab_markdown(report),
        )
        stdout_tail = json.dumps(
            {
                "passed": report.get("passed"),
                "operation_count": report.get("operation_count"),
                "failed_count": report.get("failed_count"),
                "request_transport": "in_process_internal",
                "full_io_refs": True,
            },
            ensure_ascii=False,
        )
        io_dir = Path(outputs["json_report"]).resolve(strict=False).parent / "broker_io_artifacts"
        stdout_ref = write_text_artifact(
            repo_root,
            io_dir,
            name="agent_runtime_debug_lab_in_process_stdout",
            text=stdout_tail,
            kind="tool_stdout",
            producer="agent_runtime_tool_broker",
        )
        stderr_ref = write_text_artifact(
            repo_root,
            io_dir,
            name="agent_runtime_debug_lab_in_process_stderr",
            text="",
            kind="tool_stderr",
            producer="agent_runtime_tool_broker",
        )
        return TimedCommandResult(
            returncode=0 if report.get("passed") is True else 2,
            stdout_tail=stdout_tail[-12000:],
            stderr_tail="",
            error="",
            started_at=started_at,
            finished_at=now_iso(),
            elapsed_seconds=round(max(0.0, perf_counter() - started), 3),
            stdout_ref=stdout_ref,
            stderr_ref=stderr_ref,
            stdout_chars=len(stdout_tail),
            stderr_chars=0,
        )
    except Exception as exc:  # noqa: BLE001
        return TimedCommandResult(
            returncode=1,
            stdout_tail="",
            stderr_tail="",
            error=f"{type(exc).__name__}: {exc}",
            started_at=started_at,
            finished_at=now_iso(),
            elapsed_seconds=round(max(0.0, perf_counter() - started), 3),
        )


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def safe_id(value: Any, fallback: str) -> str:
    text = str(value or fallback).strip()
    text = SAFE_ID_RE.sub("_", text).strip("._-")
    return text[:80] or fallback


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def split_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    else:
        items = [value]
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out


def compact_value(value: Any, *, max_chars: int = 2500) -> Any:
    text = json.dumps(value, ensure_ascii=False, default=str)
    if len(text) <= max_chars:
        return value
    if isinstance(value, str):
        return value[:max_chars] + "\n...[truncated]"
    return text[:max_chars] + "\n...[truncated]"


GENERATED_OUTPUT_PREFIXES = ("output/", "docs/LOCAL_VALIDATION_EVIDENCE/")
SOURCE_TREE_PREFIXES = (
    "Tools/",
    "tools/",
    "Scripting/",
    "config/",
    "docs/",
    "README.md",
    "WORKFLOW.md",
    "AGENTS.md",
    "CHATGPT/",
    "CHATGPT.md",
)


def collect_output_paths(value: Any) -> list[str]:
    paths: list[str] = []
    if isinstance(value, str) and value.strip():
        paths.append(value)
    elif isinstance(value, list):
        for item in value:
            paths.extend(collect_output_paths(item))
    elif isinstance(value, dict):
        for item in value.values():
            paths.extend(collect_output_paths(item))
    return paths


def normalized_child_path(repo_root: Path, value: str) -> str:
    text = str(value or "").strip().strip("'\"").replace("\\", "/")
    if not text:
        return ""
    path = Path(text)
    if path.is_absolute():
        try:
            text = (
                path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
            )
        except ValueError:
            text = path.as_posix()
    return text.lstrip("./")


def generated_output_path(path: str) -> bool:
    return path.startswith(GENERATED_OUTPUT_PREFIXES)


def fixture_repo_path(path: str) -> bool:
    return path.startswith("output/validation/") and "/fixture_repo/" in path


def real_source_target_path(path: str) -> bool:
    return path.startswith(SOURCE_TREE_PREFIXES) and not generated_output_path(path)


def collect_normalized_paths(repo_root: Path, *values: Any) -> list[str]:
    paths: list[str] = []
    for value in values:
        for raw in collect_output_paths(value):
            path = normalized_child_path(repo_root, raw)
            if path:
                paths.append(path)
    return paths


def output_owned_artifact_write(
    repo_root: Path, report_data: dict[str, Any], outputs: dict[str, Any]
) -> bool:
    paths = collect_normalized_paths(
        repo_root,
        outputs,
        {
            "output": report_data.get("output"),
            "markdown_output": report_data.get("markdown_output"),
            "json_output": report_data.get("json_output"),
            "csv_output": report_data.get("csv_output"),
        },
    )
    if not paths:
        return False
    if any(real_source_target_path(path) for path in paths):
        return False
    return all(generated_output_path(path) or fixture_repo_path(path) for path in paths)


def fixture_repo_write(
    repo_root: Path, report_data: dict[str, Any], outputs: dict[str, Any]
) -> bool:
    child_repo_root = normalized_child_path(repo_root, str(report_data.get("repo_root") or ""))
    if fixture_repo_path(child_repo_root):
        return True
    paths = collect_normalized_paths(
        repo_root,
        outputs,
        {
            "output": report_data.get("output"),
            "markdown_output": report_data.get("markdown_output"),
            "json_output": report_data.get("json_output"),
            "backup_dir": (
                report_data.get("safe_apply", {}).get("backup_dir")
                if isinstance(report_data.get("safe_apply"), dict)
                else None
            ),
        },
    )
    if not paths:
        return False
    all_fixture_or_generated = all(
        fixture_repo_path(path) or generated_output_path(path) for path in paths
    )
    return all_fixture_or_generated and any(fixture_repo_path(path) for path in paths)


def default_input_schema(allowed_args: tuple[str, ...]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            key: {
                "type": ["string", "number", "boolean", "array", "object", "null"],
            }
            for key in allowed_args
        },
        "additionalProperties": False,
    }


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    return True


def _validate_input_schema(
    tool_name: str,
    request_args: dict[str, Any],
    input_schema: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if input_schema.get("type") != "object":
        return [f"{tool_name}: input_schema root must be object"]
    properties = (
        input_schema.get("properties")
        if isinstance(input_schema.get("properties"), dict)
        else {}
    )
    required = input_schema.get("required") if isinstance(input_schema.get("required"), list) else []
    missing = sorted(str(item) for item in required if str(item) not in request_args)
    if missing:
        errors.append(f"{tool_name}: missing required args: {', '.join(missing)}")
    if input_schema.get("additionalProperties") is False:
        unknown = sorted(set(request_args) - set(properties))
        if unknown:
            errors.append(f"{tool_name}: unsupported args: {', '.join(unknown)}")
    for key, value in request_args.items():
        schema = properties.get(key) if isinstance(properties.get(key), dict) else {}
        expected = schema.get("type")
        expected_types = expected if isinstance(expected, list) else [expected]
        expected_types = [str(item) for item in expected_types if item]
        if expected_types and not any(_json_type_matches(value, item) for item in expected_types):
            errors.append(
                f"{tool_name}: arg {key} expected {'/'.join(expected_types)}, got {type(value).__name__}"
            )
    return errors


def validate_request_args(
    tool_name: str,
    request_args: dict[str, Any],
    allowed_args: tuple[str, ...],
    input_schema: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(request_args, dict):
        return [f"{tool_name}: args must be an object"]
    schema = input_schema if isinstance(input_schema, dict) else default_input_schema(allowed_args)
    errors.extend(_validate_input_schema(tool_name, request_args, schema))
    return errors


def base_outputs(out_dir: Path, request_id: str, stem: str) -> tuple[Path, Path]:
    return out_dir / f"{request_id}_{stem}.json", out_dir / f"{request_id}_{stem}.md"
