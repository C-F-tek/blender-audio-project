# Workflow Tools

`Tools/workflow/` contains launcher and workflow helper scripts for IA-Carmine.

This directory currently has two canonical entrypoints with different ownership:

```text
Tools/workflow/run_unified_real_product_pr.ps1
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Use `run_unified_real_product_pr.ps1` for the operator-facing real product path: Task MD or `-ProcessGateTask` in, mandatory preflight, heap/exchange universe, generated patch specs, product validation and draft review PR out.

Use `run_unified_local_ai_refactor.ps1` as the internal unified launcher and for focused diagnostics. For single-phase diagnostics, pass `-NoStrictRealRunActivation`.

Current command ownership lives in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
```

Current code-driven navigation, validation and hygiene ownership lives in:

```text
docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
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
Real product run = one wrapper entry, one dynamic heap/exchange center, one validated review-PR product exit
run_unified_real_product_pr.ps1 = operator-facing product entrypoint
run_unified_local_ai_refactor.ps1 = unified launcher / dynamic heap-exchange executor
quick/balanced/deep/custom = intensity, not scope
supporting wrappers are implementation lanes, not first entrypoints
provider/probe/workload-quality lanes are opt-out in real unified product runs
GPU1/GPU0/NPU peer exchange must enter telemetry, bundle and acceptance evidence
GPU1/Ollama advisory must consume current-stamp runtime evidence when available
GPU0 OpenVINO lane must be observable workload/support evidence, not only device presence
NPU is peer micro/diagnostic/report lane until a compute-provider lane is validated
runtime tool telemetry must use normalized statuses and broker-measured elapsed seconds when tools execute
final NPU provider work must not run on the performance-critical close path unless NpuMicroStartMode=final-provider
provider-capable workflow runners prefer IA_CARMINE_PYTHON, then .venv, before system python
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
heap/exchange entry and exit are deterministic boundaries around the dynamic center
patchkit is the preferred deterministic source-write boundary for future long or delicate patch bundles
generated patch specs must produce concrete deterministic operations for product PR application
metadata-only generated patch specs with --apply are a hard failure, not a reviewable product
preferred active runbook/docs size <=400 lines
active Markdown hard threshold <=500 lines
maintained source/script target <=400 lines
limitations are backlog to overcome, not reasons to skip available tools
```

## Operator routing

| Need | Start here |
|---|---|
| Real full product run | `run_unified_real_product_pr.ps1 -ProcessGateTask` or `-TaskFile <md>`; it performs mandatory preflight and delegates to `run_unified_local_ai_refactor.ps1` with the complete heap/exchange product lane. |
| Single-phase diagnostic | `run_unified_local_ai_refactor.ps1` with `-NoStrictRealRunActivation`. |
| Heap/exchange lifecycle product path | Real product wrapper or unified launcher with provider/evidence/patch/review lanes selected. |
| Patchkit source-write boundary | `Tools/ai/patchkit/apply_patch_bundle.py` after a reviewed `patch_specs/<bundle>/bundle.json`. |
| Markdown-to-review-PR product path | Real product wrapper plus generated patch specs/review PR flags; current owner chain below. |
| Full-toolbox internals | `run_agent_review_full_toolbox_decision_loop.py` and packaged engine. |
| Script family census | `docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md`. |
| Source-code behavior map | `docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md`. |

Do not start a normal workflow from an internal helper unless the launcher/runbook explicitly delegates to that helper or the task is a focused tool validation.

## Real product PR profile

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_real_product_pr.ps1 `
  -RepoRoot . `
  -ProcessGateTask `
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
  -PreflightTimeoutSeconds 180 `
  -OpenObserverConsoles `
  -OpenExtendedObserverConsoles `
  -ObserverRefreshSeconds 2 `
  -UseGeneratedPatchSpecs `
  -ReviewPrMaxAppliedPatches 5 `
  -Push `
  -CreatePr `
  -DraftPr
~~~

This profile is the operator-facing path from task Markdown or generated process-gate task to reviewable PR product. It enables mandatory preflight, task ingress, heap/exchange, GPU1/GPU0/NPU peer runtime evidence, shared memory, closure audit, patch suggestion/apply report, runtime evidence correlation, prepare_review_pr and optional remote draft PR creation.

The profile owns the architectural lane flags internally and keeps runtime sizing, model, Python, observer and review-PR controls external. Operators should pass task-specific budgets and context limits from the CLI instead of editing the wrapper. Its default NPU micro-start mode is `peer`, so the heap/exchange product lane starts with GPU1/GPU0/NPU as coordinated peers instead of deferring NPU participation.

## Runtime boundary

Current full product path is:

```text
IN
  task Markdown or generated process-gate task
  RepoPy/PYTHONPATH gate
  mandatory real-product preflight
  inventories/context/agent-state
  workload/capability evidence

