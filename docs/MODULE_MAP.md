# Module Map

## Purpose

This document maps the main repository areas and identifies where reusable behavior should eventually live.

Use it before editing code, creating a new Blender package, or asking an AI system to generate patches.

## Repository areas

| Area | Role | Notes |
|---|---|---|
| `analyze_wav.py` | Root audio-analysis script | Produces feature data and frame-level JSON. Candidate for service/CLI split. |
| `build_track_summary.py` | Root summary builder | Produces compact summaries from analysis JSON. Candidate for importable summary service. |
| `normalize_scene_spec.py` | Scene-spec normalizer | Contains normalization logic that should eventually move into a reusable scene-spec module. |
| `Scripting/` | Blender package/script workspace | Contains versioned workflows and AI-generated/refined Blender packages. |
| `Scripting/v61b/` | Current reference Blender workflow | Treat as the quality reference for advanced package structure. Do not destructively refactor. |
| `Scripting/v61b/main_v61b.py` | Main known Blender entry point for v61b | Orchestrates input validation, scene setup, audio strip, objects, atmosphere, physics and animation. |
| `Scripting/v61b/config.py` | v61b configuration module | Global-heavy but practical. Future shared code should use structured config adapters. |
| `Scripting/v61b/io_utils.py` | v61b JSON/input/sequencer utilities | Good candidate for shared `json_io.py` and `blender_compat.py`. |
| `Scripting/v61b/encode_ffmpeg_v61b.py` | v61b FFmpeg encoder | Good candidate for shared `ffmpeg_encoder.py`, `image_sequence.py`, and `render_profiles.py`. |
| `Scripting/v61b/spaziotempo/core/` | Scene registry and collection classification | Good model for future shared registry patterns. |
| `Scripting/v61b/hotpatch/` | Patch and diagnostic scripts | Candidate source for shared diagnostics and hotpatch base helpers. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Large generated/refined Blender package | Contains a large monolithic scene script and encoding helpers; strong extraction candidate. |
| `Scripting/_template_audio_reactive_package/` | Template package | Starting point for future generated packages. Should evolve with the shared utility strategy. |
| `Scripting/shared/` | Shared utility target | Package-neutral path, JSON, FFmpeg, Blender compatibility, render profile, diagnostics and panel helpers should live here. |
| `Tools/npu/` | AI/NPU/Ollama support tooling | Contains context builders, dual-AI pipeline, NPU review and runtime utilities. |
| `Tools/ai/` | AI artifact validation and state packets | Validates AI-produced artifacts and builds generic agent state/memory packets. |
| `Tools/repo_patch_runner/` | Structured patch runner tooling | Supports repository modification workflows. |
| `indexAI/` | Generated AI-oriented project index | Generated context and patch material. Do not hand-refactor as source. |
| `patch_specs/` | Patch specification artifacts | Structured patch records and applied patch metadata. |
| `docs/` | Stable documentation | Human and AI-readable project contracts. |
| `examples/` | Example area | Reserved for reproducible examples and small fixtures. |

## AI navigation order

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read `docs/README.md`.
4. Read this file.
5. Read `docs/DATA_FLOW.md`.
6. Read `docs/REFACTORING_AND_REUSE_PLAN.md`.
7. Read `docs/SHARED_SCRIPTING_UTILITIES.md`.
8. Read `docs/QUALITY_GATE.md`.
9. Read `Scripting/README.md`.
10. Read the README of the target package under `Scripting/`.
11. Inspect the actual script before editing.

## Current code organization

### Root tools

| File | Main responsibility | Refactor target |
|---|---|---|
| `analyze_wav.py` | Audio feature extraction and analysis JSON generation | `spaziotempo_audio.analysis` plus CLI wrapper. |
| `build_track_summary.py` | Compact summary generation | `spaziotempo_audio.summary` plus CLI wrapper. |
| `normalize_scene_spec.py` | Scene-spec defaults, palette/camera/object/audio mapping normalization | `spaziotempo_audio.scene_spec` or `Tools/lib/scene_spec.py`. |

### v61b package

