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
| Root Python tools | Audio analysis, summary building, scene-spec normalization | Convert into importable services plus CLI wrappers. |
| `Scripting/v61b/` | Main qualitative Blender reference implementation | Keep stable; extract reusable behavior additively. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Large generated/refined package | Treat as extraction candidate, especially for encoding/render profiles. |
| `Scripting/shared/` | Target area for cross-package utilities | Promote path, render, encoding, JSON, diagnostics, and Blender compatibility helpers here. |
| `Tools/npu/` | Local AI, NPU, context, and implementation-draft workflow | Split orchestration, prompts, validators, and providers. |
| `indexAI/` | Generated indexes and AI context | Keep generated; do not treat as hand-edited source. |
| `docs/` | Stable human and AI documentation | Use as the contract for package creation and refactoring. |

## Main problems to solve

### 1. Mixed CLI and library responsibilities

Files such as `analyze_wav.py`, `build_track_summary.py`, `normalize_scene_spec.py`, and several tools under `Tools/npu/` expose useful functions but are still primarily script-shaped.

Recommended direction:

```text
project module/service
  -> pure functions and dataclasses
CLI wrapper
  -> argparse, path defaults, console output
```

Target result:

```text
src/spaziotempo_audio/
  analysis.py
  summary.py
  scene_spec.py
  schemas.py

Tools/
  cli/
    analyze_wav.py
    build_track_summary.py
    normalize_scene_spec.py
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
```

This makes NPU/GPU/Ollama steps easier to run in parallel and easier to test without Blender.

### 3. Repeated path and JSON handling

Several areas load JSON, resolve local workstation paths, create output directories, and write manifests.

Recommended shared modules:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/artifact_manifest.py
```

Minimum shared API:

```python
resolve_project_root(start: Path | None = None) -> Path
read_json(path: Path) -> dict
write_json(path: Path, data: dict) -> None
ensure_file(path: Path, label: str) -> Path
```

### 4. Encoding logic duplicated across packages

The v61b encoder and the generated package encoder both implement FFmpeg command building and output profile selection.

Recommended shared modules:

```text
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
Scripting/shared/image_sequence.py
```

Suggested objects:

```python
@dataclass(frozen=True)
class EncodeProfile:
    name: str
    video_codec: str
    audio_codec: str
    pixel_format: str
    color_flags: list[str]
    extra_args: list[str]

@dataclass(frozen=True)
class ImageSequence:
    directory: Path
    prefix: str
    extension: str
    first_frame: int
    frame_count: int
    pattern: str
```

### 5. Blender API compatibility should be isolated

Blender-version-sensitive code should not be spread across scene modules.

Recommended shared module:

```text
Scripting/shared/blender_compat.py
```

Candidate functions:

```python
create_sound_strip(scene, audio_path: Path, frame_start: int = 1)
clear_sequence_editor(scene)
create_noise_or_voronoi_texture(nodes, preferred: str)
safe_set_property(obj, attr: str, value)
```

This directly reduces risk from issues such as renamed or removed Blender node types.

### 6. Configuration is currently global-heavy

`Scripting/v61b/config.py` is intentionally practical, but the next reusable layer should prefer structured config objects.

Recommended staged approach:

1. Keep current `config.py` for compatibility.
2. Add `Scripting/shared/config_model.py`.
3. Add adapters that build dataclasses from the existing module.
4. New packages consume dataclasses directly.

Example target model:

```python
@dataclass(frozen=True)
class RenderConfig:
    fps: float
    resolution_x: int
    resolution_y: int
    engine: str
    output_mode: str

@dataclass(frozen=True)
class AudioReactiveConfig:
    analysis_json: Path
    audio_path: Path
    output_dir: Path
    render: RenderConfig
```

### 7. Scene construction needs stronger object registries

The `spaziotempo/core/registry.py` direction is correct: scene layers, object naming, feature ownership, and hotpatch targeting should be data-first.

Recommended expansion:

```text
Scripting/shared/scene_registry.py
Scripting/shared/collections.py
Scripting/shared/feature_registry.py
```

Migration rule: leave `v61b` registry as-is first; new packages should reuse the shared registry pattern.

## Priority refactoring roadmap

### Phase 1: documentation and contracts

Status: safe to apply immediately.

- Add this refactoring plan.
- Update README files to show actual repository areas.
- Document extraction candidates and priority order.
- Mark `indexAI/` as generated context.
- Add `docs/ROOT_TOOLS.md` or equivalent when root CLI behavior is finalized.

### Phase 2: app-agnostic core contracts

Status: safe to apply before application migration.

Tighten the core validation surface before touching Blender package behavior:

```text
validator report consistency
AI pipeline schema/report contracts
dry-run matrix contract and output consistency
generated artifact path policy
agent memory policy
guardrail/remediation report contracts
```

This phase should reduce warning noise and make downstream automation rely on common root fields such as:

```text
schema_version
kind
repo_root
passed
errors
warnings
```

### Phase 3: service-oriented AI/NPU core

Status: medium risk, but still app-agnostic.

Split AI/NPU/backend orchestration before migrating application packages:

```text
Tools/npu/pipeline/
  config.py
  context_builder.py
  prompts.py
  providers.py
  validators.py
  artifact_writer.py
  runner.py
