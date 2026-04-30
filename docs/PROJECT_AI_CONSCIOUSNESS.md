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
  -> Tools/validation/generated_python_policy.py
  -> Tools/validation/check_generated_python_policy.py
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
| `Tools/validation/` | active foundation | Non-invasive validators exist for syntax, docs, JSON artifacts, AI pipeline, NPU helper package, dry-run matrix report contract, model JSON parsing, agent memory, generated Python policy, generated artifact path policy, Blender shared compatibility and generated Blender script policy. |
| `Tools/validation/generated_file_policy.py` | active foundation | Generic generated-file policy engine. It must remain independent from WAV/audio input and independent from the output application. |
| `Tools/validation/generated_python_policy.py` | active foundation | Generic generated Python syntax and hazard policy. It stays independent from input domains and target applications. |
| `Tools/validation/check_generated_python_policy.py` | generic generated Python guardrail | Validates generated Python concepts with deterministic samples and optional script paths before application-specific adapters. |
| `Tools/validation/check_generated_artifact_path_policy.py` | generic artifact destination guardrail | Validates proposed generated artifact destinations and can scan JSON reports with `--artifact-report` without knowing the input domain or output application. |
| `Tools/validation/check_generated_blender_script_policy.py` | first application adapter | Composes generic generated Python policy with Blender-specific generated-script rules. Blender is not the generic boundary. |
| `Tools/validation/check_ai_dry_run_matrix_contract.py` | report contract validator | Validates `output/ai_pipeline/dry_run_matrix_report.json` without running the matrix or modifying generated artifacts. |
| `Tools/validation/check_npu_pipeline_modules.py` | NPU helper smoke validator | Imports and contract-checks app-agnostic NPU helper modules without Blender, NPU, GPU, Ollama, FFmpeg or provider execution. |
| `Tools/validation/check_npu_pipeline_helper_tests.py` | NPU helper unit-test report | Runs deterministic unit tests for helper contracts and emits a validation report. |
| `Tools/validation/check_npu_pipeline_docs.py` | NPU helper docs validator | Checks `Tools/npu/pipeline/README.md` against expected helper modules and terms. |
| `Tools/ai/model_json.py` | active foundation | Reusable deterministic parser for JSON-like model outputs. Ollama response parsing delegates to it while preserving legacy `json.JSONDecodeError` behavior. |
| `Tools/ai/pipeline/` | modularized and locally validated | AI artifact pipeline is split into focused modules with a thin entrypoint, dry-run matrix, Markdown report and machine-readable status marker. |
| `Tools/npu/pipeline/` | active staged foundation | App-agnostic helper package for NPU pipeline decomposition. It contains pure helpers, fixtures, validators, planned-only provider descriptors and migration-readiness gates; runtime wiring into `run_dual_ai_pipeline.py` is still pending local validation. |
| `Tools/ai/agent_state.py` | initial foundation | Generic memory and microtask packet model for task-local agent state, persistent memory inputs and non-blocking CPU/NPU/GPU lane planning. |
| `Tools/ai/agent_memory_policy.py` | initial foundation | Deterministic retention, quarantine and promotion-candidate policy for generic agent memory. |
| `Tools/workflow/` | active foundation | Contains unattended local validation runner and focused NPU helper validation runner. |
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
docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md
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
docs/EXECUTION_PLANS/active/2026-04-30_npu_pipeline_decomposition_plan.md
Scripting/README.md
Scripting/v61b/README.md
Scripting/shared/README.md
Tools/npu/pipeline/README.md
Tools/validation/README.md
patch_specs/README.md
```

## Runtime preservation rules

These areas are sensitive:

```text
Scripting/v61b/
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/
Tools/npu/run_dual_ai_pipeline.py runtime behavior
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

Current examples:

```text
Tools/validation/generated_file_policy.py
  -> Tools/validation/generated_python_policy.py
  -> Tools/validation/check_generated_artifact_path_policy.py
  -> Tools/validation/check_generated_blender_script_policy.py

Tools/npu/pipeline/
  -> pure helper contracts
  -> focused smoke/unit/docs validation
  -> migration-readiness gates
  -> future runtime wiring only after local validation and index regeneration
```

