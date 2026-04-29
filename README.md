# Blender Audio Project

`blender-audio-project` is a production-oriented workspace for generating, refining, and rendering audio-reactive Blender visuals.

The repository combines:

- audio analysis tools;
- compact music/context generation;
- Blender Python scene packages;
- FFmpeg render/encoding workflows;
- AI-assisted planning and implementation artifacts;
- modular AI artifact pipeline orchestration;
- local NPU/GPU/Ollama support utilities;
- GitHub- and AI-friendly documentation.

The main technical goal is to turn an audio track and its derived JSON context into a controllable Blender scene with synchronized objects, materials, lighting, fog, camera motion, physics accents, and final video output.

## Current project status

This is an active work-in-progress repository. It already contains a mature Blender reference workflow under `Scripting/v61b/` and at least one additional generated/refined package under `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/`.

The current architectural direction is **progressive refactoring for reuse**:

1. keep working scene packages stable;
2. extract reusable utilities additively into `Scripting/shared/`;
3. modularize AI/NPU pipeline code into focused components;
4. use shared adapters only after validation;
5. preserve generated indexes and large JSON artifacts as pipeline context, not as hand-edited source.

The AI artifact pipeline has been modularized and is currently marked as:

```text
modular_schedule_complete_pending_local_validation
```

Read:

- `docs/AI_PIPELINE_REFACTOR_STATUS.md`
- `docs/AI_PIPELINE_ARCHITECTURE.md`
- `Tools/ai/pipeline/refactor_status.py`

See also `docs/REFACTORING_AND_REUSE_PLAN.md`.

## High-level workflow

```text
Audio file
  -> audio analysis
  -> analysis JSON
  -> compact summary / music context
  -> AI artifact pipeline
  -> scene specification or AI implementation plan
  -> Blender scene package
  -> rendered frame sequence
  -> FFmpeg encoded video
```

## Main repository layout

| Path | Role |
|---|---|
| `analyze_wav.py` | Root CLI/script for extracting audio features and frame-level analysis data. |
| `build_track_summary.py` | Builds compact summaries from full analysis JSON data. |
| `normalize_scene_spec.py` | Normalizes scene specifications into a safer downstream format. |
| `Scripting/` | Blender script/package workspace. |
| `Scripting/v61b/` | Current quality reference package for complex audio-reactive Blender scenes. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Large generated/refined scene package with YouTube-oriented output workflow. |
| `Scripting/shared/` | Reusable package-agnostic helpers. |
| `Scripting/_template_audio_reactive_package/` | Template for future generated packages. |
| `Tools/ai/` | AI artifact pipeline entrypoints, dry-run matrix and validation utilities. |
| `Tools/ai/pipeline/` | Modular AI artifact pipeline implementation. |
| `Tools/npu/` | Local AI/NPU/Ollama tooling, code indexing, context generation, review and implementation support. |
| `Tools/validation/` | Non-invasive validation scripts. |
| `Tools/repo_patch_runner/` | Structured repository patch tooling. |
| `indexAI/` | Generated AI indexes, code context, manifests, task packets and patch-library material. |
| `docs/` | Stable project documentation for developers and AI systems. |
| `examples/` | Placeholder area for reproducible examples. |
| `patch_specs/` | Structured repository modification specifications. |

## Recommended reading order

For developers and AI agents:

1. `AGENTS.md`
2. `docs/README.md`
3. `docs/PROJECT_AI_CONSCIOUSNESS.md`
4. `docs/AI_ONBOARDING.md`
5. `docs/AI_PIPELINE_REFACTOR_STATUS.md`
6. `docs/AI_PIPELINE_ARCHITECTURE.md`
7. `docs/MODULE_MAP.md`
8. `docs/DATA_FLOW.md`
9. `docs/REFACTORING_AND_REUSE_PLAN.md`
10. `docs/SHARED_SCRIPTING_UTILITIES.md`
11. `docs/QUALITY_GATE.md`
12. `Scripting/README.md`
13. the README of the target package under `Scripting/`

## Reference Blender package

`Scripting/v61b/` is the current reference implementation.

It contains:

- `main_v61b.py` as the main entry point;
- `config.py` for workflow configuration;
- scene, camera, world, render, material, fog, physics and animation modules;
- hotpatch and diagnostics helpers;
- FFmpeg and image-sequence encoding helpers;
- a scene registry under `spaziotempo/core/`.

