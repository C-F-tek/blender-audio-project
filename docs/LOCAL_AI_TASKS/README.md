# Local AI Tasks

This folder contains Markdown task entrypoints for non-interactive local AI runs.

A local AI runner can start from one task file without a chat prompt. Each task file must point back to:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
```

The local AI must always read those files first and treat them as the repository contract before acting.

## Hybrid operating model

The current model is hybrid, not a hard cutover.

```text
Chat / GitHub-only AI / Codex-style control plane
  -> strategic planning, review, issue/PR orchestration, small edits, merge only after explicit permission

Local AI/NPU prototype pipeline
  -> heavy local context processing, validators, advisory packets, repository proposals, compact evidence

Human / master AI
  -> approves promotion from advisory/proposal outputs to patch specs, reviewed replacements, apply or merge
```

This keeps token-heavy local work inside the local pipeline while preserving master-AI control over review and promotion decisions.

## Current task entrypoints

| File | Purpose |
|---|---|
| `issue-57-docs-congruence-cleanup.md` | Complete the documentation/workflow-state cleanup after selective planner merge. |
| `issue-62-hybrid-master-ai-local-pipeline.md` | Define and validate the hybrid master-AI plus local pipeline runner model. |
| `consistency-local-ai-contracts-and-powershell.md` | Compare local AI contract docs with PowerShell runners and produce consistency proposals/evidence. |
| `selected-review-workflow-ai-tools-patch-specs.md` | Multistep review of `Tools/workflow/*.ps1` and `Tools/ai/*.py` to propose safe patch-spec candidates. |
| `enrich-local-ai-memory-chunks-context-wrapper.md` | Integrate the reasoning for SQLite memory, semantic chunks, context packs and wrapper/multistep enrichment. |

## Recommended next sequence

Run these tasks in order:

```text
1. consistency-local-ai-contracts-and-powershell.md
2. selected-review-workflow-ai-tools-patch-specs.md
3. enrich-local-ai-memory-chunks-context-wrapper.md
```

The first task checks documentation/script consistency. The second task uses the consolidated model to review workflow and AI tools for safe patch-spec candidates. The third task plans the enrichment path that lets future local runs use SQLite memory, semantic chunks and bounded context packs to reduce token pressure on large MD/code work.

## Runner expectation

A local command should pass one of these Markdown files as the task/instruction file to the AI runner.

The preferred project-owned command path is:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\enrich-local-ai-memory-chunks-context-wrapper.md `
  -TaskBranch codex/enrich-local-ai-memory-chunks-context `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}" -Profile npu -RunMultistepProviderWorkflow -RunOllamaProbe -RunNpuProbe -RunNpuDecodeSmoke -UsePrimaryAdvisoryProvider -BuildEvidence -GeneratePatchSpecs -Basename enrich_local_ai_memory_chunks_context -ProposalBasename enrich_local_ai_memory_chunks_context_proposals -EvidenceBasename enrich_local_ai_memory_chunks_context_evidence -MultistepBasename enrich_local_ai_memory_chunks_context_multistep -MultistepProposalBasename enrich_local_ai_memory_chunks_context_multistep_proposals -MultistepEvidenceBasename enrich_local_ai_memory_chunks_context_multistep_evidence'
```

The runner should not require interactive chat. The task file contains:

```text
required reading order
task scope
guardrails
allowed changes
validation commands
expected PR/report content
stop conditions
```

External runners may still be used by a master/control-plane AI during the transition, but the project-owned local runner should be preferred for heavy local analysis and proposal generation.

## Hard rule

If a task file conflicts with `AGENTS.md`, preserve `AGENTS.md` hard guardrails and stop with a conflict report.