```

The core should remain independent from any one Blender package. Provider adapters, multistep scheduling, guardrail handling, memory policy and artifact writing should be testable with dry-runs and generated report contracts.

This module list is a starting map, not a ceiling. Add focused modules or functions when they remove duplication or make the pipeline easier to validate, for example:

```text
typed path/report helpers
JSON/model-output normalization helpers
guardrail scoring and remediation functions
memory filtering and promotion functions
provider capability/preflight helpers
artifact manifest builders
dry-run fixture builders
```

Avoid catch-all utility bags. A new helper should have a clear owner, a narrow responsibility and at least one validation path.

### Phase 4: additive shared utilities

Status: low risk.

Create shared modules without changing existing consumers:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
Scripting/shared/blender_compat.py
```

No existing working package should be modified in this phase. Blender compatibility helpers may exist and be validated, but adoption by Ready To Jazz or other runtime packages belongs to the application migration phase.

### Phase 5: application adapters and controlled migration

Status: requires core completion and Blender validation.

Only after the app-agnostic backend/pipeline/AI/NPU/multistep/guardrail/memory core is complete enough to validate locally, add small adapters inside packages:

Add small adapters inside packages:

```text
Scripting/v61b/adapters/
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/adapters/
```

Adapters can call shared utilities while preserving current package APIs.

Migrate one concern at a time:

1. Path and JSON utilities.
2. FFmpeg command generation.
3. Image sequence scanning.
4. Blender sequencer compatibility.
5. Render profile selection.
6. Diagnostics and hotpatch helpers.

Ready To Jazz and `blender_compat.py` package adoption should not begin until these core completion criteria are met:

```text
validation report contract warnings are either resolved or explicitly tracked
AI dry-run matrix passes after relevant changes
AI pipeline report contracts are validated without schema-v6 drift
NPU/provider decomposition preserves existing CLI behavior
guardrail and memory policies have deterministic validation
generated artifact path policy protects all planned writes
new reusable core functions have focused tests or validator coverage
AI/NPU indexes are regenerated by scripts after structural changes
```

## Specific extraction candidates

| Source | Candidate extraction | Target shared module |
|---|---|---|
| `Scripting/v61b/io_utils.py` | JSON loading, input checks, sequencer helpers | `json_io.py`, `blender_compat.py` |
| `Scripting/v61b/encode_ffmpeg_v61b.py` | FFmpeg discovery, frame scanning, profile command builder | `ffmpeg_encoder.py`, `image_sequence.py`, `render_profiles.py` |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py` | YouTube CPU/GPU encoding presets | `render_profiles.py`, `ffmpeg_encoder.py` |
| `Scripting/v61b/render_setup.py` | render configuration patterns | `render_profiles.py` |
| `Scripting/v61b/scene_tuning_panel.py` | panel registration, profile normalization | `panel_base.py`, `render_profiles.py` |
| `Scripting/v61b/hotpatch/common.py` | patch discovery and diagnostics helpers | `diagnostics.py`, `hotpatch_base.py` |
| `Tools/npu/ollama_runtime.py` | model runtime provider | `Tools/npu/pipeline/providers.py` |
| `Tools/npu/run_dual_ai_pipeline.py` | orchestration, prompt, validation, fallback writing | `Tools/npu/pipeline/*` |
| `normalize_scene_spec.py` | scene spec model and validators | `src/spaziotempo_audio/scene_spec.py` or `Tools/lib/scene_spec.py` |

## Proposed package architecture for future generated scenes

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
    README.md
    input_schema.json
  outputs/
    README.md
  notes/
    known_issues.md
    tuning_notes.md
```

Package-specific code should only contain artistic and scene-specific decisions. Generic IO, FFmpeg, render profiles, JSON parsing, and compatibility wrappers should come from `Scripting/shared/`.

## Encapsulation rules

1. Keep Blender object creation separate from audio mapping.
2. Keep material node construction separate from animation curves.
3. Keep render settings separate from encoding.
4. Keep CLI argument parsing separate from reusable business logic.
5. Keep AI prompts separate from validators.
6. Keep model-runtime providers separate from orchestration.
7. Keep local workstation defaults outside package-neutral shared modules.
8. Keep generated indexes out of source-level refactors.

## Testing strategy before migration

A refactor is acceptable only when it passes at least one relevant check:

| Refactor type | Required check |
|---|---|
| Python utility extraction | `python -m py_compile` on changed modules |
| Blender compatibility wrapper | Headless Blender import or manual Blender run |
| Encoding utility | Command preview plus one short frame-sequence encode |
| Scene package migration | Open in Blender, create scene, add audio strip, verify frame range |
| NPU/Ollama pipeline split | Dry-run with deterministic fallback enabled |
| Documentation update | Link and path review |

## Recommended next commits

1. `docs: add refactoring and reuse plan`
2. `docs: refresh repository readmes`
3. `feat(shared): add path and json utility module`
4. `feat(shared): add ffmpeg encode profile builder`
5. `refactor(v61b): add optional shared encoder adapter`
6. `refactor(npu): split dual ai pipeline prompts and validation`
7. `test: add syntax and package structure checks`

## Current conclusion

The project is ready for reuse-oriented refactoring, but only through additive extraction. The safest immediate value is to finish the app-agnostic validation and AI/NPU core first, then migrate working Blender packages one component at a time after Blender validation.