| File/folder | Main responsibility | Refactor target |
|---|---|---|
| `main_v61b.py` | Main orchestration | Keep as package entry point; introduce adapters only after shared utilities are validated. |
| `config.py` | Runtime constants and workstation paths | Add structured config adapter; do not remove existing constants yet. |
| `io_utils.py` | JSON loading, input checks, sequencer/audio strip compatibility | `Scripting/shared/json_io.py`, `Scripting/shared/blender_compat.py`. |
| `scene_utils.py` | Scene cleanup helpers | `Scripting/shared/scene_utils.py` after compatibility checks. |
| `render_setup.py` | Render and physics configuration | `Scripting/shared/render_profiles.py`. |
| `encode_ffmpeg_v61b.py` | FFmpeg discovery, image sequence scan, CPU/GPU command building | `Scripting/shared/ffmpeg_encoder.py`, `image_sequence.py`, `render_profiles.py`. |
| `encode_image_sequence_v61b.py` | Image sequence encode/export workflow | `Scripting/shared/image_sequence.py`. |
| `scene_tuning_panel.py` | UI panel and tuning profiles | `Scripting/shared/panel_base.py`, `render_profiles.py`. |
| `spaziotempo/core/registry.py` | Layer/object/feature registry | Shared registry pattern for future packages. |
| `hotpatch/` | Runtime patches and diagnostics | `Scripting/shared/diagnostics.py`, `hotpatch_base.py`. |

### NPU and AI tooling

| File | Main responsibility | Refactor target |
|---|---|---|
| `Tools/npu/run_dual_ai_pipeline.py` | End-to-end local/AI orchestration | Split into `Tools/npu/pipeline/` modules. |
| `Tools/npu/ollama_runtime.py` | Ollama runtime/session helpers | Provider module under `Tools/npu/pipeline/providers.py`. |
| `Tools/npu/npu_runtime.py` | NPU preflight | Provider/preflight module. |
| `Tools/npu/build_project_ai_index.py` | Project index generation | Keep as generator; generated output remains non-source. |
| `Tools/npu/build_ai_service_packet.py` | AI service packet generation | Keep as artifact builder; extract common JSON/path helpers later. |
| `Tools/ai/agent_state.py` | Generic memory records and microtask packet model | Keep package-neutral; connect to app workers only through explicit packet contracts. |
| `Tools/ai/build_agent_state_packet.py` | CLI for task-local agent state packets | Keep non-invasive; no Blender, GPU, NPU or FFmpeg execution. |
| `Tools/ai/agent_memory_policy.py` | Memory retention, quarantine and promotion-candidate rules | Keep deterministic and non-destructive. |
| `Tools/ai/review_agent_memory.py` | CLI for memory policy reports | Writes reports only; promotion into docs remains manual. |

## Generated package model

The `Scripting/` folder can contain multiple generated Blender packages. A package may correspond to:

- a track;
- a visual concept;
- an audio-analysis workflow;
- a render target;
- an AI-generated implementation attempt;
- a refined production version.

Do not assume that all packages share the same entry point, JSON schema, installation path, or render strategy.

## Recommended future package shape

```text
Scripting/<package_name>/
  README.md
  main.py
  config.py
  pipeline.py
  audio_mapping.py
  scene_objects.py
  materials.py
  lighting.py
  camera.py
  animation.py
  render_settings.py
  encode.py
  diagnostics.py
  inputs/
  outputs/
  notes/
```

## Editing guidance

- Prefer changes in the smallest relevant package or module.
- Preserve versioned folders and named generated packages.
- Do not replace generated context files without checking their source generator.
- For v61b runtime issues, inspect `Scripting/v61b/main_v61b.py` first.
- For package-specific issues, inspect that package README and installation notes first.
- For AI context or generated implementation packets, inspect `Tools/npu/` and `indexAI/` first.
- For reusable behavior, add a shared module first and migrate package usage only after validation.

## Refactoring guidance

Use this order:

1. Add shared utility.
2. Validate utility independently.
3. Add optional package adapter.
4. Test in Blender or with a dry-run.
5. Migrate one package call site.
6. Document result and risks.

Do not combine broad code motion, behavior changes, and artistic scene changes in the same patch.

## Not specified

A full function-level module index is not manually maintained here. Generate it from code when needed by using the project indexing tools.
