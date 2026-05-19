# Root surface context

## Role

The repository root contains the identity contracts, packaging metadata, global agent instructions and top-level navigation files for IA-Carmine.

Root files are high-impact because AI agents usually read them first. Keep them concise, current and linked to deeper context files.

## Current identity

The repository name is historical. The root README identifies the project primarily as:

```text
IA-Carmine Local AI Orchestration Workbench
```

Blender/audio remains the first application domain, but the active architecture is local AI orchestration, validation, telemetry, evidence and guardrail workflows.

## Important root files

| File | Role |
| --- | --- |
| `AGENTS.md` | Primary contract for AI assistants and local agents. |
| `CHATGPT.md` | ChatGPT/GPT operating contract. |
| `README.md` | Human-readable project identity and current orientation. |
| `WORKFLOW.md` | Workflow orientation when present/current. |
| `pyproject.toml` | Python packaging metadata and dev tool configuration. |
| `.gitignore` | Runtime/generated artifact exclusion policy. |

## Packaging and tooling metadata

`pyproject.toml` describes this as a Python project for Blender audio-reactive scripting, audio analysis and AI-assisted visual package workflows. It also defines dev tooling such as Ruff, Mypy, Pylint and Bandit.

Do not infer runtime entrypoints from `pyproject.toml` alone. Use current dispatchers and documentation:

```text
Tools/TOOL_CONTEXT.md
Tools/ai/dispatch.py
Tools/validation/dispatch.py
Tools/workflow/dispatch.py
```

## Reading order

Use this order for a fresh AI session:

```text
AGENTS.md
CHATGPT.md
README.md
docs/TOOL_CONTEXT.md
docs/SCRIPT_SURFACE_CONTEXT.md
Tools/TOOL_CONTEXT.md
nearest package TOOL_CONTEXT.md
current task or target source
```

When a conflict exists, current source and current dispatcher behavior beat stale docs. Report conflicts before editing.

## Root scripts policy

After the tool-surface refactor, new root-level scripts should be avoided. Prefer package-owned CLIs under `Tools/**` or product scripts under `Scripting/**` depending on role.

If a root-level executable file is introduced, document why it cannot live under:

```text
Tools/<area>/...
Scripting/<package>/...
docs/LOCAL_AI_TASKS/...
```

## Safety policy

Root-level changes can affect all agents. Keep them small and validated.

Do not add secrets, local credentials, raw runtime output, database dumps, generated render artifacts or large provider transcripts to root files.
