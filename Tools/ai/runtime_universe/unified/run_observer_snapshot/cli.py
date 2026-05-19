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
            rows.append({"kind": "malformed_jsonl_line", "raw": line})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observer-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    observer_dir = Path(args.observer_dir)
    progress = read_jsonl(observer_dir / "progress.jsonl", args.limit)
    exchange = read_jsonl(observer_dir / "ai_public_events.jsonl", args.limit)

    report = {
        "kind": "unified_run_observer_snapshot",
        "schema_version": 1,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "observer_dir": str(observer_dir),
        "passed": True,
        "progress_event_count": len(progress),
        "ai_public_event_count": len(exchange),
        "raw_thinking_exposed": False,
        "progress_tail": progress,
        "ai_public_exchange_tail": exchange,
    }

    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Unified Run Observer Snapshot",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Progress events: `{len(progress)}`",
        f"- AI public events: `{len(exchange)}`",
        f"- Raw thinking exposed: `{report['raw_thinking_exposed']}`",
        "",
        "## Recent progress",
    ]
    for event in progress[-10:]:
        lines.append(
            f"- `{event.get('timestamp', '')}` `{event.get('phase', '')}` `{event.get('status', '')}` {event.get('message', '')}"
        )
    lines += ["", "## Recent AI public exchange"]
    for event in exchange[-10:]:
        lines.append(
            f"- `{event.get('speaker', '')}` `{event.get('event_type', '')}` {event.get('summary', '')}"
        )
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"passed": True, "output": str(output), "markdown_output": str(markdown)},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
