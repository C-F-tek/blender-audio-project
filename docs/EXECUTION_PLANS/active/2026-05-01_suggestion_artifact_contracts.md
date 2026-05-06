# Suggestion Artifact Contracts

## Status

active

## Current review note — 2026-05-07

This older plan remains under `active/`, but the original 2026-05-01 work already produced proposal descriptors, validation and compact evidence. Treat it as **legacy active / proposal-contract follow-up**, not as the current provider architecture source of truth.

Before extending suggestion/proposal artifacts, read:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Current architecture target:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Suggestion artifacts should evolve toward blackboard-ready, broker-safe, validator-checkable records. They must remain manual-review only unless a later explicitly approved apply lane exists.

## Goal

Make repository suggestion files useful as real future work inputs by giving proposal JSON/Markdown a stable, manual-review-only contract for code, Markdown, JSON, PowerShell and workflow targets.

## Scope

```text
Tools/ai/build_repository_change_proposals.py
Tools/validation/check_repository_change_proposals.py
Tools/validation/README.md
docs/JSON_SCHEMAS.md
docs/AI_ARTIFACT_SCHEMAS.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/TECH_DEBT_TRACKER.md
```

## Out of scope

```text
auto-applying patches
changing provider behavior, model settings, temperature or prompt prose
Blender runtime changes
Ready To Jazz migration
full analysis JSON edits
generated index edits
network, secret or authentication changes
```

## Provider lane validation

Historical provider validation from the original task:

```text
Ollama/GPU/CUDA -> explicit primary advisory provider when quality routing allows it.
OpenVINO/NPU -> explicit probe, guardrail and decode smoke diagnostic.
Parallel provider jobs -> run through run_parallel_ai_provider_multistep.ps1.
```

Current target interpretation:

```text
GPU1 primary advisory / planner -> may propose, classify and synthesize suggestions.
GPU0 coworker/helper OpenVINO -> may contribute focused helper diagnostics or secondary review.
NPU microtask responder -> may contribute bounded microtask classifications or probes.
broker unico executor -> should be the future gateway for tool execution.
deterministic validators / CPU authority -> must validate proposal contracts and decide pass/fail.
telemetry/event stream -> must show whether suggestion generation was provider-backed, skipped, degraded or deterministic-only.
```

Do not claim GPU1/GPU0/NPU participation unless current telemetry/provider diagnostics prove it.

## Validation commands

```powershell
python .\Tools\ai\build_repository_change_proposals.py --repo-root . --profile npu --output-dir output\ai_pipeline --basename repository_change_proposals_contract_smoke
python .\Tools\validation\check_repository_change_proposals.py --repo-root . --proposal .\output\ai_pipeline\repository_change_proposals_contract_smoke.json --output .\output\validation\repository_change_proposals_contract.json
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_parallel_ai_provider_multistep.ps1 -Profile npu -RunOllamaProbe -RunNpuProbe -RunNpuDecodeSmoke -UsePrimaryAdvisoryProvider -Basename suggestion_artifact_contracts_gpu_npu_multistep -ProposalBasename suggestion_artifact_contracts_gpu_npu_multistep_proposals -EvidenceBasename suggestion_artifact_contracts_gpu_npu_multistep_evidence
```

Current caution:

```text
Provider execution remains explicit. For documentation-only review or GitHub-only work, do not run these commands; keep them as local validation instructions.
```

## Risk level

medium-low

The code change is small, but the validation intentionally executes local providers. Mitigation: provider execution remains explicit and report-bound, and generated proposal files stay under ignored `output/` except compact evidence bundles.

## Progress log

- 2026-05-01: Added `suggestion_outputs` descriptors to repository change proposals.
- 2026-05-01: Added `check_repository_change_proposals.py` to validate manual-review proposal reports and suggestion descriptors.
- 2026-05-01: Ran the parallel GPU/NPU multistep workflow with Ollama/GPU advisory execution, OpenVINO/NPU probe, NPU decode smoke and compact evidence generation.
- 2026-05-01: Validated the generated proposal report with `check_repository_change_proposals.py`.
- 2026-05-07: Reviewed as older active plan; aligned provider interpretation with `docs/MAIN_RUNTIME_ARCHITECTURE.md` without changing code or validators.

## Future notes

- Add a later patch-spec writer that consumes validated proposals and creates separate reviewable patch specs without applying them.
- Keep generated suggestions source-separated until a trusted apply step has explicit user approval.
- Add blackboard/broker/registry/event-stream fields only after code emits real reports.
- Consider moving this plan to `completed/` in a later explicit execution-plan cleanup.
