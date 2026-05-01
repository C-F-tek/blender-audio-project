# Improve GPU Planner Nonempty Recommendations

This task investigates why the GPU/Ollama planner can complete many planning rounds while producing zero actionable recommendations.

## Required reading order

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/ai/build_agent_review_patch_plan.py
Tools/validation/run_agent_review_patch_plan_smoke.py
```

## Problem statement

Observed local run state:

```text
parallel GPU/NPU orchestrator: passed true
GPU/Ollama rounds: 24
GPU recommendations: 0
NPU audits: 3 / 3 usable
NPU blocked GPU review: false
evidence_ready_for_manual_patch_count: 12
fallback patch-plan count: 12
fallback_used: true
```

The fallback patch-plan layer works, but the GPU planner should expose better diagnostics when evidence is ready and recommendations remain empty.

## Investigation goals

Identify code changes that would make the GPU planner report why recommendation_count is zero.

Required diagnostic categories:

```text
json_parse_failure
valid_json_empty_recommendations
recommendations_filtered_out
evidence_ready_but_no_gpu_plan
model_output_missing_required_fields
repair_attempt_failed
```

## Desired behavior

When evidence_sufficiency reports ready_for_manual_patch_count > 0 and the GPU planner returns zero recommendations, the reports should include:

```text
empty_recommendations_reason
raw_recommendation_candidate_count
filtered_recommendation_count
json_parse_error_count
repair_attempt_count
evidence_ready_for_manual_patch_count
recommended_next_layer
```

## Non-goals

Do not apply patches automatically.
Do not run Blender.
Do not execute OpenVINO/NPU providers.
Do not promote NPU output to advisory primary lane.
Do not change model/provider settings unless explicitly proposed as a manual-review recommendation.
Do not edit output/** or generated indexes as source.

## Candidate target files

```text
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/validation/run_agent_review_patch_plan_smoke.py
Tools/validation/run_agent_review_patch_plan_full_validation.py
docs/JSON_SCHEMAS.md
Tools/validation/README.md
```

## Expected output

Produce an advisory plan only.

The plan should include:

```text
root cause hypothesis
exact target files
proposed fields to add
report schema impact
validator impact
minimal patch sequence
validation commands
risks
stop conditions
```

## Validation commands after future implementation

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
python .\Tools\validation\run_agent_review_patch_plan_smoke.py --repo-root . --orchestrator .\output\ai_pipeline\agent_gpu_npu_parallel_orchestrator_live.json --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json --min-patch-plans 12 --expect-fallback --output .\output\validation\agent_review_patch_plan_smoke.json --markdown-output .\output\validation\agent_review_patch_plan_smoke.md
git diff --check
git status --short
```

## Stop conditions

Stop and report instead of editing if:

```text
the GPU report path cannot be resolved from the orchestrator
the required fix needs provider execution
the fix requires changing Blender runtime behavior
the fix requires committing output/**
the fix requires changing model temperature/provider settings without explicit approval
```
