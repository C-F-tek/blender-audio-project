# Project Status Point

## Purpose

This document records the current technical status of `blender-audio-project` after the repository documentation, shared utilities and AI artifact pipeline refactoring work.

It is intended as a practical checkpoint before the next local validation phase.

## Current conclusion

The project is no longer only a Blender scripting experiment. It is now a structured audio-reactive production workspace with:

- root audio-analysis tools;
- Blender scene packages;
- a mature reference workflow under `Scripting/v61b/`;
- one large generated/refined package for the Ready To Jazz/YouTube workflow;
- a modular AI artifact pipeline under `Tools/ai/pipeline/`;
- AI/NPU/GPU-oriented artifact generation tools;
- generated indexes under `indexAI/`;
- documentation for package generation, quality gates, refactoring and AI onboarding.

The next correct move is not a broad rewrite. The next correct move is **local validation of the modular pipeline and continued controlled encapsulation**.

## Project maturity by area

| Area | Current status | Operational meaning |
|---|---|---|
| Audio analysis | usable | Existing root tools can generate analysis and summary data. |
| Blender reference package | strong | `Scripting/v61b/` is the reference architecture. |
| Generated Blender package | usable but heavy | `ready_to_jazz_wow_youtube_profiles_audio_sync` works as a standalone package but is monolithic. |
| Shared utilities | active foundation | Path, JSON, image-sequence, FFmpeg and render-profile helpers exist; migration is still incomplete. |
| AI artifact pipeline | modularized, pending local validation | Entry point is thin; implementation is split into focused modules under `Tools/ai/pipeline/`. |
| NPU/GPU parallelism | structurally prepared | Pipeline has lanes, scheduler, dry-run matrix and guardrail remediation models. |
| Documentation | strong | Current docs now define project direction, safe modification rules and pipeline status. |
| Validation | improving | Syntax, package, JSON and AI pipeline module validators exist. Local dry-run matrix still must be executed after latest refactor. |
| JSON schemas | partial | Schema notes exist, but full production contracts are not complete. |
| CI/GitHub automation | present but not complete | Templates and patch workflow exist; full runtime validation still needs work. |

## Main source areas

### Root tools

| File | Status | Next action |
|---|---|---|
| `analyze_wav.py` | usable root CLI/script | Convert reusable logic into an importable service later. |
| `build_track_summary.py` | usable compact-summary builder | Keep CLI behavior; extract summary service later. |
| `normalize_scene_spec.py` | useful but script-shaped | Move scene-spec models/validators into a reusable module later. |

### Blender packages

| Area | Status | Next action |
|---|---|---|
| `Scripting/v61b/` | stable reference | Do not destructively refactor. Add adapters only after shared utilities exist. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | large standalone package | Good candidate for future split and extraction. |
| `Scripting/_template_audio_reactive_package/` | useful template | Update progressively as shared utilities become real. |
| `Scripting/shared/` | active shared layer | Validate existing helpers, document contracts and add missing Blender compatibility/config/diagnostics modules. |

### AI pipeline

Status marker:

```text
modular_schedule_complete_pending_local_validation
```

Primary files:

```text
Tools/ai/run_parallel_artifact_pipeline.py
Tools/ai/run_pipeline_dry_run_matrix.py
Tools/validation/check_ai_pipeline_modules.py
Tools/ai/pipeline/
```

Important docs:

```text
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
Tools/ai/pipeline/refactor_status.py
```

Module map:

| Module | Status | Meaning |
|---|---|---|
| `defaults.py` | implemented | Central pipeline defaults and report filenames. |
| `models.py` | implemented | Pipeline dataclasses and lane enum. |
| `runner.py` | implemented | Low-level command runner. |
| `compat.py` | implemented | Schema-v6 compatibility adapter. |
| `artifact_contracts.py` | implemented | Expected artifacts and planned outputs. |
| `cli.py` | implemented | Public CLI parser. |
| `preflight.py` | implemented | Non-invasive environment/input checks. |
| `steps.py` | implemented | Command and step builders. |
| `scheduler.py` | implemented | Serial/parallel scheduling policy. |
| `orchestrator.py` | implemented | Concrete step execution helpers. |
| `schema_report.py` | implemented | Report builder with `summary` and `schedule`. |
| `guardrail_models.py` | implemented | Typed guardrail remediation queue models. |
| `remediation.py` | implemented | Auto-safe remediation loop. |
| `refactor_status.py` | implemented | Machine-readable status marker. |

### AI/NPU tooling

| Area | Status | Next action |
|---|---|---|
| `Tools/ai/run_parallel_artifact_pipeline.py` | thin entrypoint | Keep thin; add behavior to modules. |
| `Tools/ai/pipeline/` | modularized | Validate locally with smoke and dry-run matrix. |
| `Tools/npu/run_dual_ai_pipeline.py` | powerful but large | Split later into config/context/prompts/providers/validators/writers. |
| `Tools/npu/ollama_runtime.py` | reusable runtime layer | Candidate for provider abstraction. |
| `Tools/npu/npu_runtime.py` | useful preflight layer | Candidate for provider/preflight module. |
| `indexAI/` | generated context | Regenerate after structural changes; do not hand-refactor as source. |

