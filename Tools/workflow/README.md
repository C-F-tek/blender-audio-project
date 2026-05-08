# Workflow Tools

`Tools/workflow/` contains launcher and workflow helper scripts for IA-Carmine.

This directory has one canonical local-AI operator entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Current command ownership lives in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Current code-driven navigation and validation ownership lives in:

```text
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Current doctrine

```text
Full0To10 = TUTTO SU TUTTO
LightFull0To10 = evidence-only profile, not provider/runtime proof
quick/balanced/deep/custom = intensity, not scope
supporting wrappers are implementation lanes, not first entrypoints
provider/probe/workload-quality lanes are opt-out in Full0To10
GPU1/GPU0/NPU peer exchange must enter telemetry, bundle and acceptance evidence
runtime tool telemetry must use normalized statuses and broker-measured elapsed seconds when tools execute
final NPU provider work must not run on the performance-critical close path unless NpuMicroStartMode=final-provider
provider-capable workflow runners prefer IA_CARMINE_PYTHON, then .venv, before system python
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
preferred active runbook/docs size <=400 lines
active Markdown hard threshold <=500 lines
maintained source/script target <=400 lines
limitations are backlog to overcome, not reasons to skip available tools
```

## Operator routing

| Need | Start here |
|---|---|
| Real full product run | `run_unified_local_ai_refactor.ps1` with `-Full0To10`. |
| Single-phase diagnostic | `run_unified_local_ai_refactor.ps1` with `-NoStrictRealRunActivation`. |
| Lightweight evidence profile | `run_unified_local_ai_refactor.ps1 -LightFull0To10`. |
| Markdown-to-review-PR product path | Unified launcher plus patch suggestion/review PR flags; current owner chain below. |
| Full-toolbox internals | `run_agent_review_full_toolbox_decision_loop.py` and packaged engine. |
| Script family census | `docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md`. |
| Source-code behavior map | `docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md`. |

Do not start a normal workflow from an internal helper unless the launcher/runbook explicitly delegates to that helper or the task is a focused tool validation.

## Markdown-to-review-PR product chain

Current owner chain:

```text
docs/LOCAL_AI_TASKS/<task>.md
  -> Tools/ai/build_task_patch_suggestion_report.py
  -> Tools/ai/apply_patch_suggestion_bundle.py
  -> Tools/validation/check_patch_suggestion_product_separation.py
  -> Tools/ai/prepare_review_pr.py
