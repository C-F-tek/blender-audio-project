# Proposal Patch Spec Writer

## Status

active

## Goal

Turn validated repository proposal reports into reviewable draft patch-spec artifacts without applying source changes, writing the GitHub Action queue, executing providers or touching Blender runtime files.

## Scope

- Add a non-mutating builder that reads `repository_change_proposals` reports.
- Write inert draft specs under ignored `output/patch_specs/`.
- Add a validator that rejects queued inbox paths, forbidden targets and concrete replacements while a spec is still a draft.
- Document the contract in validation, schema, data-flow and patch-spec workflow docs.
- Validate with both deterministic checks and the explicit parallel GPU/NPU multistep workflow.

## Guardrails

- Ollama/GPU remains the primary advisory lane only through explicit workflow flags.
- OpenVINO/NPU remains probe, guardrail and decode diagnostic evidence only.
- Draft specs must keep `replacements` empty until a separate review-to-concrete step.
- Do not write `patch_specs/inbox/` from the draft builder.
- Do not touch Blender runtime, Ready To Jazz, `Scripting/shared/blender_compat.py`, full analysis JSON or generated indexes.

## Validation Plan

```powershell
python -m Tools.validation check_python_syntax --repo-root .
python -m Tools.ai build_repository_change_proposals --repo-root . --profile npu --output-dir output\ai_pipeline --basename repository_change_proposals_contract_smoke
python -m Tools.validation check_repository_change_proposals --repo-root . --proposal .\output\ai_pipeline\repository_change_proposals_contract_smoke.json --output .\output\validation\repository_change_proposals_contract.json
python -m Tools.ai generated_patch_specs_from_proposals --repo-root . --proposal .\output\ai_pipeline\repository_change_proposals_contract_smoke.json --output-dir output\patch_specs --basename proposal_patch_specs_contract_smoke
python -m Tools.validation check_patch_spec_drafts --repo-root . --manifest .\output\patch_specs\proposal_patch_specs_contract_smoke_manifest.json --output .\output\validation\patch_spec_drafts.json
python -m Tools.workflow run_parallel_ai_provider_multistep -Profile npu -RunOllamaProbe -RunNpuProbe -RunNpuDecodeSmoke -UsePrimaryAdvisoryProvider -Basename proposal_patch_specs_gpu_npu_multistep -ProposalBasename proposal_patch_specs_gpu_npu_multistep_proposals -EvidenceBasename proposal_patch_specs_gpu_npu_multistep_evidence
```

## Exit Criteria

- Draft builder and validator pass syntax checks.
- Draft manifest validates from a static proposal report.
- Draft manifest validates from a real multistep GPU/NPU proposal report.
- Compact evidence bundle is committed under `docs/LOCAL_VALIDATION_EVIDENCE/`.
- PR documents that drafts are inert and not queued patches.
