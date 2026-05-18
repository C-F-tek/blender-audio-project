# Local AI Entrypoint: Full-Context AI/NPU Golden Path

This is a non-interactive task file for a local AI runner.

The task exercises the complete local AI/NPU full-context workflow and asks the local AI to generate richer repository proposals while remaining report-only and manual-review-only.

## Absolute first instruction

Before planning, validating, proposing changes or producing patch specs, read and obey these files in order:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
```

Then read this file again and continue from the task contract below.

If either required file is missing, stop and report the missing file. Do not infer their contents.

## Task classification

```text
full-context local AI/NPU golden path + complexity escalation proposals
```

Default behavior:

```text
report-only
proposal-only
manual-review-only
no automatic patch apply
```

Provider execution is allowed only when explicitly requested by wrapper flags.

## Goal

Run the complete local AI context enrichment pipeline as a golden path:

```text
Task MD
  -> semantic code chunks index
  -> selected focused chunks
  -> selected chunks validator/evidence
  -> bounded context pack
  -> SQLite-backed agent state packet
  -> explicit multistep GPU/NPU provider workflow
  -> advisory packet
  -> repository proposals
  -> draft patch specs
  -> compact GitHub evidence
```

The local AI must use the enriched context to produce higher-quality proposals than a flat prompt-only run.

## Core concept

The repository now supports a controlled local AI/NPU full-context loop:

```text
semantic chunks
  reduce large-code token pressure

selected chunks
  focus context on task-relevant workflow/AI tools

context pack
  carries bounded core repository context and guardrails

SQLite-backed agent state
  carries local memory and current task state without committing private DB files

multistep provider workflow
  lets Ollama/GPU act as primary advisory behind quality gate
  keeps OpenVINO/NPU as probe / guardrail / decode diagnostic

validators/evidence
  make ignored local outputs reviewable from GitHub through compact evidence
```

## NPU knowledge-broker concept

The local AI must explicitly evaluate whether the NPU lane can become a lightweight knowledge broker without becoming the primary advisory model.

Target role:

```text
NPU as local knowledge broker / context oracle
```

Allowed responsibilities:

```text
1. Create or refresh semantic chunk indexes.
2. Rank or preselect candidate Markdown/code/document chunks for a task objective.
3. Produce compact context bundles or evidence summaries.
4. Answer constrained retrieval questions such as: which docs/files/chunks are probably relevant?
5. Run decode/probe diagnostics to verify that the local NPU stack is usable.
6. Help reduce token pressure before the Ollama/GPU advisory model receives context.
```

Forbidden responsibilities:

```text
1. Do not make final patch decisions.
2. Do not become primary advisory provider.
3. Do not apply patches or rewrite source files.
4. Do not bypass selected-chunks/context-pack validators.
5. Do not replace Ollama/GPU for creative/repository advisory reasoning.
6. Do not introduce OpenVINO GPU as the primary lane.
```

The local AI must propose a safe architecture for this concept, for example:

```text
Task objective
  -> NPU knowledge broker builds/ranks candidate chunks
  -> selected chunk validator checks budget and guardrails
  -> context pack builder adds bounded docs/status context
  -> SQLite agent state adds local memory
  -> Ollama/GPU advisory model reasons over the prepared context
  -> validators/evidence decide whether proposals are reviewable
```

This must remain report-only until a future reviewed patch spec explicitly promotes an implementation.

## Required input files

The local AI must consider:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_WORKFLOW.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/full-context-ai-npu-golden-path.md
docs/AI_CHUNKING_STRATEGY.md
docs/AI_MEMORY_POLICY.md
docs/JSON_SCHEMAS.md
Tools/ai/README.md
Tools/ai/select_semantic_code_chunks.py
Tools/ai/ai_context_pack/cli.py
Tools/ai/agent_context/state_packet/cli.py
Tools/workflow/run_local_ai_markdown_task.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_parallel_ai_provider_multistep.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
Tools/validation/check_selected_semantic_chunks.py
Tools/validation/check_repository_change_proposals.py
Tools/validation/check_patch_spec_drafts.py
Tools/validation/check_github_evidence_bundle.py
```

## Complexity escalation requirement

The local AI must not only summarize the workflow. It must propose at least one controlled complexity increase.

Allowed complexity increases:

```text
1. New core/helper function proposal
   Example: extract reusable context-enrichment planning logic from the wrapper into Tools/ai or a small helper module.

2. New validator proposal
   Example: validate adapter manifests for enrichment output consistency.

3. New wrapper flag proposal
   Example: preset profile such as -FullContextGoldenPath that expands to the explicit flags but remains report-only.

4. New documentation contract proposal
   Example: define the full-context golden path in LOCAL_AI_WORKFLOW and LOCAL_AI_RUN_BOOTSTRAP.

5. New patch-spec promotion proposal
   Example: convert a reviewed proposal into a draft patch spec under output/patch_specs only.

6. NPU knowledge-broker proposal
   Example: introduce a report-only helper that lets the NPU lane build/rank/select candidate chunks or context bundles before Ollama/GPU advisory reasoning.
```

Forbidden complexity increases:

```text
automatic patch application
automatic source rewriting
automatic merge
automatic provider execution without explicit flags
NPU promotion to advisory lane
OpenVINO GPU as primary lane
Blender runtime changes
Ready To Jazz changes
Scripting/shared/blender_compat.py changes
full analysis JSON changes
manual generated-index edits
committing SQLite memory DB files
```

## Required proposal output

The final repository proposal report must include:

```text
summary
full_context_inputs_seen
selected_chunks_summary
context_pack_summary
agent_state_summary
provider_routing_summary
npu_knowledge_broker_assessment
current_capabilities
missing_contracts
complexity_escalation_candidates
safe_next_patch_specs
validation_plan
risk_notes
recommended_execution_order
```

