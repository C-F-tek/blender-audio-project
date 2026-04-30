# Project AI Consciousness

## Purpose

This document is the compact operational memory of `blender-audio-project` for AI agents and future development sessions.

It describes what the project is, what must be preserved, what is currently mature, what is risky, and how an AI system should reason before changing files.

## Project identity

`blender-audio-project` is currently an audio-reactive Blender production workspace, but its AI tooling is being shaped toward a more general pattern:

```text
input data or project context
  -> technical/context analysis
  -> AI plan, scene brief, spec or implementation draft
  -> generated artifact for a target application/runtime
  -> validation/reporting
  -> controlled execution/export only when explicitly validated
```

Current main concrete flow:

```text
audio file
  -> technical analysis JSON
  -> compact track/music context
  -> AI scene brief or scene specification
  -> Blender Python package or generated Blender script
  -> rendered frame sequence
  -> FFmpeg encoded video
```

Do not confuse the current concrete flow with the architectural boundary. The validation and policy work must stay input-agnostic and output-application-agnostic wherever possible.

## Architecture Boundary — Input-Agnostic / Output-Application-Agnostic

This is a fixed project rule for the reusable AI pipeline and generated-artifact validation work:

```text
not Blender-only
not WAV/audio-only
input-agnostic
output-application-agnostic
current execution assumption: target applications accept generated Python scripts
future extension: other runtimes, other application APIs and other input data families
```

Reason:

```text
Blender is the current real application target, but it is not the architectural limit.
WAV/audio is the current real input family, but it is not the architectural limit.
```

Interpretation:

```text
input-domain logic answers: what kind of data is being analyzed?
output-application logic answers: which app/runtime will execute or consume the generated artifact?
generated Python script policy answers: is the generated Python safe/compatible for that target app?
```

Current concrete adapter:

```text
Tools/validation/generated_file_policy.py
  -> Tools/validation/check_generated_artifact_path_policy.py
  -> Tools/validation/check_generated_blender_script_policy.py
```

Future adapters must preserve this boundary. Do not bake WAV/audio assumptions into generic policy, and do not bake Blender assumptions into non-Blender application adapters.

## Current technical state

| Area | Status | Notes |
|---|---|---|
| Root audio tools | usable | `analyze_wav.py`, `build_track_summary.py`, `normalize_scene_spec.py`. These are current input-domain tools, not the architectural limit. |
| `Scripting/v61b/` | stable reference | Current high-quality Blender reference package. Do not destructively refactor. |
| Ready To Jazz package | usable but monolithic | Good production/generation experiment; not yet reusable architecture. |
| `Scripting/shared/` | active foundation | Pure Python helpers exist for path, JSON, image sequence, FFmpeg commands and render profiles; `blender_compat.py` passed a Blender 5.1.1 no-render smoke for frame range, noise node and VSE audio strip creation. |
| `Tools/validation/` | active foundation | Non-invasive validators exist for syntax, docs, JSON artifacts, AI pipeline, dry-run matrix report contract, model JSON parsing, agent memory, generated artifact path policy, Blender shared compatibility and generated Blender script policy. |
| `Tools/validation/generated_file_policy.py` | active foundation | Generic generated-file policy engine. It must remain independent from WAV/audio input and independent from the output application. |
| `Tools/validation/check_generated_artifact_path_policy.py` | generic artifact destination guardrail | Validates proposed generated artifact destinations without knowing the input domain or output application. |
| `Tools/validation/check_generated_blender_script_policy.py` | first adapter | First application-specific adapter for generated Python scripts executed by Blender. Blender is not the generic boundary. |
| `Tools/validation/check_ai_dry_run_matrix_contract.py` | report contract validator | Validates `output/ai_pipeline/dry_run_matrix_report.json` without running the matrix or modifying generated artifacts. |
| `Tools/ai/model_json.py` | active foundation | Reusable deterministic parser for JSON-like model outputs. Ollama response parsing delegates to it while preserving legacy `json.JSONDecodeError` behavior. |
| `Tools/ai/pipeline/` | modularized and locally validated | AI artifact pipeline is split into focused modules with a thin entrypoint, dry-run matrix, Markdown report and machine-readable status marker. |
| `Tools/ai/agent_state.py` | initial foundation | Generic memory and microtask packet model for task-local agent state, persistent memory inputs and non-blocking CPU/NPU/GPU lane planning. |
| `Tools/ai/agent_memory_policy.py` | initial foundation | Deterministic retention, quarantine and promotion-candidate policy for generic agent memory. |
| `Tools/workflow/` | active foundation | Contains unattended local validation runner. |
| `Tools/ai/` and `Tools/npu/` | active pipeline | AI/NPU context, review and artifact generation tooling. |
| `indexAI/` | generated context | Regenerate after structural changes. Do not hand-refactor as source. |
| `patch_specs/` | advanced patch queue | JSON patch specs can be applied manually or by GitHub Action. |
| `docs/EXECUTION_PLANS/` | active foundation | Durable task records for multi-step work. |
| Documentation | strong | Use docs as project contract. |

