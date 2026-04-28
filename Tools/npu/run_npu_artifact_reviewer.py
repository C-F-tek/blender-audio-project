#!/usr/bin/env python3
"""
Lightweight NPU-lane artifact reviewer.

This version is a safe deterministic fallback. It is intentionally small and can
later be extended with OpenVINO GenAI while preserving this fallback path.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def targets(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if input_path.is_dir():
        return sorted(input_path.glob("*.json"))
    return []


def review(path: Path) -> dict[str, Any]:
    try:
        payload = load_json(path)
        text = json.dumps(payload, ensure_ascii=False)
    except Exception as exc:
        return {"path": str(path), "review_score": 0.0, "warnings": [f"JSON read error: {exc}"], "positives": []}

    warnings: list[str] = []
    positives: list[str] = []
    if len(text) > 120000:
        warnings.append("Artifact is large for NPU prompt context; use compact summaries.")
    else:
        positives.append("Artifact size is suitable for compact review.")
    if isinstance(payload, dict) and payload.get("schema_version"):
        positives.append("schema_version present.")
    else:
        warnings.append("schema_version missing.")
    if "ShaderNodeTexMusgrave" in text:
        warnings.append("Blocked Blender node detected: ShaderNodeTexMusgrave.")
    if "C:\\Users\\" in text:
        warnings.append("Potential hardcoded Windows user path detected.")

    return {
        "path": str(path),
        "size_chars": len(text),
        "review_score": max(0.0, round(1.0 - len(warnings) * 0.15, 4)),
        "warnings": warnings,
        "positives": positives,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="output/ai_pipeline/npu_artifact_review.json")
    parser.add_argument("--device", default="NPU")
    parser.add_argument("--max-workers", type=int, default=4)
    args = parser.parse_args()

    items = targets(Path(args.input).resolve())
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.max_workers)) as pool:
        reviews = list(pool.map(review, items))
    warnings = [w for r in reviews for w in r.get("warnings", [])]
    avg = round(sum(r.get("review_score", 0.0) for r in reviews) / len(reviews), 4) if reviews else 0.0
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "backend": "heuristic",
        "requested_device": args.device,
        "review_count": len(reviews),
        "average_score": avg,
        "passed": not warnings,
        "reviews": reviews,
        "summary": {"warnings": warnings, "note": "Safe fallback reviewer for NPU-sized tasks."},
    }
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
