#!/usr/bin/env python3
"""NPU-sized artifact reviewer with deterministic fallback."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def list_targets(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(path.glob("*.json"))
    return []


def expect_for_name(
    path: Path, data: dict[str, Any], warnings: list[str], positives: list[str]
) -> None:
    name = path.name
    if name == "track_summary.json":
        readiness = data.get("ai_readiness") or {}
        score = readiness.get("score")
        if isinstance(score, (int, float)):
            positives.append(f"ai_readiness={score}")
            if score < 0.5:
                warnings.append("Low ai_readiness score; planner needs more manual context.")
        if data.get("primary_series_trend"):
            positives.append(f"primary_series_trend={data.get('primary_series_trend')}")
    elif name == "music_segments.json":
        segments = data.get("segments") or []
        if segments:
            positives.append(f"segments={len(segments)}")
        if not all(isinstance(s, dict) and s.get("visual_directive") for s in segments):
            warnings.append("Some segments are missing visual_directive metadata.")
    elif name == "ai_mapping_candidates.json":
        candidates = data.get("candidates") or []
        if len(candidates) >= 2:
            positives.append(f"mapping_candidates={len(candidates)}")
        else:
            warnings.append("Not enough mapping candidates for robust AI selection.")
    elif name == "ai_scene_brief.json":
        if data.get("recommended_visual_progression"):
            positives.append("recommended_visual_progression present.")
        if not data.get("assumptions"):
            warnings.append("Scene brief has no explicit assumptions.")


def review(path: Path) -> dict[str, Any]:
    try:
        data = load(path)
        text = json.dumps(data, ensure_ascii=False)
    except Exception as exc:
        return {
            "path": str(path),
            "review_score": 0.0,
            "warnings": [f"JSON read error: {exc}"],
            "positives": [],
            "ai_usefulness": "blocked",
        }

    warnings: list[str] = []
    positives: list[str] = []
    if len(text) > 120000:
        warnings.append("Artifact is large for NPU prompt context; use compact summaries.")
    else:
        positives.append("Artifact size is suitable for compact review.")
    if isinstance(data, dict) and data.get("schema_version"):
        positives.append("schema_version present.")
    else:
        warnings.append("schema_version missing.")
    if isinstance(data, dict):
        expect_for_name(path, data, warnings, positives)
    if "ShaderNodeTexMusgrave" in text:
        warnings.append("Blocked Blender node detected: ShaderNodeTexMusgrave.")
    if "C:\\Users\\" in text:
        warnings.append("Potential hardcoded Windows user path detected.")

    score = max(0.0, round(1.0 - len(warnings) * 0.12 + min(0.2, len(positives) * 0.02), 4))
    usefulness = "high" if score >= 0.85 else "medium" if score >= 0.6 else "low"
    return {
        "path": str(path),
        "size_chars": len(text),
        "review_score": min(score, 1.0),
        "ai_usefulness": usefulness,
        "warnings": warnings,
        "positives": positives,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default="output/ai_pipeline/npu_artifact_review.json")
    ap.add_argument("--device", default="NPU")
    ap.add_argument("--max-workers", type=int, default=4)
    args = ap.parse_args()
    items = list_targets(Path(args.input).resolve())
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max(1, min(args.max_workers, 4))
    ) as pool:
        reviews = list(pool.map(review, items))
    warnings = [w for r in reviews for w in r.get("warnings", [])]
    avg = (
        round(sum(r.get("review_score", 0.0) for r in reviews) / len(reviews), 4)
        if reviews
        else 0.0
    )
    report = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "backend": "heuristic",
        "requested_device": args.device,
        "worker_count": max(1, min(args.max_workers, 4)),
        "review_count": len(reviews),
        "average_score": avg,
        "passed": not warnings,
        "reviews": reviews,
        "summary": {
            "warnings": warnings,
            "high_usefulness_count": sum(1 for r in reviews if r.get("ai_usefulness") == "high"),
            "note": "Safe deterministic reviewer for NPU-sized tasks; can be replaced by OpenVINO GenAI later.",
        },
    }
    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
