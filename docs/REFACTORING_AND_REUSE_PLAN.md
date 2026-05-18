# Refactoring and Reuse Plan

## Purpose

This document defines the recommended refactoring strategy for `blender-audio-project`.

The project already contains working Blender scripts, generated packages, AI/NPU tooling, and GitHub-facing documentation. The next improvement should not be a broad rewrite. The correct direction is **progressive encapsulation**: extract stable, reusable behavior into shared modules while keeping existing production scripts operational.

The app-specific Blender packages are downstream consumers of the core. Ready To Jazz migration and package adoption of `Scripting/shared/blender_compat.py` should wait until the AI/NPU/backend core is app-agnostic, validated and documented.

Core is not limited to a fixed module list. If useful shared functions, pure helpers, dataclasses, report builders, validators, policy checks or provider adapters emerge during implementation, they should be added to the core when they are app-agnostic and locally validated. The boundary is conceptual: reusable infrastructure belongs in the core; package-specific artistic or Blender-scene behavior belongs in application packages.

## Current technical assessment

The repository is now structured as a production-oriented audio-reactive Blender workspace rather than a single script collection.

Observed structure:

| Area | Current role | Refactoring meaning |
|---|---|---|
| `Tools/workflow/workflow_run/audio_analysis/` and `Tools/workflow/workflow_run/scene_spec/` | Audio analysis, summary building, scene-spec normalization | Keep importable services plus thin CLI wrappers. |
| `Scripting/v61b/` | Main qualitative Blender reference implementation | Keep stable; extract reusable behavior additively only after core/backend work is stable. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Large generated/refined package | Treat as future extraction candidate; not current scope. |
| `Scripting/shared/` | Target area for cross-package utilities | Existing helper area; broad adoption remains future work. |
| `Tools/npu/` | Local AI, NPU, context, and implementation-draft workflow | Runtime helper adoption has started in narrow validated phases. |
| `Tools/npu/pipeline/` | App-agnostic NPU helper package | Helper contracts, fixtures, validators, readiness gates and planned provider descriptors exist; selected helper groups are now consumed by `Tools/npu/run_dual_ai_pipeline.py`. |
| `Tools/validation/` | Non-invasive validation layer | Includes generic policy validators, AI pipeline validators and focused NPU helper/runtime bridge validators. |
| `indexAI/` | Generated indexes and AI context | Keep generated; do not treat as hand-edited source. |
| `docs/` | Stable human and AI documentation | Use as the contract for package creation and refactoring. |

## Main problems to solve

### 1. Mixed CLI and library responsibilities

Files such as the workflow audio/scene CLIs and several tools under `Tools/npu/` expose useful functions; keep reusable logic in importable service modules and public files as wrappers.

Recommended direction:

```text
project module/service
  -> pure functions and dataclasses
CLI wrapper
  -> argparse, path defaults, console output
```

This can be staged without moving files immediately by first adding importable wrappers under `Scripting/shared/` or `Tools/lib/`.

### 2. Oversized orchestration functions

The dual-AI pipeline and some Blender packages contain long functions that perform path resolution, prompt construction, model calls, validation, fallback generation, and output writing in the same flow.

Recommended decomposition:

```text
PipelineConfig
InputResolver
ContextBuilder
ModelProvider
PromptBuilder
ResponseParser
DraftValidator
ArtifactWriter
RuntimeOutputManifest
```

This makes NPU/GPU/Ollama steps easier to run in parallel and easier to test without Blender.

Current NPU decomposition status after PR #41-#47:

```text
Tools/npu/pipeline/ helper package exists
Tools/npu/run_dual_ai_pipeline.py has already adopted helper groups incrementally
IO helper aliases are wired
contract/path helpers are wired
prompt payload helpers are wired
context-summary and generated support-file write-planning helpers are wired
exact legacy output policy and provider-preflight normalization are wired
provider execution adapters remain future work and should stay separately scoped
```

### 3. Repeated path and JSON handling

Several areas load JSON, resolve local workstation paths, create output directories, and write manifests.

Current state:

```text
Tools/npu/pipeline/io_utils.py exists and selected legacy-compatible aliases are consumed by the NPU runtime orchestrator.
Scripting/shared/json_io.py exists for package/shared code.
```

Future direction:

```text
keep IO helpers app-agnostic
avoid hand-editing generated indexes
avoid broad Blender package migration until core validation remains stable
```

### 4. Encoding logic duplicated across packages

The v61b encoder and the generated package encoder both implement FFmpeg command building and output profile selection.

Recommended future shared modules:

```text
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
Scripting/shared/image_sequence.py
```

This remains below NPU/backend stabilization in priority.

### 5. Blender API compatibility should be isolated

Blender-version-sensitive code should not be spread across scene modules.

Recommended shared module:

```text
Scripting/shared/blender_compat.py
```

Current rule:

```text
helper existence and smoke validation are not permission for broad runtime adoption.
Ready To Jazz and blender_compat adoption stay out of the current NPU/backend phase.
```

### 6. Configuration is currently global-heavy

`Scripting/v61b/config.py` is intentionally practical, but the next reusable layer should prefer structured config objects.

Recommended staged approach:

1. Keep current `config.py` for compatibility.
2. Add structured config adapters later.
3. New packages consume dataclasses directly only after validation.

### 7. Scene construction needs stronger object registries

The `spaziotempo/core/registry.py` direction is correct: scene layers, object naming, feature ownership, and hotpatch targeting should be data-first.

Migration rule: leave `v61b` registry as-is first; new packages should reuse the shared registry pattern later.

## Priority refactoring roadmap

### Phase 1: documentation and contracts

Status: active maintenance.

