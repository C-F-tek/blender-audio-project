# Evidence Chunk 0006/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `1379`
- line_end: `1480`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0005.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0007.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: Final validation before push; Review of the initial problem; What to send to a master AI after push. Preview: ## Final validation before push Run standard validation: ```powershell python .\Tools\validation\check_python_syntax.py ` --repo-root . ` --output .\output\validation\python_syntax.json python .\Tools\validation\check_validation_report_contract.py ` --repo-roo...

## Context before

  --bundle .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.json `
  --output .\output\validation\gpu_planner_nonempty_recommendations_evidence_validation.json
```

Inspect validation:

```powershell
Get-Content .\output\validation\gpu_planner_nonempty_recommendations_evidence_validation.json -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, bundle_count, errors, warnings
```


## Chunk content

````md
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

```

````

## Context after

### `Tools/ai/run_agent_review_decision_loop.py`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.py`
- Size bytes: `14608`
- SHA-256: `e996e04b636a7aea8076d9115c2ee12424bb8f5bbb2cb59bb0e67322b80e914c`
- Content included: `True`
- Content truncated: `False`

```text
#!/usr/bin/env python3
