"""Smoke test generic runtime tool-cycle normalization."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ia_carmine.runtime.runtime_tool.tool_cycle_contract import normalize_tool_cycle_status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    cases = {
        "requested_unparsed": normalize_tool_cycle_status({"tool_requested": True}),
        "parsed_invalid": normalize_tool_cycle_status(
            {"tool_requested": True, "tool_call_parsed": True, "tool_call_validated": False}
        ),
        "result_pending_provider_resume": normalize_tool_cycle_status(
            {
                "tool": "runtime_file_window",
                "provider_native_tool_call": True,
                "returncode": 0,
                "executed": True,
                "passed": True,
                "outputs": {"json_report": "output/validation/tool_result.json"},
            }
        ),
        "result_consumed": normalize_tool_cycle_status(
            {
                "tool": "runtime_file_window",
                "provider_native_tool_call": True,
                "returncode": 0,
                "executed": True,
                "passed": True,
                "outputs": {"json_report": "output/validation/tool_result.json"},
                "tool_result_consumed_by_provider": True,
            }
        ),
    }
    expected = {name: name for name in cases}
    errors = [
        f"{name}: expected {status}, got {cases[name].get('tool_status')}"
        for name, status in expected.items()
        if cases[name].get("tool_status") != status
    ]
    report = {
        "schema_version": 1,
        "kind": "runtime_tool_cycle_contract_smoke",
        "repo_root": str(repo_root),
        "passed": not errors,
        "tool_statuses": {key: value.get("tool_status") for key, value in cases.items()},
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
