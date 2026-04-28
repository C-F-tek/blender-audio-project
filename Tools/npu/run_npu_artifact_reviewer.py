#!/usr/bin/env python3
"""NPU-sized artifact reviewer with deterministic fallback."""
from __future__ import annotations
import argparse, concurrent.futures, json
from datetime import datetime, timezone
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def list_targets(path: Path):
    if path.is_file(): return [path]
    if path.is_dir(): return sorted(path.glob("*.json"))
    return []


def review(path: Path):
    try:
        data = load(path); text = json.dumps(data, ensure_ascii=False)
    except Exception as exc:
        return {"path": str(path), "review_score": 0.0, "warnings": [f"JSON read error: {exc}"], "positives": []}
    warnings, positives = [], []
    if len(text) > 120000: warnings.append("Artifact is large for NPU prompt context; use compact summaries.")
    else: positives.append("Artifact size is suitable for compact review.")
    if isinstance(data, dict) and data.get("schema_version"): positives.append("schema_version present.")
    else: warnings.append("schema_version missing.")
    if "ShaderNodeTexMusgrave" in text: warnings.append("Blocked Blender node detected: ShaderNodeTexMusgrave.")
    if "C:\\Users\\" in text: warnings.append("Potential hardcoded Windows user path detected.")
    return {"path": str(path), "size_chars": len(text), "review_score": max(0.0, round(1.0 - len(warnings) * 0.15, 4)), "warnings": warnings, "positives": positives}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default="output/ai_pipeline/npu_artifact_review.json")
    ap.add_argument("--device", default="NPU")
    ap.add_argument("--max-workers", type=int, default=4)
    args = ap.parse_args()
    items = list_targets(Path(args.input).resolve())
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.max_workers)) as pool:
        reviews = list(pool.map(review, items))
    warnings = [w for r in reviews for w in r.get("warnings", [])]
    avg = round(sum(r.get("review_score", 0.0) for r in reviews) / len(reviews), 4) if reviews else 0.0
    report = {"schema_version": 1, "generated_at": datetime.now(timezone.utc).isoformat(), "backend": "heuristic", "requested_device": args.device, "review_count": len(reviews), "average_score": avg, "passed": not warnings, "reviews": reviews, "summary": {"warnings": warnings, "note": "Safe fallback reviewer for NPU-sized tasks."}}
    out = Path(args.output).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
