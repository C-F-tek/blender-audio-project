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
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
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
heap/exchange entry and exit are deterministic boundaries around the dynamic center
patchkit is the preferred deterministic source-write boundary for future long or delicate patch bundles
preferred active runbook/docs size <=400 lines
active Markdown hard threshold <=500 lines
maintained source/script target <=400 lines
limitations are backlog to overcome, not reasons to skip available tools
```

## Operator routing

| Need | Start here |
|---|---|
| Real full product run | `run_unified_real_product_pr.ps1 -TaskFile <md>`; it delegates to `run_unified_local_ai_refactor.ps1` with the complete heap/exchange product lane. |
| Single-phase diagnostic | `run_unified_local_ai_refactor.ps1` with `-NoStrictRealRunActivation`. |
| Lightweight evidence profile | `run_unified_local_ai_refactor.ps1 -LightFull0To10`. |
| Heap/exchange lifecycle product path | Unified launcher with provider/evidence/patch/review lanes selected. |
| Patchkit source-write boundary | `Tools/ai/patchkit/apply_patch_bundle.py` after a reviewed `patch_specs/<bundle>/bundle.json`. |
| Markdown-to-review-PR product path | Unified launcher plus patch specs/review PR flags; current owner chain below. |
| Full-toolbox internals | `run_agent_review_full_toolbox_decision_loop.py` and packaged engine. |
| Script family census | `docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md`. |
| Source-code behavior map | `docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md`. |

Do not start a normal workflow from an internal helper unless the launcher/runbook explicitly delegates to that helper or the task is a focused tool validation.

## Real product PR profile

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_real_product_pr.ps1 `
  -RepoRoot . `
  -TaskFile .\docs\LOCAL_AI_TASKS\my-task.md `
  -RunIntensity custom `
  -BudgetMinutes 10 `
  -MaxRounds 600 `
  -FilesPerRound 6 `
  -MaxContextFiles 3020 `
  -MaxCharsPerFile 7000 `
  -MaxNewTokens 2200 `
  -KeepAlive 15m `
  -ProviderMaxContextChars 14000 `
  -ContextPackMaxTotalChars 72000 `
  -ContextPackMaxFileChars 5000 `
  -AgentStateMaxMemoryChars 28000 `
  -MaxRecommendations 700 `
  -MaxPatchPlans 700 `
  -OfficialAdapterTimeoutSeconds 600 `
  -OpenObserverConsoles `
  -OpenExtendedObserverConsoles `
  -ObserverRefreshSeconds 2 `
  -UseGeneratedPatchSpecs `
  -ReviewPrMaxAppliedPatches 5 `
  -Push `
  -CreatePr `
  -DraftPr
~~~

This profile is the operator-facing path from task Markdown to reviewable PR product. It enables task ingress, heap/exchange, GPU1/GPU0/NPU peer runtime evidence, shared memory, closure audit, patch suggestion/apply report, prepare_review_pr and optional remote PR creation.

The profile owns the architectural lane flags internally and keeps runtime sizing, model, Python, observer and review-PR controls external. Operators should pass task-specific budgets and context limits from the CLI instead of editing the wrapper. Its default NPU micro-start mode is `peer`, so the heap/exchange product lane starts with GPU1/GPU0/NPU as coordinated peers instead of deferring NPU participation.

## Runtime boundary

Current full product path is:

```text
IN
  task Markdown
  RepoPy/PYTHONPATH gate
  inventories/context/agent-state
  workload/capability evidence

LOOP / HEAP / EXCHANGE
  dynamic provider/context/broker/runtime lane cooperation
  runtime state
  public exchange events

OUT
  heap exchange exit product
  concrete deterministic operation candidates
  lifecycle validation
  patchkit or deterministic patch bridge
  review PR product
```

The center is dynamic. Entry and exit are controlled.

## Markdown-to-review-PR product chain

Current owner chain:

```text
docs/LOCAL_AI_TASKS/<task>.md
  -> inventories/context/agent-state/workload-quality
  -> Tools/ai/build_heap_exchange_runtime_entry.py
  -> official adapter/provider/patch-spec lanes
  -> Tools/ai/build_heap_exchange_runtime_exit.py
  -> Tools/validation/check_heap_exchange_runtime_lifecycle.py
  -> Tools/ai/patchkit/apply_patch_bundle.py or deterministic patch suggestion bridge
  -> Tools/ai/prepare_review_pr.py
```

Legacy deterministic suggestion bridge remains available:

```text
Tools/ai/build_task_patch_suggestion_report.py
Tools/ai/apply_patch_suggestion_bundle.py
Tools/validation/check_patch_suggestion_product_separation.py
```

Focused chain smoke:

```text
Tools/validation/run_full0to10_product_pr_chain_smoke.py
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
Tools/validation/run_patchkit_smoke.py
```

Current limitations:

