# Local AI Entrypoint: Enrich Local AI Pipeline with Memory, Chunks and Context Packs

This is a non-interactive task file for a local AI runner.

The purpose is to make the local AI reason over the newly verified enrichment path:

```text
SQLite agent memory
semantic code chunks
bounded context packs
local Markdown task packets
multistep provider workflow
repository proposals
compact evidence
```

The local AI must integrate this reasoning into documentation and produce safe proposals for wrapper integration. It must not apply patches.

## Absolute first instruction

Before planning, editing, validating, opening a PR or generating proposals, read and obey these files in order:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
```

Then read this task file again and continue from the task contract below.

If the local AI cannot read `AGENTS.md` or `docs/LOCAL_AI_RUN_BOOTSTRAP.md`, it must stop and report the missing file. It must not infer their contents.

## Task classification

```text
docs/workflow-state + validation/evidence + proposal-only wrapper integration planning
```

Default provider execution:

```text
allowed only when explicitly requested by wrapper flags
```

Patch application:

```text
forbidden
```

The local AI may generate repository proposals and inert draft patch specs only when explicitly requested. It must not write source changes or apply patches.

## Goal

Review and integrate the project-owned enrichment strategy into the local AI workflow documentation and produce safe wrapper integration proposals.

The local AI must verify how these existing components can work together:

```text
Tools/ai/agent_state.py
Tools/ai/build_agent_state_packet.py
Tools/ai/review_agent_memory.py
Tools/ai/agent_memory_policy.py
Tools/npu/build_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
Tools/workflow/run_local_ai_markdown_task.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_parallel_ai_provider_multistep.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
```

Reference documentation:

```text
Tools/ai/README.md
docs/AI_CHUNKING_STRATEGY.md
docs/AI_MEMORY_POLICY.md
docs/AI_SMART_POLICY.md
docs/LOCAL_AI_WORKFLOW.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
```

Recent evidence to consider:

```text
docs/LOCAL_VALIDATION_EVIDENCE/issue62_multistep_heavy_work_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/issue62_multistep_provider_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/selected_review_workflow_ai_tools_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/selected_review_workflow_ai_tools_multistep_evidence.md
```

## Required reasoning

The local AI must explicitly reason about this target flow:

```text
master-AI task MD
  -> run_local_ai_markdown_task.ps1 builds local_ai_prompt.md
  -> optional build_semantic_code_chunks.py updates semantic chunk artifacts
  -> optional build_ai_context_pack.py creates bounded task context
  -> optional build_agent_state_packet.py reads SQLite memory + current files + operator notes
  -> run_local_ai_task_via_pipeline.ps1 passes prompt + task + enriched context files
  -> optional explicit run_parallel_ai_provider_multistep.ps1 produces provider evidence
  -> run_post_validation_ai_packet.ps1 builds advisory packet/proposals
  -> validators check proposals / patch specs / evidence
  -> master AI and human decide promotion
```

The local AI must identify the smallest safe integration points for the wrapper.

## Required checks

Evaluate whether the current scripts/docs already support or need proposals for:

```text
1. Extra context files passed into run_local_ai_task_via_pipeline.ps1.
2. Agent state packet generation with SQLite memory.
3. Safe save-inputs-to-memory-db behavior.
4. Semantic chunk generation before heavy review.
5. Context pack generation with bounded max-total/max-file chars.
6. Passing generated context pack / agent state / chunk manifest into ContextFile lists.
7. Recording enrichment outputs in adapter manifest.
8. Validating enriched outputs without committing ignored output/ files.
9. Avoiding token/context overflow by using chunks and bounded summaries.
10. Preserving hard guardrails: no runtime edits, no patch apply, no implicit provider execution.
```

## Required output from the local AI

The local pipeline must produce a repository proposal report with:

```text
summary
current_capabilities_found
missing_integration_points
safe_doc_update_proposals
safe_wrapper_update_proposals
validation_plan
risk_notes
recommended_execution_order
```

Each proposal must include:

```text
proposal_id
title
target_files
change_type: docs_only | wrapper_flag | manifest_field | context_enrichment | validator_needed | follow_up_task
rationale
evidence_source_files
expected_outputs
expected_validator_commands
risk_level: low | medium | high
requires_provider_execution: true | false
requires_manual_review: true
apply_allowed_now: false
```

## Preferred proposal candidates

The local AI should prioritize safe proposals such as:

```text
add -ExtraContextFile to run_local_ai_task_via_pipeline.ps1
add -BuildAgentStatePacket / -MemoryDb / -SaveInputsToMemoryDb flags
add -BuildSemanticChunks flag
add -BuildContextPack / -ContextPackProfile flags
record enrichment output paths in adapter manifest
update LOCAL_AI_WORKFLOW with enriched pipeline flow
update LOCAL_AI_RUN_BOOTSTRAP with enriched preflight commands
add a validator or evidence bundle for enriched local AI runs
```

Do not propose broad refactors in the first pass.

## Recommended local preflight commands

If the operator wants to generate enrichment artifacts before this task run, these commands are allowed and report-only:

```powershell
py .\Tools\npu\build_semantic_code_chunks.py --repo-root .

