#!/usr/bin/env python3
"""Smoke-test heap/exchange closure audit helper."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


STAMP = "heap_exchange_closure_audit_smoke_20990101-010203"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/heap_exchange_closure_audit_smoke.json"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="heap-exchange-closure-audit-") as tmp_raw:
        repo = Path(tmp_raw) / "repo"
        repo.mkdir()

        peer = repo / "output/ai_packets/stamp/heap_peer_runtime_manifest.json"
        runtime_state = repo / "output/ai_packets/stamp/heap_exchange_runtime_state.jsonl"
        observer = repo / "output/local_ai_runs/stamp_observer"
        output = repo / "output/ai_packets/stamp/heap_exchange_closure_audit.json"
        markdown = repo / "output/ai_packets/stamp/heap_exchange_closure_audit.md"

        write_json(
            peer,
            {
                "schema_version": 1,
                "kind": "heap_peer_runtime_manifest",
                "passed": True,
                "dynamic_peers": [
                    {"id": "gpu1", "role": "primary advisory planner"},
                    {"id": "gpu0", "role": "companion OpenVINO tool worker"},
                    {"id": "npu", "role": "microoperation efficiency peer"},
                ],
                "audit_lane": {
                    "id": "deterministic_audit",
                    "role": "deterministic/script audit lane",
                    "reusable_before_heap_exchange_closure": True,
                },
            },
        )
        write_jsonl(
            runtime_state,
            [
                {"kind": "heap_peer_runtime_manifest", "summary": "GPU1/GPU0/NPU registered"},
                {
                    "kind": "deterministic_audit",
                    "summary": "script audit lane reusable before closure",
                },
            ],
        )

        env = dict(os.environ)
        env["PYTHONPATH"] = str(source_repo)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "Tools.ai",
                "heap_exchange_closure_audit",
                "--repo-root",
                str(repo),
                "--stamp",
                STAMP,
                "--heap-peer-runtime",
                str(peer),
                "--runtime-state",
                str(runtime_state),
                "--observer-dir",
                str(observer),
                "--output",
                str(output),
                "--markdown-output",
                str(markdown),
            ],
            cwd=repo,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        report = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
        if result.returncode != 0:
            errors.append(f"closure audit helper failed: {result.stderr[-500:]}")
        if report.get("passed") is not True:
            errors.append(f"closure audit report did not pass: {report.get('errors')}")
        if report.get("closure_state") != "ready_for_final_chain_contract":
            errors.append("closure audit did not reach ready_for_final_chain_contract")
        if report.get("npu_dynamic_role") != "microoperation_efficiency_peer":
            errors.append("NPU dynamic role regressed")
        if not markdown.exists():
            errors.append("closure audit markdown missing")
        if not (observer / "ai_public_events.jsonl").exists():
            errors.append("closure audit observer event missing")

    final = {
        "schema_version": 1,
        "kind": "heap_exchange_closure_audit_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": [],
    }

    output_path = resolve_output_path(source_repo, args.output)
    print(write_json_report(final, output_path), end="")
    return 0 if final["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
