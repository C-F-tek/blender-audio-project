# Hybrid Local Pipeline Runner Evidence

- Generated at: `2026-05-01T10:56:06.3872199+02:00`
- Branch: `codex/hybrid-local-pipeline-runner`
- HEAD: `04db51978813f1ce3af9b1a462213a1a0019a590`
- Issue: `#62`
- PR: `#63`
- Run dir: `output/local_ai_runs/20260501_105413_issue-62-hybrid-master-ai-local-pipeline`
- Provider execution requested: `False`
- Provider execution performed by adapter: `False`
- Patch application performed: `False`
- Passed: `True`

## Outputs

- Wrapper manifest: `output/local_ai_runs/20260501_105413_issue-62-hybrid-master-ai-local-pipeline/local_ai_run_manifest.json`
- Adapter manifest: `output/local_ai_runs/20260501_105413_issue-62-hybrid-master-ai-local-pipeline/pipeline/local_ai_task_pipeline_adapter_manifest.json`
- Packet Markdown: `output/local_ai_runs/20260501_105413_issue-62-hybrid-master-ai-local-pipeline/pipeline/local_ai_task_pipeline.md`
- Proposals Markdown: `output/local_ai_runs/20260501_105413_issue-62-hybrid-master-ai-local-pipeline/pipeline/local_ai_task_pipeline_proposals.md`

## Validation

- `./output/validation/python_syntax.json`: exists=`True` passed=`True` kind=`python_syntax`
- `./output/validation/docs_links.json`: exists=`True` passed=`True` kind=`docs_links`
- `./output/validation/validation_report_contract.json`: exists=`True` passed=`True` kind=`validation_report_contract`
- `./output/validation/local_ai_task_pipeline_repository_change_proposals_contract.json`: exists=`True` passed=`True` kind=`repository_change_proposal_contract`

## Runtime/provider statement

- No Blender runtime execution.
- No FFmpeg execution.
- No automatic patch apply.
- No implicit provider execution.
- NPU remains probe/guardrail/decode diagnostic.
- Ollama/GPU remains primary advisory only behind quality gate.