- Keep status docs current after fast PR chains.
- Keep execution plans stateful and move/mark completed plans after merge.
- Update README files to show actual repository areas.
- Mark `indexAI/` as generated context.

### Phase 2: app-agnostic core contracts

Status: active.

Tighten the core validation surface before touching Blender package behavior:

```text
validator report consistency
AI pipeline schema/report contracts
dry-run matrix contract and output consistency
generated artifact path policy
agent memory policy
guardrail/remediation report contracts
NPU helper/runtime bridge report contract consistency
```

This phase should reduce warning noise and make downstream automation rely on common root fields such as:

```text
schema_version
kind
repo_root
passed
errors
warnings
checks
```

### Phase 3: service-oriented AI/NPU core

Status: active; helper adoption is partially completed; provider execution adapters remain future work.

Current helper package:

```text
Tools/npu/pipeline/
  config.py
  artifact_paths.py
  io_utils.py
  legacy_compat.py
  fixtures.py
  prompts.py
  context_builder.py
  providers.py
  runner.py
  validators.py
  artifact_writer.py
  migration_readiness.py
  reports.py
```

Already adopted by runtime in narrow validated phases:

```text
IO helper aliases
implementation draft contract/path helpers
prompt payload helpers
context summary helper
support-file write-planning helper
legacy output policy guard
provider-preflight normalization helper
```

Still future work:

```text
provider execution adapters
provider result parsing/reporting
runtime-output manifest/reporting
prompt prose extraction
full artifact writer runtime migration
memory/guardrail runtime integration
```

Current rule:

```text
continue one helper group at a time
preserve provider/model execution behavior unless explicitly scoped
run focused NPU validation and full local validation before merge
regenerate AI/NPU indexes after structural changes
```

### Phase 4: additive shared utilities

Status: lower priority than NPU/backend stabilization.

Shared modules may be added without changing existing consumers, but broad package adoption is deferred:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
Scripting/shared/blender_compat.py
```

### Phase 5: application adapters and controlled migration

Status: future phase requiring explicit approval and Blender validation.

Only after the app-agnostic backend/pipeline/AI/NPU/multistep/guardrail/memory core is complete enough to validate locally, add small adapters inside packages.

Ready To Jazz and `blender_compat.py` package adoption should not begin until these core criteria are met:

```text
validation report contract warnings are either resolved or explicitly tracked
AI dry-run matrix passes after relevant changes
NPU runtime helper bridge remains green
provider execution changes, if any, are separately scoped and validated
guardrail and memory policies have deterministic validation
generated artifact path policy protects all planned writes
AI/NPU indexes are regenerated by scripts after structural changes
```

## Specific extraction candidates

| Source | Candidate extraction | Target shared module |
|---|---|---|
| `Scripting/v61b/io_utils.py` | JSON loading, input checks, sequencer helpers | `json_io.py`, `blender_compat.py` later. |
| `Scripting/v61b/encode_ffmpeg_v61b.py` | FFmpeg discovery, frame scanning, profile command builder | `ffmpeg_encoder.py`, `image_sequence.py`, `render_profiles.py` later. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py` | YouTube CPU/GPU encoding presets | `render_profiles.py`, `ffmpeg_encoder.py` later. |
| `Tools/npu/provider_mesh/_shared/ollama_runtime.py` | model runtime provider | Provider execution adapter phase, not current default. |
| `Tools/npu/run_dual_ai_pipeline.py` | orchestration, prompt, validation, fallback writing | Continue `Tools/npu/pipeline/*` adoption one helper group at a time. |
| `Tools/workflow/workflow_run/scene_spec/` | scene spec model and validators | Keep under workflow service modules unless promoted to a shared library later. |

## Encapsulation rules

1. Keep Blender object creation separate from audio mapping.
2. Keep material node construction separate from animation curves.
3. Keep render settings separate from encoding.
4. Keep CLI argument parsing separate from reusable business logic.
5. Keep AI prompts separate from validators.
6. Keep model-runtime providers separate from orchestration.
7. Keep local workstation defaults outside package-neutral shared modules.
8. Keep generated indexes out of source-level refactors.
9. Keep provider execution changes separate from helper-contract/runtime bridge PRs.

## Testing strategy before migration

| Refactor type | Required check |
|---|---|
| Python utility extraction | `python -m py_compile` on changed modules or `check_python_syntax.py`. |
| NPU helper/runtime bridge change | `run_npu_pipeline_helper_validation.ps1` plus full local runner. |
| NPU/Ollama provider execution change | Separate execution plan, focused tests, full local validation and explicit maintainer approval. |
| Blender compatibility wrapper | Headless Blender import or manual Blender run. |
| Encoding utility | Command preview plus one short frame-sequence encode. |
| Scene package migration | Open in Blender, create scene, add audio strip, verify frame range. |
| Documentation update | Link and path review. |

## Recommended next commits

Current immediate sequence:

1. `docs: reconcile post 47 npu state`
2. `test(npu): normalize helper report contract checks`
3. `feat(npu): add runtime output manifest report`
4. `test(npu): validate runtime output manifest without provider changes`

Historical/general commit examples:

```text
docs: add refactoring and reuse plan
docs: refresh repository readmes
feat(shared): add path and json utility module
feat(shared): add ffmpeg encode profile builder
refactor(npu): wire pipeline helper group into dual ai pipeline
test: add syntax and package structure checks
```

## Current conclusion

The project is ready for continued reuse-oriented refactoring, but only through additive extraction and narrow runtime bridge phases. The safest immediate value is to finish post-PR #47 documentation/status reconciliation, then normalize NPU report contracts, then add runtime-output observability before touching provider execution behavior.
