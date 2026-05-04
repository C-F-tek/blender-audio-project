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
| `Tools/npu/pipeline/` | App-agnostic NPU helper package | Staged helper contracts, validators, fixtures and readiness gates. Not wired into runtime orchestrator until local validation/index regeneration pass. |
| `Tools/ai/` | AI artifact validation and state packets | Validates AI-produced artifacts and builds generic agent state/memory packets. |
| `Tools/ai/pipeline/` | Modular AI artifact pipeline | Focused modules for defaults, models, preflight, scheduling, reports, guardrails and orchestration. |
| `Tools/validation/` | Repository validators | Non-invasive syntax, docs, AI pipeline, NPU helper, generated artifact and policy validators. |
| `Tools/workflow/` | Local workflow runners and helper shells | Unified launcher is canonical; additional shell/GUI/helper scripts are supporting and must be classified before promotion. |
| `Tools/repo_patch_runner/` | Structured patch runner tooling | Supports repository modification workflows. |
| `indexAI/` | Generated AI-oriented project index | Generated context and patch material. Do not hand-refactor as source. |
| `patch_specs/` | Patch specification artifacts | Structured patch records and applied patch metadata. |
| `docs/` | Stable documentation | Human and AI-readable project contracts. |
| `examples/` | Example area | Reserved for reproducible examples and small fixtures. |

## AI navigation order

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read `docs/README.md`.
4. Read `docs/PROJECT_AI_CONSCIOUSNESS.md`.
5. Read this file.
6. Read `docs/DATA_FLOW.md`.
7. Read `docs/REFACTORING_AND_REUSE_PLAN.md`.
8. Read `docs/SHARED_SCRIPTING_UTILITIES.md`.
9. Read `docs/QUALITY_GATE.md`.
10. For NPU helper work, read `Tools/npu/pipeline/README.md`.
11. Read `Tools/validation/README.md` when changing validators/workflows.
12. Read `Scripting/README.md` for Blender package work.
13. Read the README of the target package under `Scripting/`.
14. Inspect the actual script before editing.

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
| `Tools/npu/run_dual_ai_pipeline.py` | End-to-end local/AI orchestration | Split gradually into `Tools/npu/pipeline/` modules after focused validation and index regeneration. |
| `Tools/npu/ollama_runtime.py` | Ollama runtime/session helpers | Provider module under `Tools/npu/pipeline/providers.py` in a later runtime-wiring phase. |
| `Tools/npu/npu_runtime.py` | NPU preflight | Provider/preflight module in a later runtime-wiring phase. |
| `Tools/npu/build_project_ai_index.py` | Project index generation | Keep as generator; generated output remains non-source. |
| `Tools/npu/build_ai_service_packet.py` | AI service packet generation | Keep as artifact builder; extract common JSON/path helpers later. |
| `Tools/ai/agent_state.py` | Generic memory records and microtask packet model | Keep package-neutral; connect to app workers only through explicit packet contracts. |
| `Tools/ai/build_agent_state_packet.py` | CLI for task-local agent state packets | Keep non-invasive; no Blender, GPU, NPU or FFmpeg execution. |
| `Tools/ai/agent_memory_policy.py` | Memory retention, quarantine and promotion-candidate rules | Keep deterministic and non-destructive. |
| `Tools/ai/review_agent_memory.py` | CLI for memory policy reports | Writes reports only; promotion into docs remains manual. |

### AI inventory, memory and evidence helpers

| File | Main responsibility | Documentation status |
|---|---|---|
| `Tools/ai/build_agent_memory_inventory.py` | Build memory inventory / visibility report. | Supporting tool; add to future memory/toolbox catalog. |
| `Tools/ai/build_agent_agnostic_tool_inventory.py` | Build agent-agnostic tool inventory. | Supporting tool; candidate for unified toolbox visibility. |
| `Tools/ai/build_code_interpreter_report.py` | Build code-interpreter capability/report surface. | Supporting tool; not a launcher replacement. |
| `Tools/ai/build_refactor_duplication_audit.py` | Audit duplication across refactor surfaces. | Supporting audit tool. |
| `Tools/ai/github_evidence_bundle_reports.py` | Helper module for evidence bundle report summaries. | Internal helper; document as library, not user command. |
| `Tools/ai/agent_runtime_sqlite_memory.py` | Runtime SQLite memory support. | Internal/local state helper; do not commit DB outputs. |
| `Tools/ai/agent_memory_routing_policy.py` | Memory routing policy logic. | Internal policy helper. |

