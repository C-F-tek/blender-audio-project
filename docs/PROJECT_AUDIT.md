# Project Audit

## Audit scope

This audit summarizes the current state of `blender-audio-project` after reviewing the repository structure, README files, documentation, generated indexes and key script areas.

The audit is intentionally non-invasive. It recommends refactoring and encapsulation strategy, but it does not require immediate destructive changes to working Blender packages.

## Executive summary

The repository has evolved from a Blender scripting workspace into a structured audio-reactive visual production environment.

It now contains:

- root audio-analysis and scene-spec tooling;
- a mature reference Blender workflow under `Scripting/v61b/`;
- at least one large generated/refined Blender package under `Scripting/`;
- shared-utility policy under `Scripting/shared/`;
- a reusable package template under `Scripting/_template_audio_reactive_package/`;
- AI, NPU and Ollama support tooling under `Tools/npu/`;
- AI project indexes, manifests and patch material under `indexAI/`;
- documentation for AI-assisted and future local-AI workflows;
- GitHub-facing templates and patch workflow support.

## Current maturity assessment

| Area | Assessment | Notes |
|---|---|---|
| Project identity | good | Root README, docs index, AGENTS and package docs exist. |
| AI orientation | good | AI navigation, quality gate, package standards and generated indexes exist. |
| Blender reference workflow | strong | `Scripting/v61b/` is modular and suitable as the reference model. |
| Generated package workflow | good | Template and generated package structures exist. |
| Shared utilities | planned | Policy is documented; full utility extraction is not complete. |
| Local AI workflow | active/planned | NPU/Ollama tooling exists, but orchestration should be decomposed. |
| JSON schemas | partial | Schema notes exist, but real production schemas still need stronger validation. |
| Automated validation | partial/weak | Tooling exists, but CI-style validation and Blender checks are still limited. |
| Refactoring readiness | good | The project is ready for additive extraction, not broad rewrites. |

## Important repository areas

| Area | Role |
|---|---|
| `analyze_wav.py` | Audio-analysis entry point. |
| `build_track_summary.py` | Compact track-summary builder. |
| `normalize_scene_spec.py` | Scene-spec normalization and defaulting. |
| `Scripting/v61b/` | Main quality reference for complex Blender package structure. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Large generated/refined package and strong extraction candidate. |
| `Scripting/_template_audio_reactive_package/` | Template for future generated packages. |
| `Scripting/shared/` | Target area for reusable package-agnostic utilities. |
| `Tools/npu/` | Local AI, NPU, context-building, review and implementation tooling. |
| `Tools/ai/` | AI artifact validation. |
| `Tools/repo_patch_runner/` | Structured patch runner tooling. |
| `indexAI/` | Generated code indexes, manifests, context and patch materials. |
| `docs/` | Stable project documentation. |
| `patch_specs/` | Structured patch specification records. |

## Strengths

### 1. Clear AI operating context

AI systems have a stable reading order and operating rules through `AGENTS.md`, `docs/README.md`, `docs/MODULE_MAP.md`, `docs/DATA_FLOW.md`, `docs/QUALITY_GATE.md`, and the new refactoring plan.

### 2. Strong reference implementation

`Scripting/v61b/` is complex enough to act as a qualitative reference for future generated packages. It contains modular Blender logic, render/encoding helpers, scene tuning, hotpatch patterns and a richer composition model than a one-file prototype.

### 3. Data-first scene registry direction

The `spaziotempo/core/registry.py` approach is technically correct because it makes object ownership, scene layers, feature modules and hotpatch targets explicit.

### 4. Package generation discipline

The repository has a template package and documented workflow for generating future Blender packages from audio data and compact JSON context.

### 5. Non-destructive shared-utility strategy

The project correctly avoids breaking working code through premature refactoring. Shared utilities should be created additively and adopted only after validation.

### 6. Local AI direction is practical

The repository records the current external AI workflow and the intended local AI/NPU/GPU-assisted direction. This is the right base for improving artifact production.

## Risks and gaps

### 1. Shared utility code is not fully implemented

`Scripting/shared/` currently defines direction and policy. Production-ready shared modules such as `ffmpeg_encoder.py`, `render_profiles.py`, `path_utils.py`, `json_io.py` and `blender_compat.py` still need to be implemented or completed.

### 2. Large scripts concentrate too many responsibilities

`Tools/npu/run_dual_ai_pipeline.py` and the generated package script under `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` are large enough to make testing, reuse and patching harder.

Recommended solution: split orchestration, prompts, providers, validators and artifact writing into focused modules.

### 3. Root tools are still script-shaped

`analyze_wav.py`, `build_track_summary.py` and `normalize_scene_spec.py` contain reusable logic but are not yet cleanly separated into importable service modules plus CLI wrappers.

### 4. Encoding logic should become shared

v61b and the generated package both need FFmpeg and YouTube-style output workflows. This should become shared profile-based command generation.

### 5. Blender compatibility should be isolated

Compatibility fallbacks for sequencer API, node types and scene properties should live in one shared compatibility layer instead of being repeated inside package modules.

### 6. JSON schemas need stronger contracts

Schema files exist, but real audio-analysis, music-context, implementation-draft, scene-spec and render-manifest schemas still need validation against representative files.

### 7. Automated validation is incomplete

The project needs non-invasive checks for Python syntax, package structure, docs links, JSON schemas and minimal Blender import/execution where feasible.

### 8. Generated indexes can become stale

`indexAI/` and `Tools/npu/` generated indexes must be regenerated after structural changes. They are context artifacts, not source-of-truth code.

## Recommended next actions

### Priority 1: implement first shared utilities

Create pure Python shared modules first:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/image_sequence.py
```

These can be tested without Blender.

### Priority 2: extract FFmpeg profiles additively

Create:

```text
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
```

Keep existing package encoders unchanged at first.

### Priority 3: add Blender compatibility wrappers

Create:

```text
Scripting/shared/blender_compat.py
```

Use it for sound-strip creation, sequencer cleanup, safe node creation and safe scene property setting.

### Priority 4: split NPU pipeline orchestration

Refactor `Tools/npu/run_dual_ai_pipeline.py` into:

```text
Tools/npu/pipeline/config.py
Tools/npu/pipeline/context_builder.py
Tools/npu/pipeline/prompts.py
Tools/npu/pipeline/providers.py
Tools/npu/pipeline/validators.py
Tools/npu/pipeline/artifact_writer.py
Tools/npu/pipeline/runner.py
```

The split should preserve current CLI behavior.

### Priority 5: add validation scripts

Add lightweight validation helpers:

```text
Tools/validation/check_python_syntax.py
Tools/validation/check_package_structure.py
Tools/validation/check_docs_links.py
Tools/validation/check_json_artifacts.py
```

### Priority 6: regenerate indexes after structural changes

Regenerate:

```text
indexAI/project_code_manifest.json
indexAI/project_code_index.md
Tools/npu/npu_code_manifest.json
Tools/npu/npu_code_index.md
```

## Refactoring conclusion

The project is ready for reuse-oriented refactoring, but the safest strategy is additive extraction.

Do not rewrite working Blender packages wholesale. First create shared modules, test them, add adapters, then migrate one concern at a time.