This means:

```text
WAV/audio analysis is one input-domain adapter family
Blender is one output-application adapter family
Python scripting is the first generated-output execution style
NPU/Ollama provider execution is a runtime adapter concern, not a helper-contract concern
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

Validated locally before the active NPU helper batch:

```text
Python syntax validation: PASS
AI model JSON parser validation: PASS
AI pipeline module smoke validation: PASS
AI pipeline dry-run matrix: PASS
AI dry-run matrix report contracts: PASS after PR #38/#39/#40 sequence when maintainer reported green
Agent memory policy validation: PASS
Generated Blender script policy sample validation: PASS
Package structure validation: PASS
JSON artifact validation: PASS
Project AI index generation: PASS
NPU code context generation: PASS
```

The active NPU helper batch local validation remains pending until the maintainer runs:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

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
| `Tools/validation/generated_python_policy.py` | Generic generated Python syntax and hazard policy for application adapters. |
| `Tools/validation/check_generated_python_policy.py` | CLI smoke for the generic generated Python policy layer. |
| `Tools/validation/check_generated_artifact_path_policy.py` | Generic destination validator for generated artifact paths. |
| `Tools/validation/check_generated_blender_script_policy.py` | Blender-specific generated Python script policy adapter composed over the generic Python layer. |
| `Tools/validation/check_ai_dry_run_matrix_contract.py` | Dry-run matrix report contract validator. Does not execute matrix cases. |
| `Tools/validation/check_npu_pipeline_modules.py` | NPU helper module smoke validator. Does not execute provider/runtime calls. |
| `Tools/validation/check_npu_pipeline_helper_tests.py` | NPU helper unit-test report wrapper. |
| `Tools/validation/check_npu_pipeline_docs.py` | NPU helper documentation/module alignment validator. |

Next shared candidates:

```text
Scripting/shared/config_model.py
Scripting/shared/diagnostics.py
additional generated Python script policy adapters only after one-at-a-time validation
input-domain validators separate from output-application validators
runtime wiring from Tools/npu/pipeline/ to Tools/npu/run_dual_ai_pipeline.py after focused validation and regenerated indexes
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
| `Tools/validation/check_generated_python_policy.py` | Validates generic generated Python syntax and warning policy without application assumptions. |
| `Tools/validation/check_generated_blender_script_policy.py` | Validates the first generated Python script policy adapter for Blender by composing generic Python rules with Blender rules. |
| `Tools/validation/check_npu_pipeline_modules.py` | Checks app-agnostic NPU helper imports, contracts, compatibility aliases and readiness gates. |
| `Tools/validation/check_npu_pipeline_helper_tests.py` | Runs deterministic unit tests for NPU helper modules and emits a JSON validation report. |
| `Tools/validation/check_npu_pipeline_docs.py` | Checks NPU helper README/module alignment. |

Preferred local validation:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python .\Tools\validation\check_npu_pipeline_docs.py --repo-root . --output .\output\validation\npu_pipeline_docs.json
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
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
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
```

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

Unattended validation runner:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
```

Add new validators to the unattended runner only after focused smoke validation shows they are cheap, deterministic and non-rendering.

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

1. Validate the active NPU helper batch locally using the focused helper runner and the full local validation runner.
2. Regenerate AI/NPU indexes after the NPU helper batch validation.
3. If the batch is green, merge it and start a narrow runtime-wiring phase for IO helpers only.
4. Keep generated Python script policy input-agnostic and application-agnostic; Blender remains only the first adapter.
5. Continue formal JSON/report contracts without changing existing schema-v6 field meanings.
6. Continue `TD-010` only after schema/report contracts remain stable; do not inject agent packets into prompts yet.
7. Select one non-critical `Scripting/shared/blender_compat.py` call-site pilot only after confirming the no-render smoke result on the workstation.
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
wire Tools/npu/pipeline/ helpers into Tools/npu/run_dual_ai_pipeline.py before focused validation, full validation and index regeneration
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
