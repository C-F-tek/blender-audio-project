# Tools/git context

## Role

`Tools/git` contains controlled Git helper wrappers used by IA-Carmine workflows. This area is intentionally small and should not become a general-purpose Git automation layer.

Canonical invocation:

```powershell
python -m Tools.git <tool> [tool args...]
```

The source of truth for public Git helper names is `Tools/git/dispatch.py`.

## Current tools

```text
auto_push_generated_artifacts
auto_push_generated_data
```

Both tools dispatch to maintained PowerShell wrappers under `_powershell/`.

## Safety model

Git helpers are high-risk because they can publish repository state. Keep these rules explicit:

```text
never use git add .
never commit output/**
never commit *.db / *.sqlite / *.sqlite-wal / *.sqlite-shm
never commit renders/**
never commit indexAI/code_chunks/** or indexAI/project_code_chunks/**
never force-push or rewrite history without explicit operator confirmation
```

Use targeted staging and clear evidence of what is being pushed.

## When to use

Use `Tools.git` helpers only when the workflow has already produced reviewed, Git-trackable artifacts or documentation and the operator explicitly requests publication.

For normal development, prefer manual commands:

```powershell
git status --short
git add <explicit files>
git diff --cached --check
git commit -m "..."
git push origin <branch>
```

## Safe extension rules

- Add only narrow, auditable Git helpers.
- Keep destructive operations out unless gated by explicit confirmation.
- Keep wrappers under `_powershell/` and register them in `dispatch.py`.
- Print branch, status and staged files before any commit/push operation.
