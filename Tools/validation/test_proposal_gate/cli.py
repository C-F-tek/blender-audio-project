#!/usr/bin/env python3
"""Smoke-test proposal gating in compose_heap_final_proposals.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
COMPOSER = REPO_ROOT / "Tools" / "ai" / "compose_heap_final_proposals.py"


def write_proposal(
    proposal_dir: Path,
    name: str,
    source: str,
    response_text: str,
    accepted: bool,
) -> None:
    proposal_dir.mkdir(parents=True, exist_ok=True)
    proposal = {
        "name": name,
        "revision": name,
        "source": source,
        "response_text": response_text,
        "quality_passed": accepted,
        "implementation_quality": {"errors": []},
        "proposal_progress": {"errors": []},
    }
    json_path = proposal_dir / f"heap_proposal_revision_{name}.json"
    json_path.write_text(json.dumps(proposal, indent=2), encoding="utf-8")
    json_path.with_suffix(".md").write_text(
        f"# Proposal {name}\n\n{response_text}\n",
        encoding="utf-8",
    )


def run_composer(run_dir: Path, allowlist: list[str]) -> dict[str, Any]:
    allowlist_path = run_dir / "allowlist.json"
    allowlist_path.write_text(json.dumps(allowlist), encoding="utf-8")
    documents_root = run_dir / "documents"
    env = os.environ.copy()
    env["PROPOSAL_ALLOWLIST_PATH"] = str(allowlist_path)
    cmd = [
        sys.executable,
        str(COMPOSER),
        "--repo-root",
        str(REPO_ROOT),
        "--run-dir",
        str(run_dir),
        "--documents-root",
        str(documents_root),
        "--write-documents",
    ]
    completed = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    if completed.returncode not in {0, 2}:
        raise AssertionError(
            "composer failed unexpectedly\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    payload = json.loads(completed.stdout)
    decision_file = Path(payload["documents_dir"]) / "OPERATOR_DECISION.txt"
    if not decision_file.exists():
        raise AssertionError(f"missing decision file: {decision_file}")
    payload["operator_decision_text"] = decision_file.read_text(encoding="utf-8")
    return payload


def test_fake_source_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="proposal-gate-") as tmp:
        run_dir = Path(tmp) / "run"
        proposal_dir = run_dir / "team_context" / "proposal_iterations"
        write_proposal(
            proposal_dir,
            "001",
            "tools/fake/real_existing_file.py",
            "some code with pass/TODO",
            False,
        )
        payload = run_composer(run_dir, [])
        decision = payload["operator_decision"]["decision"]
        assert decision == "BLOCKED_NO_VERIFIED_TARGET", decision
        assert "forbidden placeholder" in payload["operator_decision_text"]


def test_similarity_loop_breaker() -> None:
    with tempfile.TemporaryDirectory(prefix="proposal-gate-") as tmp:
        run_dir = Path(tmp) / "run"
        proposal_dir = run_dir / "team_context" / "proposal_iterations"
        text = "TARGET_FILES: src/module.py\n\ndef foo():\n    return 1"
        write_proposal(proposal_dir, "001", "src/module.py", text, False)
        write_proposal(
            proposal_dir,
            "002",
            "src/module.py",
            text,
            False,
        )
        payload = run_composer(run_dir, ["src/module.py"])
        decision = payload["operator_decision"]["decision"]
        assert decision == "DIAGNOSTIC_ONLY", decision
        reasons = "\n".join(payload["operator_decision"]["gate_reasons"])
        assert "repeated rejected proposal" in reasons


def test_accepted_patchable_target() -> None:
    with tempfile.TemporaryDirectory(prefix="proposal-gate-") as tmp:
        run_dir = Path(tmp) / "run"
        proposal_dir = run_dir / "team_context" / "proposal_iterations"
        target = "Tools/ai/heap_final_proposals/cli.py"
        text = (
            f"TARGET_FILES: {target}\n\n"
            "IMPLEMENTATION_CHANGES:\n"
            "- Wire operator_decision into the composer output.\n\n"
            "VALIDATION_COMMANDS:\n"
            "- python -m py_compile Tools/ai/heap_final_proposals/cli.py\n"
        )
        write_proposal(proposal_dir, "001", target, text, True)
        payload = run_composer(run_dir, [target])
        decision = payload["operator_decision"]["decision"]
        assert decision == "ACCEPTED_PATCHABLE", decision
        assert payload["operator_decision"]["accepted_count"] == 1


def main() -> int:
    test_fake_source_rejected()
    test_similarity_loop_breaker()
    test_accepted_patchable_target()
    print("proposal gate smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
