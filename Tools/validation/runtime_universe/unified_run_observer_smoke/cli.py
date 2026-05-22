#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    observer_dir = repo_root / "output/validation/unified_run_observer_smoke_observer"
    observer_dir.mkdir(parents=True, exist_ok=True)
    (observer_dir / "progress.jsonl").write_text(
        json.dumps({"kind": "unified_run_progress_event", "phase": "smoke", "status": "passed"})
        + "\n",
        encoding="utf-8",
    )
    (observer_dir / "ai_public_events.jsonl").write_text(
        json.dumps(
            {
                "kind": "ai_public_exchange_event",
                "speaker": "AI1",
                "event_type": "recommendation",
                "summary": "smoke public event",
                "raw_thinking_exposed": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    snapshot_json = repo_root / "output/validation/unified_run_observer_snapshot_smoke.json"
    snapshot_md = repo_root / "output/validation/unified_run_observer_snapshot_smoke.md"
    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "ia_carmine/runtime/runtime_universe/unified/run_observer_snapshot/cli.py"),
            "--observer-dir",
            str(observer_dir),
            "--output",
            str(snapshot_json),
            "--markdown-output",
            str(snapshot_md),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
    )

    report = {
        "kind": "unified_run_observer_smoke",
        "schema_version": 1,
        "passed": result.returncode == 0 and snapshot_json.is_file() and snapshot_md.is_file(),
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-1000:],
        "stderr_tail": result.stderr[-1000:],
        "guardrails": {"raw_thinking_exposed": False, "provider_execution_performed": False},
    }

    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    markdown.write_text(
        f"# Unified Run Observer Smoke\n\n- Passed: `{report['passed']}`\n", encoding="utf-8"
    )
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
