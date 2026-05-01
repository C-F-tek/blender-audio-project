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
| `full-context-ai-npu-golden-path.md` | End-to-end full-context AI/NPU golden path with selected chunks, selected-chunks evidence, context pack, SQLite agent state, multistep providers and controlled complexity escalation proposals. |
| `full-context-golden-docs-contract.md` | Validate that the full-context golden path is documented as a stable contract. |
| `apply-agent-review-doc-patch-plan.md` | Apply only low-risk documentation patch plans after manual review. |
| `gpu-npu-parallel-evidence-runbook.md` | Runbook for GPU/NPU evidence and planner diagnostics. |
| `improve-gpu-planner-nonempty-recommendations.md` | Task entrypoint for GPU planner non-empty recommendation diagnostics. |
| `heavy-gpu-local-ai-diagnostics-handoff.md` | Handoff for heavy local GPU diagnostics when GitHub-only agents cannot execute providers. |

## Recommended next sequence

Historical task progression:

```text
1. consistency-local-ai-contracts-and-powershell.md
2. selected-review-workflow-ai-tools-patch-specs.md
3. enrich-local-ai-memory-chunks-context-wrapper.md
4. full-context-ai-npu-golden-path.md
```

The first task checks documentation/script consistency. The second task uses the consolidated model to review workflow and AI tools for safe patch-spec candidates. The third task plans the enrichment path that lets future local runs use SQLite memory, semantic chunks and bounded context packs to reduce token pressure on large MD/code work. The fourth task exercises the current full-context golden path and asks the local AI to propose controlled complexity increases such as a new core/helper function, validator, wrapper flag, documentation contract or patch-spec promotion.

Current post-PR #106 next sequence:

```text
1. Use LOCAL_AI_CORE_TOOL_ACTIVATION as the preferred app-agnostic activation lane.
2. Use gpu-npu-parallel-evidence-runbook.md for real GPU/NPU evidence diagnostics.
3. Use agent review evidence sufficiency and patch-plan tooling for documentation-only manual-review patch plans.
4. Promote one validated proposal or patch-plan family at a time into focused implementation PRs.
```

## Runner expectation

A local command should pass one of these Markdown files as the task/instruction file to the AI runner.

The preferred project-owned command path for the full-context golden path is:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -TaskBranch codex/full-context-ai-npu-golden-run `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}" -Profile npu -BuildSemanticChunks -SelectSemanticChunks -BuildSelectedChunksEvidence -SelectedChunksEvidenceBasename full_context_golden_selected_chunks_evidence -ChunkQuery "workflow adapter local ai full context enrichment selected chunks sqlite memory provider multistep proposals validators" -ChunkPathBoost Tools/workflow,Tools/ai,Tools/validation -SelectedChunksBasename full_context_golden_selected_chunks -MaxSelectedChunks 24 -MaxSelectedChunkChars 32000 -MaxSelectedChunkExcerptChars 2500 -BuildContextPack -ContextPackProfile core_ai_backend -ContextPackBasename full_context_golden_core_ai_backend -ContextPackEvidenceBasename full_context_golden_core_ai_backend_context_pack_evidence -BuildAgentStatePacket -AgentStateBasename full_context_golden_agent_state -AgentStateObjective "Run full-context local AI/NPU golden path and propose controlled complexity escalation such as core helper, validator, wrapper flag or docs contract." -MemoryDb .\indexAI\agent_memory\agent_memory.sqlite -SaveInputsToMemoryDb -RunMultistepProviderWorkflow -RunOllamaProbe -RunNpuProbe -RunNpuDecodeSmoke -UsePrimaryAdvisoryProvider -BuildEvidence -GeneratePatchSpecs -Basename full_context_golden_local_ai_context -ProposalBasename full_context_golden_local_ai_context_proposals -EvidenceBasename full_context_golden_local_ai_context_evidence -MultistepBasename full_context_golden_local_ai_context_multistep -MultistepProposalBasename full_context_golden_local_ai_context_multistep_proposals -MultistepEvidenceBasename full_context_golden_local_ai_context_multistep_evidence'
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
