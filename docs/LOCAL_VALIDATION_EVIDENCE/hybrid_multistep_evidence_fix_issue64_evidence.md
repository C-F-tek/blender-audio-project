# Hybrid Multistep Evidence Fix Validation

- Generated at: `2026-05-01T11:11:21.9751695+02:00`
- Branch: `codex/hybrid-multistep-evidence-fix`
- HEAD: `f9d6e4900f4883f463d8964c94452ee0ca7d9ea0`
- PR: `#64`
- Base PR: `#63`
- Passed: `True`
- Multistep provider workflow requested in dry-run: `True`
- Provider execution requested in dry-run manifest: `True`
- Patch application performed: `False`

## Script line counts

- `Tools/ai/build_github_evidence_bundle.py`: `326` lines
- `Tools/workflow/run_local_ai_task_via_pipeline.ps1`: `335` lines

## Validation

- `./output/validation/python_syntax.json`: exists=`True` passed=`True` kind=`python_syntax`
- `./output/validation/docs_links.json`: exists=`True` passed=`True` kind=`docs_links`
- `./output/validation/validation_report_contract.json`: exists=`True` passed=`True` kind=`validation_report_contract`

## Evidence decision fix

The synthetic `npu_excluded_when_unusable` decision is expected to derive from:

- `ai_workload_report_quality.unusable_lanes`
- `ai_workload_quality_lane_routing.routing.excluded_advisory_lanes`
- `npu_decode_quality_remediation.checks.npu_usable_for_advisory == false`
- `legacy excluded context-file signals`

## Runtime/provider statement

- Adapter multistep path was validated in dry-run mode.
- No patch application.
- No automatic merge.
- Provider execution remains explicit.
- NPU remains probe / guardrail / decode diagnostic.
- Ollama/GPU remains primary advisory behind quality gate.
