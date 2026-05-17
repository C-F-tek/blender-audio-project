# Project Audit

## Status

Historical repository audit snapshot.

This document predates the current unified launcher, heap/exchange lifecycle and patchkit operating model. Use it for application-domain context and older refactor rationale, not as current AI/tooling architecture state.

Current first-read sources:

```text
AGENTS.md
README.md
WORKFLOW.md
docs/AI_ONBOARDING.md
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
docs/MODULE_MAP.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Current code-driven caveat:

```text
Tools/ai/ and Tools/workflow/ now own most local-AI orchestration surfaces.
Tools/npu/ remains important for NPU/OpenVINO support, but it is not the sole AI workflow root.
Current product paths must account for heap/exchange entry, runtime state, exit product, lifecycle validation and patchkit or deterministic patch bridge.
```

## Audit scope

This audit summarizes an older reviewed state of `blender-audio-project` after reviewing the repository structure, README files, documentation, generated indexes and key script areas.

The audit is intentionally non-invasive. It recommends refactoring and encapsulation strategy, but it does not require immediate destructive changes to working Blender packages.

## Executive summary

The repository has evolved from a Blender scripting workspace into a structured audio-reactive visual production environment.

It contains:

- workflow-owned audio-analysis and scene-spec tooling;
- a mature reference Blender workflow under `Scripting/v61b/`;
- at least one large generated/refined Blender package under `Scripting/`;
- shared-utility policy under `Scripting/shared/`;
- a reusable package template under `Scripting/_template_audio_reactive_package/`;
- AI, NPU and Ollama support tooling under `Tools/npu/`;
- AI orchestration, context, evidence, patch and review tooling under `Tools/ai/`;
- workflow launchers under `Tools/workflow/`;
- AI project indexes, manifests and patch material under `indexAI/`;
- documentation for AI-assisted and future local-AI workflows;
- GitHub-facing templates and patch workflow support.

## Historical maturity assessment

| Area | Assessment | Notes |
|---|---|---|
| Project identity | good | Root README, docs index, AGENTS and package docs exist. |
| AI orientation | good | Current AI orientation has moved to heap/exchange and patchkit maps. |
| Blender reference workflow | strong | `Scripting/v61b/` is modular and suitable as the reference model. |
| Generated package workflow | good | Template and generated package structures exist. |
| Shared utilities | active foundation | Initial path, JSON, image-sequence, FFmpeg and render-profile helpers exist; full migration is not complete. |
| Local AI workflow | evolved | Earlier NPU/Ollama focus has expanded into unified launcher, provider lanes, heap/exchange and patchkit. |
| JSON schemas | partial | Schema notes exist; current artifact schemas are indexed separately. |
| Automated validation | evolving | Validation now includes launcher/report contracts, lifecycle checks and patchkit smoke in addition to earlier checks. |
| Refactoring readiness | good | The project is ready for additive extraction, not broad rewrites. |

## Important repository areas

| Area | Role |
|---|---|
| `Tools/workflow/audio_analysis/analyze_cli.py` | Audio-analysis entry point. |
| `Tools/workflow/audio_analysis/summary_cli.py` | Compact track-summary builder. |
| `Tools/workflow/scene_spec/cli.py` | Scene-spec normalization and defaulting. |
| `Scripting/v61b/` | Main quality reference for complex Blender package structure. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Large generated/refined package and strong extraction candidate. |
| `Scripting/_template_audio_reactive_package/` | Template for future generated packages. |
| `Scripting/shared/` | Target area for reusable package-agnostic utilities. |
| `Tools/workflow/` | Current workflow/launcher ownership. |
| `Tools/ai/` | Current AI orchestration, context, telemetry, evidence, heap/exchange, patchkit and review tooling. |
| `Tools/npu/` | Local AI, NPU, context-building, review and implementation tooling. |
| `Tools/validation/` | Validators, smokes and report-contract checks. |
| `Tools/repo_patch_runner/` | Legacy structured patch runner tooling. |
| `indexAI/` | Generated code indexes, manifests, context and patch materials. |
| `docs/` | Stable project documentation. |
| `patch_specs/` | Structured patch specification records and patchkit bundle specs when selected. |

## Strengths

### 1. Clear AI operating context

AI systems have a stable reading order and operating rules through `AGENTS.md`, `docs/README.md`, `docs/MODULE_MAP.md`, `docs/DATA_FLOW.md`, `docs/QUALITY_GATE.md`, the heap/exchange operating model and the documentation panorama.

### 2. Strong reference implementation

`Scripting/v61b/` is complex enough to act as a qualitative reference for future generated packages. It contains modular Blender logic, render/encoding helpers, scene tuning, hotpatch patterns and a richer composition model than a one-file prototype.

### 3. Data-first scene registry direction

The `spaziotempo/core/registry.py` approach is technically correct because it makes object ownership, scene layers, feature modules and hotpatch targets explicit.

### 4. Package generation discipline

The repository has a template package and documented workflow for generating future Blender packages from audio data and compact JSON context.

### 5. Non-destructive shared-utility strategy

The project correctly avoids breaking working code through premature refactoring. Shared utilities should be created additively and adopted only after validation.

### 6. Local AI direction is practical

The repository records external AI workflow and local AI/NPU/GPU-assisted direction. Current work has expanded this into a unified launcher plus heap/exchange and patchkit product boundaries.

## Risks and gaps

### 1. Shared utility code is not fully implemented or adopted

`Scripting/shared/` contains initial package-agnostic helpers for paths, JSON, image sequences, FFmpeg command building and render profiles. Missing or incomplete areas still include Blender compatibility wrappers, config models, diagnostics and package adapters.

### 2. Large scripts concentrate too many responsibilities

Some workflow and application scripts are large enough to make testing, reuse and patching harder.

Recommended solution: split orchestration, prompts, providers, validators and artifact writing into focused modules when touching those areas.

### 3. Audio/scene workflow tools need service-shaped ownership

The audio analysis, track summary and scene-spec tools now live under `Tools/workflow/`; keep reusable logic in importable modules and keep only thin CLI wrappers public.

### 4. Encoding logic should become shared

v61b and the generated package both need FFmpeg and YouTube-style output workflows. This should become shared profile-based command generation.

### 5. Blender compatibility should be isolated

Compatibility fallbacks for sequencer API, node types and scene properties should live in one shared compatibility layer instead of being repeated inside package modules.

### 6. JSON schemas need stronger contracts

Schema files exist, but real audio-analysis, music-context, implementation-draft, scene-spec, render-manifest and AI runtime artifact schemas still need validation against representative files.

### 7. Automated validation is still expanding

The project needs continuous improvement for Python syntax, package structure, docs links, JSON schemas, heap/exchange lifecycle, patchkit bundles and minimal Blender import/execution where feasible.

### 8. Generated indexes can become stale

`indexAI/` generated indexes must be regenerated after structural changes. They are context artifacts, not source-of-truth code.

## Recommended next actions

### Priority 1: validate and complete shared utilities

Existing pure Python shared modules should be validated and documented before package migration:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/image_sequence.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
```

