#!/usr/bin/env python3
"""Validate AI pipeline artifacts without touching runtime packages."""
from __future__ import annotations

import argparse, json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = {
    "track_summary.json": ["schema_version", "source_analysis"],
    "music_segments.json": ["schema_version", "segments"],
    "audio_event_map.json": ["schema_version"],
    "ai_scene_brief.json": ["schema_version", "creative_intent", "technical_intent"],
    "ai_resource_budget.json": ["schema_version", "recommendations"],
    "ai_selected_mapping.json": ["schema_version", "selected"],
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def load_patterns(capsules: Path):
    blocked, warnings = [], []
    if capsules.exists():
        for path in sorted(capsules.glob("*.json")):
            try:
                data = load_json(path)
            except Exception:
                continue
            blocked += data.get("blocked_patterns", []) if isinstance(data, dict) else []
            warnings += data.get("warning_patterns", []) if isinstance(data, dict) else []
    return blocked, warnings


def scan(path: Path, blocked, warn_patterns, errors, warnings):
    text = path.read_text(encoding="utf-8", errors="replace")
    for item in blocked:
        pattern = item.get("pattern")
        if pattern and pattern in text:
            errors.append(f"{path}: blocked pattern `{pattern}`: {item.get('reason', 'blocked')}")
    for item in warn_patterns:
        pattern = item.get("pattern")
        if pattern and pattern in text:
            warnings.append(f"{path}: warning pattern `{pattern}`: {item.get('reason', 'warning')}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--artifact-dir", default="output/ai_pipeline")
    ap.add_argument("--capsules-dir", default="indexAI/task_capsules")
    ap.add_argument("--package-dir")
    ap.add_argument("--output", default="output/ai_pipeline/ai_validation_report.json")
    ap.add_argument("--allow-errors", action="store_true")
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    artifact_dir = (repo / args.artifact_dir).resolve()
    errors, warnings, checked = [], [], []

    if artifact_dir.exists():
        for path in sorted(artifact_dir.glob("*.json")):
            checked.append(str(path))
            try:
                data = load_json(path)
            except Exception as exc:
                errors.append(f"Invalid JSON {path}: {exc}")
                continue
            for key in REQUIRED.get(path.name, []):
                if not isinstance(data, dict) or key not in data:
                    errors.append(f"{path.name} missing `{key}`")
    else:
        warnings.append(f"Artifact directory not found: {artifact_dir}")

    blocked, warn_patterns = load_patterns((repo / args.capsules_dir).resolve())
    files = list(artifact_dir.rglob("*")) if artifact_dir.exists() else []
    if args.package_dir:
        pkg = (repo / args.package_dir).resolve()
        if not pkg.exists():
            errors.append(f"Package directory not found: {pkg}")
        else:
            if not (pkg / "README.md").exists():
                errors.append("Generated package missing README.md")
            files += list(pkg.rglob("*"))
    for path in files:
        if path.is_file() and path.suffix in {".py", ".md", ".json"}:
            scan(path, blocked, warn_patterns, errors, warnings)

    score = max(0.0, round(1.0 - min(0.7, len(errors) * 0.2) - min(0.3, len(warnings) * 0.04), 4))
    report = {"schema_version": 1, "generated_at": datetime.now(timezone.utc).isoformat(), "passed": not errors, "score": score, "checked_files": checked, "blocking_errors": errors, "warnings": warnings}
    out = Path(args.output).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] or args.allow_errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
