# AI External Knowledge

## Purpose

This document records external AI-coding knowledge that is useful for this repository.

It is intentionally tool-neutral. It should guide local AI agents, remote coding assistants, review agents, and future automation without depending on one specific vendor or IDE.

This document is guidance, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
```

## Source material

This file summarizes knowledge extracted from externally supplied Markdown references, the latest technical audit report, and OpenAI official engineering articles adapted for this repository.

Source groups:

| Source | Use in this project |
|---|---|
| `agents-md-best-practices.md` | Rules for machine-readable repository guidance, command-first instructions, permission boundaries, validation commands and keeping AI docs short and actionable. |
| `Tool-AI-Reference.md` | General AI-assisted coding workflow: task decomposition, PRD/task lists, prompt logs, testing and validation loops. |
| `deep-research-report.md` | External technical audit of `blender-audio-project`: infrastructure risks, packaging, path handling, broad exception handling, import/reload risks and suggested remediation. |
| `OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md` | OpenAI Harness Engineering and Symphony concepts adapted to this repo: agent-first repositories, task/workspace orchestration, proof-of-work reports, guardrails and workflow versioning. |

## Current project adaptation: flusso unico

External AI-coding guidance is useful only after it is mapped to the current IA-Carmine operating model.

The active model is:

```text
one canonical launcher flow
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
perimeter of tutto can expand explicitly
telemetry accompanies evidence and patch plans for completeness
```

Focused validation remains useful for small edits and validator debugging. It must not be confused with the canonical full-run proof.

For broad local-AI work, proof-of-work now means:

```text
manifest
phase reports
compact evidence
patch-plan artifacts when produced
runtime tool usage telemetry
runtime tool capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
```

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
| Knowledge in repo | Store workflow, architecture, status, validation, telemetry, capability and task context in versioned Markdown/JSON. |
| Mechanical guardrails | Use validators, dry-run matrix, schema reports, status consistency checks, telemetry/capability manifests, AI-to-AI bundles and NPU helper smoke/unit/docs validators. |
| Task tracker as control plane | Use GitHub issues, patch specs, execution plans or checklist docs for complex work. |
| Workspace per task | Prefer branch/output-folder/task-scope isolation for larger automated work. |
| Proof of work | Require JSON/Markdown reports, telemetry, capability manifests, git diff summaries and validation logs. |
| Technical drift cleanup | Maintain docs, shared utilities, validators, telemetry contracts and tech debt tracker as recurring work. |

Adopted repository assets derived from those notes:

```text
AGENTS.md
WORKFLOW.md
docs/EXECUTION_PLANS/README.md
docs/TECH_DEBT_TRACKER.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
Tools/validation/check_refactor_status_consistency.py
Tools/validation/check_docs_links.py
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Current active extension of these concepts:

```text
Tools/ai/agent_runtime_tool_broker.py
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/ai/build_runtime_tool_capability_manifest.py
Tools/ai/build_full_toolbox_run_telemetry_summary.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
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
- safe commands/command owners;
- validation ownership;
- permission boundaries;
- refactoring rules;
- expected reporting format;
- telemetry/capability handoff expectations.

Keep it short enough to stay useful in AI context windows. Keep detailed task state in `docs/`, execution plans and package-level README files.

### 2. Commands must be concrete, but owned by the right document

External guidance favors copy-pasteable commands. In this repository, root/canonical docs should usually point to command owners instead of duplicating command blocks.

Command owners:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

### 3. Prefer focused validation for small edits; full-run for full proof

For AI-assisted changes, focused checks are useful when the change is narrow.

For full local-AI work, use the unified launcher and preserve `TUTTO SU TUTTO` coverage.

Focused checks must not be presented as proof that:

```text
Full0To10 passed
providers succeeded
runtime broker tools executed
capabilities were available
patch application did or did not happen
source writes did or did not happen
```

Those claims require manifest/telemetry/capability/bundle context.

Heavy Blender renders, full AI generation and long GPU workloads remain explicit human decisions.

### 4. Work in small tasks, but maintain whole-run contracts

Avoid project-wide blind rewrites.

Preferred narrow-edit workflow:

```text
specify one task
  -> inspect relevant files
  -> patch minimal files
  -> run focused validation when local execution is available
  -> report diff and line counts
  -> decide next task
```

Preferred broad local-AI workflow:

```text
unified launcher
  -> manifest
  -> phase reports
  -> evidence
  -> patch plan when produced
  -> telemetry/capability/final summary
  -> human/master-AI review
```

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
- AI prompts, providers, validators, telemetry and artifact writers should be separate.
- NPU/Ollama provider execution remains a runtime adapter concern, not a helper-contract concern.

### 6. Keep a prompt/history trail where useful

For long AI-assisted coding sessions, keep records of:

- the goal;
- the prompt/task;
- files changed;
- validation results;
- telemetry/capability summary when relevant;
- follow-up decisions.

Recommended repository-friendly locations:

```text
docs/PROJECT_STATUS_POINT.md
docs/EXECUTION_PLANS/
docs/LOCAL_VALIDATION_EVIDENCE/
indexAI/patch_library/ when explicitly scoped
output/ai_pipeline/ local ignored reports
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
- Update telemetry/capability/evidence documentation.

### Require explicit human approval

- File deletion.
- Runtime Blender behavior changes.
- Large generated script rewrites.
- Dependency additions.
- CI workflow changes.
- Long Blender renders.
- GPU-heavy generation.
- Any operation that modifies full frame-by-frame analysis data.
- Wiring staged NPU helper modules into runtime orchestrators before local validation, quality gates, telemetry/bundle visibility and regenerated indexes are green.
- Queueing or applying patch specs.

## How external knowledge should influence future work

Use this priority order:

1. preserve working Blender packages;
2. preserve the unified full-run contract;
3. validate before migration;
4. create shared utilities additively;
5. keep AI context compact;
6. report changed files and line counts;
7. keep patches small and reversible;
8. prefer patch specs when a change is mechanical and reviewable;
9. treat workflow, status, proof-of-work reports, telemetry and capability manifests as first-class repository artifacts;
10. prefer focused helper validation for narrow edits and full launcher evidence for broad claims.

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
