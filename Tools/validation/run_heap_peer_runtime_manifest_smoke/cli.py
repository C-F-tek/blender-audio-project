#!/usr/bin/env python3
"""Smoke-test heap peer runtime manifest builder."""

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


STAMP = "heap_peer_runtime_manifest_smoke_20990101-010203"


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
        "--output", default="output/validation/heap_peer_runtime_manifest_smoke.json"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="heap-peer-runtime-manifest-smoke-") as tmp_raw:
        repo = Path(tmp_raw) / "repo"
        repo.mkdir()

        entry = repo / "output/ai_packets/stamp/heap_exchange_runtime_entry.json"
        runtime_state = repo / "output/ai_packets/stamp/heap_exchange_runtime_state.jsonl"
        observer = repo / "output/local_ai_runs/stamp_observer"
        output = repo / "output/ai_packets/stamp/heap_peer_runtime_manifest.json"
        markdown = repo / "output/ai_packets/stamp/heap_peer_runtime_manifest.md"

        write_json(
            entry,
            {
                "schema_version": 1,
                "kind": "heap_exchange_runtime_entry",
                "passed": True,
                "source_of_knowledge": "heap_exchange",
                "lanes": [
                    {"name": "gpu1", "role": "primary advisory planner", "available": True},
                    {"name": "gpu0", "role": "companion openvino tool worker", "available": True},
                    {"name": "npu", "role": "microoperation efficiency peer", "available": True},
                    {
                        "name": "deterministic_audit",
                        "role": "deterministic script audit lane",
                        "available": True,
                    },
                ],
            },
        )
        write_jsonl(
            runtime_state,
            [
                {"kind": "lane_registered", "lane": "gpu1", "role": "primary advisory planner"},
                {
                    "kind": "lane_registered",
                    "lane": "gpu0",
                    "role": "companion openvino tool worker",
                },
                {
                    "kind": "lane_registered",
                    "lane": "npu",
                    "role": "microoperation efficiency peer",
                },
                {"kind": "shared_memory", "summary": "heap exchange blackboard ai-to-ai bundle"},
            ],
        )

        env = dict(os.environ)
        env["PYTHONPATH"] = str(source_repo)
        result = subprocess.run(
            [
                sys.executable,
                str(source_repo / "Tools/ai/build_heap_peer_runtime_manifest/cli.py"),
                "--repo-root",
                str(repo),
                "--stamp",
                STAMP,
                "--runtime-entry",
                str(entry),
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
            errors.append(f"builder failed: {result.stderr[-500:]}")
        if report.get("passed") is not True:
            errors.append("manifest report did not pass")
        peers = {peer.get("id"): peer for peer in report.get("dynamic_peers") or []}
        for peer in ("gpu1", "gpu0", "npu"):
            if peer not in peers:
                errors.append(f"missing peer: {peer}")
            elif peers[peer].get("available") is not True:
                errors.append(f"peer not available: {peer}")
        if report.get("npu_role") != "microoperation efficiency peer":
            errors.append("NPU role is not microoperation efficiency peer")
        if "deterministic/script" not in str(report.get("audit_role")):
            errors.append("audit lane is not deterministic/script")
        if not markdown.exists():
            errors.append("markdown report missing")
        if not (observer / "ai_public_events.jsonl").exists():
            errors.append("observer public event missing")

    final = {
        "schema_version": 1,
        "kind": "heap_peer_runtime_manifest_smoke",
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