## Files and folders to understand first

```text
AGENTS.md
WORKFLOW.md
README.md
docs/README.md
docs/PROJECT_AI_CONSCIOUSNESS.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/AI_MEMORY_POLICY.md
docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
docs/AI_EXTERNAL_KNOWLEDGE.md
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
docs/EXECUTION_PLANS/README.md
docs/TECH_DEBT_TRACKER.md
docs/MODULE_MAP.md
docs/DATA_FLOW.md
docs/REFACTORING_AND_REUSE_PLAN.md
docs/QUALITY_GATE.md
docs/SHARED_SCRIPTING_UTILITIES.md
docs/PROJECT_STATUS_POINT.md
docs/PATCH_SPEC_WORKFLOW.md
docs/EXECUTION_PLANS/active/2026-04-29_json_parser_utility_review.md
docs/EXECUTION_PLANS/active/2026-04-29_formal_json_schema_validation.md
docs/EXECUTION_PLANS/active/2026-04-29_generated_file_policy_blender_first.md
docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md
Scripting/README.md
Scripting/v61b/README.md
Scripting/shared/README.md
Tools/validation/README.md
patch_specs/README.md
```

## Runtime preservation rules

These areas are sensitive:

```text
Scripting/v61b/
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/
output full frame-level JSON files
render output paths
FFmpeg command behavior
Blender audio/frame sync behavior
```

Do not modify these casually.

## Current direction

The active architectural direction is:

```text
working package code
  -> additive shared utility or generic validator
  -> local validation
  -> optional adapter
  -> controlled migration
```

Do not start by rewriting working Blender packages.

When a concept may be reused outside Blender or outside audio/WAV inputs, split it into:

```text
generic core
  -> generated Python/script policy concepts when applicable
  -> application-specific adapter
  -> optional input-domain validator
  -> report
```

Current example:

```text
Tools/validation/generated_file_policy.py
  -> Tools/validation/check_generated_artifact_path_policy.py
  -> Tools/validation/check_generated_blender_script_policy.py
```

This means:

```text
WAV/audio analysis is one input-domain adapter family
Blender is one output-application adapter family
Python scripting is the first generated-output execution style
```

## Durable task control

The project now uses explicit workflow and task-control files:

```text
WORKFLOW.md
docs/EXECUTION_PLANS/README.md
docs/EXECUTION_PLANS/active/
docs/EXECUTION_PLANS/completed/
docs/EXECUTION_PLANS/abandoned/
docs/TECH_DEBT_TRACKER.md
```

Use execution plans for multi-step work involving source code, shared utilities, generic policy engines, AI pipeline behavior, Blender package migration, GitHub workflow changes or validation/debug cycles.

Use the technical debt tracker when a known issue is real but not fixed immediately.

## External AI engineering knowledge

OpenAI Harness Engineering and Symphony concepts have been adapted into:

```text
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
docs/AI_EXTERNAL_KNOWLEDGE.md
```

Adopted principles:

```text
AGENTS.md as short index, not encyclopedia
docs/ as versioned project knowledge
validators and dry-runs as mechanical guardrails
Markdown/JSON reports as proof of work
workflow files as operational control plane
small scoped tasks over broad rewrites
execution plans and tech-debt tracking as drift control
```

## AI artifact pipeline status

The AI artifact pipeline refactor is locally validated.

Read before changing pipeline code:

```text
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
Tools/ai/pipeline/refactor_status.py
```

Current module family:

