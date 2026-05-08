# Code-driven data flow map — 2026-05-07

Status: active navigation map  
Scope: current IA-Carmine flows from script owners to outputs.

This map is shorter and more operational than `docs/DATA_FLOW.md`. Use it to choose the correct flow variant without getting lost.

## Flow 0: source of truth order

```text
source script
-> code-derived-ai-toolchain-map-2026-05-07.md
-> single-owner-scripts-and-flow-boundaries-2026-05-07.md
-> this data-flow map
-> launcher runbook
-> package README
-> historical evidence only when needed
```

## Flow 1: normal full product run

```text
Task Markdown
-> run_unified_local_ai_refactor.ps1
-> unified manifest
-> Markdown/script/JSON/Python inventories
-> context/chunks/agent-state lanes
-> deterministic foundation
-> provider mesh if selected by Full0To10/strict activation
-> peer exchange and broker results
-> telemetry/capability summaries
-> shared AI-to-AI bundle
-> optional patch suggestion product
-> optional deterministic apply
-> product separation validator for product/apply path
-> optional review PR preparation
```

Owner:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Do not start this flow from internal provider scripts.

## Flow 2: phase diagnostic

```text
Mode selected by operator
-> run_unified_local_ai_refactor.ps1
-> -NoStrictRealRunActivation
-> selected phase only
-> manifest/phase reports
-> no provider/GPU/NPU unless selected mode is provider/full
```

Mandatory diagnostic flags:

```text
-SkipGitSync
-NoBranch
-AllowDirty
-NoStrictRealRunActivation
-Prod
-NoExecutionTail
```

Purpose: isolate `md`, `json`, `python`, `contract`, `chunks`, `context_pack`, `agent_state`, `official`, `patch_specs`, `evidence` without accidental Full0To10 promotion.

## Flow 3: provider mesh

```text
Full0To10/provider selected
-> py_engine.py enters provider stage
-> py_mesh.py builds provider command
-> run_agent_gpu_npu_parallel_orchestrator.py
-> run_agent_gpu_deep_planning_supervised.py for GPU1/Ollama
-> run_gpu0_peer_companion_worker.py for GPU0/OpenVINO support
-> optional/deferred NPU micro support
-> agent_runtime_tool_broker.py for provider tool requests
-> runtime heap events/snapshot
-> provider/peer contracts
-> telemetry and bundle absorption
```

Owners:

```text
py_mesh.py
run_agent_gpu_npu_parallel_orchestrator.py
agent_runtime_tool_broker.py
```

Do not execute provider-requested tools outside the broker.

## Flow 4: deterministic foundation

```text
launcher/full-toolbox engine
-> Python line-count inventory
-> Python syntax validation
-> code interpreter/static report
-> repository consistency map/smoke
-> GPU planner contract smoke
-> deterministic recommendation smoke
-> decision-loop smoke
-> OpenVINO/NPU/provider environment reports
-> megalithic review/refinement when selected
```

Owner:

```text
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_engine.py
```

Purpose: build report-bound evidence before trusting provider suggestions.

## Flow 5: context and memory

```text
source/docs
-> semantic chunks
-> selected chunks
-> AI context pack
-> agent state packet
-> optional SQLite memory surfaces
-> official adapter or provider packet consumers
```

Owners:

```text
Tools/npu/build_semantic_code_chunks.py
Tools/ai/select_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
Tools/ai/build_agent_state_packet.py
```

Policy:

```text
SQLite DB files are local/private.
Generated chunks/indexes are not source docs.
Do not commit output/** or generated chunk folders.
```

## Flow 6: patch suggestion product

```text
Task Markdown and run reports
-> build_task_patch_suggestion_report.py
-> repository_update_suggestions / repository_change_proposals
-> apply_patch_suggestion_bundle.py dry-run
-> essential_patch_suggestion_items
-> supplemental_telemetry_debug_items
-> check_patch_suggestion_product_separation.py
```

Owners:

