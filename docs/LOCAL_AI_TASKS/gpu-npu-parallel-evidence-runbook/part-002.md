<!-- IA-CARMINE-MD-SPLIT: part -->
# gpu-npu-parallel-evidence-runbook — parte 002 di 002

Sorgente indice: [`../gpu-npu-parallel-evidence-runbook.md`](../gpu-npu-parallel-evidence-runbook.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Git-trackable evidence bundle procedure

Do not upload or commit raw `output/**` reports directly.

The project-owned evidence flow is:

```text
build_github_evidence_bundle.py
→ docs/LOCAL_VALIDATION_EVIDENCE/*.json/*.md
→ check_github_evidence_bundle.py
→ git add only compact evidence docs
→ commit/push
```

Build the compact evidence bundle:

```powershell
python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename gpu_planner_nonempty_recommendations_evidence `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\ai_packets\gpu_planner_nonempty_recommendations_advisory.json `
  --report .\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json `
  --report .\output\patch_specs\agent_review_patch_plan.json `
  --report .\output\validation\agent_review_patch_plan_full_validation.json `
  --report .\output\validation\agent_review_patch_plan_smoke.json `
  --report .\output\validation\validation_report_contract.json `
  --report .\output\ai_pipeline\repository_change_proposals.json `
  --report .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --report .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_parallel_gpu.json
```

Expected Git-trackable outputs:

```text
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
```

Validate the evidence bundle:

```powershell
python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --bundle .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.json `
  --output .\output\validation\gpu_planner_nonempty_recommendations_evidence_validation.json
```

Inspect validation:

```powershell
Get-Content .\output\validation\gpu_planner_nonempty_recommendations_evidence_validation.json -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, bundle_count, errors, warnings
```

## Final validation before push

Run standard validation:

```powershell
python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract.json

git diff --check
git status --short
```

Only Git-trackable compact evidence should be staged for an evidence-only update:

```text
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
```

Commit and push:

```powershell
git add `
  .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.json `
  .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.md

git commit -m "test(ai): add gpu planner nonempty recommendations evidence bundle"

git push -u origin codex/improve-gpu-planner-nonempty-recommendations
```

## Review of the initial problem

The initial problem is not that the GPU/NPU full run fails. The full run can be healthy while still exposing a planning-quality issue.

Observed state:

```text
orchestrator passed
GPU/Ollama completed many rounds
NPU/OpenVINO audits were usable and non-blocking
patch_application_performed was false
GPU recommendation_count was 0
agent_review_evidence_sufficiency had ready manual-review candidates
patch-plan fallback generated candidates
```

Interpretation:

```text
The infrastructure works.
The GPU planner needs better diagnostics and/or stricter output contract enforcement.
The fallback patch-plan layer is currently required to convert evidence sufficiency into actionable manual-review plans.
```

Recommended fix direction:

```text
1. Add explicit diagnostics to GPU planner round reports:
   - json_ok
   - parse_error
   - repair_attempt_count
   - raw_recommendation_candidate_count
   - filtered_recommendation_count
   - recommendation_count
   - empty_recommendations_reason
   - evidence_ready_for_manual_patch_count

2. If evidence_sufficiency.ready_for_manual_patch_count > 0 and GPU recommendations remain empty, report:
   - empty_recommendations_reason: evidence_ready_but_no_gpu_plan
   - recommended_next_layer: build_agent_review_patch_plan.py

3. Keep fallback patch-plan generation deterministic and manual-review-only.

4. Do not force the GPU planner to invent recommendations. Prefer explicit empty-state diagnostics over hallucinated patch plans.
```

Acceptable end state:

```text
GPU recommendations may still be 0.
But the report must explain why and point to the fallback/manual-review patch-plan layer.
```

## What to send to a master AI after push

After pushing the evidence bundle, send either the branch/PR or these two files:

```text
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
```

Do not send raw `output/**` unless explicitly requested for local-only debugging.
