#!/usr/bin/env python3
"""Smoke test artifact-owned patch candidate synthesis."""

from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CORE_RUNTIME_GUARD = True

try:
    from Tools.validation._shared.report_utils import write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.validation._shared.report_utils import write_json_report  # type: ignore


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def build_fixture(work_dir: Path) -> Path:
    repo = work_dir / "fixture_repo"
    target = repo / "ia_carmine" / "fixture_tool.py"
    write_text(
        target,
        """from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


def normalize_repo_path(repo_root: Path, raw: str) -> tuple[str, str]:
    text = str(raw or "").strip().replace("\\\\", "/")
    if not text:
        return "", "empty path"
    candidate = repo_root / text
    if not candidate.exists():
        return text, "path does not exist"
    return text, ""
""",
    )
    subprocess.run(["git", "init"], cwd=repo, capture_output=True, text=True, check=False)
    return repo


def read_json(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def unified_diff(rel_path: str, before: str, after: str) -> str:
    body = "\n".join(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=f"a/{rel_path}",
            tofile=f"b/{rel_path}",
            lineterm="",
        )
    )
    return f"diff --git a/{rel_path} b/{rel_path}\n{body}\n"


def write_evidence_report(path: Path, rel_path: str, before: str) -> None:
    after = before.replace(
        "return text, \"\"",
        "return text.replace(\"//\", \"/\"), \"\"",
        1,
    )
    report = {
        "kind": "provider_proposal_fixture",
        "target_files": [rel_path],
        "response_text": (
            "TARGET_FILES\n"
            f"- {rel_path}\n\n"
            "PATCH_SKETCH_UNIFIED_DIFF\n"
            "```diff\n"
            f"{unified_diff(rel_path, before, after)}"
            "```\n"
        ),
    }
    write_text(path, json.dumps(report, indent=2, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/patch_candidate_synthesis_smoke.json")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    work_dir = repo_root / "output" / "validation" / f"patch_candidate_synthesis_smoke_{stamp}"
    fixture_repo = build_fixture(work_dir)
    target = fixture_repo / "ia_carmine" / "fixture_tool.py"
    before = target.read_text(encoding="utf-8")
    candidate_json = fixture_repo / "output" / "validation" / "patch_candidate_synthesis.json"
    candidate_md = candidate_json.with_suffix(".md")
    evidence_json = fixture_repo / "output" / "validation" / "provider_evidence.json"
    write_evidence_report(evidence_json, "ia_carmine/fixture_tool.py", before)
    command = [
        sys.executable,
        "-m",
        "ia_carmine",
        "synthesize_patch_candidates",
        "--repo-root",
        str(fixture_repo),
        "--target-file",
        "ia_carmine/fixture_tool.py",
        "--operator-request",
        "extract provider unified diff for verified target",
        "--evidence-report",
        str(evidence_json),
        "--output",
        str(candidate_json),
        "--markdown-output",
        str(candidate_md),
        "--candidate-dir",
        str(fixture_repo / "output" / "validation" / "diffs"),
    ]
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        timeout=args.timeout_seconds,
    )
    data = read_json(candidate_json)
    after = target.read_text(encoding="utf-8")
    md_body = candidate_md.read_text(encoding="utf-8-sig") if candidate_md.exists() else ""
    errors: list[str] = []
    if completed.returncode != 0 or data.get("passed") is not True:
        errors.append("patch synthesis command failed")
    if int(data.get("patch_candidate_synthesis_passed_count") or 0) <= 0:
        errors.append("no validated candidate produced")
    if int(data.get("candidate_count") or 0) != 1:
        errors.append("provider evidence diff should produce exactly one candidate")
    candidates = data.get("candidates") if isinstance(data.get("candidates"), list) else []
    if not candidates or candidates[0].get("diff_source") != "evidence_owned":
        errors.append("candidate must be evidence_owned, not current worktree diagnostic")
    if data.get("current_worktree_diagnostic_candidate_count") != 0:
        errors.append("default synthesis must not copy current worktree diffs")
    if candidates and candidates[0].get("unified_diff"):
        errors.append("candidate report must not inline full unified_diff")
    if candidates and not candidates[0].get("diff_ref"):
        errors.append("candidate report must publish diff_ref")
    if before != after:
        errors.append("source file was modified by synthesis")
    if "```diff" in md_body:
        errors.append("markdown report must not inline full diff block")
    report = {
        "schema_version": 1,
        "kind": "patch_candidate_synthesis_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": not errors,
        "errors": errors,
        "command": command,
        "returncode": completed.returncode,
        "candidate_json": str(candidate_json),
        "candidate_markdown": str(candidate_md),
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
        "source_writes_performed": False,
        "patch_application_performed": False,
    }
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