```text
Tools/ai/build_task_patch_suggestion_report.py
Tools/ai/apply_patch_suggestion_bundle.py
Tools/validation/check_patch_suggestion_product_separation.py
```

Patch notes and proposal ledgers are not source edits until this flow classifies and applies deterministic operations or emits manual-review product suggestions.

## Flow 7: deterministic patch apply

```text
review branch
-> apply_patch_suggestion_bundle.py --apply
-> deterministic operations only
-> changed source/doc files
-> apply report
-> product separation validation when review PR path is selected
-> validation cycle
```

Owner:

```text
Tools/ai/apply_patch_suggestion_bundle.py
```

Guardrails:

```text
no provider execution
no commit
no PR creation
no output/** target edits
no generated chunk/DB/render edits
```

## Flow 8: review PR preparation

```text
review branch
-> patch suggestion product separation has passed or failed explicitly
-> explicit include path list
-> prepare_review_pr.py
-> path policy validation
-> git add allowed paths
-> reject disallowed staged paths
-> commit when requested
-> push when requested
-> gh pr create when requested
-> review_pr_prepare report
```

Owner:

```text
Tools/ai/prepare_review_pr.py
```

Current limits:

```text
include paths are explicit only
no automatic include-path derivation from apply report yet
no --draft PR creation yet
```

## Flow 9: validation and smoke

```text
changed docs/code/scripts
-> focused validator or smoke
-> JSON/MD report under output/validation
-> optional compact evidence under docs/LOCAL_VALIDATION_EVIDENCE
-> git diff --check
```

Owners include:

```text
Tools/validation/check_python_syntax.py
Tools/validation/check_validation_report_contract.py
Tools/validation/check_docs_links.py
Tools/validation/check_file_line_limits.py
Tools/validation/run_patch_suggestion_bundle_apply_smoke.py
Tools/validation/run_agent_runtime_tool_broker_smoke.py
Tools/validation/check_ai_peer_exchange_contract.py
```

Pick the smallest validation cycle that proves the modified flow.

## Flow 10: docs-only update

```text
source code inspection
-> docs update
-> line-budget policy check when relevant
-> docs link validation when local execution is available
-> git diff --check
```

No provider execution required.

## Flow 11: LightFull0To10

```text
launcher -LightFull0To10
-> light evidence-only runner
-> promotion/evidence JSON/MD
-> no provider execution
-> no patch apply
-> no Blender/FFmpeg
```

Owner:

```text
Tools/workflow/run_unified_light_full0to10_profile.ps1
```

Do not cite LightFull0To10 as proof of real provider execution.

## Flow 12: reset planning

```text
launcher reset mode
-> reset candidate report
-> no deletion by default
-> deletion only with exact confirmation
```

Owner:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Deletion requires explicit reset flags and confirmation string.

## Output class map

| Output class | Location | Commit policy |
|---|---|---|
| Source docs | `docs/**`, `README.md`, `Tools/**/README.md` | Commit when reviewed. |
| Source code/scripts | `Tools/**`, app source | Commit when reviewed and validated. |
| Runtime reports | `output/**` | Do not commit. |
| Compact evidence | `docs/LOCAL_VALIDATION_EVIDENCE/**` | Commit selectively when useful. |
| SQLite DB | `*.db`, `*.sqlite`, `*.sqlite3` | Do not commit. |
| Generated chunks/indexes | `indexAI/code_chunks/**`, `indexAI/project_code_chunks/**` | Do not commit unless explicitly requested as generated evidence. |
| Renders/media | `renders/**`, media outputs | Do not commit. |

## Do-not-bypass list

```text
launcher -> do not bypass for normal runs
broker -> do not bypass for provider tool execution
patch suggestion apply -> do not bypass for suggestion source edits
prepare_review_pr -> do not bypass for staging/commit/push/PR creation
validation scripts -> do not replace with ad-hoc unverifiable checks
bundle builders -> do not hand-write production handoff bundles
```
