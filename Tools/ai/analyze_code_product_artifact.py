#!/usr/bin/env python3
"""Analyze run-produced CODE_PRODUCT_FULL_PATCH.md artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from tools.ai.code_product_artifact_apply import safe_apply_sections
    from tools.ai.code_product_artifact_report import render_markdown
except ImportError:  # pragma: no cover
    import sys

    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.code_product_artifact_apply import safe_apply_sections  # type: ignore
    from tools.ai.code_product_artifact_report import render_markdown  # type: ignore


DEFAULT_OUTPUT = "output/validation/code_product_artifact_intake.json"
DEFAULT_MARKDOWN = "output/validation/code_product_artifact_intake.md"
DENY_PREFIXES = ("output/", "renders/", "indexAI/code_chunks/", "indexAI/project_code_chunks/")
DENY_SUFFIXES = (".db", ".sqlite", ".sqlite3", ".sqlite-wal", ".sqlite-shm")
SAFE_PREFIXES = ("Tools/", "docs/", "config/")
FENCE_RE = re.compile(r"```diff\n(.*?)\n```", re.DOTALL)
INTEGRATED_STATUSES = (
    "already_integrated",
    "already_integrated_with_context_drift",
    "already_integrated_truncated_dump",
)

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_text(path: Path, limit: int | None = None) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return text if limit is None else text[:limit]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def repo_rel(repo_root: Path, value: str | Path) -> str:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(value).replace("\\", "/")

def normalize_target(raw: str) -> str:
    return str(raw or "").strip().strip("`").replace("\\", "/")


def target_error(target: str) -> str:
    normalized = normalize_target(target)
    lower = normalized.lower()
    if not normalized:
        return "empty target"
    if Path(normalized).is_absolute():
        return "target is absolute"
    if ".." in Path(normalized).parts:
        return "target escapes repository"
    if any(lower.startswith(prefix.lower()) for prefix in DENY_PREFIXES):
        return "target prefix is denied"
    if any(lower.endswith(suffix) for suffix in DENY_SUFFIXES):
        return "target suffix is denied"
    if not any(normalized.startswith(prefix) for prefix in SAFE_PREFIXES):
        return "target prefix is not allowlisted"
    return ""

def split_sections(text: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    current_target = ""
    current_lines: list[str] = []
    current_start = 0
    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.startswith("### "):
            if current_target:
                sections.append(
                    {
                        "target": current_target,
                        "start_line": str(current_start),
                        "body": "\n".join(current_lines),
                    }
                )
            current_target = normalize_target(line[4:])
            current_lines = []
            current_start = line_no
            continue
        if current_target:
            current_lines.append(line)
    if current_target:
        sections.append(
            {
                "target": current_target,
                "start_line": str(current_start),
                "body": "\n".join(current_lines),
            }
        )
    return sections


def metadata_value(body: str, name: str) -> str:
    pattern = re.compile(rf"^- {re.escape(name)}:\s*`?(.*?)`?\.?$", re.MULTILINE)
    match = pattern.search(body)
    return match.group(1).strip() if match else ""


def document_metadata_value(text: str, name: str) -> str:
    pattern = re.compile(rf"^- {re.escape(name)}:\s*`?([^`\n]+)`?", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def document_metadata_int(text: str, name: str) -> int | None:
    value = document_metadata_value(text, name)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def declared_empty_code_product(text: str) -> bool:
    if document_metadata_int(text, "Effective code product count") == 0:
        return True
    return (
        "# CODE_PRODUCT_FULL_PATCH" in text
        and "Nessun diff/code effettivo" in text
    )


def code_block(body: str) -> str:
    match = FENCE_RE.search(body)
    return match.group(1).strip("\n") if match else ""


def normalized_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"


def run_git_apply_check(
    repo_root: Path, patch_text: str, output_dir: Path, target: str, reverse: bool
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", target).strip("_") or "patch"
    patch_path = output_dir / f"{name}.diff"
    write_text(patch_path, patch_text)
    command = ["git", "apply", "--check", "--whitespace=nowarn"]
    if reverse:
        command.append("--reverse")
    command.append(str(patch_path))
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    return {
        "returncode": completed.returncode,
        "ok": completed.returncode == 0,
        "stderr_tail": (completed.stderr or "")[-2000:],
        "stdout_tail": (completed.stdout or "")[-1000:],
        "patch_file": repo_rel(repo_root, patch_path),
    }


def new_file_payload_content(payload: str) -> str:
    marker = "\n\n"
    if marker not in payload:
        return ""
    return payload.split(marker, 1)[1]


def added_line_ratio(payload: str, current_text: str) -> float:
    added = [
        line[1:]
        for line in payload.splitlines()
        if line.startswith("+") and not line.startswith("+++") and line[1:].strip()
    ]
    unique = list(dict.fromkeys(added))
    return 0.0 if not unique else sum(1 for line in unique if line in current_text) / len(unique)


def truncated_prefix(text: str) -> str:
    return text.split("\n...[", 1)[0] if "\n...[" in text else text


def payload_truncated(payload: str) -> bool:
    markers = ("[diff truncated]", "[code product excerpt truncated")
    for line in str(payload or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("...") and any(marker in stripped for marker in markers):
            return True
    return False


def analyze_section(repo_root: Path, output_dir: Path, item: dict[str, str]) -> dict[str, Any]:
    target = normalize_target(item["target"])
    body = item["body"]
    payload = code_block(body)
    error = target_error(target)
    target_path = repo_root / target
    exists = target_path.exists()
    section_hash = hashlib.sha256((target + "\n" + payload).encode("utf-8")).hexdigest()
    result: dict[str, Any] = {
        "target_file": target,
        "start_line": int(item["start_line"]),
        "section_sha256": section_hash,
        "git_status": metadata_value(body, "Git status"),
        "implementation_status": metadata_value(body, "Implementation status"),
        "diff_hunk_count": metadata_value(body, "Diff hunks"),
        "target_exists": exists,
        "payload_chars": len(payload),
        "payload_truncated": payload_truncated(payload),
        "status": "unknown",
        "errors": [],
        "warnings": [],
    }
    if error:
        result["status"] = "blocked_unsafe_target"
        result["errors"].append(error)
        return result
    if not payload:
        result["status"] = "missing_payload"
        result["errors"].append("section has no diff code block")
        return result
    if payload.startswith("diff --git "):
        result["payload_kind"] = "unified_diff"
        if result["payload_truncated"]:
            ratio = added_line_ratio(payload, read_text(target_path) if exists else "")
            if exists and ratio >= 0.80:
                result["status"] = "already_integrated_with_context_drift"
                result["warnings"].append(f"truncated diff appears integrated; added-line ratio={ratio:.2f}")
            else:
                result["status"] = "truncated_payload"
                result["errors"].append("payload is truncated")
            return result
        check_dir = output_dir / "patch_checks"
        reverse = run_git_apply_check(repo_root, payload, check_dir, target + "_reverse", True)
        forward = run_git_apply_check(repo_root, payload, check_dir, target + "_forward", False)
        result["reverse_apply_check"] = reverse
        result["forward_apply_check"] = forward
        if reverse["ok"]:
            result["status"] = "already_integrated"
        elif forward["ok"]:
            result["status"] = "forward_applicable"
        else:
            ratio = added_line_ratio(payload, read_text(target_path) if exists else "")
            if exists and ratio >= 0.80:
                result["status"] = "already_integrated_with_context_drift"
                result["warnings"].append(f"diff appears integrated despite context drift; added-line ratio={ratio:.2f}")
            else:
                result["status"] = "needs_manual_review"
                result["warnings"].append("neither forward nor reverse git apply check passed")
        return result
    if payload.startswith("new file:"):
        result["payload_kind"] = "new_file_dump"
        content = new_file_payload_content(payload)
        if not content:
            result["status"] = "missing_new_file_content"
            result["errors"].append("new file payload has no content")
        elif result["payload_truncated"] and exists:
            prefix = normalized_text(truncated_prefix(content)).rstrip()
            current = normalized_text(read_text(target_path)).rstrip()
            if prefix and current.startswith(prefix):
                result["status"] = "already_integrated_truncated_dump"
                result["warnings"].append("truncated new-file dump matches current file prefix")
            else:
                result["status"] = "truncated_payload"
                result["errors"].append("payload is truncated")
        elif result["payload_truncated"]:
            result["status"] = "truncated_payload"
            result["errors"].append("payload is truncated")
        elif exists:
            current = read_text(target_path)
            if normalized_text(current) == normalized_text(content):
                result["status"] = "already_integrated"
            else:
                result["status"] = "target_exists_content_differs"
                result["warnings"].append("target exists but content differs from artifact dump")
        else:
            result["status"] = "forward_applicable_new_file"
        return result
    result["payload_kind"] = "unknown"
    result["status"] = "needs_manual_review"
    result["warnings"].append("unrecognized payload format")
    return result


def summarize_sections(sections: list[dict[str, Any]]) -> tuple[dict[str, int], list[str], list[str]]:
    counts: dict[str, int] = {}
    errors: list[str] = []
    warnings: list[str] = []
    for section in sections:
        status = str(section.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
        target = str(section.get("target_file") or "")
        errors.extend(f"{target}: {err}" for err in section.get("errors", []))
        warnings.extend(f"{target}: {warn}" for warn in section.get("warnings", []))
    return counts, errors, warnings


def analyze(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    code_product = Path(args.code_product).expanduser().resolve()
    output = Path(args.output or DEFAULT_OUTPUT)
    if not output.is_absolute():
        output = repo_root / output
    markdown = Path(args.markdown_output or DEFAULT_MARKDOWN)
    if not markdown.is_absolute():
        markdown = repo_root / markdown
    output_dir = output.parent
    errors: list[str] = []
    warnings: list[str] = []
    if not code_product.exists():
        errors.append(f"missing code product: {code_product}")
        text = ""
    else:
        text = read_text(code_product)
    empty_code_product = declared_empty_code_product(text)
    raw_sections = split_sections(text)
    sections = [analyze_section(repo_root, output_dir, item) for item in raw_sections]
    initial_status_counts, initial_errors, initial_warnings = summarize_sections(sections)
    safe_apply_report: dict[str, Any] = {
        "requested": bool(args.apply_safe),
        "performed": False,
        "applied_count": 0,
    }
    if args.apply_safe and not initial_errors:
        safe_apply_report.update(
            safe_apply_sections(repo_root, output_dir, raw_sections, sections)
        )
        sections = [analyze_section(repo_root, output_dir, item) for item in raw_sections]
    status_counts, section_errors, section_warnings = summarize_sections(sections)
    errors.extend(section_errors)
    warnings.extend(section_warnings)
    errors.extend(str(item) for item in safe_apply_report.get("errors", []))
    warnings.extend(str(item) for item in safe_apply_report.get("warnings", []))
    all_integrated = (not sections and empty_code_product) or bool(sections) and all(
        section.get("status") in INTEGRATED_STATUSES for section in sections
    )
    forward_applicable = sum(
        1
        for section in sections
        if str(section.get("status") or "").startswith("forward_applicable")
    )
    needs_review = sum(
        1
        for section in sections
        if section.get("status")
        not in {*INTEGRATED_STATUSES, "forward_applicable", "forward_applicable_new_file"}
    )
    if not sections and empty_code_product:
        warnings.append("code product declares zero effective code sections; nothing to apply")
    elif not sections:
        errors.append("no target sections found")
    if args.require_all_integrated and not all_integrated:
        errors.append("not all code product sections are already integrated")
    report = {
        "schema_version": 1,
        "kind": "code_product_artifact_intake",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "code_product_path": str(code_product),
        "code_product_lines": len(text.splitlines()) if text else 0,
        "code_product_chars": len(text),
        "target_count": len(sections),
        "empty_code_product": bool(not sections and empty_code_product),
        "status_counts": status_counts,
        "initial_status_counts": initial_status_counts,
        "already_integrated_count": sum(status_counts.get(status, 0) for status in INTEGRATED_STATUSES),
        "forward_applicable_count": forward_applicable,
        "needs_review_count": needs_review,
        "all_integrated": all_integrated,
        "passed": bool((sections or empty_code_product) and not errors),
        "require_all_integrated": bool(args.require_all_integrated),
        "apply_safe_requested": bool(args.apply_safe),
        "safe_apply": safe_apply_report,
        "provider_execution_performed": False,
        "patch_application_performed": bool(safe_apply_report.get("performed")),
        "source_writes_performed": bool(safe_apply_report.get("performed")),
        "git_write_performed": False,
        "errors": errors,
        "warnings": warnings,
        "sections": sections,
        "output": str(output),
        "markdown_output": str(markdown),
    }
    write_json(output, report)
    write_text(markdown, render_markdown(report))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--code-product", required=True)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument("--require-all-integrated", action="store_true")
    parser.add_argument(
        "--apply-safe",
        action="store_true",
        help="Apply only fully forward-applicable safe sections, then re-analyze.",
    )
    return parser.parse_args()


def main() -> int:
    report = analyze(parse_args())
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