Each complexity escalation candidate must include:

```text
proposal_id
title
target_files
change_type: core_helper | validator | wrapper_flag | docs_contract | patch_spec_promotion | knowledge_broker | follow_up_task
rationale
evidence_source_files
expected_outputs
expected_validator_commands
risk_level: low | medium | high
requires_provider_execution: true | false
requires_manual_review: true
apply_allowed_now: false
```

## Minimum expected candidates

Produce at least these proposal families:

```text
P1: adapter manifest validator
P2: reusable enrichment-plan helper
P3: full-context golden path docs update
P4: optional wrapper preset flag
P5: selected-chunks evidence in standard local validation block
P6: NPU knowledge-broker helper / context oracle prototype
```

Do not implement these proposals in this task. Generate proposals and draft patch specs only.

## Recommended execution command

Run this task through the project-owned wrapper:

```powershell
python -m Tools.workflow run_local_ai_markdown_task `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -TaskBranch codex/full-context-ai-npu-golden-run `
  -RunnerCommand 'python -m Tools.workflow run_local_ai_task_via_pipeline -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}" -Profile npu -BuildSemanticChunks -SelectSemanticChunks -BuildSelectedChunksEvidence -SelectedChunksEvidenceBasename full_context_golden_selected_chunks_evidence -ChunkQuery "workflow adapter local ai full context enrichment selected chunks sqlite memory provider multistep proposals validators npu knowledge broker context oracle retrieval ranking" -ChunkPathBoost Tools/workflow,Tools/ai,Tools/validation,Tools/npu -SelectedChunksBasename full_context_golden_selected_chunks -MaxSelectedChunks 24 -MaxSelectedChunkChars 32000 -MaxSelectedChunkExcerptChars 2500 -BuildContextPack -ContextPackProfile core_ai_backend -ContextPackBasename full_context_golden_core_ai_backend -ContextPackEvidenceBasename full_context_golden_core_ai_backend_context_pack_evidence -BuildAgentStatePacket -AgentStateBasename full_context_golden_agent_state -AgentStateObjective "Run full-context local AI/NPU golden path and propose controlled complexity escalation such as core helper, validator, wrapper flag, docs contract or NPU knowledge broker." -MemoryDb .\indexAI\agent_memory\agent_memory.sqlite -SaveInputsToMemoryDb -RunMultistepProviderWorkflow -RunOllamaProbe -RunNpuProbe -RunNpuDecodeSmoke -UsePrimaryAdvisoryProvider -BuildEvidence -GeneratePatchSpecs -Basename full_context_golden_local_ai_context -ProposalBasename full_context_golden_local_ai_context_proposals -EvidenceBasename full_context_golden_local_ai_context_evidence -MultistepBasename full_context_golden_local_ai_context_multistep -MultistepProposalBasename full_context_golden_local_ai_context_multistep_proposals -MultistepEvidenceBasename full_context_golden_local_ai_context_multistep_evidence'
```

## Required post-run validation

Replace `<actual-run-dir>` with the real run directory.

```powershell
python -m Tools.validation check_selected_semantic_chunks `
  --repo-root . `
  --bundle .\output\ai_context_packs\full_context_golden_selected_chunks.json `
  --output .\output\validation\full_context_golden_selected_chunks_contract.json `
  --evidence-output .\docs\LOCAL_VALIDATION_EVIDENCE\full_context_golden_selected_chunks_evidence.json `
  --markdown-output .\docs\LOCAL_VALIDATION_EVIDENCE\full_context_golden_selected_chunks_evidence.md `
  --max-total-chars 32000

python -m Tools.validation check_repository_change_proposals `
  --repo-root . `
  --proposal .\output\local_ai_runs\<actual-run-dir>\pipeline\full_context_golden_local_ai_context_proposals.json `
  --output .\output\validation\full_context_golden_local_ai_context_proposals_contract.json

python -m Tools.validation check_patch_spec_drafts `
  --repo-root . `
  --manifest .\output\patch_specs\full_context_golden_local_ai_context_patch_specs_manifest.json `
  --output .\output\validation\full_context_golden_local_ai_context_patch_spec_drafts.json

python -m Tools.validation check_ai_context_pack_contract `
  --repo-root . `
  --pack .\output\ai_context_packs\full_context_golden_core_ai_backend.json `
  --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\full_context_golden_core_ai_backend_context_pack_evidence.json `
  --output .\output\validation\full_context_golden_core_ai_backend_context_pack_contract.json

python -m Tools.validation check_github_evidence_bundle `
  --repo-root . `
  --output .\output\validation\github_evidence_bundle.json

python -m Tools.validation check_validation_report_contract `
  --repo-root . `
  --output .\output\validation\validation_report_contract.json

git diff --check
```

## Allowed tracked outputs

The following compact evidence may be committed:

```text
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_core_ai_backend_context_pack_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_core_ai_backend_context_pack_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_multistep_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_multistep_evidence.md
```

Do not commit:

```text
output/**
indexAI/agent_memory/**
SQLite DB files
raw provider outputs
patch specs unless explicitly promoted in a separate reviewed PR
generated indexes changed manually
```

If semantic chunk indexes change only because the builder regenerated them, do not include them in this evidence PR unless a separate index-refresh decision is made.

## Final local report

At the end, report:

```text
branch
run directory
selected chunks evidence path
context pack evidence path
github evidence path
proposal JSON/MD paths
patch spec manifest path
validator results
provider execution statement
patch application statement
top 5 complexity escalation candidates
NPU knowledge-broker assessment
recommended next patch-spec promotion
```
