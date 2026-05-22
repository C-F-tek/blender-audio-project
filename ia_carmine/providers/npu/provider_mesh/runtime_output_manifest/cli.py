#!/usr/bin/env python3
"""Build an additive NPU runtime-output manifest.

This script is observability-only. It does not run providers, does not execute
Blender, does not call Ollama/NPU, and does not modify legacy runtime outputs.
It only writes a manifest report describing expected or extra runtime output
paths and whether they match the existing exact legacy output policy.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def ensure_repo_imports(repo_root: Path) -> None:
    for path in (repo_root, repo_root / "Tools" / "npu"):
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)


def slugify_track_stem(value: str, max_len: int = 72) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return slug[:max_len] or "track"


def default_legacy_output_paths(repo_root: Path, track_stem: str) -> list[Path]:
    tools_dir = repo_root / "Tools" / "npu"
    output_dir = repo_root / "output"
    scene_scripts_dir = repo_root / "indexAI" / "scene_scripts"
    scene_script = scene_scripts_dir / f"{slugify_track_stem(track_stem)}_scene_builder_candidate.py"
    return [
        output_dir / f"{track_stem}_dual_ai_scene_plan.json",
        tools_dir / "context_artifacts" / "dual_ai_blender_agent_brief.md",
        output_dir / f"{track_stem}_ollama_music_insights.json",
        tools_dir / "context_artifacts" / "ollama_music_insights.md",
        tools_dir / "context_artifacts" / "npu_dual_ai_technical_notes.md",
        tools_dir / "npu_preflight_report.json",
        output_dir / f"{track_stem}_ai_implementation_draft.json",
        scene_script,
        tools_dir / "context_artifacts" / "generated_implementation_notes.md",
        tools_dir / "context_artifacts" / "npu_dual_ai_implementation_notes.md",
    ]


def path_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    name = path.name.lower()
    if name.endswith("preflight_report.json"):
        return "provider_preflight_report"
    if suffix == ".json":
        return "json_runtime_output"
    if suffix == ".md":
        return "markdown_runtime_output"
    if suffix == ".py":
        return "python_candidate_output"
    return "runtime_output"


def build_manifest(
    *,
    repo_root: Path,
    track_stem: str,
    extra_paths: list[str],
    provider_execution_performed: bool,
) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from ia_carmine.providers.npu.pipeline.artifact_paths import (  # noqa: PLC0415
        is_allowed_legacy_runtime_output_path,
        repo_relative_path,
    )
    from ia_carmine.providers.npu.pipeline.reports import (  # noqa: PLC0415
        RuntimeOutputManifestEntry,
        build_runtime_output_manifest,
    )

    paths = default_legacy_output_paths(repo_root, track_stem)
    paths.extend(Path(item) for item in extra_paths)

    entries: list[RuntimeOutputManifestEntry] = []
    for path in paths:
        absolute = path if path.is_absolute() else repo_root / path
        relative = repo_relative_path(absolute, repo_root=repo_root)
        allowed = is_allowed_legacy_runtime_output_path(
            absolute,
            repo_root=repo_root,
            track_stem=track_stem,
        )
        entries.append(
            RuntimeOutputManifestEntry(
                path=relative,
                kind=path_kind(absolute),
                policy_source="legacy_runtime_output_policy",
                allowed=allowed,
                legacy=allowed,
                generated=False,
                provider_execution_performed=provider_execution_performed,
                reason="" if allowed else "not in exact legacy runtime output allowlist",
            )
        )

    manifest = build_runtime_output_manifest(
        repo_root=repo_root,
        entries=entries,
        provider_execution_performed=provider_execution_performed,
    )
    manifest["track_stem"] = track_stem
    manifest["mode"] = "observability_only"
    manifest["output_policy"] = "exact_legacy_runtime_output_policy"
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--track-stem", default="Feel The Light-Luca Vera_Master")
    parser.add_argument(
        "--output",
        default="output/validation/npu_runtime_output_manifest.json",
        help="Manifest JSON output path. Defaults to validation output.",
    )
    parser.add_argument(
        "--extra-path",
        action="append",
        default=[],
        help="Additional runtime output path to include in the manifest. Repeatable.",
    )
    parser.add_argument(
        "--provider-execution-performed",
        action="store_true",
        help="Mark provider execution as performed. Do not use from validation-only flows.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest = build_manifest(
        repo_root=repo_root,
        track_stem=args.track_stem,
        extra_paths=list(args.extra_path or []),
        provider_execution_performed=bool(args.provider_execution_performed),
    )
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": manifest.get("passed"),
                "output": str(output),
                "blocked_count": manifest.get("blocked_count"),
            },
            indent=2,
        )
    )
    return 0 if manifest.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
