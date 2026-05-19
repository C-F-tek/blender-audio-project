from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any

from .common import normalize_target, read_text, repo_rel, target_error, write_text

FENCE_RE = re.compile(r"```diff\n(.*?)\n```", re.DOTALL)


def split_sections(text: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    current_target = ""
    current_lines: list[str] = []
    current_start = 0
    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.startswith("### "):
            if current_target:
                sections.append(_section(current_target, current_start, current_lines))
            current_target = normalize_target(line[4:])
            current_lines = []
            current_start = line_no
            continue
        if current_target:
            current_lines.append(line)
    if current_target:
        sections.append(_section(current_target, current_start, current_lines))
    return sections


def _section(target: str, start_line: int, lines: list[str]) -> dict[str, str]:
    return {"target": target, "start_line": str(start_line), "body": "\n".join(lines)}


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
    return "# CODE_PRODUCT_FULL_PATCH" in text and "Nessun diff/code effettivo" in text


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
    result = _base_section_result(target, body, payload, exists, int(item["start_line"]))
    if error:
        result["status"] = "blocked_unsafe_target"
        result["errors"].append(error)
        return result
    if not payload:
        if no_worktree_diff_marker(body):
            result["payload_kind"] = "no_worktree_diff_marker"
            result["status"] = "already_integrated_no_worktree_diff"
            result["warnings"].append("verified target has no captured worktree diff")
            return result
        result["status"] = "missing_payload"
        result["errors"].append("section has no diff code block")
        return result
    if payload.startswith("diff --git "):
        return _analyze_diff_payload(repo_root, output_dir, target, target_path, exists, payload, result)
    if payload.startswith("new file:"):
        return _analyze_new_file_payload(target_path, exists, payload, result)
    result["payload_kind"] = "unknown"
    result["status"] = "needs_manual_review"
    result["warnings"].append("unrecognized payload format")
    return result


def no_worktree_diff_marker(body: str) -> bool:
    status = metadata_value(body, "Implementation status")
    if status == "already_integrated_no_worktree_diff":
        status = "verified_target_no_worktree_diff"
    hunks = metadata_value(body, "Diff hunks")
    normalized = body.lower()
    return (
        status == "verified_target_no_worktree_diff"
        and hunks == "0"
        and "[no worktree diff captured]" in normalized
    )


def _base_section_result(
    target: str, body: str, payload: str, exists: bool, start_line: int
) -> dict[str, Any]:
    section_hash = hashlib.sha256((target + "\n" + payload).encode("utf-8")).hexdigest()
    return {
        "target_file": target,
        "start_line": start_line,
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


def _analyze_diff_payload(
    repo_root: Path,
    output_dir: Path,
    target: str,
    target_path: Path,
    exists: bool,
    payload: str,
    result: dict[str, Any],
) -> dict[str, Any]:
    result["payload_kind"] = "unified_diff"
    if result["payload_truncated"]:
        return _classify_truncated_diff(target_path, exists, payload, result)
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
            result["warnings"].append(
                f"diff appears integrated despite context drift; added-line ratio={ratio:.2f}"
            )
        else:
            result["status"] = "needs_manual_review"
            result["warnings"].append("neither forward nor reverse git apply check passed")
    return result


def _classify_truncated_diff(
    target_path: Path, exists: bool, payload: str, result: dict[str, Any]
) -> dict[str, Any]:
    ratio = added_line_ratio(payload, read_text(target_path) if exists else "")
    if exists and ratio >= 0.80:
        result["status"] = "already_integrated_with_context_drift"
        result["warnings"].append(f"truncated diff appears integrated; added-line ratio={ratio:.2f}")
    else:
        result["status"] = "truncated_payload"
        result["errors"].append("payload is truncated")
    return result


def _analyze_new_file_payload(
    target_path: Path, exists: bool, payload: str, result: dict[str, Any]
) -> dict[str, Any]:
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
    elif exists and normalized_text(read_text(target_path)) == normalized_text(content):
        result["status"] = "already_integrated"
    elif exists:
        result["status"] = "target_exists_content_differs"
        result["warnings"].append("target exists but content differs from artifact dump")
    else:
        result["status"] = "forward_applicable_new_file"
    return result


def summarize_sections(
    sections: list[dict[str, Any]],
) -> tuple[dict[str, int], list[str], list[str]]:
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