```

Focused chain smoke:

```text
Tools/validation/run_full0to10_product_pr_chain_smoke.py
```

Current limitations:

```text
ReviewPrIncludePath remains supported for explicit/manual allowlists.
prepare_review_pr.py can auto-discover include paths from apply reports with `--auto-include-from-apply-report` plus `--apply-report`.
prepare_review_pr.py does not create draft PRs yet.
```

## Tool classification

| Script | Classification | Notes |
|---|---|---|
| `run_unified_local_ai_refactor.ps1` | canonical-entrypoint | Primary run-unica launcher. Dispatches `-LightFull0To10` profile when selected. |
| `run_unified_light_full0to10_profile.ps1` | evidence-only profile | Dispatches light evidence run and promotion JSON builder. |
| `run_full0to10_light_evidence_only.ps1` | evidence-only supporting lane | Produces light evidence report; no provider execution, patch apply, Blender runtime or FFmpeg runtime. |
| `run_local_validation_after_refactor.ps1` | supporting-tool | Local validation wrapper; not first entrypoint. |
| `run_local_ai_task_via_pipeline.ps1` | launcher-internal/supporting-tool | Official adapter lane. |
| `run_post_validation_ai_packet.ps1` | launcher-internal/supporting-tool | Advisory packet lane. |
| `run_parallel_ai_provider_multistep.ps1` | launcher-internal/supporting-tool | Provider/probe lane. |
| `run_agent_review_full_toolbox_decision_loop.ps1` | thin shell wrapper | Resolves Python and forwards the public CLI without owning orchestration behavior. Legacy PowerShell is explicit fallback only. |
| `run_agent_review_full_toolbox_decision_loop.py` | Python control entrypoint | Preserves the public CLI and runs the packaged Python engine under `run_agent_review_full_toolbox_decision_loop/`. |
| `run_agent_review_full_toolbox_decision_loop/py_engine.py` | Python engine package | Static foundation and top-level phase sequencing. |
| `run_agent_review_full_toolbox_decision_loop/py_mesh.py` | Python engine package | GPU1/GPU0/NPU provider mesh, runtime heap live signals and broker-controlled peer tool execution. |
| `run_agent_review_full_toolbox_decision_loop/py_product.py` | Python engine package | Decision loop, final local AI product, evidence bundle, telemetry, semantic chunks and artifact path policy. |
| `run_agent_review_full_toolbox_decision_loop/py_support.py` | Python engine package | Shared paths, execution helpers and compact artifact stamp generation. |
| `run_agent_review_full_toolbox_decision_loop_integrated.ps1` | supporting selected phase | Not primary operator path. |
| `run_local_ai_markdown_task.ps1` | supporting-tool | Markdown helper; prefer unified launcher. |
| `run_docs_md_refactor_10min.ps1` | legacy-superseded/supporting-tool | Prefer unified launcher `md`/validation phases. |
| `startup_preflight.ps1` | diagnostic-only | Startup/preflight helper. |
| `startup_check.py` | diagnostic-only | Startup check helper. |
| `workflow_shell.py` | gui-or-shell-helper | Interactive helper; not canonical headless flow. |
| `workflow_shell_with_push.py` | unsafe-or-write-capable | Push-capable; explicit user intent required. |
| `git_auto_push.py` | unsafe-or-write-capable | Push behavior requires explicit user intent. |
| `asset_inventory.py` | supporting-tool | Asset inventory helper. |
| `scene_brief.py` | supporting-tool/application-domain | Scene brief helper. |
| `artifact_consult.py` | supporting-tool | Artifact consultation helper. |
| `project_awareness.py` | supporting-tool | Project-awareness context helper. |
| `smart_ai_context.py` | supporting-tool | Smart context helper. |
| `ai_runtime_diagnostics.py` | diagnostic-only | Runtime diagnostics helper. |

## Diagnostic rule

For single-mode diagnostics, use the launcher with `-NoStrictRealRunActivation`. Without that flag, a real non-smoke run may promote to TUTTO SU TUTTO and start provider/GPU/NPU lanes.

## LightFull0To10 behavior

The light profile is a report/evidence profile for fast visibility and promotion planning.

Verified behavior from `run_full0to10_light_evidence_only.ps1`:

```text
kind=full0to10_light_evidence_only_run
provider_execution_performed=false
patch_application_performed=false
blender_runtime_execution_performed=false
ffmpeg_execution_performed=false
```

It may run optional evidence steps. Optional missing scripts are represented as step records and must not be interpreted as silent full-run success.

## Guardrails

Workflow helpers must not silently:

```text
merge to master
force-push or rewrite history
apply patch specs
commit output/**
commit SQLite DB files
run Blender or FFmpeg
produce audio/media output
change provider/model execution semantics
claim provider execution from light evidence-only profiles
claim draft PR support before prepare_review_pr.py implements it
```

Push-capable helpers are not default validation commands and require explicit user intent.

## Full-run handoff rule

When a workflow helper contributes to Full0To10 evidence, recommendations, patch plans or patch specs, its output must be visible through:

```text
launcher manifest
phase_status / phase_reports
runtime tool usage telemetry
runtime/hardware capability manifest
patch notes quality product when selected
patch suggestion product/separation reports when selected
AI peer-exchange report and contract when provider execution is selected
runtime-heap tool catalog exchange before final telemetry
Full0To10 final local AI product package when selected
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/index/discovery/file-line evidence when relevant
generated artifact path policy evidence when long bundle names are possible
```

## Line-budget policy

Maintained workflow scripts and docs must stay under the active line-budget policy.

```text
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Markdown >500 lines -> compact index + <file>.md/part-001.md layout.
Preferred active runbook size -> <=400 lines.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Validator:

```text
Tools/validation/check_file_line_limits.py
```

## Related docs

```text
WORKFLOW.md
docs/WORKFLOW_HELPER_SCRIPTS_POLICY.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```