LOOP / HEAP / EXCHANGE
  dynamic provider/context/broker/runtime lane cooperation
  GPU1/Ollama advisory
  GPU0 OpenVINO observable support workload
  NPU micro peer diagnostic/report lane
  runtime state
  public exchange events

OUT
  heap exchange exit product
  generated patch specs
  concrete deterministic operation candidates
  lifecycle validation
  runtime evidence correlation
  patchkit or deterministic patch bridge
  prepare_review_pr.py
  review PR product
```

The center is dynamic. Entry and exit are controlled.

## Markdown-to-review-PR product chain

Current owner chain:

```text
run_unified_real_product_pr.ps1
  -> docs/LOCAL_AI_TASKS/<task>.md or output/local_ai_task_inputs/<generated-task>.md
  -> mandatory preflight
  -> run_unified_local_ai_refactor.ps1
  -> inventories/context/agent-state/workload-quality
  -> Tools/ai/build_heap_exchange_runtime_entry.py
  -> official adapter/provider/patch-spec lanes
  -> Tools/ai/build_heap_exchange_runtime_exit.py
  -> Tools/validation/check_heap_exchange_runtime_lifecycle.py
  -> Tools/ai/build_repository_change_proposals.py
  -> Tools/ai/build_patch_specs_from_proposals.py
  -> Tools/ai/apply_generated_patch_specs_for_review_pr.py
  -> Tools/ai/prepare_review_pr.py
  -> Tools/validation/check_review_pr_final_product_contract.py
```

Legacy deterministic suggestion bridge remains available:

```text
Tools/ai/build_task_patch_suggestion_report.py
Tools/ai/apply_patch_suggestion_bundle.py
Tools/validation/check_patch_suggestion_product_separation.py
```

Focused chain smoke:

```text
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
Tools/validation/run_patchkit_smoke.py
Tools/validation/run_repository_change_proposals_runtime_evidence_smoke.py
Tools/validation/run_generated_patch_specs_empty_product_smoke.py
```

Current limitations and hard gates:

```text
ReviewPrIncludePath remains supported for explicit/manual allowlists.
prepare_review_pr.py can auto-discover include paths from apply reports with `--auto-include-from-apply-report` plus `--apply-report`.
prepare_review_pr.py supports draft PR creation through `--draft-pr` when `--create-pr` and `--push` are selected.
metadata-only patch drafts are not enough for a successful review PR product.
operation_count=0 under generated patch-spec --apply is a hard failure.
P-NEXT-NPU-OBSERVABILITY is fallback/backlog, not final success when runtime peer evidence exists.
P-RUNTIME-PEER-EVIDENCE-FEED is the expected proposal when runtime evidence exists but prior generated product was metadata-only.
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
| `run_unified_real_product_pr.ps1` | canonical-product-entrypoint | Operator-facing task-MD/process-gate to reviewable-PR wrapper; mandatory preflight first, architecture flags internal, runtime controls external. |
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
| `run_local_ai_markdown_task.ps1` | supporting-tool | Markdown helper; prefer unified launcher or real product wrapper. |
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


The light profile is a report/evidence profile for fast visibility and promotion planning.


```text
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
apply patch specs without explicit apply/review lane
commit output/**
commit SQLite DB files
run Blender or FFmpeg
produce audio/media output
change provider/model execution semantics
claim provider execution from light evidence-only profiles
claim NPU compute-provider work when only diagnostic/report lane ran
claim draft PR support before prepare_review_pr.py implements it
claim metadata-only generated patch specs as reviewable product
bypass heap/exchange lifecycle for review PR product paths
bypass patchkit for new long/delicate patch bundles when patchkit can express the change
```

Push-capable helpers are not default validation commands and require explicit user intent.

## Full-run handoff rule

When a workflow helper contributes to real product evidence, recommendations, patch plans or patch specs, its output must be visible through:

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
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/index/discovery/file-line evidence when relevant
generated artifact path policy evidence when long bundle names are possible
runtime evidence correlation JSON/Markdown when requested
repository change proposals with runtime_report_paths when current runtime evidence exists
generated patch-spec apply report with concrete operation_count/changed_count for review PR product
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
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
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

The real product profile is not a manually guided chain. The operator provides a task Markdown file or asks the wrapper to generate a process-gate task, then the run enters the heap/exchange runtime. Inside that dynamic center, GPU1, GPU0, NPU, shared memory, SQLite FTS memory, broker/tool-agnostic capabilities and deterministic script lanes cooperate as peers and evidence producers.

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

