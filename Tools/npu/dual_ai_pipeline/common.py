from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.npu.provider_mesh.ai_service_packet import build_ai_service_packet
from Tools.npu.provider_mesh.ai_service_packet import slugify as packet_slugify
from Tools.npu.provider_mesh.blender_manual_context import build_manual_context
from Tools.npu.provider_mesh.npu_code_context import main as build_code_context
from Tools.npu.provider_mesh.music_context import build_music_context
from Tools.npu.provider_mesh._shared.npu_runtime import (
    DEFAULT_MODEL_DIR,
    DEFAULT_NPU_PYTHON,
    npu_preflight,
    write_npu_preflight_report,
)
from Tools.npu.provider_mesh._shared.ollama_runtime import OllamaModelManager, parse_json_response
from Tools.npu.provider_mesh.project_ai_index import (
    PROJECT_INDEX_MD,
    PROJECT_MANIFEST_JSON,
    build_project_ai_index,
)
from Tools.npu.provider_mesh.ollama_music_agent import build_prompt as build_music_prompt
from Tools.npu.provider_mesh.ollama_music_agent import markdown_from_insights

try:
    from pipeline.artifact_paths import (
        is_allowed_generated_artifact_path,
        normalize_repo_relative_path,
        validate_legacy_runtime_output_paths,
    )
    from pipeline.artifact_writer import PlannedArtifactWrite, write_planned_artifact
    from pipeline.context_builder import summarize_music_context
    from pipeline.io_utils import read_json, read_optional_json, read_text, write_json
    from pipeline.prompts import (
        build_creative_scene_prompt_payload,
        build_implementation_retry_payload,
        build_merge_prompt_payload,
    )
    from pipeline.providers import normalize_provider_preflight_report
    from pipeline.validators import validate_implementation_draft_contract
except ImportError:  # Allows package-style imports from repo-root validation.
    from Tools.npu.pipeline.artifact_paths import (  # type: ignore
        is_allowed_generated_artifact_path,
        normalize_repo_relative_path,
        validate_legacy_runtime_output_paths,  # type: ignore
    )
    from Tools.npu.pipeline.artifact_writer import (  # type: ignore
        PlannedArtifactWrite,
        write_planned_artifact,
    )
    from Tools.npu.pipeline.context_builder import summarize_music_context  # type: ignore
    from Tools.npu.pipeline.io_utils import (  # type: ignore
        read_json,
        read_optional_json,
        read_text,
        write_json,
    )
    from Tools.npu.pipeline.prompts import (  # type: ignore
        build_creative_scene_prompt_payload,
        build_implementation_retry_payload,
        build_merge_prompt_payload,
    )
    from Tools.npu.pipeline.providers import normalize_provider_preflight_report  # type: ignore
    from Tools.npu.pipeline.validators import validate_implementation_draft_contract  # type: ignore


ROOT = Path(__file__).resolve().parents[3]
TOOLS_DIR = ROOT / "Tools" / "npu"
CONTEXT_ARTIFACTS_DIR = TOOLS_DIR / "context_artifacts"
OUTPUT_DIR = ROOT / "output"
INDEX_AI_DIR = ROOT / "indexAI"
SCENE_SCRIPTS_DIR = INDEX_AI_DIR / "scene_scripts"

DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
TRACK_STEM = DEFAULT_TRACK_STEM

MUSIC_AI_CONTEXT = OUTPUT_DIR / f"{TRACK_STEM}_analysis_ai_context.json"
DUAL_PLAN_JSON = OUTPUT_DIR / f"{TRACK_STEM}_dual_ai_scene_plan.json"
DUAL_BRIEF_MD = CONTEXT_ARTIFACTS_DIR / "dual_ai_blender_agent_brief.md"
OLLAMA_INSIGHTS_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ollama_music_insights.json"
OLLAMA_INSIGHTS_MD = CONTEXT_ARTIFACTS_DIR / "ollama_music_insights.md"
NPU_TECH_MD = CONTEXT_ARTIFACTS_DIR / "npu_dual_ai_technical_notes.md"
NPU_PREFLIGHT_JSON = TOOLS_DIR / "npu_preflight_report.json"
IMPLEMENTATION_DRAFT_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ai_implementation_draft.json"
IMPLEMENTATION_SCRIPT = (
    SCENE_SCRIPTS_DIR / f"{packet_slugify(TRACK_STEM)}_scene_builder_candidate.py"
)
IMPLEMENTATION_NOTES = CONTEXT_ARTIFACTS_DIR / "generated_implementation_notes.md"
NPU_IMPLEMENTATION_NOTES = CONTEXT_ARTIFACTS_DIR / "npu_dual_ai_implementation_notes.md"


ALLOWED_NEW_PREFIXES = ("indexAI/scene_scripts/", "indexAI/patch_library/")
PREFERRED_IMPLEMENTATION_FILES = (
    "Scripting/v61b/materials.py",
    "Scripting/v61b/fog_dynamics.py",
    "Scripting/v61b/physics_setup.py",
    "Scripting/v61b/scene_tuning_panel.py",
    "Scripting/v61b/config.py",
    "Scripting/v61b/render_setup.py",
    "Scripting/v61b/hot_update_scene_v61b.py",
)

