# Patch Spec Review Promotion

## Status

completed

## Goal

Add the next non-destructive step after proposal-derived draft patch specs: promote one draft plus an explicit replacement plan into a reviewed patch spec that has passed dry-run, without applying source changes or writing the GitHub Action queue.

## Scope

- Add a promotion tool for `proposal_patch_spec_draft` plus `patch_spec_replacement_plan`.
- Add a validator for `reviewed_patch_spec` and `reviewed_patch_spec_manifest`.
- Add deterministic fixtures that prove dry-run promotion without modifying source files.
- Document the review-to-concrete contract in validation, schema, data-flow and patch-spec workflow docs.
- Validate with static checks and the explicit parallel GPU/NPU multistep workflow.

## Guardrails

- Promotion tools must never call `apply_repo_mods.py --write`.
- Reviewed specs remain under ignored `output/patch_specs/`.
- Reviewed specs must not be copied into `patch_specs/inbox/` without explicit approval.
- Replacement plans may only target files already listed in their source draft.
- Do not touch Blender runtime, Ready To Jazz, `Scripting/shared/blender_compat.py`, full analysis JSON or generated indexes.
- Ollama/GPU remains primary advisory only through explicit flags; OpenVINO/NPU remains probe/guardrail/decode diagnostic evidence only.

## Validation Plan

```powershell
python -m Tools.validation check_python_syntax --repo-root .
python -m Tools.ai generated_patch_specs_promote_draft --repo-root . --draft .\Tools\ai\fixtures\patch_spec_review_draft.json --replacement-plan .\Tools\ai\fixtures\patch_spec_review_replacement_plan.json --output-dir output\patch_specs --basename reviewed_patch_spec_fixture
python -m Tools.validation reviewed_patch_specs_check --repo-root . --manifest .\output\patch_specs\reviewed_patch_spec_fixture_manifest.json --output .\output\validation\reviewed_patch_specs.json
python -m Tools.workflow run_parallel_ai_provider_multistep -Profile npu -RunOllamaProbe -RunNpuProbe -RunNpuDecodeSmoke -UsePrimaryAdvisoryProvider -Basename patch_spec_review_promotion_gpu_npu_multistep -ProposalBasename patch_spec_review_promotion_gpu_npu_multistep_proposals -EvidenceBasename patch_spec_review_promotion_gpu_npu_multistep_evidence
```

## Exit Criteria

- Promotion tool and reviewed-spec validator pass syntax checks.
- Fixture promotion writes a reviewed spec under `output/patch_specs/`.
- Reviewed-spec validator reruns dry-run and passes.
- Compact evidence bundle is committed under `docs/LOCAL_VALIDATION_EVIDENCE/`.
- PR documents that reviewed specs are still not applied and not queued.

## Result

- Added `Tools/ai/generated_patch_specs/review_cli.py` for non-mutating promotion from `proposal_patch_spec_draft` plus `patch_spec_replacement_plan` to `reviewed_patch_spec`.
- Added `Tools/validation/generated_patch_specs/reviewed_patch_specs_check/cli.py` to validate reviewed specs and rerun mandatory dry-run.
- Added deterministic fixtures proving one concrete replacement without modifying the target file.
- Produced compact GPU/NPU evidence at `docs/LOCAL_VALIDATION_EVIDENCE/patch_spec_review_promotion_gpu_npu_multistep_evidence.json`.
- Confirmed Ollama/GPU primary advisory execution and NPU probe/decode-smoke execution; old NPU workload output remains excluded from advisory context.
