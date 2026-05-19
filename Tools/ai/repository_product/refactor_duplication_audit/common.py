"""Shared constants and filesystem helpers for refactor duplication audits."""

from __future__ import annotations

import re
import sys
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import (
        read_json_report,
        resolve_output_path,
        write_json_report,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.validation._shared.report_utils import (
        read_json_report,
        resolve_output_path,
        write_json_report,
    )

DEFAULT_OUTPUT = "output/analysis/refactor_duplication_audit.json"
DEFAULT_MARKDOWN = "output/analysis/refactor_duplication_audit.md"
DEFAULT_ROOTS: tuple[str, ...] = (
    "tools/ai",
    "tools/validation",
    "tools/workflow",
    "tools/npu",
)
DEFAULT_EXCLUDE_PARTS: tuple[str, ...] = ("__pycache__", ".venv", "venv", ".git")
SAFE_ID_RE = re.compile(r"[^A-Za-z0-9_.-]+")

HELPER_RULES: tuple[dict[str, Any], ...] = (
    {
        "candidate_id": "dup_path_helpers",
        "name_pattern": re.compile(
            r"^(repo_rel|repo_relative|resolve_path|resolve_repo_path|normalize_repo_path|normalize_manifest_path)$"
        ),
        "repeated_logic": "Repository-relative and path resolution helper patterns.",
        "existing_helper_available": True,
        "preferred_existing_helper_or_module": "Tools.ai._shared.github_evidence_bundle_io for evidence-bundle paths; Tools.validation._shared.report_utils for validation output paths.",
        "recommendation_type": "reuse_existing_helper",
        "risk": "medium",
        "schema_or_cli_impact": "none expected if imports preserve path normalization semantics.",
    },
    {
        "candidate_id": "dup_json_text_helpers",
        "name_pattern": re.compile(
            r"^(read_json|read_json_if_exists|write_json|write_text|write_json_report)$"
        ),
        "repeated_logic": "JSON/text read-write helpers repeated across report scripts and smoke tests.",
        "existing_helper_available": True,
        "preferred_existing_helper_or_module": "Tools.validation._shared.report_utils.write_json_report plus existing evidence-bundle IO helpers for read paths.",
        "recommendation_type": "promote_existing_function",
        "risk": "low",
        "schema_or_cli_impact": "none if UTF-8 and JSON indentation are preserved.",
    },
    {
        "candidate_id": "dup_markdown_renderers",
        "name_pattern": re.compile(r"^(render_markdown|build_markdown|render_.*markdown)$"),
        "repeated_logic": "Local Markdown renderers with repeated status/guardrail sections.",
        "existing_helper_available": False,
        "preferred_existing_helper_or_module": "Keep report-specific renderers local unless a stable shared status-section schema emerges.",
        "recommendation_type": "keep_local_by_design",
        "risk": "low",
        "schema_or_cli_impact": "none; markdown is presentation-only but should remain reviewable.",
    },
    {
        "candidate_id": "dup_split_compact_helpers",
        "name_pattern": re.compile(
            r"^(split_values|split_path_values|coalesce_list|compact_value|as_list)$"
        ),
        "repeated_logic": "Argument/list splitting and compact-value helpers.",
        "existing_helper_available": True,
        "preferred_existing_helper_or_module": "Reuse Tools.ai._shared.github_evidence_bundle_io.split_path_values/compact_value when the semantics match.",
        "recommendation_type": "reuse_existing_helper",
        "risk": "medium",
        "schema_or_cli_impact": "possible subtle CLI behavior changes; validate with broker/orchestrator smoke tests.",
    },
    {
        "candidate_id": "dup_line_count_helpers",
        "name_pattern": re.compile(r"^(line_count|load_line_counts|count_lines)$"),
        "repeated_logic": "Line-count calculation/loading helper patterns.",
        "existing_helper_available": True,
        "preferred_existing_helper_or_module": "Tools.validation.docs_hygiene.build_python_line_count_csv is the authoritative generator; use report CSV/JSON outputs instead of re-counting when possible.",
        "recommendation_type": "reuse_existing_helper",
        "risk": "low",
        "schema_or_cli_impact": "none if CSV schema remains File/Lines.",
    },
    {
        "candidate_id": "dup_artifact_chunk_helpers",
        "name_pattern": re.compile(
            r"^(summarize_artifact|build_included_artifact|discover_related_artifacts|build_included_artifacts|build_artifact_chunk_index|chunk_file_lines)$"
        ),
        "repeated_logic": "Artifact discovery, inclusion and large-file chunk pointer logic.",
        "existing_helper_available": True,
        "preferred_existing_helper_or_module": "Tools.ai._shared.github_evidence_bundle_artifacts.",
        "recommendation_type": "reuse_existing_helper",
        "risk": "medium",
        "schema_or_cli_impact": "must preserve bundle schema fields and chunk pointer metadata.",
    },
    {
        "candidate_id": "dup_tool_request_packet_logic",
        "name_pattern": re.compile(
            r"^(tool_request|build_.*tool_requests|execute_tool_request|extract_tool_requests|run_.*runtime_tool_broker.*)$"
        ),
        "repeated_logic": "Runtime tool-request packet construction, extraction and broker execution summaries.",
        "existing_helper_available": False,
        "preferred_existing_helper_or_module": "Advisory: consider a future small request-packet helper only after broker/orchestrator schemas stabilize.",
        "recommendation_type": "advisory_only",
        "risk": "medium",
        "schema_or_cli_impact": "possible broker/orchestrator schema impact; do not refactor automatically.",
    },
)

LINE_COUNT_SHARED_DELEGATION_TOKENS = (
    "physical_line_count(",
    "count_file_lines(",
    "parse_line_count_csv_row(",
    "load_line_count_csv_map(",
    "line_count_for_path(",
    "shared_line_count_for_path(",
)

def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def split_values(values: Iterable[str] | None) -> list[str]:
    out: list[str] = []
    for value in values or []:
        for part in str(value).split(","):
            normalized = part.strip().strip("'\"")
            if normalized and normalized not in out:
                out.append(normalized)
    return out

def safe_id(value: str, fallback: str = "dup_candidate") -> str:
    text = SAFE_ID_RE.sub("_", str(value or "").strip()).strip("._-")
    return text[:100] or fallback

def read_text(path: Path) -> tuple[str, str | None]:
    try:
        return path.read_text(encoding="utf-8-sig"), None
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8", errors="replace"), None
        except Exception as exc:  # noqa: BLE001
            return "", f"{type(exc).__name__}: {exc}"
    except Exception as exc:  # noqa: BLE001
        return "", f"{type(exc).__name__}: {exc}"