- A full product chain smoke is not considered valid unless the static mesh contract passes first.
- This keeps Task MD ingress, heap/exchange activation, GPU1/GPU0/NPU peer lanes, shared memory, SQLite FTS, tool broker, direct reasoning assistance, static deterministic product lane, heap/exchange close and review PR readiness tied to the final PR product.

<!-- IA-CARMINE-REAL-PRODUCT-PREFLIGHT-GATE-BEGIN -->
## Real product preflight gate

Before launching a real product run, execute the deterministic preflight gate:

- `Tools/validation/run_real_product_preflight_gate.py`
- `Tools/validation/run_real_product_preflight_gate_smoke.py`

The preflight gate runs profile, intrinsic capability, runtime mesh, OpenVINO peer topology, review PR args, review PR readiness, full product PR chain, runtime evidence correlation, launcher wiring, manifest correlation schema and review PR final product smokes. It does not execute providers, does not apply patches, does not run Blender/FFmpeg and does not write source products.

It is the safe static readiness gate before entering the dynamic heap/exchange runtime.
<!-- IA-CARMINE-REAL-PRODUCT-PREFLIGHT-GATE-END -->

<!-- IA-CARMINE-MANDATORY-PREFLIGHT-BEGIN -->
## Mandatory real product preflight

The real product wrapper always runs `Tools/validation/run_real_product_preflight_gate.py` before delegating to the heap/exchange launcher.

There is no skip switch for this gate. A failed preflight stops the run before provider activity, patch application, Blender/FFmpeg execution or review-PR preparation.

The provider surface checked by the runtime mesh contract includes Ollama/GPU1 advisory wiring, OpenVINO/GPU0 workload wiring, NPU peer micro lane, SQLite FTS memory, broker/tool-agnostic execution, direct reasoning assistance, static deterministic product lane, heap/exchange close and final review PR readiness.
<!-- IA-CARMINE-MANDATORY-PREFLIGHT-END -->

<!-- IA-CARMINE-OPENVINO-PEER-TOPOLOGY-WIRING-BEGIN -->
## OpenVINO peer topology preflight wiring

The mandatory real product preflight includes `run_openvino_peer_topology_contract_smoke.py`.

The runtime mesh contract also requires the OpenVINO peer topology contract as an intrinsic capability. This means a real product run cannot enter heap/exchange unless GPU.1 remains reserved for Ollama/CUDA advisory, GPU.0 remains the OpenVINO peer/support lane, and NPU remains a micro peer using heap/tool context.

This wiring keeps OpenVINO GPU0/NPU topology inside the same Task MD IN -> heap/exchange -> peer lanes -> close -> product readiness -> review PR path.
<!-- IA-CARMINE-OPENVINO-PEER-TOPOLOGY-WIRING-END -->

<!-- IA-CARMINE-RUNTIME-EVIDENCE-CORRELATION-BEGIN -->
## Runtime evidence correlation

The real product validation surface includes `Tools/validation/check_runtime_evidence_correlation.py`.

Use it after a real product run to prove that one stamp contains the complete product evidence mesh:

- mandatory preflight result;
- heap/exchange entry;
- heap peer runtime manifest;
- GPU0 OpenVINO peer/support evidence;
- NPU micro peer evidence;
- shared memory / AI-to-AI evidence;
- tool broker capability or usage telemetry;
- heap/exchange closure audit;
- review PR product readiness;
- `prepare_review_pr.py` result;
- final unified chain contract.

The smoke `Tools/validation/run_runtime_evidence_correlation_smoke.py` is also part of the mandatory preflight to prevent drift in the validator itself. It is report-only and does not execute providers or apply patches.
<!-- IA-CARMINE-RUNTIME-EVIDENCE-CORRELATION-END -->

<!-- IA-CARMINE-RUNTIME-EVIDENCE-CORRELATION-LAUNCHER-HARDENING-BEGIN -->
## Runtime evidence correlation launcher hardening

The mandatory real product preflight validates `run_runtime_evidence_correlation_launcher_wiring_smoke.py`.

The full product PR chain smoke also checks that runtime evidence correlation is present after the final unified chain contract. This prevents drift where the launcher emits a final chain contract but forgets to emit the correlated runtime evidence report for the same stamp.

Required final order:

1. final unified chain contract
2. runtime evidence correlation JSON/Markdown report

The hardening remains report-only: no provider execution, no patch application, no git push and no PR creation.
<!-- IA-CARMINE-RUNTIME-EVIDENCE-CORRELATION-LAUNCHER-HARDENING-END -->

<!-- IA-CARMINE-REAL-PRODUCT-PROFILE-CORRELATION-HARDENING-BEGIN -->
## Real product profile correlation hardening

The real product profile smoke requires the wrapper to pass `-BuildRuntimeEvidenceCorrelation` to the launcher.

