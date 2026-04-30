# Suggestion Artifact Contracts

## Status

active

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

This milestone should be validated both statically and through the real parallel provider workflow:

```text
Ollama/GPU/CUDA -> explicit primary advisory provider when quality routing allows it.
OpenVINO/NPU -> explicit probe, guardrail and decode smoke diagnostic.
Parallel provider jobs -> run through run_parallel_ai_provider_multistep.ps1.
```

## Validation commands

```powershell
python .\Tools\ai\build_repository_change_proposals.py --repo-root . --profile npu --output-dir output\ai_pipeline --basename repository_change_proposals_contract_smoke
python .\Tools\validation\check_repository_change_proposals.py --repo-root . --proposal .\output\ai_pipeline\repository_change_proposals_contract_smoke.json --output .\output\validation\repository_change_proposals_contract.json
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_parallel_ai_provider_multistep.ps1 -Profile npu -RunOllamaProbe -RunNpuProbe -RunNpuDecodeSmoke -UsePrimaryAdvisoryProvider -Basename suggestion_artifact_contracts_gpu_npu_multistep -ProposalBasename suggestion_artifact_contracts_gpu_npu_multistep_proposals -EvidenceBasename suggestion_artifact_contracts_gpu_npu_multistep_evidence
```

## Risk level

medium-low

The code change is small, but the validation intentionally executes local providers. Mitigation: provider execution remains explicit and report-bound, and generated proposal files stay under ignored `output/` except compact evidence bundles.

## Progress log

- 2026-05-01: Added `suggestion_outputs` descriptors to repository change proposals.
- 2026-05-01: Added `check_repository_change_proposals.py` to validate manual-review proposal reports and suggestion descriptors.
- 2026-05-01: Ran the parallel GPU/NPU multistep workflow with Ollama/GPU advisory execution, OpenVINO/NPU probe, NPU decode smoke and compact evidence generation.
- 2026-05-01: Validated the generated proposal report with `check_repository_change_proposals.py`.

## Future notes

- Add a later patch-spec writer that consumes validated proposals and creates separate reviewable patch specs without applying them.
- Keep generated suggestions source-separated until a trusted apply step has explicit user approval.