```text
ReviewPrIncludePath remains supported for explicit/manual allowlists.
prepare_review_pr.py can auto-discover include paths from apply reports with `--auto-include-from-apply-report` plus `--apply-report`.
prepare_review_pr.py supports draft PR creation through `--draft-pr` when `--create-pr` and `--push` are selected.
metadata-only patch drafts are not enough for a successful review PR product.
```

## Patchkit bundle procedure

Future patch work should centralize the modification core:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Standard commands:

```powershell
python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Patchkit handles backup, encoding/newlines, dry-run chain state, idempotency, parser checks, compile checks, `git diff --check`, JSON/Markdown reports and line counts.

## Tool classification

| Script | Classification | Notes |
|---|---|---|
| `run_unified_local_ai_refactor.ps1` | canonical-entrypoint | Primary run-unica launcher. Dispatches `-LightFull0To10` profile when selected. |
| `run_unified_real_product_pr.ps1` | product-entrypoint | Operator-facing task-MD to reviewable-PR wrapper; architecture flags internal, runtime controls external. |
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
bypass heap/exchange lifecycle for review PR product paths
bypass patchkit for new long/delicate patch bundles when patchkit can express the change
```

Push-capable helpers are not default validation commands and require explicit user intent.

## Full-run handoff rule

When a workflow helper contributes to Full0To10 evidence, recommendations, patch plans or patch specs, its output must be visible through:

```text
launcher manifest
phase_status / phase_reports
heap/exchange runtime entry
heap/exchange runtime state
heap/exchange runtime exit product
heap/exchange lifecycle report
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
patchkit reports when source writes are applied through patchkit
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
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```

<!-- IA-CARMINE-REAL-PRODUCT-RUNTIME-MESH-BEGIN -->
## Real product runtime mesh contract

The real product profile is not a manually guided chain. The operator provides a task Markdown file, then the run enters the heap/exchange runtime. Inside that dynamic center, GPU1, GPU0, NPU, shared memory, SQLite FTS memory, broker/tool-agnostic capabilities and deterministic script lanes cooperate as peers and evidence producers.

Required route:

- Task MD IN
- heap/exchange activation
- GPU1 primary advisory
- GPU0 OpenVINO/tool workload
- NPU peer micro lane
- shared memory / SQLite FTS / tool broker / direct reasoning assistance
- static deterministic script/product lane
- heap/exchange CLOSE
- product readiness
- prepare_review_pr.py
- PR finale testabile

Static gate:

- `Tools/validation/check_real_product_runtime_mesh_contract.py`
- `Tools/validation/run_real_product_runtime_mesh_contract_smoke.py`

The gate is deterministic. It does not run providers, does not apply patches, does not run Blender/FFmpeg and does not write source products. Its job is to fail early when the real product profile stops wiring one of the intrinsic project capabilities into the final review-PR path.
<!-- IA-CARMINE-REAL-PRODUCT-RUNTIME-MESH-END -->

Full product PR chain gate:

- `Tools/validation/run_full0to10_product_pr_chain_smoke.py` now runs the real product runtime mesh contract before the deterministic product PR chain smoke.
- A full product chain smoke is not considered valid unless the static mesh contract passes first.
- This keeps Task MD ingress, heap/exchange activation, GPU1/GPU0/NPU peer lanes, shared memory, SQLite FTS, tool broker, direct reasoning assistance, static deterministic product lane, heap/exchange close and review PR readiness tied to the final PR product.

<!-- IA-CARMINE-REAL-PRODUCT-PREFLIGHT-GATE-BEGIN -->
## Real product preflight gate

Before launching a real product run, execute the deterministic preflight gate:

- `Tools/validation/run_real_product_preflight_gate.py`
- `Tools/validation/run_real_product_preflight_gate_smoke.py`

The preflight gate runs profile, intrinsic capability, runtime mesh, review PR args, review PR readiness and full product PR chain smokes. It does not execute providers, does not apply patches, does not run Blender/FFmpeg and does not write source products.

It is the safe static readiness gate before entering the dynamic heap/exchange runtime.
<!-- IA-CARMINE-REAL-PRODUCT-PREFLIGHT-GATE-END -->

<!-- IA-CARMINE-MANDATORY-PREFLIGHT-BEGIN -->
## Mandatory real product preflight

The real product wrapper always runs `Tools/validation/run_real_product_preflight_gate.py` before delegating to the heap/exchange launcher.

There is no skip switch for this gate. A failed preflight stops the run before provider activity, patch application, Blender/FFmpeg execution or review-PR preparation.

The provider surface checked by the runtime mesh contract includes Ollama/GPU1 advisory wiring, OpenVINO/GPU0 workload wiring, NPU peer micro lane, SQLite FTS memory, broker/tool-agnostic execution, direct reasoning assistance, static deterministic product lane, heap/exchange close and final review PR readiness.
<!-- IA-CARMINE-MANDATORY-PREFLIGHT-END -->
