#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    observer_dir = repo_root / "output/validation/unified_observer_extended_smoke_observer"
    observer_dir.mkdir(parents=True, exist_ok=True)

    (observer_dir / "current_state.json").write_text(
        json.dumps(
            {
                "kind": "unified_run_observer_state",
                "schema_version": 1,
                "stamp": "extended_observer_smoke",
                "repo_root": str(repo_root),
                "run_dir": str(repo_root / "output/validation/unified_observer_extended_smoke_run"),
                "observer_dir": str(observer_dir),
                "raw_thinking_exposed": False,
                "ai_public_exchange_only": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    (observer_dir / "progress.jsonl").write_text(
        json.dumps(
            {
                "kind": "unified_run_progress_event",
                "phase": "observer",
                "status": "initialized",
                "message": "",
            }
        )
        + "\n"
        + json.dumps(
            {
                "kind": "unified_run_progress_event",
                "phase": "smoke",
                "status": "passed",
                "message": "",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    (observer_dir / "ai_public_events.jsonl").write_text(
        json.dumps(
            {
                "kind": "ai_public_exchange_event",
                "lane": "official",
                "speaker": "AI1",
                "event_type": "recommendation",
                "summary": "Extended observer smoke public recommendation.",
                "raw_thinking_exposed": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    conversation_json = repo_root / "output/validation/unified_ai_conversation_feed_smoke.json"
    conversation_md = repo_root / "output/validation/unified_ai_conversation_feed_smoke.md"
    raw_json = repo_root / "output/validation/unified_raw_debug_good_info_feed_smoke.json"
    raw_md = repo_root / "output/validation/unified_raw_debug_good_info_feed_smoke.md"

    commands = [
        [
            sys.executable,
            str(repo_root / "ia_carmine/runtime/runtime_universe/unified/ai_conversation_feed/cli.py"),
            "--repo-root",
            str(repo_root),
            "--observer-dir",
            str(observer_dir),
            "--output",
            str(conversation_json),
            "--markdown-output",
            str(conversation_md),
        ],
        [
            sys.executable,
            str(repo_root / "ia_carmine/runtime/runtime_universe/unified/raw_debug_good_info_feed/cli.py"),
            "--repo-root",
            str(repo_root),
            "--observer-dir",
            str(observer_dir),
            "--output",
            str(raw_json),
            "--markdown-output",
            str(raw_md),
        ],
    ]

    results = [run(cmd, repo_root) for cmd in commands]
    passed = all(result.returncode == 0 for result in results)

    payloads = []
    for path in (conversation_json, raw_json):
        if path.is_file():
            payloads.append(json.loads(path.read_text(encoding="utf-8")))
        else:
            passed = False

    passed = passed and all(
        payload.get("raw_hidden_chain_of_thought_exposed") is False for payload in payloads
    )

    report = {
        "kind": "unified_observer_extended_smoke",
        "schema_version": 1,
        "passed": passed,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "raw_hidden_chain_of_thought_exposed": False,
        "results": [
            {
                "returncode": result.returncode,
                "stdout_tail": result.stdout[-1000:],
                "stderr_tail": result.stderr[-1000:],
            }
            for result in results
        ],
    }

    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    markdown.write_text(
        "# Unified Observer Extended Smoke\n\n"
        f"- Passed: `{passed}`\n"
        "- Provider execution performed: `False`\n"
        "- Patch application performed: `False`\n"
        "- Raw hidden chain-of-thought exposed: `False`\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"passed": passed, "output": str(output), "markdown_output": str(markdown)}, indent=2
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
