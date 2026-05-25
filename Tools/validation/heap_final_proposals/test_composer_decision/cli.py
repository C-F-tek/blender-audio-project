#!/usr/bin/env python3
"""Smoke-test heap final proposal decision outputs."""

from __future__ import annotations

import json
import os
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]


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
    env["PYTHONPATH"] = str(REPO_ROOT)
    env["IA_CARMINE_ALLOW_INTERNAL_DISPATCH"] = "1"
    cmd = [
        sys.executable,
        "-m",
        "ia_carmine",
        "heap_final_proposals",
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


def test_all_rejected_gives_blocked_provider_review() -> None:
    """When proposals exist but all are rejected for quality, decision is BLOCKED_PROVIDER_REVIEW."""
    with tempfile.TemporaryDirectory(prefix="composer-decision-") as tmp:
        run_dir = Path(tmp) / "run"
        proposal_dir = run_dir / "team_context" / "proposal_iterations"
        # Write two proposals with same content (similarity loop breaker) targeting allowed source
        text = "TARGET_FILES: ia_carmine/product/heap_final_proposals/cli.py\n\ndef foo():\n    return 1"
        write_proposal(proposal_dir, "001", "ia_carmine/product/heap_final_proposals/cli.py", text, False)
        write_proposal(proposal_dir, "002", "ia_carmine/product/heap_final_proposals/cli.py", text, False)
        payload = run_composer(run_dir, ["ia_carmine/product/heap_final_proposals/cli.py"])
        decision = payload["operator_decision"]["decision"]
        assert decision == "BLOCKED_PROVIDER_REVIEW", (
            f"Expected BLOCKED_PROVIDER_REVIEW, got {decision}"
        )
        reasons = "\n".join(payload["operator_decision"]["gate_reasons"])
        assert "repeated rejected proposal" in reasons


def test_accepted_proposal_gives_patchable() -> None:
    """When at least one proposal is accepted and passes gate, decision is ACCEPTED_PATCHABLE."""
    with tempfile.TemporaryDirectory(prefix="composer-decision-") as tmp:
        run_dir = Path(tmp) / "run"
        proposal_dir = run_dir / "team_context" / "proposal_iterations"
        target = "ia_carmine/product/heap_final_proposals/cli.py"
        text = (
            f"TARGET_FILES: {target}\n\n"
            "IMPLEMENTATION_CHANGES:\n"
            "- Wire operator_decision into the composer output.\n\n"
            "VALIDATION_COMMANDS:\n"
            "- python -m py_compile ia_carmine/product/heap_final_proposals/cli.py\n"
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
        target = "ia_carmine/product/heap_final_proposals/cli.py"
        text = f"TARGET_FILES: {target}\n\nIMPLEMENTATION_CHANGES:\n- Test.\n\nVALIDATION_COMMANDS:\n- python -m py_compile {target}\n"
        write_proposal(proposal_dir, "001", target, text, True)
        payload = run_composer(run_dir, [target])
        decision_text = payload["operator_decision_text"]
        assert "Targets considered" in decision_text
        assert "heap_final_proposals" in decision_text


def main() -> int:
    cases = {
        "no_verified_target": test_no_verified_target_emits_blocked,
        "all_rejected": test_all_rejected_gives_blocked_provider_review,
        "accepted_patchable": test_accepted_proposal_gives_patchable,
        "forbidden_markers": test_forbidden_markers_also_set_blocked,
        "decision_targets": test_decision_file_lists_targets,
    }
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--section",
        action="append",
        default=[],
        help="Optional test section to run. Omit to run all composer decision sections.",
    )
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    selected = [str(item).strip() for item in args.section or [] if str(item).strip()]
    if args.list:
        print(json.dumps({"sections": sorted(cases)}, indent=2))
        return 0
    unknown = sorted(set(selected) - set(cases))
    if unknown:
        raise SystemExit(f"unknown test section(s): {', '.join(unknown)}")
    for name in selected or list(cases):
        cases[name]()
    print("composer decision smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