This protects the final product path from regressing to a run that prepares a PR without emitting the correlated runtime evidence report. The profile-level smoke now checks all three levels:

1. wrapper requests runtime evidence correlation;
2. launcher exposes and emits the final correlation artifact;
3. preflight/README document the wiring smoke that guards the contract.

This remains static and report-only. It does not execute providers, does not apply patches and does not create remote PRs.
<!-- IA-CARMINE-REAL-PRODUCT-PROFILE-CORRELATION-HARDENING-END -->

<!-- IA-CARMINE-MANIFEST-RUNTIME-EVIDENCE-CORRELATION-BEGIN -->
## Manifest runtime evidence correlation schema

When `runtime_evidence_correlation_requested` is true, the final unified manifest must expose the produced correlation artifact in `phase_reports.runtime_evidence_correlation` and must include the JSON report in `report_files`.

The smoke `Tools/validation/run_unified_manifest_runtime_evidence_correlation_smoke.py` validates three cases:

1. requested and report declared: pass;
2. requested and report missing: fail;
3. not requested: pass.

This prevents downstream tooling from relying on implicit path guesses for the final runtime evidence correlation report.
<!-- IA-CARMINE-MANIFEST-RUNTIME-EVIDENCE-CORRELATION-END -->

<!-- IA-CARMINE-REVIEW-PR-FINAL-PRODUCT-CONTRACT-BEGIN -->
## Review PR final product contract

`Tools/validation/check_review_pr_final_product_contract.py` validates the output of `prepare_review_pr.py`.

It distinguishes two modes:

1. local review branch product: product commit and safe include paths are required;
2. remote PR product: push, GitHub PR creation and PR URL are also required.

The smoke `Tools/validation/run_review_pr_final_product_contract_smoke.py` covers local-product pass, remote-product pass and missing-remote-PR fail. The check is report-only and does not create branches, commits, pushes or PRs during preflight.
<!-- IA-CARMINE-REVIEW-PR-FINAL-PRODUCT-CONTRACT-END -->

<!-- IA-CARMINE-REAL-PRODUCT-SINGLE-ENTRY-EXIT-BEGIN -->
## Real product single entry / single exit

The operator-facing entry point is `Tools/workflow/run_unified_real_product_pr.ps1`.

For the first real process-product PR, use `-ProcessGateTask` instead of an external task-generation script. The wrapper creates the ignored task Markdown under `output/local_ai_task_inputs`, delegates the universe between entry and exit to `run_unified_local_ai_refactor.ps1`, and then validates the final review PR product through `check_review_pr_final_product_contract.py`.

When `-CreatePr` is used, final product validation automatically runs in remote PR mode and requires push, GitHub PR creation and PR URL. This preserves the model:

- one entry: real product launcher;
- universe in the heap/exchange runtime;
- one exit: validated review PR final product.
<!-- IA-CARMINE-REAL-PRODUCT-SINGLE-ENTRY-EXIT-END -->

<!-- IA-CARMINE-RUNTIME-PEER-EVIDENCE-FEED-BEGIN -->
## Runtime peer evidence feed into proposals

`Tools/ai/build_repository_change_proposals.py` reads current-stamp heap/exchange, GPU0, NPU, runtime-correlation and generated patch-spec apply reports when available.

If those reports prove that the runtime mesh existed but generated patch specs were metadata-only, the expected product proposal is `P-RUNTIME-PEER-EVIDENCE-FEED`. The fallback `P-NEXT-NPU-OBSERVABILITY` remains a backlog/default proposal and must not be treated as successful final product when runtime peer evidence exists.

`Tools/ai/build_patch_specs_from_proposals.py` can carry reviewed `concrete_operations` into generated patch specs. Allowed operations remain deterministic and reviewable: `replace_once`, `append_once`, `insert_after_once`, `insert_before_once`, `write_file`.

`Tools/validation/run_repository_change_proposals_runtime_evidence_smoke.py` covers the complete route: runtime evidence -> proposal -> patch spec -> generated patch apply.
<!-- IA-CARMINE-RUNTIME-PEER-EVIDENCE-FEED-END -->

## Standalone heap lane is not the full-run entrypoint yet

The standalone heap universe lane is currently an incubation path under `Tools/ai/`:

```text
Tools/ai/run_heap_runtime_context_closure.py
```

Workflow wrappers should not treat it as the canonical product entrypoint until its promotion checklist passes. The full product entrypoint remains:

```text
Tools/workflow/run_unified_real_product_pr.ps1
```

Promotion into run-unica should happen only after the standalone lane proves tool-owned preload, SQLite/FTS5 or operational memory visibility, semantic chunk/context artifacts, same-heap GPU1/GPU0/NPU participation, in-heap refinement and composer package export.
