# Tools context index

## Purpose

This directory contains the operator-facing and AI-facing tool surface for IA-Carmine. The post-refactor convention is to avoid launching scattered legacy files directly and to prefer package dispatchers:

```powershell
python -m Tools.<area> <tool> [tool args...]
```

The shared dispatcher implementation is `Tools/tool_dispatch.py`. Area dispatchers map stable tool names to concrete package CLIs or controlled PowerShell wrappers.

## Areas

| Area | Context file | Canonical command surface | Role |
| --- | --- | --- | --- |
| `Tools/ai` | `Tools/ai/TOOL_CONTEXT.md` | `python -m Tools.ai <tool>` | Heap runtime, provider lanes, context/memory, code product, patch product, AI-to-AI bundle artifacts. |
| `Tools/validation` | `Tools/validation/TOOL_CONTEXT.md` | `python -m Tools.validation <tool>` | Validators, smoke tests, gates, contracts, readiness checks. |
| `Tools/workflow` | `Tools/workflow/TOOL_CONTEXT.md` | `python -m Tools.workflow <tool>` | Operator workflow wrappers, GUI/shell surfaces, startup and orchestration scripts. |
| `Tools/npu` | `Tools/npu/TOOL_CONTEXT.md` | `python -m Tools.npu <tool>` | NPU/provider mesh support, context builders, music/code/manual packets. |
| `Tools/docs` | `Tools/docs/TOOL_CONTEXT.md` | `python -m Tools.docs <tool>` | Documentation hygiene, repo/tool surface audit, Markdown split/coherence helpers. |
| `Tools/git` | `Tools/git/TOOL_CONTEXT.md` | `python -m Tools.git <tool>` | Controlled Git helper wrappers for generated artifacts/data. |
| `Tools/repo_patch_runner` | `Tools/repo_patch_runner/TOOL_CONTEXT.md` | `python -m Tools.repo_patch_runner <tool>` | Controlled repository patch runner utilities. |

## Operational model

The intended flow is not a linear script chain. The tool surface supports a shared runtime universe:

```text
request -> startup context/memory reload -> heap blackboard -> brokered tools
-> provider lanes -> validation/matrix/lab -> code product or blocked diagnosis
```

For new work, prefer reusing an existing area dispatcher and package. Do not create new top-level one-off scripts when a package-owned CLI can be added under an existing area.

## Known context-source conflict

The operating contract references a root `CHATGPT.md`, but the current checkout does not contain that file. `CHATGPT/README.md` is present and should be treated as the available project-local ChatGPT context source until a root `CHATGPT.md` is intentionally restored or the contract is updated. Do not invent missing contract files; record the mismatch and continue only from files that exist in the checkout.

## Safety defaults

Do not commit runtime artifacts, databases, render outputs, or ignored generated folders:

```text
output/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```

Use generated evidence bundles or session notes only when they are explicitly intended to be Git-trackable documentation.