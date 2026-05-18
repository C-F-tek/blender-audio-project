<!-- IA-CARMINE-MD-SPLIT: part -->
# README â€” parte 002 di 003

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)
- [Parte successiva](part-003.md)

## Patchkit bundle procedure

Future patch work should centralize the modification core:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Standard commands:

```powershell
python -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python -m Tools.ai apply_patch_bundle `
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
| `python -m Tools.workflow run_agent_review_full_toolbox_decision_loop` | Python control entrypoint | Preserves the public CLI and runs the packaged Python engine under `run_agent_review_full_toolbox_decision_loop/`. |
| `run_agent_review_full_toolbox_decision_loop/py_engine.py` | Python engine package | Static foundation and top-level phase sequencing. |
| `run_agent_review_full_toolbox_decision_loop/py_mesh.py` | Python engine package | GPU1/GPU0/NPU provider mesh, runtime heap live signals and broker-controlled peer tool execution. |
| `run_agent_review_full_toolbox_decision_loop/py_product.py` | Python engine package | Decision loop, final local AI product, evidence bundle, telemetry, semantic chunks and artifact path policy. |
| `run_agent_review_full_toolbox_decision_loop/py_support.py` | Python engine package | Shared paths, execution helpers and compact artifact stamp generation. |
| `run_agent_review_full_toolbox_decision_loop_integrated.ps1` | supporting selected phase | Not primary operator path. |
| `run_local_ai_markdown_task.ps1` | supporting-tool | Markdown helper; prefer unified launcher or real product wrapper. |
| `run_docs_md_refactor_10min.ps1` | legacy-superseded/supporting-tool | Prefer unified launcher `md`/validation phases. |
| `startup_preflight.ps1` | diagnostic-only | Startup/preflight helper. |
| `python -m Tools.workflow startup_check` | diagnostic-only | Startup check helper. |
| `python -m Tools.workflow workflow_shell` | gui-or-shell-helper | Interactive helper; not canonical headless flow. |
| `python -m Tools.workflow workflow_shell_with_push` | unsafe-or-write-capable | Push-capable; explicit user intent required. |
| `git_auto_push.py` | unsafe-or-write-capable | Push behavior requires explicit user intent. |
| `asset_inventory.py` | supporting-tool | Asset inventory helper. |
| `scene_brief.py` | supporting-tool/application-domain | Scene brief helper. |
| `artifact_consult.py` | supporting-tool | Artifact consultation helper. |
| `project_awareness.py` | supporting-tool | Project-awareness context helper. |
| `python -m Tools.workflow smart_ai_context` | supporting-tool | Smart context helper. |
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
claim draft PR support before agent_review_prepare_pr.py implements it
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
- agent_review_prepare_pr.py
- PR finale testabile

Static gate:

- `Tools/validation/real_product/runtime_mesh_contract/cli.py`
- `Tools/validation/real_product/runtime_mesh_contract_smoke/cli.py`

The gate is deterministic. It does not run providers, does not apply patches, does not run Blender/FFmpeg and does not write source products. Its job is to fail early when the real product profile stops wiring one of the intrinsic project capabilities into the final review-PR path.
<!-- IA-CARMINE-REAL-PRODUCT-RUNTIME-MESH-END -->

Full product PR chain gate:

- A full product chain smoke is not considered valid unless the static mesh contract passes first.
- This keeps Task MD ingress, heap/exchange activation, GPU1/GPU0/NPU peer lanes, shared memory, SQLite FTS, tool broker, direct reasoning assistance, static deterministic product lane, heap/exchange close and review PR readiness tied to the final PR product.

<!-- IA-CARMINE-REAL-PRODUCT-PREFLIGHT-GATE-BEGIN -->