## Most important technical findings

### 1. `v61b` should remain the stable reference

`Scripting/v61b/main_v61b.py` already has a clean orchestration sequence: input validation, JSON loading, render/world setup, audio strip, camera, scene base, assets, atmosphere, physics, animation, structure classification and summary output.

This is the right shape for a reference package. It should not be rewritten wholesale.

### 2. The generated Ready To Jazz package is useful but monolithic

`Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` is a large standalone script. It is practical for one workflow, but not ideal as reusable architecture.

The right treatment is not immediate splitting. First extract shared infrastructure such as FFmpeg profiles, image sequence handling and path/config helpers.

### 3. Shared utilities are now the critical migration layer

Implemented pure Python helpers:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/image_sequence.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
```

Next missing shared modules:

```text
Scripting/shared/blender_compat.py
Scripting/shared/config_model.py
Scripting/shared/diagnostics.py
```

### 4. AI artifact pipeline modularization is structurally complete

The old large orchestrator has been split into focused modules. The current state is intentionally marked as pending workstation validation, not as incomplete refactoring.

Required local validation:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

### 5. The project now needs local validation and index regeneration

After the latest structural and documentation changes, the next workstation task is:

```text
pull latest
run validation block
run dry-run matrix
regenerate AI/NPU indexes
commit generated index files only
```

## Current blockers

| Blocker | Impact | Recommendation |
|---|---|---|
| Latest AI pipeline split not yet locally dry-run validated | Possible import/path issues may still exist | Run smoke validator and dry-run matrix. |
| Shared utilities not fully adopted | New packages can still duplicate logic | Validate existing helpers, then add optional package adapters. |
| Large monolithic generated script | Harder to maintain and patch | Extract infrastructure before artistic scene logic. |
| NPU dual pipeline scripts are large | Harder to test and evolve | Split providers, prompts, validators and artifact writers later. |
| JSON contracts partial | AI-generated artifacts can drift | Strengthen schema docs and validators. |
| Generated indexes stale after edits | AI context may miss new docs/modules | Regenerate indexes after documentation and structural changes. |
| Blender validation not automated | Runtime regressions can be missed | Add manual checklist first, then headless checks where possible. |

## Recommended next implementation order

### Phase 1: local validation of modular AI pipeline

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

### Phase 2: regenerate indexes

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Expected refreshed files:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

### Phase 3: review dry-run reports

Inspect:

```text
output/validation/ai_pipeline_modules.json
output/ai_pipeline/dry_run_matrix_report.json
```

Key fields:

```text
passed
summary
schedule
lanes
guardrail_remediation_loop
```

### Phase 4: validate and extend shared utilities

Existing:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/image_sequence.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
```

These do not import `bpy` and should remain testable with normal Python. Next, add focused tests or fixtures before migrating package code.

### Phase 5: add Blender compatibility layer

Create:

```text
Scripting/shared/blender_compat.py
```

Initial target functions:

```text
clear_sequence_editor
create_sound_strip
safe_set_scene_sync_audio
safe_create_node
```

### Phase 6: add package adapters

Only after shared modules are tested:

```text
Scripting/v61b/adapters/
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/adapters/
```

### Phase 7: split NPU orchestration

Refactor later:

```text
Tools/npu/pipeline/config.py
Tools/npu/pipeline/context_builder.py
Tools/npu/pipeline/prompts.py
Tools/npu/pipeline/providers.py
Tools/npu/pipeline/validators.py
Tools/npu/pipeline/artifact_writer.py
Tools/npu/pipeline/runner.py
```

Preserve current CLI behavior while splitting.

## Practical next commit sequence

Recommended next commits after local validation:

```text
chore: regenerate ai and npu indexes
fix(ai): resolve any dry-run matrix failures
docs: record ai pipeline validation results
test(shared): add fixtures for path, json and image sequence helpers
feat(shared): add blender compatibility wrappers
refactor(v61b): add optional shared utility adapters
```

## Do not do yet

Do not do these in the next immediate step:

- do not rewrite `Scripting/v61b/main_v61b.py`;
- do not split the Ready To Jazz script before shared infrastructure is validated;
- do not migrate package imports to `Scripting/shared/` before tests exist;
- do not edit full frame-by-frame analysis JSON files;
- do not collapse generated packages into one folder;
- do not run heavy Blender rendering and GPU model generation at the same time on the current workstation profile;
- do not change schema-v6 report field meanings before dry-run matrix validation.

## Final technical position

The project is in a good state for the next engineering phase.

The best next step is to make the codebase safer before making it more ambitious:

1. validate the modular AI artifact pipeline;
2. regenerate indexes;
3. inspect dry-run reports;
4. keep runtime Blender packages stable;
5. migrate shared utility usage only after tests.

This gives the project a reusable foundation for future generated Blender scenes and for the local AI/NPU/GPU pipeline.