```text
Tools/ai/run_parallel_artifact_pipeline.py
Tools/ai/run_pipeline_dry_run_matrix.py
Tools/ai/model_json.py
Tools/ai/pipeline/defaults.py
Tools/ai/pipeline/models.py
Tools/ai/pipeline/runner.py
Tools/ai/pipeline/compat.py
Tools/ai/pipeline/artifact_contracts.py
Tools/ai/pipeline/cli.py
Tools/ai/pipeline/preflight.py
Tools/ai/pipeline/steps.py
Tools/ai/pipeline/scheduler.py
Tools/ai/pipeline/orchestrator.py
Tools/ai/pipeline/schema_report.py
Tools/ai/pipeline/markdown_report.py
Tools/ai/pipeline/guardrail_models.py
Tools/ai/pipeline/remediation.py
Tools/ai/pipeline/refactor_status.py
```

Validated locally before this TD-006 branch:

```text
Python syntax validation: PASS
AI model JSON parser validation: PASS
AI pipeline module smoke validation: PASS
AI pipeline dry-run matrix: PASS
Agent memory policy validation: PASS
Generated Blender script policy sample validation: PASS
Package structure validation: PASS
JSON artifact validation: PASS
Project AI index generation: PASS
NPU code context generation: PASS
```

TD-006 adds a new report-contract validator. Its local validation remains pending until the dry-run matrix report exists in the workstation workspace.

The dry-run matrix writes both JSON and Markdown:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix_report.md
```

The dry-run matrix contract validator reads the JSON report only:

```powershell
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
```

## Implemented shared foundation

Current shared modules:

| Module | Role |
|---|---|
| `Scripting/shared/path_utils.py` | Project root, file/directory checks, relative path helpers. |
| `Scripting/shared/json_io.py` | UTF-8 JSON read/write and small validation helpers for clean project JSON files. |
| `Scripting/shared/image_sequence.py` | Frame scan, contiguous sequence detection, FFmpeg pattern generation. |
| `Scripting/shared/ffmpeg_encoder.py` | Package-agnostic FFmpeg command building and dry-run execution helper. |
| `Scripting/shared/render_profiles.py` | Reusable encode profile definitions for YouTube-oriented output. |
| `Scripting/shared/blender_compat.py` | Blender-aware compatibility wrappers for VSE strips, frame range, FPS and node compatibility; validated by no-render smoke but not yet adopted by runtime packages. |

Current AI/generic validation foundations:

| Module | Role |
|---|---|
| `Tools/ai/model_json.py` | Deterministic parser for JSON-like model output. |
| `Tools/validation/generated_file_policy.py` | Generic policy primitives for generated file validation. Input-agnostic and application-agnostic. |
| `Tools/validation/check_generated_artifact_path_policy.py` | Generic destination validator for generated artifact paths. |
| `Tools/validation/check_generated_blender_script_policy.py` | Blender-specific generated Python script policy adapter. |
| `Tools/validation/check_ai_dry_run_matrix_contract.py` | Dry-run matrix report contract validator. Does not execute matrix cases. |

Next shared candidates:

```text
Scripting/shared/config_model.py
Scripting/shared/diagnostics.py
additional generated Python script policy adapters only after one-at-a-time validation
input-domain validators separate from output-application validators
```

## Implemented validation foundation

Current validators:

| Tool | Role |
|---|---|
| `Tools/validation/check_python_syntax.py` | Compiles Python files without importing them. |
| `Tools/validation/check_package_structure.py` | Inspects Blender package folders under `Scripting/`. |
| `Tools/validation/check_json_artifacts.py` | Checks JSON parseability without rewriting artifacts; accepts UTF-8 with or without BOM. |
| `Tools/validation/check_ai_pipeline_modules.py` | Smoke-checks modular AI pipeline imports, step builders, preflight and report generation without heavy workloads. |
| `Tools/validation/check_ai_model_json.py` | Validates reusable model-output JSON parser and Ollama legacy wrapper behavior. |
| `Tools/validation/check_ai_dry_run_matrix_contract.py` | Validates the AI dry-run matrix report contract without running the matrix. |
| `Tools/validation/check_refactor_status_consistency.py` | Checks that duplicated AI pipeline refactor status remains consistent across docs and code. |
| `Tools/validation/check_docs_links.py` | Checks internal documentation links after doc changes. |
| `Tools/validation/check_agent_memory_policy.py` | Checks local agent memory policy and optional generated memory DB state. |
| `Tools/validation/check_blender_shared_compat_smoke.py` | Runs a Blender no-render compatibility smoke when Blender is available. |
| `Tools/validation/check_generated_blender_script_policy.py` | Validates the first generated Python script policy adapter for Blender using reusable generated-file rules. |

Preferred local validation:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

Generic agent state packet smoke:

```powershell
python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Plan generic generated Python validation" --include-file .\docs\QUALITY_GATE.md --include-file .\Tools\validation\README.md
```

Optional persistent memory can use SQLite without external dependencies:

```powershell
python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Plan generic generated Python validation" --memory-db .\indexAI\agent_memory\agent_memory.sqlite --save-inputs-to-memory-db --memory-note "Keep input-domain policy separate from output-application policy."
```

Memory retention and promotion review:

```powershell
python .\Tools\ai\review_agent_memory.py --repo-root .
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
```

Blender shared compatibility smoke:

```powershell
python .\Tools\validation\check_blender_shared_compat_smoke.py --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
```

Generated Blender script policy smoke:

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

Unattended validation runner:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
```

