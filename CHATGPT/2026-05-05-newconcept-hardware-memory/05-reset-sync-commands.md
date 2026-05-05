# 05 — Reset and sync commands

## Purpose

Local operator commands to clean stale local state, keep only intentional changes, and synchronize the branch before continuing with the new hardware/memory architecture work.

This is a command reference for the maintainer. It does not run automatically.

## Safe reset of staged mistakes

If too many files were staged by mistake:

```powershell
git restore --staged .
git status --short
```

Then add only explicit files.

## Reset one local uncommitted CHATGPT handoff if not wanted

If the local handoff file is staged but should not be committed:

```powershell
git restore --staged .\CHATGPT\next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
git status --short
```

If it should be discarded entirely:

```powershell
git restore .\CHATGPT\next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
git status --short
```

If it is untracked and should be deleted locally:

```powershell
Remove-Item .\CHATGPT\next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
git status --short
```

## Commit the local handoff if intentional

If the handoff is correct and should be pushed:

```powershell
git add .\CHATGPT\next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
git commit -m "docs(chatgpt): add refactor reuse full-run handoff"
git push origin codex/unified-local-ai-refactor-launcher
```

## Sync branch after GitHub-only commits

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git checkout codex/unified-local-ai-refactor-launcher
git pull --ff-only origin codex/unified-local-ai-refactor-launcher
git status --short
git log --oneline -8
```

Expected after clean sync:

```text
git status --short is empty or contains only intentional local files
latest commits include CHATGPT hardware/memory concept docs
```

## Validate doc-only sync

```powershell
git diff --check

python .\Tools\validation\check_docs_links.py `
  --repo-root . `
  --output .\output\validation\docs_links_after_chatgpt_hardware_memory_docs.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract_after_chatgpt_hardware_memory_docs.json
```

## Forbidden broad add

Never use:

```powershell
git add .
git add output
git add .\output
```

Never commit:

```text
output/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
*.db
*.sqlite
*.sqlite3
renders/**
raw audio/video/media
```

## Pull conflict stop condition

If `git pull --ff-only` fails:

```powershell
git status --short
git log --oneline --decorate -8
git branch --show-current
```

Do not merge manually. Resolve by inspecting local commits/changes first.

## After current run finishes

Collect and upload/send:

```text
bundle ZIP
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
decision loop JSON/MD
recommendations JSON/MD
patch plan JSON/MD
script/function/class/method inventory CSV/MD/JSON
Python line-count CSV/MD
repository consistency reports
provider diagnostics
ai_workload_report_quality
auto-discovery/index repair reports when present
```

Then paste the compact run status block used by `FULL_RUN_UNICA_TUTTO_SU_TUTTO.md`.