Keep existing package encoders unchanged at first.

### Priority 2: add Blender compatibility wrappers

Create or verify:

```text
Scripting/shared/blender_compat.py
```

Use it for sound-strip creation, sequencer cleanup, safe node creation and safe scene property setting.

### Priority 3: keep local-AI orchestration owner-aligned

Current AI workflow should remain owner-aligned:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/ai/build_heap_exchange_runtime_entry.py
Tools/ai/build_heap_exchange_runtime_exit.py
Tools/validation/check_heap_exchange_runtime_lifecycle.py
Tools/ai/patchkit/apply_patch_bundle.py
Tools/ai/prepare_review_pr.py
```

Do not resurrect older monolithic flows as primary entrypoints.

### Priority 4: extend validation scripts

Existing lightweight validation helpers should be extended with docs-link, schema, lifecycle and patchkit checks:

```text
Tools/validation/check_python_syntax.py
Tools/validation/check_package_structure.py
Tools/validation/check_json_artifacts.py
Tools/validation/check_docs_links.py
Tools/validation/check_heap_exchange_runtime_lifecycle.py
Tools/validation/run_patchkit_smoke.py
```

### Priority 5: regenerate indexes after structural changes

Regenerate indexes only as ignored/generated artifacts unless a task explicitly requests compact committed evidence.

## Refactoring conclusion

The project is ready for reuse-oriented refactoring, but the safest strategy is additive extraction.

Do not rewrite working Blender packages wholesale. First create shared modules, test them, add adapters, then migrate one concern at a time.
