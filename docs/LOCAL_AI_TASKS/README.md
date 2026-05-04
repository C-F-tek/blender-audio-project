# Local AI Tasks

Markdown entrypoints for non-interactive local AI runs.

Every task file must point back to:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
```

If a task conflicts with `AGENTS.md`, preserve hard guardrails and stop with a conflict report.

## First entrypoints

| User intent | Start here |
|---|---|
| Full toolbox, 0-10, tutto su tutto, multi-phase, full repository run | `full-toolbox-0-to-10-semi-automatic-procedure.md` |
| Code/script refactor, helper reuse, function discovery, line-count inventory | `code-refactor-0-to-10-procedure.md` |
| Markdown refactor inside the 0-10 refactor flow | `code-refactor-0-to-10-procedure.md` plus `code-refactor-md-lane-extension.md` |
| Documentation cleanup, Markdown pruning, obsolete/redundant MD review | `../DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` plus `build_markdown_inventory.py` |
| GPU/NPU evidence diagnostics | `gpu-npu-parallel-evidence-runbook.md` |
| Full-context local AI/NPU golden path | `full-context-ai-npu-golden-path.md` |

## Current maintained task files

| File | Purpose |
|---|---|
| `full-toolbox-0-to-10-semi-automatic-procedure.md` | Canonical full-toolbox process: evidence -> recommendations -> decision -> patch plan -> patch bundle -> explicit apply -> validation -> PR. |
| `code-refactor-0-to-10-procedure.md` | Canonical code/refactor process with line counts, script/tool discovery, helper reuse and compact evidence. |
| `code-refactor-md-lane-extension.md` | Markdown/documentation refactor lane to run inside the canonical code-refactor 0 -> 10 procedure. |
| `docs-md-obsolete-pruning-next-step.md` | Follow-up triage task for obsolete/superseded Markdown after the entrypoint reduction baseline. |
| `gpu-npu-parallel-evidence-runbook.md` | GPU/NPU evidence and planner diagnostics. |
| `full-context-ai-npu-golden-path.md` | Full-context local AI/NPU path with chunks, context packs, memory state, multistep providers and proposals. |
| `full-context-golden-docs-contract.md` | Contract validation for the full-context golden path. |
| `apply-agent-review-doc-patch-plan.md` | Apply low-risk documentation patch plans after manual review. |
| `consistency-local-ai-contracts-and-powershell.md` | Compare local AI contract docs with PowerShell runners. |
| `selected-review-workflow-ai-tools-patch-specs.md` | Review workflow/AI tools for safe patch-spec candidates. |
| `enrich-local-ai-memory-chunks-context-wrapper.md` | Plan memory, semantic chunks, context packs and wrapper enrichment. |
| `improve-gpu-planner-nonempty-recommendations.md` | GPU planner non-empty recommendation diagnostics. |
| `heavy-gpu-local-ai-diagnostics-handoff.md` | Handoff for heavy local GPU diagnostics when GitHub-only agents cannot execute providers. |

## Historical task files

These remain useful as past state or scoped handoffs, but should not become the first reading path unless explicitly referenced:

```text
issue-57-docs-congruence-cleanup.md
issue-62-hybrid-master-ai-local-pipeline.md
post-pr*.md
next-chat-handoff-*.md
shared-*-next-task-*.md
project-complete-*.md
```

Historical files may be marked `superseded` or `historical` in future cleanup, but deletion requires explicit user approval.

## Inventory commands used by current flows

```powershell
python .\Tools\validation\build_markdown_inventory.py --repo-root . --output .\output\validation\markdown_inventory.json --markdown-output .\output\validation\markdown_inventory.md
python .\Tools\validation\build_script_inventory.py --repo-root . --output .\output\validation\script_inventory.json --csv-output .\output\validation\script_inventory.csv --markdown-output .\output\validation\script_inventory.md
```

`build_script_inventory.py` complements the older Python line-count CSV: it adds descriptions, functions, classes, methods, language and category for the full script/tool surface.

## Runner expectation

Project-owned local runner pattern:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\<task>.md `
  -TaskBranch codex/<task-branch> `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}"'
```

Generated outputs under `output/**` are local-only unless converted into compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`.
