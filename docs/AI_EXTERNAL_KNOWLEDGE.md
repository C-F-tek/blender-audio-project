# AI External Knowledge

## Purpose

This document records external AI-coding knowledge that is useful for this repository.

It is intentionally tool-neutral. It should guide local AI agents, remote coding assistants, review agents, and future automation without depending on one specific vendor or IDE.

## Source material

This file summarizes knowledge extracted from externally supplied Markdown references and from the latest technical audit report.

Source groups:

| Source | Use in this project |
|---|---|
| `agents-md-best-practices.md` | Rules for machine-readable repository guidance, command-first instructions, permission boundaries, validation commands and keeping AI docs short and actionable. |
| `Tool-AI-Reference.md` | General AI-assisted coding workflow: task decomposition, PRD/task lists, prompt logs, testing and validation loops. |
| `deep-research-report.md` | External technical audit of `blender-audio-project`: infrastructure risks, packaging, path handling, broad exception handling, import/reload risks and suggested remediation. |

## Core principles adopted

### 1. AGENTS.md is the main machine-readable entry point

`AGENTS.md` complements `README.md`. It should contain practical instructions for AI systems:

- repository identity;
- important folders;
- safe commands;
- validation commands;
- permission boundaries;
- refactoring rules;
- expected reporting format.

Keep it short enough to stay useful in AI context windows.

### 2. Commands must be concrete

Prefer copy-pasteable commands over generic language.

Good:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
```

Bad:

```text
Run the tests.
```

### 3. Prefer focused validation

For AI-assisted changes, small checks are better than running heavy workflows every time.

Preferred quick checks:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

Heavy Blender renders, full AI generation and long GPU workloads should be explicit human decisions.

### 4. Work in small tasks

Avoid project-wide prompts and broad rewrites.

Preferred workflow:

```text
specify one task
  -> inspect relevant files
  -> patch minimal files
  -> run focused validation
  -> report diff and line counts
  -> decide next task
```

This fits the current project direction: controlled encapsulation, not broad rewrites.

### 5. Separate engine code from policy code

The external references strongly support the same architectural direction already chosen for this repository:

```text
reusable engine code
  -> Scripting/shared/

package-specific artistic policy
  -> Scripting/<package>/
```

For this project, that means:

- JSON/path/image-sequence/FFmpeg helpers should become shared infrastructure.
- Scene-specific visual choices remain inside the Blender package.
- AI prompts, providers, validators and artifact writers should be separate.

### 6. Keep a prompt/history trail where useful

For long AI-assisted coding sessions, keep records of:

- the goal;
- the prompt/task;
- files changed;
- validation results;
- follow-up decisions.

Recommended repository-friendly locations:

```text
indexAI/patch_library/
output/ai_pipeline/
docs/PROJECT_STATUS_POINT.md
```

Do not store secrets or private credentials in prompt logs.

## External audit findings mapped to current project state

The external audit report identified several issues. Some are already resolved or partially resolved in the current repository.

| Audit finding | Current status | Action |
|---|---|---|
| Missing dependency manifest | resolved/mostly resolved | `pyproject.toml` now exists. Keep it maintained. |
| Need Python 3.10+ declaration | resolved/mostly resolved | `pyproject.toml` declares Python target; keep validators aligned. |
| Need lint/type/security tooling | partially resolved | Tool config exists; local validation scripts added; full CI is still future work. |
| Fragile `sys.path` / reload patterns | active technical debt | Do not refactor destructively; centralize gradually. |
| Hardcoded workstation paths | active/accepted for some packages | Move reusable logic to config/env adapters over time. |
| Broad `except Exception` handling | active technical debt | Replace gradually in touched modules, with logging and explicit failure modes. |
| `v61b_backgood` duplicate/backup folder | active cleanup candidate | Exclude from package validation or archive intentionally. |
| Legacy Blender add-on packaging | deferred | Keep current workflow until Blender runtime validation is stable. |
| Need smoke tests/validation | partially resolved | `Tools/validation/` now provides non-invasive checks. Blender runtime checks still manual. |

## Project-specific AI operating policy

### Allowed autonomous actions

- Read files.
- Inspect repository structure.
- Add additive documentation.
- Add non-invasive validation tools.
- Add pure Python shared utilities that do not alter runtime behavior.
- Produce patch specs for review.

### Require explicit human approval

- File deletion.
- Runtime Blender behavior changes.
- Large generated script rewrites.
- Dependency additions.
- CI workflow changes.
- Long Blender renders.
- GPU-heavy generation.
- Any operation that modifies full frame-by-frame analysis data.

## How external knowledge should influence future work

Use this priority order:

1. preserve working Blender packages;
2. validate before migration;
3. create shared utilities additively;
4. keep AI context compact;
5. report changed files and line counts;
6. keep patches small and reversible;
7. prefer patch specs when a change is mechanical and reviewable.

## Not adopted

The external files mention several tool-specific integrations. This repository currently does not require tool-specific instruction files. Keep the project centered on:

```text
AGENTS.md
docs/
Tools/validation/
Scripting/shared/
patch_specs/
```