### Workflow helper scripts

The unified launcher remains the canonical headless entrypoint. The following scripts exist as supporting helpers and must not be promoted to primary flow without explicit review.

| File | Initial classification | Notes |
|---|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | canonical-entrypoint | Active local-AI entrypoint. |
| `Tools/workflow/run_local_validation_after_refactor.ps1` | supporting-tool | Full local validation wrapper. |
| `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | launcher-internal/supporting-tool | Official local AI task adapter. |
| `Tools/workflow/run_post_validation_ai_packet.ps1` | launcher-internal/supporting-tool | Advisory packet builder. |
| `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | launcher-internal/supporting-tool | Explicit multistep provider workflow. |
| `Tools/workflow/run_docs_md_refactor_10min.ps1` | legacy-superseded/supporting-tool | Prefer unified launcher `md` mode. |
| `Tools/workflow/run_local_ai_markdown_task.ps1` | supporting-tool | Markdown task helper. |
| `Tools/workflow/startup_preflight.ps1` | diagnostic-only | Startup/preflight wrapper. |
| `Tools/workflow/startup_check.py` | diagnostic-only | Startup check used by launcher/smoke paths. |
| `Tools/workflow/workflow_shell.py` | gui-or-shell-helper | Interactive helper; not canonical headless flow. |
| `Tools/workflow/workflow_shell_with_push.py` | unsafe-or-write-capable, gui-or-shell-helper | Push-capable; requires explicit user intent. |
| `Tools/workflow/workflow_debug.py` | diagnostic-only | Debug helper. |
| `Tools/workflow/workflow_shell_with_push.py` | unsafe-or-write-capable | Do not use as default example. |
| `Tools/workflow/gui/workflow_gui_modern.py` | gui-or-shell-helper | GUI helper. |
| `Tools/workflow/gui/workflow_gui_with_push.py` | unsafe-or-write-capable, gui-or-shell-helper | Push-capable GUI helper; explicit intent required. |
| `Tools/workflow/asset_inventory.py` | supporting-tool | Asset inventory helper. |
| `Tools/workflow/scene_brief.py` | supporting-tool/application-domain | Scene brief helper. |
| `Tools/workflow/artifact_consult.py` | supporting-tool | Artifact consultation helper. |
| `Tools/workflow/project_awareness.py` | supporting-tool | Project-awareness context helper. |
| `Tools/workflow/smart_ai_context.py` | supporting-tool | Smart AI context helper. |
| `Tools/workflow/ai_runtime_diagnostics.py` | diagnostic-only | Runtime diagnostics helper. |
| `Tools/workflow/git_auto_push.py` | unsafe-or-write-capable | Any push behavior requires explicit user intent. |

For the audit trail, see:

```text
docs/LOCAL_AI_TASKS/forgotten-scripts-documentation-audit.md
```

### GPU/NPU diagnostics and smokes

| File | Initial classification | Notes |
|---|---|---|
| `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` | launcher-internal or legacy-superseded | Verify current caller before changing docs. |
| `Tools/ai/run_npu_gpu_deep_review_auditor.py` | diagnostic-only | Explicit local diagnostic. |
| `Tools/validation/run_gpu_runner_provider_error_smoke.py` | diagnostic-only | Provider error smoke. |
| `Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py` | diagnostic-only | GPU counter smoke. |
| `Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py` | diagnostic-only | Runtime tool routing smoke. |

### NPU helper package

