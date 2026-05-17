#!/usr/bin/env python3
"""Smoke-test composer decision output: OPERATOR_DECISION.txt and HUMAN_PATCH_PROPOSAL.md."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
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


def test_no_verified_target_emits_blocked() -> None:
    """When all proposals use fake sources and allowlist is empty, decision must be BLOCKED_NO_VERIFIED_TARGET."""
    with tempfile.TemporaryDirectory(prefix="composer-decision-") as tmp:
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
        assert decision == "BLOCKED_NO_VERIFIED_TARGET", (
            f"Expected BLOCKED_NO_VERIFIED_TARGET, got {decision}"
        )
        assert "forbidden placeholder" in payload["operator_decision_text"]
        # Verify OPERATOR_DECISION.txt content
        assert "BLOCKED_NO_VERIFIED_TARGET" in payload["operator_decision_text"]


def test_all_rejected_gives_diagnostic_only() -> None:
    """When proposals exist but all are rejected for quality (not fake-path), decision is DIAGNOSTIC_ONLY."""
    with tempfile.TemporaryDirectory(prefix="composer-decision-") as tmp:
        run_dir = Path(tmp) / "run"
        proposal_dir = run_dir / "team_context" / "proposal_iterations"
        # Write two proposals with same content (similarity loop breaker) targeting allowed source
        text = "TARGET_FILES: Tools/ai/compose_heap_final_proposals.py\n\ndef foo():\n    return 1"
        write_proposal(proposal_dir, "001", "Tools/ai/compose_heap_final_proposals.py", text, False)
        write_proposal(proposal_dir, "002", "Tools/ai/compose_heap_final_proposals.py", text, False)
        payload = run_composer(run_dir, ["Tools/ai/compose_heap_final_proposals.py"])
        decision = payload["operator_decision"]["decision"]
        assert decision == "DIAGNOSTIC_ONLY", f"Expected DIAGNOSTIC_ONLY, got {decision}"
        reasons = "\n".join(payload["operator_decision"]["gate_reasons"])
        assert "repeated rejected proposal" in reasons


def test_accepted_proposal_gives_patchable() -> None:
    """When at least one proposal is accepted and passes gate, decision is ACCEPTED_PATCHABLE."""
    with tempfile.TemporaryDirectory(prefix="composer-decision-") as tmp:
        run_dir = Path(tmp) / "run"
        proposal_dir = run_dir / "team_context" / "proposal_iterations"
        target = "Tools/ai/compose_heap_final_proposals.py"
        text = (
            f"TARGET_FILES: {target}\n\n"
            "IMPLEMENTATION_CHANGES:\n"
            "- Wire operator_decision into the composer output.\n\n"
            "VALIDATION_COMMANDS:\n"
            "- python -m py_compile Tools/ai/compose_heap_final_proposals.py\n"
        )
        write_proposal(proposal_dir, "001", target, text, True)
        payload = run_composer(run_dir, [target])
        decision = payload["operator_decision"]["decision"]
        assert decision == "ACCEPTED_PATCHABLE", f"Expected ACCEPTED_PATCHABLE, got {decision}"
        assert payload["operator_decision"]["accepted_count"] == 1


def test_forbidden_markers_also_set_blocked() -> None:
    """Proposals with FIXME markers and fake source paths result in BLOCKED_NO_VERIFIED_TARGET."""
    with tempfile.TemporaryDirectory(prefix="composer-decision-") as tmp:
        run_dir = Path(tmp) / "run"
        proposal_dir = run_dir / "team_context" / "proposal_iterations"
        write_proposal(
            proposal_dir,
            "001",
            "Tools/data_processor/real_existing_file.py",
            "some code with FIXME here",
            False,
        )
        payload = run_composer(run_dir, [])
        decision = payload["operator_decision"]["decision"]
        assert decision == "BLOCKED_NO_VERIFIED_TARGET", (
            f"Expected BLOCKED_NO_VERIFIED_TARGET, got {decision}"
        )
        decision_text = payload["operator_decision_text"]
        assert "forbidden placeholder" in decision_text


def test_decision_file_lists_targets() -> None:
    """OPERATOR_DECISION.txt must list targets considered."""
    with tempfile.TemporaryDirectory(prefix="composer-decision-") as tmp:
        run_dir = Path(tmp) / "run"
        proposal_dir = run_dir / "team_context" / "proposal_iterations"
        target = "Tools/ai/compose_heap_final_proposals.py"
        text = f"TARGET_FILES: {target}\n\nIMPLEMENTATION_CHANGES:\n- Test.\n\nVALIDATION_COMMANDS:\n- python -m py_compile {target}\n"
        write_proposal(proposal_dir, "001", target, text, True)
        payload = run_composer(run_dir, [target])
        decision_text = payload["operator_decision_text"]
        assert "Targets considered" in decision_text
        assert "compose_heap_final_proposals.py" in decision_text


def main() -> int:
    test_no_verified_target_emits_blocked()
    test_all_rejected_gives_diagnostic_only()
    test_accepted_proposal_gives_patchable()
    test_forbidden_markers_also_set_blocked()
    test_decision_file_lists_targets()
    print("composer decision smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
