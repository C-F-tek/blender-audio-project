#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

PATTERNS = (
    "proposal",
    "recommend",
    "patch",
    "plan",
    "peer",
    "broker",
    "decision",
    "warning",
    "quality",
    "runtime",
)


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


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return {"read_error": str(exc)}


def summarize_json(path: Path) -> dict:
    data = read_json(path)
    return {
        "path": str(path),
        "kind": data.get("kind", ""),
        "passed": data.get("passed", None),
        "summary": data.get("summary", data.get("title", "")),
        "recommendation_count": data.get(
            "recommendation_count",
            (
                len(data.get("recommendations", []))
                if isinstance(data.get("recommendations"), list)
                else None
            ),
        ),
        "patch_plan_count": data.get(
            "patch_plan_count",
            (
                len(data.get("patch_plans", []))
                if isinstance(data.get("patch_plans"), list)
                else None
            ),
        ),
        "warning_count": data.get(
            "warning_count",
            (len(data.get("warnings", [])) if isinstance(data.get("warnings"), list) else None),
        ),
        "failed_count": data.get("failed_count", None),
        "provider_execution_performed": data.get("provider_execution_performed", None),
        "read_error": data.get("read_error", ""),
    }


def candidate_files(repo_root: Path, limit: int) -> list[Path]:
    roots = [
        repo_root / "output/ai_pipeline",
        repo_root / "output/patch_specs",
        repo_root / "output/validation",
        repo_root / "output/ai_packets",
        repo_root / "docs/LOCAL_VALIDATION_EVIDENCE",
    ]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md"}:
                name = path.name.lower()
                if any(pattern in name for pattern in PATTERNS):
                    files.append(path)
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[:limit]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--observer-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    observer_dir = Path(args.observer_dir)
    events = read_jsonl(observer_dir / "ai_public_events.jsonl", args.limit)
    progress = read_jsonl(observer_dir / "progress.jsonl", min(args.limit, 20))
    surfaces = []
    for path in candidate_files(repo_root, args.limit):
        item = {
            "path": str(path),
            "mtime": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
        }
        if path.suffix.lower() == ".json":
            item.update(summarize_json(path))
        surfaces.append(item)

    report = {
        "kind": "unified_ai_conversation_feed",
        "schema_version": 1,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": True,
        "raw_hidden_chain_of_thought_exposed": False,
        "observer_dir": str(observer_dir),
        "event_count": len(events),
        "surface_count": len(surfaces),
        "ai_public_events_tail": events,
        "progress_tail": progress,
        "public_report_surfaces": surfaces,
    }

    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Unified AI Conversation Feed",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Raw hidden chain-of-thought exposed: `{report['raw_hidden_chain_of_thought_exposed']}`",
        f"- Event count: `{len(events)}`",
        f"- Surface count: `{len(surfaces)}`",
        "",
        "## AI public events",
    ]
    for event in events[-20:]:
        lines.append(
            f"- `{event.get('speaker', '')}` `{event.get('event_type', '')}` {event.get('summary', event.get('message', ''))}"
        )
    lines.extend(["", "## Public report surfaces"])
    for item in surfaces[:20]:
        lines.append(
            f"- `{item.get('kind', '')}` passed=`{item.get('passed', '')}` `{item.get('path', '')}`"
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