RUNTIME_GLOBAL_NAMES = (
    "ROOT",
    "TOOLS_DIR",
    "OUTPUT_DIR",
    "TRACK_STEM",
    "MUSIC_AI_CONTEXT",
    "DUAL_PLAN_JSON",
    "DUAL_BRIEF_MD",
    "OLLAMA_INSIGHTS_JSON",
    "OLLAMA_INSIGHTS_MD",
    "NPU_TECH_MD",
    "NPU_PREFLIGHT_JSON",
    "IMPLEMENTATION_DRAFT_JSON",
    "IMPLEMENTATION_SCRIPT",
    "IMPLEMENTATION_NOTES",
    "NPU_IMPLEMENTATION_NOTES",
)


def propagate_runtime_globals() -> None:
    """Keep split dual-pipeline modules aligned after runtime path changes."""
    package = __package__
    if not package:
        return
    for suffix in (
        "cli",
        "implementation_fallback",
        "implementation_generation",
        "implementation_parse",
        "implementation_validation",
        "prompts",
        "technical",
        "writers",
    ):
        module = sys.modules.get(f"{package}.{suffix}")
        if module is None:
            continue
        for name in RUNTIME_GLOBAL_NAMES:
            setattr(module, name, globals()[name])


def legacy_runtime_output_policy_report(extra_paths: list[Path] | None = None) -> dict[str, object]:
    paths = [
        DUAL_PLAN_JSON,
        DUAL_BRIEF_MD,
        OLLAMA_INSIGHTS_JSON,
        OLLAMA_INSIGHTS_MD,
        NPU_TECH_MD,
        NPU_PREFLIGHT_JSON,
        IMPLEMENTATION_DRAFT_JSON,
        IMPLEMENTATION_SCRIPT,
        IMPLEMENTATION_NOTES,
        NPU_IMPLEMENTATION_NOTES,
    ]
    if extra_paths:
        paths.extend(extra_paths)
    return validate_legacy_runtime_output_paths(
        paths,
        repo_root=ROOT,
        track_stem=TRACK_STEM,
    )

def assert_legacy_runtime_output(path: Path) -> None:
    report = validate_legacy_runtime_output_paths(
        [path],
        repo_root=ROOT,
        track_stem=TRACK_STEM,
    )
    if not report["ok"]:
        raise ValueError(f"Refusing legacy runtime write outside exact output policy: {report}")

def write_legacy_text_output(path: Path, text: str) -> None:
    assert_legacy_runtime_output(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def write_legacy_json_output(path: Path, payload: dict[str, Any]) -> None:
    assert_legacy_runtime_output(path)
    write_json(path, payload)

def normalize_npu_preflight_report(
    raw_report: dict[str, Any],
    *,
    npu_python: str | Path,
    npu_model_dir: str | Path,
) -> dict[str, Any]:
    return normalize_provider_preflight_report(
        raw_report,
        provider="openvino_npu",
        model=Path(npu_model_dir).name,
        executable=str(npu_python),
        model_dir=str(npu_model_dir),
    )

def write_legacy_npu_preflight_report(report: dict[str, Any], path: Path) -> None:
    assert_legacy_runtime_output(path)
    write_npu_preflight_report(report, path)

def update_track_paths(track_stem: str, analysis_ai_context: str | None = None) -> None:
    global TRACK_STEM
    global MUSIC_AI_CONTEXT, DUAL_PLAN_JSON, OLLAMA_INSIGHTS_JSON
    global IMPLEMENTATION_DRAFT_JSON, IMPLEMENTATION_SCRIPT

    TRACK_STEM = track_stem
    MUSIC_AI_CONTEXT = (
        Path(analysis_ai_context)
        if analysis_ai_context
        else OUTPUT_DIR / f"{TRACK_STEM}_analysis_ai_context.json"
    )
    DUAL_PLAN_JSON = OUTPUT_DIR / f"{TRACK_STEM}_dual_ai_scene_plan.json"
    OLLAMA_INSIGHTS_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ollama_music_insights.json"
    IMPLEMENTATION_DRAFT_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ai_implementation_draft.json"
    IMPLEMENTATION_SCRIPT = (
        SCENE_SCRIPTS_DIR / f"{packet_slugify(TRACK_STEM)}_scene_builder_candidate.py"
    )
    propagate_runtime_globals()

def apply_default_input_paths(args: argparse.Namespace) -> None:
    if args.analysis is None:
        args.analysis = str(OUTPUT_DIR / f"{args.track_stem}_analysis.json")
    if args.track_summary is None:
        args.track_summary = str(OUTPUT_DIR / f"{args.track_stem}_track_summary.json")
    if args.compact_json is None:
        args.compact_json = str(OUTPUT_DIR / f"{args.track_stem}_music_context.json")
    if args.analysis_ai_context is None:
        args.analysis_ai_context = str(OUTPUT_DIR / f"{args.track_stem}_analysis_ai_context.json")
    if args.blender_keyframes_json is None:
        args.blender_keyframes_json = str(
            OUTPUT_DIR / f"{args.track_stem}_analysis_blender_keyframes.json"
        )

def validate_input_files(args: argparse.Namespace) -> None:
    required = [
        ("analysis JSON", Path(args.analysis)),
        ("track summary JSON", Path(args.track_summary)),
        ("compact music context JSON", Path(args.compact_json)),
        ("analysis AI context JSON", Path(args.analysis_ai_context)),
        ("full Blender keyframes JSON", Path(args.blender_keyframes_json)),
    ]
    if args.phase == "implementation":
        required.append(("dual AI scene plan JSON", DUAL_PLAN_JSON))

    missing = [f"{label}: {path}" for label, path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Prerequisiti mancanti per la pipeline AI:\n"
            + "\n".join(f"- {item}" for item in missing)
            + "\nEsegui/rigenera analysis, track summary, music context e piano prima del draft."
        )
