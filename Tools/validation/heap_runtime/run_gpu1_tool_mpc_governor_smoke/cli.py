"""Smoke test GPU1 MPC-lite tool governor decisions without providers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from ia_carmine.runtime.heap_gate.gpu1_tool_mpc_governor import (
    build_gpu1_tool_mpc_governor_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    owner = SimpleNamespace(provider_reports=[], repo_root=repo_root)
    cases = {
        "pending_tool_result": build_gpu1_tool_mpc_governor_report(
            owner,
            [],
            response_text="",
            revision=1,
            gpu1_tool_result_consumption={
                "gpu1_unconsumed_tool_result_ids": ["tool-1"],
                "gpu1_tool_result_blocker": "gpu1_requested_tool_result_not_consumed",
            },
        ),
        "same_tool_repeat": build_gpu1_tool_mpc_governor_report(
            owner,
            [],
            response_text="",
            revision=1,
            gpu1_tool_result_consumption={
                "gpu1_tool_result_ledger": [
                    {"tool": "runtime_file_refs", "args_ref": {"query": "x"}},
                    {"tool": "runtime_file_refs", "args_ref": {"query": "x"}},
                ]
            },
        ),
        "failed_tool_consumed": build_gpu1_tool_mpc_governor_report(
            owner,
            [],
            response_text="",
            revision=1,
            gpu1_tool_result_consumption={
                "gpu1_consumed_failed_tool_result_ids": ["tool-failed"]
            },
        ),
        "valid_final_delta": build_gpu1_tool_mpc_governor_report(
            owner,
            [],
            response_text="",
            revision=1,
            final_product_protocol={"passed": True},
            gpu1_tool_result_consumption={},
        ),
    }
    expected = {
        "pending_tool_result": "force_consume_tool_result",
        "same_tool_repeat": "block_repeat_tool_call",
        "failed_tool_consumed": "block_with_reason",
        "valid_final_delta": "emit_final_delta",
    }
    decisions = {key: value.get("decision") for key, value in cases.items()}
    errors = [
        f"{key}: expected {decision}, got {decisions.get(key)}"
        for key, decision in expected.items()
        if decisions.get(key) != decision
    ]
    report = {
        "schema_version": 1,
        "kind": "gpu1_tool_mpc_governor_smoke",
        "repo_root": str(repo_root),
        "passed": not errors,
        "decisions": decisions,
        "first_blockers": {key: value.get("first_blocker") for key, value in cases.items()},
        "cases": cases,
        "errors": errors,
    }
    _write(args.output, repo_root, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


def _write(output: str, repo_root: Path, report: dict[str, Any]) -> None:
    if not output:
        return
    path = Path(output)
    if not path.is_absolute():
        path = repo_root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
