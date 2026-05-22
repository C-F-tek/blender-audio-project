"""Extract validated patch candidates from provider/proposal evidence."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from ia_carmine.runtime.runtime_tool.file_refs import RuntimeFileRef

EVIDENCE_DIFF_KEYS = {
    "unified_diff",
    "diff",
    "diff_text",
    "patch",
    "full_patch",
    "proposed_patch",
    "patch_sketch",
    "patch_sketch_unified_diff",
    "code_or_patch_sketch",
    "response_text",
}


def _resolve(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _json_text_sources(value: Any, location: str = "root") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        out: list[tuple[str, str]] = []
        for key, child in value.items():
            child_location = f"{location}.{key}"
            key_l = str(key).lower()
            if isinstance(child, str) and key_l in EVIDENCE_DIFF_KEYS:
                out.append((child, child_location))
            out.extend(_json_text_sources(child, child_location))
        return out
    if isinstance(value, list):
        out: list[tuple[str, str]] = []
        for index, child in enumerate(value):
            out.extend(_json_text_sources(child, f"{location}[{index}]"))
        return out
    if isinstance(value, str) and "diff --git" in value:
        return [(value, location)]
    return []


def _diff_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    for match in re.finditer(r"(?is)```(?:diff|patch)?\s*\n(.*?)```", text):
        body = match.group(1).strip()
        if "diff --git" in body:
            blocks.append(_normalize_diff(body))
    raw = re.sub(r"(?is)```(?:diff|patch)?\s*\n.*?```", "", text)
    raw = re.sub(r"\r\n?", "\n", raw)
    for match in re.finditer(r"(?ms)^diff --git .+?(?=^diff --git |\Z)", raw):
        body = match.group(0).strip()
        if body:
            blocks.append(_normalize_diff(body))
    return blocks


def _normalize_diff(text: str) -> str:
    body = re.sub(r"\r\n?", "\n", str(text or "")).strip()
    return body + "\n" if body else ""


def diff_targets(diff_text: str) -> list[str]:
    targets: list[str] = []
    for line in _normalize_diff(diff_text).splitlines():
        match = re.match(r"diff --git a/(.*?) b/(.*?)$", line)
        if match:
            for value in (match.group(1), match.group(2)):
                if value != "/dev/null" and value not in targets:
                    targets.append(value)
        match = re.match(r"\+\+\+ b/(.*?)$", line)
        if match and match.group(1) != "/dev/null" and match.group(1) not in targets:
            targets.append(match.group(1))
    return targets


def _git_apply_check(repo_root: Path, diff_path: Path, timeout: int) -> dict[str, Any]:
    completed = subprocess.run(
        ["git", "apply", "--check", "--ignore-whitespace", str(diff_path)],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return {
        "command": ["git", "apply", "--check", "--ignore-whitespace", str(diff_path)],
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": (completed.stdout or "")[-2000:],
        "stderr_tail": (completed.stderr or "")[-2000:],
    }


def _validation_commands(targets: list[str], diff_path: Path) -> list[str]:
    commands = [f"git apply --check --ignore-whitespace {diff_path}"]
    py_targets = [target for target in targets if target.endswith(".py")]
    if py_targets:
        commands.append("python -m py_compile " + " ".join(py_targets))
    commands.append("git diff --check")
    return commands


def _evidence_sources(repo_root: Path, evidence_reports: list[str]) -> tuple[list[tuple[str, str]], list[str]]:
    sources: list[tuple[str, str]] = []
    warnings: list[str] = []
    for raw in evidence_reports:
        path = _resolve(repo_root, raw)
        if not path.exists():
            warnings.append(f"evidence report not found: {raw}")
            continue
        text = _read_text(path)
        try:
            payload = json.loads(text)
        except Exception:
            sources.append((text, str(raw)))
        else:
            sources.extend(_json_text_sources(payload, str(raw)))
    return sources, warnings


def build_evidence_candidates(
    *,
    repo_root: Path,
    candidate_dir: Path,
    refs: list[RuntimeFileRef],
    evidence_reports: list[str],
    start_index: int,
    max_candidates: int,
    timeout: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    allowed = {ref.repo_relative for ref in refs if ref.patchable}
    candidates: list[dict[str, Any]] = []
    warnings: list[str] = []
    seen: set[str] = set()
    sources, source_warnings = _evidence_sources(repo_root, evidence_reports)
    warnings.extend(source_warnings)
    for source_text, source_ref in sources:
        for diff_text in _diff_blocks(source_text):
            if len(candidates) >= max_candidates:
                return candidates, warnings
            digest = hashlib.sha256(diff_text.encode("utf-8")).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            targets = diff_targets(diff_text)
            missing = [target for target in targets if target not in allowed]
            if not targets or missing:
                warnings.append(
                    f"evidence diff skipped; targets={targets} missing_from_verified={missing}"
                )
                continue
            safe_name = "__".join(targets).replace("/", "__").replace("\\", "__")
            diff_path = candidate_dir / f"{start_index + len(candidates):03d}_{safe_name}.diff"
            diff_path.write_text(diff_text, encoding="utf-8")
            check = _git_apply_check(repo_root, diff_path, max(30, timeout))
            passed = check.get("passed") is True
            candidates.append(
                {
                    "target_file": targets[0],
                    "target_files": targets,
                    "reason": "validated unified diff extracted from provider/proposal evidence",
                    "pattern_id": "evidence_unified_diff",
                    "evidence": [
                        f"evidence_report={source_ref}",
                        "all diff targets are verified repo-relative source paths",
                        "applicability checked with git apply --check",
                    ],
                    "unified_diff": diff_text,
                    "diff_path": str(diff_path),
                    "validation_commands": _validation_commands(targets, diff_path),
                    "applicability_check": check,
                    "semantic_check": {"passed": passed, "checks": ["git_apply_check"]},
                    "passed": passed,
                    "errors": [] if passed else [check.get("stderr_tail") or "git apply failed"],
                    "warnings": [],
                }
            )
    return candidates, warnings