Do not destructively refactor `Scripting/v61b/` just to create shared utilities. Shared extraction should be additive first.

## Modular AI artifact pipeline

The AI artifact pipeline entrypoint is:

```text
Tools/ai/run_parallel_artifact_pipeline.py
```

It is intentionally thin. Implementation details live under:

```text
Tools/ai/pipeline/
```

Key modules:

| Module | Role |
|---|---|
| `defaults.py` | Pipeline constants and report filenames. |
| `models.py` | Pipeline dataclasses and lane enum. |
| `runner.py` | Low-level command execution. |
| `compat.py` | Adapter layer for schema-v6 compatible report payloads. |
| `artifact_contracts.py` | Expected artifacts and path metadata. |
| `cli.py` | CLI parser. |
| `preflight.py` | Input/environment checks. |
| `steps.py` | Command and step construction. |
| `scheduler.py` | Serial/parallel scheduling policy. |
| `orchestrator.py` | Concrete serial/parallel execution helpers. |
| `schema_report.py` | Schema-v6 report generation and summary fields. |
| `guardrail_models.py` | Typed guardrail remediation request models. |
| `remediation.py` | Guardrail action queue and remediation loop. |
| `refactor_status.py` | Machine-readable refactor state marker. |

Pipeline smoke validation:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
```

Dry-run matrix:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

## Refactoring direction

The recommended encapsulation strategy is:

```text
working package code
  -> copied/adapted shared utility
  -> isolated validation
  -> optional adapter
  -> controlled package migration
```

Current reusable modules include:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/image_sequence.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
```

Next shared candidates:

```text
Scripting/shared/blender_compat.py
Scripting/shared/config_model.py
Scripting/shared/diagnostics.py
```

## Installation

Minimum Python-side requirements are defined in `pyproject.toml`.

Typical Python dependencies include:

```text
numpy
matplotlib
librosa
```

Blender execution requires a compatible Blender Python environment. FFmpeg is required for final video encoding workflows.

Detailed setup notes are in:

- `docs/INSTALLATION.md`
- `docs/COMPATIBILITY.md`
- `docs/FFMPEG_WORKFLOW.md`

## Basic usage

Audio analysis:

```bash
python analyze_wav.py path/to/audio.wav
```

Track summary:

```bash
python build_track_summary.py path/to/analysis.json
```

Scene specification normalization:

```bash
python normalize_scene_spec.py
```

Blender package execution depends on the target package. For `v61b`, open the package in Blender and run:

```text
Scripting/v61b/main_v61b.py
```

After rendering an image sequence, use the package encoding helper or the documented FFmpeg workflow.

## Validation

General validation:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

AI pipeline validation:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

Regenerate AI/NPU indexes after documentation or structural changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## AI-generated package rules

When generating or modifying Blender packages:

- read the target package README first;
- keep paths configurable;
- do not overwrite full analysis JSON files unless explicitly requested;
- do not collapse independent generated packages into one folder;
- keep package-specific artistic logic inside the package;
- move reusable operational logic into `Scripting/shared/` only through additive extraction;
- report changed files, risks, tests and line counts for scripts.

## Documentation map

Start from `docs/README.md`.

Key files:

- `docs/PROJECT_OVERVIEW.md`
- `docs/PROJECT_AI_CONSCIOUSNESS.md`
- `docs/AI_PIPELINE_REFACTOR_STATUS.md`
- `docs/AI_PIPELINE_ARCHITECTURE.md`
- `docs/MODULE_MAP.md`
- `docs/DATA_FLOW.md`
- `docs/REFACTORING_AND_REUSE_PLAN.md`
- `docs/SHARED_SCRIPTING_UTILITIES.md`
- `docs/AI_GENERATED_PACKAGE_STANDARD.md`
- `docs/PACKAGE_CREATION_WORKFLOW.md`
- `docs/QUALITY_GATE.md`
- `docs/LOCAL_AI_WORKFLOW.md`
- `docs/DEVELOPER_GUIDE.md`

## Current limitations

- Formal JSON schemas are still partial.
- Automated Blender validation is not complete.
- Some large scripts are still intentionally package-specific.
- The modular AI artifact pipeline still requires local workstation dry-run validation after the latest refactor.
- `indexAI/` and NPU code indexes must be regenerated after structural changes.
- Shared utility extraction is planned but not fully migrated across packages.
