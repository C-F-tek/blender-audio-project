# Unified Local AI Refactor Launcher

This is the operator-facing runbook for `Tools/workflow/run_unified_local_ai_refactor.ps1`.

Use this file when an agent or operator needs one entrypoint for Markdown refactor, JSON/report contracts, Python/script inventory, smoke tests, validation, SQLite memory/context enrichment, provider advisory and patch-planner proposal generation.

## Absolute first instruction

Before running or modifying this launcher, read and obey:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
```

If any of these files are missing, stop. Do not infer their contents.

## What the launcher is

`run_unified_local_ai_refactor.ps1` is a console-style selector, similar to a minimal installer prompt.

The task Markdown file remains stable. The operator chooses what phases to execute.

Default task file:

```text
docs/LOCAL_AI_TASKS/docs-md-obsolete-pruning-next-step.md
```

Primary script:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

## What it must never do

The launcher is report/proposal-only by default.

It must not:

```text
apply patches automatically
commit
push
merge
force-push
rewrite history
run Blender runtime
run FFmpeg runtime
delete local artifacts unless explicit reset confirmation is supplied
commit SQLite DB files
commit output/** files
```

## Safe execution order

When multiple modes are selected, they must run in this order:

```text
baseline
  -> smoke
  -> reset
  -> validation
  -> md
  -> json
  -> python
  -> chunks
  -> context_pack
  -> agent_state
  -> official
  -> provider
  -> patch_specs
  -> evidence
  -> contract
  -> full_validation
```

This order prevents agents from using stale evidence, stale context or stale inventories.

## Mode catalog

| Mode | Purpose | Main expected tools |
|---|---|---|
| `smoke` | Fast initial health checks. | `git diff --check`, optional `Tools/workflow/startup_check.py` |
| `reset` | Plan or explicitly apply cleanup of old local generated artifacts. | internal reset planner in launcher |
| `validation` | Run broader local validation wrapper. | `Tools/workflow/run_local_validation_after_refactor.ps1` |
| `md` | Build Markdown inventory, links report and MD cleanup evidence. | `Tools/validation/build_markdown_inventory.py`, `Tools/validation/check_docs_links.py` |
| `json` | Validate JSON/report contracts from current run. | `Tools/validation/check_validation_report_contract.py` |
| `python` | Build script/tool inventory with CSV and Markdown outputs. | `Tools/validation/build_script_inventory.py` |
| `chunks` | Build semantic chunks for focused context. | `Tools/npu/build_semantic_code_chunks.py` |
| `context_pack` | Build bounded AI context packs. | `Tools/ai/build_ai_context_pack.py` |
| `agent_state` | Build agent-state packet using local files and optional SQLite memory. | `Tools/ai/build_agent_state_packet.py`, `Tools/ai/agent_state.py` |
| `official` | Run the official local AI task pipeline adapter. | `Tools/workflow/run_local_ai_task_via_pipeline.ps1` |
| `provider` | Run explicit advisory/provider path. | `Tools/workflow/run_post_validation_ai_packet.ps1`, optional Ollama/GPU advisory |
| `patch_specs` | Generate review-only patch specs from proposals. | pipeline adapter patch-spec path |
| `evidence` | Build compact evidence artifacts when requested. | pipeline adapter evidence path |
| `contract` | Validate task-scoped reports. | `Tools/validation/check_validation_report_contract.py` |
| `full_validation` | Final diff/status consistency checks. | `git diff --check`, `git status --short` |
| `all` | Run every available phase in safe order. | all of the above |

## Interactive mode

If no mode is supplied, or `-Interactive` is supplied, the launcher prints available modes and asks for a selection.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Interactive
```

Valid prompt examples:

```text
smoke,md,python,contract,full_validation
md,json,python,official,patch_specs
all
reset
```

## Command-line mode syntax

Comma-separated syntax is supported:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode smoke,md,python,contract,full_validation
```

Array-style syntax is also supported:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode smoke md python contract full_validation
```

Useful aliases:

| Alias | Canonical mode |
|---|---|
| `docs`, `markdown`, `documentazione` | `md` |
| `scripts`, `script`, `py`, `ps1` | `python` |
| `report`, `reports`, `json_contract` | `json` |
| `ollama`, `gpu`, `npu`, `provider_advisory` | `provider` |
| `patch_plan`, `patch_planner` | `patch_specs` |
| `test`, `tests`, `validate` | `validation` |
| `cleanup`, `pulizia`, `purge`, `clean` | `reset` |
| `full` | `all` |

## SQLite memory must not be forgotten

SQLite memory is part of the intended local AI enrichment flow.

Relevant task:

```text
docs/LOCAL_AI_TASKS/enrich-local-ai-memory-chunks-context-wrapper.md
```

Relevant tools:

```text
Tools/ai/agent_state.py
Tools/ai/build_agent_state_packet.py
Tools/ai/review_agent_memory.py
Tools/ai/agent_memory_policy.py
```

Relevant options supported by `build_agent_state_packet.py`:

```text
--memory-db
--memory-db-limit
--save-inputs-to-memory-db
--memory-note
--include-file
```

Default local memory DB path used by the project flow:

```text
indexAI/agent_memory/agent_memory.sqlite
```

Policy:

```text
SQLite DB is local/private runtime state.
Do not commit .sqlite/.db files.
Commit only compact evidence or documented summaries when explicitly allowed.
```

## Agent-state flow

The `agent_state` mode should create local context from:

```text
selected files
operator notes
optional SQLite memory DB
optional semantic chunk manifest
optional context pack outputs
```

The expected conceptual command is:

```powershell
python .\Tools\ai\build_agent_state_packet.py `
  --repo-root . `
  --objective "Unified local AI refactor run" `
  --memory-db .\indexAI\agent_memory\agent_memory.sqlite `
  --save-inputs-to-memory-db `
  --memory-note "Unified launcher report-only run." `
  --include-file .\AGENTS.md `
  --include-file .\docs\LOCAL_AI_RUN_BOOTSTRAP.md
```

If `agent_state` is requested and `Tools/ai/build_agent_state_packet.py` or `Tools/ai/agent_state.py` is missing, the run must stop or report the missing capability. Do not silently claim memory support.

## Semantic chunks and context packs

The enrichment flow is:

```text
master task MD
  -> optional semantic chunks
  -> optional bounded context pack
  -> optional SQLite-backed agent-state packet
  -> official local AI task pipeline
  -> optional provider/Ollama advisory
  -> proposals / patch specs / evidence
```

Relevant tools:

```text
Tools/npu/build_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
Tools/ai/build_agent_state_packet.py
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
```

## Provider and Ollama behavior

Provider execution must be explicit.

Ollama advisory is enabled by flags such as:

```text
-UseOllamaAdvisory
-UsePrimaryAdvisoryProvider
-RunMultistepProviderWorkflow
-RunOllamaProbe
```

Expected provider role:

```text
advisory/recommendation/proposal generation only
no automatic source patch application
no automatic commit/push
```

## Reset mode

`reset` is for cleaning local generated artifacts and stale run outputs.

By default it creates only a plan:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode reset `
  -ResetBeforeDate 2026-05-03 `
  -SkipGitSync `
  -NoBranch
```

Possible reset categories:

```text
output/local_ai_runs/**
output/ai_pipeline/**
output/validation/**
output/ai_context_packs/**
output/patch_specs/**
indexAI/agent_memory/** when -IncludeMemoryReset is supplied
indexAI/code_chunks/** when -IncludeGeneratedIndexReset is supplied
indexAI/project_code_chunks/** when -IncludeGeneratedIndexReset is supplied
```

Real deletion requires both:

```text
-ApplyReset
-ConfirmResetText "DELETE LOCAL AI ARTIFACTS"
```

Never delete source files, docs, scripts, branch history or tracked project files through reset mode.

## Full practical examples

Dry-run parser and smoke check:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode smoke,md,python,contract,full_validation `
  -DryRun
```

Local report-only run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode smoke,md,python,contract,full_validation `
  -SkipGitSync `
  -NoBranch
```

Full enriched proposal run with Ollama advisory and patch specs:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode md,python,chunks,context_pack,agent_state,official,provider,patch_specs,contract,full_validation `
  -UseOllamaAdvisory `
  -UsePrimaryAdvisoryProvider `
  -GeneratePatchSpecs `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Reset plan including memory/generated-index candidates:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode reset `
  -ResetBeforeDate 2026-05-03 `
  -IncludeMemoryReset `
  -IncludeGeneratedIndexReset `
  -SkipGitSync `
  -NoBranch
```

## Output contract

Every run writes:

```text
output/local_ai_runs/<stamp>_<mode>_unified/pipeline/unified_local_ai_refactor_manifest.json
```

The manifest must include:

```text
selected modes
available modes
profile/model
stamp
task file
branch/run dir
provider_execution_requested
reset_apply_requested
patch_application_performed=false
patch_specs_requested
build_evidence_requested
context_files
report_files
phase_status
phase_reports
warnings
errors
```

## Stop conditions

Stop or report failure if a requested phase needs a missing tool:

```text
agent_state requested but build_agent_state_packet.py or agent_state.py is missing
chunks requested but build_semantic_code_chunks.py is missing
context_pack requested but build_ai_context_pack.py is missing
provider requested but run_post_validation_ai_packet.ps1 is missing
official requested but run_local_ai_task_via_pipeline.ps1 is missing
reset apply requested without exact confirmation text
working tree dirty and -AllowDirty was not supplied
```

## Agent instruction

A lazy agent must not skip this mapping.

Before proposing changes to this launcher or to the local AI flow, explicitly check:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
Tools/ai/build_agent_state_packet.py
Tools/ai/agent_state.py
Tools/npu/build_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
docs/LOCAL_AI_TASKS/enrich-local-ai-memory-chunks-context-wrapper.md
```

If a tool is referenced in documentation but not available in the repository, either remove that reference or mark it clearly as future/optional. Do not describe non-existent capabilities as active.
