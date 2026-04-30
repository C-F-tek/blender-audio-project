# AI External Knowledge

## Purpose

This document records external AI-coding knowledge that is useful for this repository.

It is intentionally tool-neutral. It should guide local AI agents, remote coding assistants, review agents, and future automation without depending on one specific vendor or IDE.

## Source material

This file summarizes knowledge extracted from externally supplied Markdown references, the latest technical audit report, and OpenAI official engineering articles adapted for this repository.

Source groups:

| Source | Use in this project |
|---|---|
| `agents-md-best-practices.md` | Rules for machine-readable repository guidance, command-first instructions, permission boundaries, validation commands and keeping AI docs short and actionable. |
| `Tool-AI-Reference.md` | General AI-assisted coding workflow: task decomposition, PRD/task lists, prompt logs, testing and validation loops. |
| `deep-research-report.md` | External technical audit of `blender-audio-project`: infrastructure risks, packaging, path handling, broad exception handling, import/reload risks and suggested remediation. |
| `OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md` | OpenAI Harness Engineering and Symphony concepts adapted to this repo: agent-first repositories, task/workspace orchestration, proof-of-work reports, guardrails and workflow versioning. |

## OpenAI Harness Engineering and Symphony notes

Dedicated note file:

```text
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
```

Main adopted concepts:

| Concept | Project translation |
|---|---|
| Repository agent-first | Keep `AGENTS.md`, `docs/`, validators, status markers and reports synchronized. |
| AGENTS.md as index | Keep `AGENTS.md` concise and point to structured docs rather than making it an encyclopedia. |
| Knowledge in repo | Store workflow, architecture, status, validation and task context in versioned Markdown/JSON. |
| Mechanical guardrails | Use validators, dry-run matrix, schema reports, status consistency checks and NPU helper smoke/unit/docs validators. |
| Task tracker as control plane | Use GitHub issues, patch specs, execution plans or checklist docs for complex work. |
| Workspace per task | Prefer branch/output-folder/task-scope isolation for larger automated work. |
| Proof of work | Require JSON/Markdown reports, git diff summaries and validation logs. |
| Technical drift cleanup | Maintain docs, shared utilities, validators and tech debt tracker as recurring work. |

Adopted repository assets derived from those notes:

```text
WORKFLOW.md
docs/EXECUTION_PLANS/README.md
docs/TECH_DEBT_TRACKER.md
Tools/validation/check_refactor_status_consistency.py
Tools/validation/check_docs_links.py
Tools/workflow/run_local_validation_after_refactor.ps1
Tools/workflow/run_npu_pipeline_helper_validation.ps1
```

Current active extension of these concepts:

```text
Tools/npu/pipeline/                  app-agnostic NPU helper contracts
Tools/validation/check_npu_pipeline_modules.py
Tools/validation/check_npu_pipeline_helper_tests.py
Tools/validation/check_npu_pipeline_docs.py
```

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

Keep it short enough to stay useful in AI context windows. Keep detailed task state in `docs/`, execution plans and package-level README files.

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

AI pipeline checks:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

NPU helper checks:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
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
  -> Tools/ai/pipeline/
  -> Tools/npu/pipeline/

package-specific artistic policy
  -> Scripting/<package>/
```

For this project, that means:

- JSON/path/image-sequence/FFmpeg helpers should remain shared infrastructure.
- Scene-specific visual choices remain inside the Blender package.
- AI prompts, providers, validators and artifact writers should be separate.
- NPU/Ollama provider execution remains a runtime adapter concern, not a helper-contract concern.

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
output/local_validation/
docs/PROJECT_STATUS_POINT.md
docs/EXECUTION_PLANS/
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
| Need smoke tests/validation | partially resolved | `Tools/validation/` now provides non-invasive checks, including NPU helper package validation. Blender runtime checks still manual. |

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
- Wiring staged NPU helper modules into runtime orchestrators before local validation and regenerated indexes are green.

## How external knowledge should influence future work

Use this priority order:

1. preserve working Blender packages;
2. validate before migration;
3. create shared utilities additively;
4. keep AI context compact;
5. report changed files and line counts;
6. keep patches small and reversible;
7. prefer patch specs when a change is mechanical and reviewable;
8. treat workflow, status and proof-of-work reports as first-class repository artifacts;
9. prefer focused helper validation before broad full-run validation.

## Not adopted

The external files mention several tool-specific integrations. This repository currently does not require tool-specific instruction files. Keep the project centered on:

```text
AGENTS.md
docs/
Tools/validation/
Tools/workflow/
Tools/ai/pipeline/
Tools/npu/pipeline/
Scripting/shared/
patch_specs/
```
