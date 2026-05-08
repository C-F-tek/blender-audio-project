#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def read_jsonl(path: Path, limit: int) -> list[dict]:
    if not path.is_file():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"kind": "malformed_jsonl_line", "raw": line[:500]})
    return rows


def probe_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return {"path": str(path), "read_error": str(exc)}
    return {
        "path": str(path),
        "kind": data.get("kind", ""),
        "passed": data.get("passed", None),
        "failed_count": data.get("failed_count", None),
        "warning_count": data.get("warning_count", len(data.get("warnings", [])) if isinstance(data.get("warnings"), list) else None),
        "error_count": data.get("error_count", len(data.get("errors", [])) if isinstance(data.get("errors"), list) else None),
        "provider_execution_performed": data.get("provider_execution_performed", None),
        "patch_application_performed": data.get("patch_application_performed", None),
        "git_write_performed": data.get("git_write_performed", None),
        "stdout_tail": str(data.get("stdout_tail", ""))[-500:],
        "stderr_tail": str(data.get("stderr_tail", ""))[-500:],
    }


def latest_json_reports(repo_root: Path, limit: int) -> list[dict]:
    roots = [
        repo_root / "output/validation",
        repo_root / "output/ai_pipeline",
        repo_root / "output/ai_packets",
        repo_root / "docs/LOCAL_VALIDATION_EVIDENCE",
    ]
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(path for path in root.rglob("*.json") if path.is_file())
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return [probe_json(path) for path in files[:limit]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--observer-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--limit", type=int, default=60)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    observer_dir = Path(args.observer_dir)
    progress = read_jsonl(observer_dir / "progress.jsonl", args.limit)
    reports = latest_json_reports(repo_root, args.limit)

    report = {
        "kind": "unified_raw_debug_good_info_feed",
        "schema_version": 1,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": True,
        "raw_hidden_chain_of_thought_exposed": False,
        "observer_dir": str(observer_dir),
        "progress_event_count": len(progress),
        "report_count": len(reports),
        "progress_tail": progress,
        "latest_reports": reports,
    }

    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Unified RAW Debug Good Info Feed",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Raw hidden chain-of-thought exposed: `{report['raw_hidden_chain_of_thought_exposed']}`",
        f"- Progress events: `{len(progress)}`",
        f"- Reports inspected: `{len(reports)}`",
        "",
        "## Recent progress",
    ]
    for event in progress[-20:]:
        lines.append(f"- `{event.get('phase','')}` `{event.get('status','')}` {event.get('message','')}")
    lines.extend(["", "## Latest JSON reports"])
    for item in reports[:25]:
        lines.append(
            f"- `{item.get('kind','')}` passed=`{item.get('passed','')}` failed=`{item.get('failed_count','')}` warnings=`{item.get('warning_count','')}` `{item.get('path','')}`"
        )
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"passed": True, "output": str(output), "markdown_output": str(markdown)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
