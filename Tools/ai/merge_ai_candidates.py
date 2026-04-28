#!/usr/bin/env python3
"""Deterministically merge AI mapping candidates."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def score(candidate: dict[str, Any]) -> float:
    for key in ("score", "confidence", "rank_score"):
        if isinstance(candidate.get(key), (int, float)):
            return float(candidate[key])
    return 0.5


def extract(payload: Any, source: Path) -> list[dict[str, Any]]:
    raw = payload.get("candidates", []) if isinstance(payload, dict) else payload if isinstance(payload, list) else [payload]
    out = []
    for i, item in enumerate(raw):
        candidate = dict(item) if isinstance(item, dict) else {"description": str(item)}
        candidate.setdefault("source", str(source))
        candidate.setdefault("candidate_id", f"{source.stem}:{i}")
        candidate.setdefault("score", score(candidate))
        out.append(candidate)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--output", default="output/ai_pipeline/ai_selected_mapping.json")
    parser.add_argument("--limit", type=int, default=2)
    args = parser.parse_args()

    candidates = []
    for item in args.input:
        path = Path(item).resolve()
        if path.exists():
            candidates.extend(extract(load_json(path), path))
    ranked = sorted(candidates, key=score, reverse=True)
    selected = ranked[: max(args.limit, 1)]
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "selection_policy": "highest score/confidence first",
        "selected": selected[0] if selected else {"candidate_id": "none", "score": 0.0},
        "selected_candidates": selected,
        "all_candidate_count": len(candidates),
    }
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