| File | Main responsibility | Runtime scope |
|---|---|---|
| `Tools/npu/pipeline/config.py` | Repository paths, track defaults and data-only pipeline configuration. | No runtime execution. |
| `Tools/npu/pipeline/artifact_paths.py` | Generated artifact path normalization, allowed-prefix validation and exact legacy runtime output policy. | No provider/runtime execution. |
| `Tools/npu/pipeline/io_utils.py` | UTF-8 text and JSON-object IO helpers plus legacy-compatible aliases. | Filesystem IO only. |
| `Tools/npu/pipeline/legacy_compat.py` | Compare legacy helper behavior against new helpers before wiring. | No runtime execution. |
| `Tools/npu/pipeline/fixtures.py` | Deterministic fixture payloads for tests and dry-runs. | No runtime execution. |
| `Tools/npu/pipeline/prompts.py` | Deterministic prompt payload builders. | No provider execution. |
| `Tools/npu/pipeline/context_builder.py` | Bounded context slices and compact context bundle metrics. | No model/provider execution. |
| `Tools/npu/pipeline/providers.py` | Planned-only provider request/result envelopes and provider preflight report normalization. | Does not call providers. |
| `Tools/npu/pipeline/runner.py` | Planned-only stage-plan reports. | Does not orchestrate runtime. |
| `Tools/npu/pipeline/validators.py` | Contract-level validators preserving unknown future fields. | No runtime execution. |
| `Tools/npu/pipeline/artifact_writer.py` | Validated generated-artifact write helpers. | Writes only explicitly allowed generated artifact paths. |
| `Tools/npu/pipeline/migration_readiness.py` | Runtime-wiring readiness gates. | Blocks runtime wiring by default. |
| `Tools/npu/pipeline/reports.py` | Helper-boundary report utilities. | No runtime execution. |

### Validation tooling

| File | Main responsibility | Refactor target |
|---|---|---|
| `Tools/validation/generated_file_policy.py` | Generic generated-file and generated-artifact path policy primitives | Keep input-agnostic and output-application-agnostic. |
| `Tools/validation/generated_python_policy.py` | Generic generated Python syntax and hazard policy | Keep independent from input domains and target applications. |
| `Tools/validation/check_generated_python_policy.py` | CLI validator for generic generated Python policy | Keep as the language-level layer before application adapters. |
| `Tools/validation/check_generated_artifact_path_policy.py` | Generic safe-destination validator for generated artifact paths | Use before allowing generated outputs outside existing safe prefixes. |
| `Tools/validation/check_generated_blender_script_policy.py` | Blender-specific generated Python script policy adapter | Compose generic Python rules with Blender assumptions here, not in the generic policy engine. |
| `Tools/validation/check_ai_dry_run_matrix_contract.py` | Dry-run matrix report contract validator | Keep as report-contract validation, not runtime execution. |
| `Tools/validation/check_npu_pipeline_modules.py` | NPU helper import/contract smoke validator | Keep provider-free, Blender-free and runtime-free. |
| `Tools/validation/check_npu_pipeline_helper_tests.py` | JSON-report wrapper for NPU helper unit tests | Keep deterministic and temporary-directory only. |
| `Tools/validation/check_npu_pipeline_docs.py` | NPU helper README/module alignment validator | Keep as docs consistency check. |
| `Tools/validation/test_npu_pipeline_helpers.py` | Unit tests for app-agnostic NPU helper modules | No provider, Blender, GPU, NPU, Ollama or FFmpeg execution. |

### Workflow tooling

| File | Main responsibility |
|---|---|
| `Tools/workflow/run_local_validation_after_refactor.ps1` | Full local validation workflow after AI-assisted refactors. |
| `Tools/workflow/run_npu_pipeline_helper_validation.ps1` | Focused NPU helper validation workflow for smoke, unit, docs and syntax checks. |

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
- For NPU helper work, keep `Tools/npu/pipeline/` runtime-free until local validation and index regeneration are green.

## Refactoring guidance

Use this order:

1. Add shared utility.
2. Validate utility independently.
3. Add optional package adapter.
4. Test in Blender or with a dry-run.
5. Migrate one package call site.
6. Document result and risks.

For NPU pipeline decomposition:

1. Add or validate helper contracts under `Tools/npu/pipeline/`.
2. Run focused NPU helper validation.
3. Run full local validation.
4. Regenerate AI/NPU indexes.
5. Wire one helper group into `Tools/npu/run_dual_ai_pipeline.py` in a later PR.
6. Compare local outputs after the wiring step.

Do not combine broad code motion, behavior changes, and artistic scene changes in the same patch.

## Not specified

A full function-level module index is not manually maintained here. Generate it from code when needed by using the project indexing tools.
