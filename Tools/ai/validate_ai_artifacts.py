#!/usr/bin/env python3
"""Validate AI artifacts and optional generated package folders."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED = {
    "track_summary.json": ["schema_version", "source_analysis"],
    "music_segments.json": ["schema_version", "segments"],
    "audio_event_map.json": ["schema_version"],
    "ai_scene_brief.json": ["schema_version", "creative_intent", "technical_intent"],
    "ai_resource_budget.json": ["schema_version", "recommendations"],
    "ai_mapping_candidates.json": ["schema_version", "candidates"],
    "ai_selected_mapping.json": ["schema_version", "selected"],
    "ai_patch_plan.json": ["schema_version"],
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def capsule_patterns(capsules_dir: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    blocked, warnings = [], []
    if not capsules_dir.exists():
        return blocked, warnings
    for path in sorted(capsules_dir.glob("*.json")):
        try:
            payload = load_json(path)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            blocked.extend(payload.get("blocked_patterns", []) or [])
            warnings.extend(payload.get("warning_patterns", []) or [])
    return blocked, warnings


def scan_text_files(paths: list[Path], blocked: list[dict[str, str]], warn_patterns: list[dict[str, str]], errors: list[str], warnings: list[str]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for item in blocked:
            pattern = item.get("pattern", "")
            if pattern and pattern in text:
                errors.append(f"{path}: blocked pattern `{pattern}` found: {item.get('reason', 'blocked')}")
        for item in warn_patterns:
            pattern = item.get("pattern", "")
            if pattern and pattern in text:
                warnings.append(f"{path}: warning pattern `{pattern}` found: {item.get('reason', 'warning')}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--artifact-dir", default="output/ai_pipeline")
    parser.add_argument("--package-dir")
    parser.add_argument("--capsules-dir", default="indexAI/task_capsules")
    parser.add_argument("--output", default="output/ai_pipeline/ai_validation_report.json")
    parser.add_argument("--allow-errors", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    artifacts = (repo / args.artifact_dir).resolve()
    capsules = (repo / args.capsules_dir).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    if not artifacts.exists():
        warnings.append(f"Artifact directory not found: {artifacts}")
    else:
        for path in sorted(artifacts.glob("*.json")):
            checked.append(str(path))
            try:
                payload = load_json(path)
            except json.JSONDecodeError as exc:
                errors.append(f"Invalid JSON {path}: {exc}")
                continue
            for key in REQUIRED.get(path.name, []):
                if not isinstance(payload, dict) or key not in payload:
                    errors.append(f"{path.name} missing required key `{key}`")

    package_files: list[Path] = []
    if args.package_dir:
        package = (repo / args.package_dir).resolve()
        if not package.exists():
            errors.append(f"Package directory not found: {package}")
        else:
            if not (package / "README.md").exists():
                errors.append("Generated package missing README.md")
            for recommended in ("config.py", "main.py", "TEST_CHECKLIST.md"):
                if not (package / recommended).exists():
                    warnings.append(f"Generated package missing recommended file: {recommended}")
            package_files = [p for p in package.rglob("*") if p.is_file() and p.suffix in {".py", ".md", ".json"}]

    blocked, warn_patterns = capsule_patterns(capsules)
    scan_targets = ([p for p in artifacts.rglob("*") if p.is_file() and p.suffix in {".py", ".md", ".json"}] if artifacts.exists() else []) + package_files
    scan_text_files(scan_targets, blocked, warn_patterns, errors, warnings)

    score = max(0.0, round(1.0 - min(0.7, len(errors) * 0.2) - min(0.3, len(warnings) * 0.04), 4))
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "passed": not errors,
        "score": score,
        "checked_files": checked,
        "blocking_errors": errors,
        "warnings": warnings,
        "info": ["No blocking errors detected."] if not errors else [],
    }
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] or args.allow_errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