python .\Tools\ai\build_ai_context_pack.py `
  --repo-root . `
  --profile core_ai_backend `
  --basename enriched_local_ai_core_ai_backend `
  --evidence-basename enriched_local_ai_core_ai_backend_context_pack_evidence `
  --max-total-chars 96000 `
  --max-file-chars 8000

py .\Tools\ai\build_agent_state_packet.py `
  --repo-root . `
  --objective "Integrate SQLite memory, semantic chunks and context packs into the local AI wrapper/multistep workflow." `
  --memory-db .\indexAI\agent_memory\agent_memory.sqlite `
  --save-inputs-to-memory-db `
  --memory-note "Use semantic chunks and bounded context packs to reduce token pressure for large MD/code review." `
  --include-file .\AGENTS.md `
  --include-file .\docs\LOCAL_AI_RUN_BOOTSTRAP.md `
  --include-file .\docs\LOCAL_AI_WORKFLOW.md `
  --include-file .\docs\AI_CHUNKING_STRATEGY.md `
  --include-file .\Tools\ai\README.md `
  --include-file .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 `
  --include-file .\indexAI\code_chunks\semantic_code_chunks_manifest.json `
  --include-file .\output\ai_context_packs\enriched_local_ai_core_ai_backend.md
```

## Recommended execution command: enriched multistep proposal pass

Run through the project-owned local wrapper and adapter:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\enrich-local-ai-memory-chunks-context-wrapper.md `
  -TaskBranch codex/enrich-local-ai-memory-chunks-context `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}" -Profile npu -RunMultistepProviderWorkflow -RunOllamaProbe -RunNpuProbe -RunNpuDecodeSmoke -UsePrimaryAdvisoryProvider -BuildEvidence -GeneratePatchSpecs -Basename enrich_local_ai_memory_chunks_context -ProposalBasename enrich_local_ai_memory_chunks_context_proposals -EvidenceBasename enrich_local_ai_memory_chunks_context_evidence -MultistepBasename enrich_local_ai_memory_chunks_context_multistep -MultistepProposalBasename enrich_local_ai_memory_chunks_context_multistep_proposals -MultistepEvidenceBasename enrich_local_ai_memory_chunks_context_multistep_evidence'
```

## Required validation after run

Run:

```powershell
python .\Tools\validation\check_repository_change_proposals.py `
  --repo-root . `
  --proposal .\output\local_ai_runs\<actual-run-dir>\pipeline\enrich_local_ai_memory_chunks_context_proposals.json `
  --output .\output\validation\enrich_local_ai_memory_chunks_context_proposals_contract.json

python .\Tools\validation\check_patch_spec_drafts.py `
  --repo-root . `
  --manifest .\output\patch_specs\enrich_local_ai_memory_chunks_context_patch_specs_manifest.json `
  --output .\output\validation\enrich_local_ai_memory_chunks_context_patch_spec_drafts.json

python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --output .\output\validation\github_evidence_bundle.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract.json

git diff --check
```

Replace `<actual-run-dir>` manually with the generated run directory name. Do not paste `<actual-run-dir>` literally into PowerShell.

## Allowed tracked outputs

Allowed tracked outputs:

```text
docs/LOCAL_VALIDATION_EVIDENCE/enrich_local_ai_memory_chunks_context_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/enrich_local_ai_memory_chunks_context_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/enrich_local_ai_memory_chunks_context_multistep_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/enrich_local_ai_memory_chunks_context_multistep_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/enriched_local_ai_core_ai_backend_context_pack_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/enriched_local_ai_core_ai_backend_context_pack_evidence.md
```

Allowed ignored outputs:

```text
output/local_ai_runs/**
output/ai_context_packs/**
output/ai_pipeline/agent_state/**
output/validation/**
output/patch_specs/**
indexAI/code_chunks/** if generated by the chunk builder and intentionally tracked according to repository policy
indexAI/agent_memory/** should remain local unless a future policy explicitly allows tracked memory exports
```

## Forbidden changes

Do not touch:

```text
Blender runtime
Ready To Jazz
Scripting/shared/blender_compat.py
full analysis JSON
generated indexes manually without explicit chunk-builder output
provider behavior without explicit scope
prompt prose legacy
models
temperatures
automatic source patch application
automatic merge
```

Do not promote NPU to advisory.

Do not introduce OpenVINO GPU as primary lane.

Do not commit SQLite memory DB files unless a later explicit policy says they are safe to track. Treat memory DB as local/private runtime state.

## Stop conditions

Stop and report if:

```text
AGENTS.md is missing
LOCAL_AI_RUN_BOOTSTRAP.md is missing
agent_state.py or build_agent_state_packet.py is missing
semantic chunk builder is missing
context pack builder is missing
a proposal requires committing private/local SQLite memory
a proposal requires automatic source patch application
a proposal touches forbidden runtime files
```

## Final local report

At the end, report:

```text
branch name
run directory
proposal JSON path
proposal Markdown path
patch spec manifest path, if generated
evidence paths
context pack evidence paths
agent state packet paths
semantic chunk paths
validator results
provider execution statement
patch application statement
top 5 safe integration proposals
recommended next task
```
