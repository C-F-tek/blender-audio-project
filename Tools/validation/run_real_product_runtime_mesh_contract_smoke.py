#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/real_product_runtime_mesh_contract_smoke.json"
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    contract_json = (
        repo_root / "output/validation/real_product_runtime_mesh_contract_smoke_contract.json"
    )
    contract_md = (
        repo_root / "output/validation/real_product_runtime_mesh_contract_smoke_contract.md"
    )

    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo_root)

    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "Tools/validation/check_real_product_runtime_mesh_contract.py"),
            "--repo-root",
            str(repo_root),
            "--output",
            str(contract_json),
            "--markdown-output",
            str(contract_md),
        ],
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    contract = (
        json.loads(contract_json.read_text(encoding="utf-8-sig")) if contract_json.exists() else {}
    )
    errors: list[str] = []

    require(result.returncode == 0, errors, "runtime mesh contract validator failed")
    require(contract.get("passed") is True, errors, "runtime mesh contract did not pass")

    for key in contract.get("capability_order") or []:
        require(contract.get(key) is True, errors, f"runtime mesh capability failed: {key}")

    require(contract_md.exists(), errors, "runtime mesh markdown report missing")

    report = {
        "schema_version": 1,
        "kind": "real_product_runtime_mesh_contract_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "contract_report": contract,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
