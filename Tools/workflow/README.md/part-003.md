<!-- IA-CARMINE-MD-SPLIT: part -->
# README â€” parte 003 di 003

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-002.md)

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

The operator-facing entry point is `python -m Tools.ai run`.

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

## Operator Heap/Universe Run Surface

The operator heap/universe lane has one Python non-GUI surface and one GUI view:

```text
python -m Tools.ai run
python -m Tools.ai operator_product_gui
```

The lower-level heap closure remains an internal dispatched tool:

```text
python -m Tools.ai run_heap_runtime_context_closure
```

Workflow wrappers should call the Python dispatcher instead of direct script paths.
