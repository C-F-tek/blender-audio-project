#!/usr/bin/env python3
"""Validate a produced GPU1 one-turn runtime gate report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return {"_read_error": f"{type(exc).__name__}: {exc}"}
    return data if isinstance(data, dict) else {"_read_error": "gate report is not a JSON object"}


def validate_gate(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("_read_error"):
        return [str(report["_read_error"])]
    if report.get("kind") != "gpu1_one_turn_runtime_gate":
        errors.append("kind_not_gpu1_one_turn_runtime_gate")
    if report.get("passed") is not True:
        errors.append("gpu1_one_turn_runtime_gate_not_passed")
    if int(report.get("gpu1_turn0_native_tool_call_count") or report.get("gpu1_one_turn_native_tool_call_count") or 0) <= 0:
        errors.append("gpu1_one_turn_native_tool_call_missing")
    if int(report.get("broker_result_passed_count") or report.get("gpu1_one_turn_broker_result_passed_count") or 0) <= 0:
        errors.append("gpu1_one_turn_broker_result_missing")
    if report.get("role_tool_reinjected") is not True and report.get("gpu1_one_turn_role_tool_reinjected") is not True:
        errors.append("gpu1_one_turn_role_tool_reinjection_missing")
    if report.get("tool_result_consumed_by_gpu1") is not True and report.get("gpu1_one_turn_tool_result_consumed") is not True:
        errors.append("gpu1_one_turn_tool_result_not_consumed")
    if report.get("final_product_delta_valid") is not True and report.get("gpu1_one_turn_final_product_delta_valid") is not True:
        errors.append("gpu1_one_turn_final_product_delta_empty")
    return errors


def build_report(repo_root: Path, gate_report: Path) -> dict[str, Any]:
    report = read_json(gate_report)
    errors = validate_gate(report)
    return {
        "schema_version": 1,
        "kind": "gpu1_one_turn_runtime_gate_validation",
        "repo_root": str(repo_root),
        "gate_report": str(gate_report),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--gate-report", required=True)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    gate_report = Path(args.gate_report)
    if not gate_report.is_absolute():
        gate_report = repo_root / gate_report
    result = build_report(repo_root, gate_report.resolve(strict=False))
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
