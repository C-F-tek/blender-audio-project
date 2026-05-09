# Documentation/code alignment audit — 2026-05-10

## Scope

Audit code-driven della documentazione IA-Carmine dopo la catena #270-#296. L'obiettivo è verificare che i documenti operativi descrivano il codice attuale, non una visione architetturale desiderata.

File documentali correlati:

- `Tools/workflow/README.md`;
- `docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md`;
- `docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md`.

## Owner code rilevati

| Area | File owner | Stato doc |
|---|---|---|
| Entrata operatore real product | `Tools/workflow/run_unified_real_product_pr.ps1` | Coperto dal runbook run unica. |
| Centro heap/exchange | `Tools/workflow/run_unified_local_ai_refactor.ps1` | Coperto da README e runbook. |
| Preflight obbligatorio | `Tools/validation/run_real_product_preflight_gate.py` | Coperto da README e runbook. |
| Runtime mesh static contract | `Tools/validation/check_real_product_runtime_mesh_contract.py` | Coperto da README e problems list. |
| OpenVINO peer topology | `Tools/validation/check_openvino_peer_topology_contract.py` | Coperto da README. |
| GPU0 observable workload | `Tools/ai/build_openvino_gpu0_workload_report.py` | Coperto dal runbook e problems list. |
| NPU peer diagnostic companion | `Tools/ai/build_npu_micro_task_companion_report.py` | Coperto dal runbook e problems list. |
| Metadata-only generated specs fail-fast | `Tools/ai/apply_generated_patch_specs_for_review_pr.py` | Coperto dal runbook. |
| Runtime evidence feed proposals | `Tools/ai/build_repository_change_proposals.py` | Coperto dal runbook e problems list. |
| Concrete ops into patch specs | `Tools/ai/build_patch_specs_from_proposals.py` | Coperto dal runbook. |
| End-to-end runtime evidence smoke | `Tools/validation/run_repository_change_proposals_runtime_evidence_smoke.py` | Coperto dal runbook. |
| Empty generated product smoke | `Tools/validation/run_generated_patch_specs_empty_product_smoke.py` | Coperto dal runbook/problems list. |

## Alignment checks

### Entry/exit model

Doc statement:

- one entry: real product wrapper;
- dynamic universe: unified launcher heap/exchange;
- one exit: review PR final product.

Code evidence owners:

- `run_unified_real_product_pr.ps1` owns operator-facing wrapper and delegates to launcher;
- `run_unified_local_ai_refactor.ps1` owns dynamic phase execution;
- `check_review_pr_final_product_contract.py` validates final product semantics.

Status: aligned.

### Task Markdown semantics

Doc statement:

- task Markdown generated under `output/local_ai_task_inputs/` is entry contract;
- it is not required to embed patch suggestion fences;
- runtime/generated patch specs are expected downstream.

Code evidence owner:

- `Tools/ai/build_task_patch_suggestion_report.py` now allows generated process-gate task deferral to runtime product.

Status: aligned.

### Metadata-only generated patches

Doc statement:

- metadata-only patch specs are not real product;
- with `--apply`, empty concrete operation set must fail.

Code evidence owner:

- `Tools/ai/apply_generated_patch_specs_for_review_pr.py` emits error when generated specs produce no concrete review product;
- `Tools/validation/run_generated_patch_specs_empty_product_smoke.py` protects the behavior.

Status: aligned.

### Runtime evidence proposals

Doc statement:

- proposal builder can consume current-stamp runtime evidence;
- if runtime evidence exists and patch apply is metadata-only, expected proposal is `P-RUNTIME-PEER-EVIDENCE-FEED`.

Code evidence owner:

- `Tools/ai/build_repository_change_proposals.py` discovers runtime reports and emits runtime peer evidence proposal;
- `Tools/ai/build_patch_specs_from_proposals.py` can carry `concrete_operations` into patch specs;
- `Tools/validation/run_repository_change_proposals_runtime_evidence_smoke.py` covers proposal -> spec -> apply.

Status: aligned.

### GPU0/NPU wording

Doc statement:

- GPU0 must be observable OpenVINO support/workload lane;
- NPU is micro peer diagnostic/report lane unless future compute provider is validated.

Code evidence owners:

- `Tools/ai/build_openvino_gpu0_workload_report.py` owns observable GPU0 report fields;
- `Tools/ai/build_npu_micro_task_companion_report.py` owns NPU peer activity classification;
- `Tools/validation/run_observable_peer_activity_contract_smoke.py` protects semantics.

Status: aligned.

## Drift still present

### README size drift

`Tools/workflow/README.md` remains too large and mixes:

- operator routing;
- runbook details;
- historical contracts;
- current dynamic runtime semantics;
- static validation notes.

Action candidate:

- keep README as index/router;
- move long operational details to `docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md`;
- do not remove anchors used by smoke validators without updating the validators in the same PR.

### Naming drift: Full0To10 legacy alias

Some validators still expose names such as `full0to10_product_pr_chain_smoke`. The effective model is now `single_dynamic_heap_exchange_run`.

Action candidate:

- keep legacy names as compatibility aliases;
- document alias explicitly;
- avoid mass rename until smoke/manifest consumers are mapped.

### Artifact path drift

Runtime can still dirty:

- `indexAI/code_chunks/**`;
- `docs/LOCAL_VALIDATION_EVIDENCE/**`.

Action candidate:

- decide which artifacts are source/versioned vs runtime/generated;
- add a deterministic pre-run cleanup/check plan;
- prevent false attribution to generated task Markdown.

### Structured error consistency

The wrapper has structured error reports, but PowerShell throw paths may still exist.

Action candidate:

- replace unstructured throw-only paths progressively;
- keep non-zero exit;
- always emit JSON with provider/patch/source-write booleans.

## Documentation state after this audit

| Document | Role | Status |
|---|---|---|
| `Tools/workflow/README.md` | broad index + legacy/current contracts | Accurate but oversized. |
| `real-product-run-unica-runbook-2026-05-10.md` | operator runbook | Current with #295/#296 behavior. |
| `problems-and-hygiene-candidates-2026-05-10.md` | tomorrow hygiene queue | Current and prioritized. |
| This file | code/doc alignment audit | Current snapshot. |

## Next safe documentation change

The next documentation-only patch should update `Tools/workflow/README.md` with only a compact pointer to the two new documents and this audit, without adding another long section.
