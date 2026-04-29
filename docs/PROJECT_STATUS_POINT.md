# Project Status Point

## Purpose

This document records the current technical status of `blender-audio-project` after reviewing the repository structure, documentation, generated indexes, Blender packages, AI/NPU tooling and refactoring direction.

It is intended as a practical checkpoint before starting the next implementation phase.

## Current conclusion

The project is no longer only a Blender scripting experiment. It is now a structured audio-reactive production workspace with:

- root audio-analysis tools;
- Blender scene packages;
- a mature reference workflow under `Scripting/v61b/`;
- one large generated/refined package for the Ready To Jazz/YouTube workflow;
- AI/NPU/GPU-oriented artifact generation tools;
- generated indexes under `indexAI/`;
- documentation for package generation, quality gates and refactoring.

The next correct move is not a broad rewrite. The next correct move is **controlled encapsulation**.

## Project maturity by area

| Area | Current status | Operational meaning |
|---|---|---|
| Audio analysis | usable | Existing root tools can generate analysis and summary data. |
| Blender reference package | strong | `Scripting/v61b/` is the reference architecture. |
| Generated Blender package | usable but heavy | `ready_to_jazz_wow_youtube_profiles_audio_sync` works as a standalone package but is monolithic. |
| Shared utilities | planned | Policy exists; code extraction is still the next implementation step. |
| AI/NPU pipeline | active | There is an additive orchestrator and guardrail direction. |
| NPU/GPU parallelism | conceptually correct | Task-level lanes are defined: CPU parsing, NPU review, GPU heavy generation. |
| Documentation | strong | Current docs now define project direction and safe modification rules. |
| Validation | partial | Quality gate exists, but automated validation is still incomplete. |
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
| `Scripting/shared/` | target layer | Implement first shared modules here. |

### AI/NPU tooling

| Area | Status | Next action |
|---|---|---|
| `Tools/ai/run_parallel_artifact_pipeline.py` | active additive orchestrator | Keep; validate with dry runs and small artifacts. |
| `Tools/npu/run_dual_ai_pipeline.py` | powerful but too large | Split later into config/context/prompts/providers/validators/writers. |
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

### 3. Shared utilities are now the critical missing layer

The project has documentation for `Scripting/shared/`, but the actual implementation is still incomplete.

First shared modules should be pure Python:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/image_sequence.py
```

Then Blender/FFmpeg modules:

```text
Scripting/shared/blender_compat.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
```

### 4. AI/NPU pipeline direction is technically sound

The project is already using the right mental model: task-level parallelism, not splitting one model across devices.

Recommended lane model:

```text
CPU -> parsing, compact artifacts, validation
NPU -> review, scoring, warning detection
GPU -> optional heavy generation
```

This should remain the operational model.

### 5. The project needs validation more than more documentation

Documentation is now strong enough to guide developers and AI systems. The next value is validation:

```text
Tools/validation/check_python_syntax.py
Tools/validation/check_package_structure.py
Tools/validation/check_docs_links.py
Tools/validation/check_json_artifacts.py
```

Later, add Blender-specific validation where feasible.

## Current blockers

| Blocker | Impact | Recommendation |
|---|---|---|
| Shared utilities not implemented | New packages still duplicate logic | Implement pure Python shared modules first. |
| Large monolithic generated script | Harder to maintain and patch | Extract infrastructure before artistic scene logic. |
| AI/NPU pipeline scripts are large | Harder to test and evolve | Split providers, prompts, validators and artifact writers. |
| JSON contracts partial | AI-generated artifacts can drift | Strengthen schema docs and validators. |
| Generated indexes stale after edits | AI context may miss new docs | Regenerate indexes after documentation and structural changes. |
| Blender validation not automated | Runtime regressions can be missed | Add manual checklist first, then headless checks where possible. |

## Recommended next implementation order

### Phase 1: regenerate indexes

After recent documentation changes, regenerate project indexes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Expected refreshed files:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

### Phase 2: implement pure shared utilities

Create:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/image_sequence.py
```

These should not import `bpy` and should be testable with normal Python.

### Phase 3: add validation tools

Create:

```text
Tools/validation/check_python_syntax.py
Tools/validation/check_package_structure.py
Tools/validation/check_json_artifacts.py
```

These will protect the repository before bigger refactors.

### Phase 4: implement FFmpeg/render shared layer

Create:

```text
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
```

Initial target: reproduce command-building behavior without changing existing package encoders.

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

### Phase 7: split AI/NPU orchestration

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

Recommended commit order:

```text
chore: regenerate ai project indexes
feat(shared): add path and json helpers
feat(shared): add image sequence scanner
test: add repository validation scripts
feat(shared): add ffmpeg profile models
feat(shared): add blender compatibility wrappers
refactor(v61b): add optional shared utility adapters
refactor(npu): split dual ai pipeline modules
```

## Do not do yet

Do not do these in the next immediate step:

- do not rewrite `Scripting/v61b/main_v61b.py`;
- do not split the 2197-line Ready To Jazz script before shared infrastructure exists;
- do not migrate package imports to `Scripting/shared/` before tests exist;
- do not edit full frame-by-frame analysis JSON files;
- do not collapse generated packages into one folder;
- do not run heavy Blender rendering and GPU model generation at the same time on the current workstation profile.

## Final technical position

The project is in a good state for the next engineering phase.

The best next step is to make the codebase safer before making it more ambitious:

1. regenerate indexes;
2. add validation scripts;
3. create the first shared utility modules;
4. keep runtime Blender packages stable;
5. migrate only after tests.

This gives the project a reusable foundation for future generated Blender scenes and for the local AI/NPU/GPU pipeline.
