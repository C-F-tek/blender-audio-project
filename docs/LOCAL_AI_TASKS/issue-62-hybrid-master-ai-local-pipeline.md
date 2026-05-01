# Local AI Entrypoint: Issue 62 Hybrid Master-AI and Local Pipeline Runner

This is a non-interactive task file for a local AI runner.

The task implements the hybrid operating model where chat/GitHub-only AI remains the master/control-plane while the local AI/NPU prototype pipeline handles heavier local report/proposal/evidence work.

## Absolute first instruction

Before planning, editing, validating or opening a PR, read and obey these files in order:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
```

Then read this task file again and continue from the task contract below.

If the local AI cannot read `AGENTS.md` or `docs/LOCAL_AI_RUN_BOOTSTRAP.md`, it must stop and report the missing file. It must not infer their contents.

## Task source

GitHub issue:

```text
#62 - Local AI task: define hybrid master-AI and local pipeline runner model
```

Repository:

```text
C-F-tek/blender-audio-project
```

Start from updated `master`.

## Task classification

```text
docs/workflow-state + workflow adapter
```

Default provider execution:

```text
not required
not allowed implicitly
```

## Goal

Document and implement the current hybrid model:

```text
Chat / GitHub-only AI / Codex-style control plane
  -> strategic planning, review, issue/PR orchestration, small edits, human-facing summaries

Local AI/NPU prototype pipeline
  -> heavy local context processing, validators, advisory packets, repository proposals, compact evidence

Human / master AI
  -> approves promotion from advisory/proposal outputs to patch specs, reviewed replacements, apply or merge
```

This is not an immediate full replacement of Codex/GitHub-only AI. It is a staged migration that reduces token-heavy chat work by moving large local analysis into the project-owned pipeline.

## Required implementation

Add or update:

```text
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_local_ai_markdown_task.ps1
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_WORKFLOW.md
docs/LOCAL_AI_TASKS/README.md
```

The adapter must:

```text
accept -PromptFile, -TaskFile and -RunDir
call existing report-only/proposal-only repository tools
write outputs under output/local_ai_runs/<run>/pipeline/
produce advisory packet/proposal outputs
not apply patches
not execute providers unless explicit provider flags are passed
keep NPU as probe/guardrail/decode diagnostic
keep Ollama/GPU as primary advisory only behind quality gate
```

## Preferred runner command shape

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\issue-62-hybrid-master-ai-local-pipeline.md `
  -TaskBranch codex/hybrid-local-pipeline-runner `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}"'
```

## Staged migration model

```text
Stage 0: GitHub/chat master AI controls workflow; local pipeline prepares evidence and proposals.
Stage 1: Local pipeline consumes Markdown task entrypoints and produces advisory packet/proposals.
Stage 2: Local pipeline emits draft patch specs from validated proposals.
Stage 3: Reviewed patch specs can be dry-run validated.
Stage 4: Apply/merge remains explicit and human/master-AI controlled.
Stage 5: Future local automation may replace more chat/GitHub-only work after quality gates mature.
```

## Allowed changes

Allowed:

```text
add report-only workflow adapter
update local AI runner examples
update local AI workflow docs
update task index docs
add this task entrypoint
```

## Forbidden changes

Do not touch:

```text
Blender runtime
Ready To Jazz
Scripting/shared/blender_compat.py
full analysis JSON
generated indexes manually
provider behavior without explicit scope
prompt prose legacy
models
temperatures
provider orchestration semantics
automatic source patch application
automatic merge
automatic provider promotion
```

Do not introduce OpenVINO GPU as primary lane.

Do not promote NPU to advisory.

## Required validation

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\issue-62-hybrid-master-ai-local-pipeline.md `
  -TaskBranch codex/hybrid-local-pipeline-runner `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}"' `
  -DryRun

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 `
  -PromptFile .\docs\LOCAL_AI_TASKS\issue-62-hybrid-master-ai-local-pipeline.md `
  -TaskFile .\docs\LOCAL_AI_TASKS\issue-62-hybrid-master-ai-local-pipeline.md `
  -RunDir .\output\local_ai_runs\issue62_adapter_smoke `
  -DryRun

python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

If the adapter is run without `-DryRun`, it must remain report-only/proposal-only unless explicit provider flags are passed.

## Acceptance criteria

- Hybrid master-AI/local-pipeline model is documented.
- Codex/GitHub-only AI is not described as obsolete.
- Project-owned pipeline adapter is present.
- Markdown wrapper examples prefer the project-owned adapter.
- No implicit provider execution is introduced.
- No automatic patch apply is introduced.
- Validation commands pass or failures are documented with exact blockers.

## Final local report

At the end, report:

```text
branch name
changed files
line counts for created/modified scripts
validator results
whether providers were executed
whether patch apply occurred
PR URL, if opened
```