Do not add new validators to the unattended runner until they have remained cheap and deterministic across at least one local validation cycle.

## Generated index policy

After documentation or structural changes, regenerate:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Expected generated files:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

If only these files changed after regeneration, that is expected.

## Patch-spec capability

The repository contains an advanced patch runner:

```text
Tools/repo_patch_runner/apply_repo_mods.py
patch_specs/inbox/
patch_specs/applied/
.github/workflows/apply_repo_mods.yml
```

Use it for small, mechanical, reviewable edits.

Capabilities:

- dry-run;
- exact replacement;
- regex replacement;
- insert before/after anchor;
- path safety checks;
- before/after content validation;
- optional backup;
- line count summary;
- optional git diff display;
- GitHub Action queue through `patch_specs/inbox/*.json`.

## High-priority next tasks

1. Validate the newly aligned documentation and regenerate AI/NPU indexes.
2. Keep generated Python script policy input-agnostic and application-agnostic; Blender remains only the first adapter.
3. Add generated Blender script policy to the local workflow only after another stable validation cycle.
4. Complete `TD-006` with local dry-run matrix report contract validation.
5. Continue `TD-010` only after schema/report contracts remain stable; do not inject agent packets into prompts yet.
6. Select one non-critical `Scripting/shared/blender_compat.py` call-site pilot only after confirming the no-render smoke result on the workstation.
7. Open the `TD-007` NPU pipeline decomposition plan before splitting orchestration files into config, context builder, prompts, provider adapter, validators, artifact writer and runner.
8. Keep `TD-001` PowerShell runner compatibility under review when changing validation commands.
9. Evaluate CI/GitHub Actions only after the local runner remains stable and the intended checks are cheap, deterministic and non-rendering.

## Avoid now

Do not do these without explicit instruction:

```text
rewrite Scripting/v61b/main_v61b.py
split Ready To Jazz monolithic script
remove v61b_backgood before checking if it contains unique fixes
change Blender render behavior
change final FFmpeg output behavior
add dependencies without validation
modify generated full analysis JSON files
run long Blender renders or GPU generation automatically
change AI pipeline schema-v6 field meanings without local dry-run matrix validation
mass-migrate runtime packages to Scripting/shared/blender_compat.py
add AI GitHub Actions that call paid or external model APIs automatically
use prompt-based repair for JSON parsing as a default path
turn generic generated-file policy into Blender-only or WAV-only logic
mix input-domain validators with output-application validators without a clear adapter boundary
```

## Reporting format for AI agents

Every implementation response should include:

```text
changed files
purpose
resulting line count for every created or modified script
validation commands run
validation result
risks
next recommended action
```

## Mental model

The project should be treated as a production pipeline, not a demo.

Correct posture:

```text
stability first
small patches
generic utility before adapter
input-domain logic separate from output-application logic
shared utilities before migration
validation before commit
indexes regenerated after structure changes
proof-of-work reports for agentic work
execution plans for multi-step work
technical debt tracked instead of rediscovered
```
