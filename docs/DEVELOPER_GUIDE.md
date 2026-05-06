# Developer Guide

## Purpose

Practical development guide for `IA-Carmine Local AI Orchestration Workbench`.

The repository slug remains `blender-audio-project`, but the active architecture is local AI orchestration, validation, evidence, telemetry, provider diagnostics, tool governance and manual-review patch planning.

Blender/audio remains the first application domain. It is not the boundary of current backend/tooling development.

This guide is not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Current doctrine

```text
master contains PR #187 unified launcher baseline
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
400-line policy applies to maintained docs and source files
limitations are backlog to overcome, not reasons to skip available tools
```

## Recommended workflow

1. Read `AGENTS.md`, `CHATGPT.md` and `CHATGPT/README.md`.
2. Read `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md`.
3. Read `docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md`.
4. Read `README.md`, `WORKFLOW.md` and `docs/README.md`.
5. Read `docs/MODULE_MAP.md` and `docs/DATA_FLOW.md`.
6. Read the nearest package/tool README and inspect the target source file.
7. Make the smallest coherent change.
8. Keep maintained docs/source files under 400 lines.
9. Validate locally when available, or state GitHub-only limits honestly.
10. Report changed files, purpose, validation status, risks and script line counts.

## Working with run-unica tooling

Primary local-AI entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Primary runbook:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Supporting wrappers must not become new first entrypoints unless explicitly promoted into the launcher contract.

When a change affects run-unica evidence, provider diagnostics, patch plans or patch specs, keep the handoff complete:

```text
launcher manifest
phase_status / phase_reports
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/index/discovery/file-line evidence when relevant
```

## Working with AI pipeline code

Current AI pipeline code is under:

```text
Tools/ai/
Tools/ai/pipeline/
```

Read before editing:

```text
docs/AI_PIPELINE_ARCHITECTURE.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md
docs/AI_GUARDRAILS_VALIDATION_GUIDE.md
Tools/ai/pipeline/refactor_status.py
```

Keep pipeline modules:

```text
provider-agnostic
import-safe
fixture/dry-run testable
report-oriented
schema/validator friendly
under 400 lines or split by responsibility
```

Provider output must not bypass validation, telemetry/capability context or manual review.

## Working with AI/NPU tooling

For `Tools/npu/` and `Tools/npu/pipeline/`:

- keep helper modules provider-free unless explicitly scoped;
- keep prompts separate from validators;
- keep generated artifacts separate from maintained source;
- preserve deterministic fallbacks;
- keep model outputs out of source modules;
- document expected inputs/outputs;
- keep NPU as probe/guardrail/decode diagnostic unless a quality-gated promotion changes the contract.

Read:

```text
docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md
Tools/npu/pipeline/README.md
```

Do not wire helpers into runtime orchestrators without focused validation, broad launcher validation, quality gates, telemetry/bundle visibility and maintainer approval.

## Working with validators

Validators live under:

```text
Tools/validation/
```

New validators should be:

```text
report-only by default
non-destructive
schema_version/kind based
clear about source_writes_performed and patch_application_performed
safe under GitHub-only review
under 400 lines or split by responsibility
```

Current line-limit validator:

```text
Tools/validation/check_file_line_limits.py
```

Large validator catalogs are references. Keep compact task notes for new validator contracts when useful.

## Working with Blender/application code

Blender/audio scripts remain application-domain assets.

Rules:

- keep local paths configurable;
- isolate Blender-version compatibility;
- avoid destructive refactors of working packages;
- separate object creation, materials, animation, render settings and encoding where practical;
- do not run Blender, FFmpeg or media output during normal AI/tooling work;
- test inside Blender only when the task explicitly enters application-domain runtime work.

Reference areas:

```text
Scripting/v61b/
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/
Scripting/shared/
```

## Working with root tools

Root scripts such as these are application-domain tools, not default broker tools:

```text
analyze_wav.py
build_track_summary.py
normalize_scene_spec.py
```

Future direction:

```text
importable service function
  -> CLI wrapper
  -> explicit input/output paths
  -> predictable JSON/report output
```

Preserve existing CLI behavior unless a task explicitly allows a breaking change.

## Working with generated data

Do not commit:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
indexAI/code_chunks/**
raw provider outputs
generated audio/video/media output
```

Treat `indexAI/` as generated context unless a specific curated source file is clearly documented.

Index repair/regeneration is plan/report-first unless explicitly requested.

## Documentation update map

| Change | Documentation to update |
|---|---|
| New launcher mode/manifest field | `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md`, launcher runbook, current code-flow guide. |
| New validator | Compact task note if needed, `docs/AI_ARTIFACT_SCHEMAS.md`, `docs/MODULE_MAP.md`, nearest README. |
| New run-unica evidence lane | `docs/DATA_FLOW.md`, `docs/LOCAL_AI_WORKFLOW.md`, `docs/LOCAL_AI_TASKS/README.md`. |
| New AI pipeline module | `docs/AI_PIPELINE_ARCHITECTURE.md`, `docs/AI_PIPELINE_REFACTOR_STATUS.md`, nearest package README. |
| New NPU helper | `Tools/npu/pipeline/README.md`, `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md`. |
| New shared Blender utility | `Scripting/shared/README.md`, `docs/SHARED_SCRIPTING_UTILITIES.md`, `docs/MODULE_MAP.md`. |
| New application-domain entrypoint | nearest package README and relevant Blender/application docs. |
| New JSON/report contract | `docs/AI_ARTIFACT_SCHEMAS.md` or compact contract doc; avoid making `docs/JSON_SCHEMAS.md` a primary entrypoint. |

## 400-line rule

Maintained documentation and source files must stay under 400 lines.

```text
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Use `Tools/validation/check_file_line_limits.py` for report-only measurement.

## Commit/report style

Use concise commits, for example:

```text
docs(ai): align module map with current validation flow
feat(validation): add file line limit report
refactor(ai): split provider report helpers
fix(blender): add node compatibility fallback
test(ai): add pipeline helper validation
```

Every implementation report should include:

```text
changed files
purpose
line counts for created/modified scripts
400-line policy impact
validation status or GitHub-only limitation
provider/runtime/media execution status
risks
follow-up
```

## Minimal validation checklist

| Change type | Minimum validation |
|---|---|
| Markdown/docs only | Link/path review and file-line-limit check when maintainability is in scope. |
| Pure Python utility | Python syntax/import-focused validation. |
| Validator | Focused validator run plus JSON parseability/report contract review. |
| AI pipeline | Focused AI pipeline validation and dry-run matrix when local execution is available. |
| NPU helper | Focused NPU helper validation; no provider proof unless provider run is explicit. |
| Blender module | Blender runtime smoke only when explicitly scoped. |
| FFmpeg utility | Print command or short encode only when explicitly scoped. |
| Generated package | Application-domain package validation, not normal AI/tooling validation. |

## Not specified

- Formal release automation.
- Branch protection policy.
- Complete Blender headless CI.
- Full JSON schema enforcement for every artifact.
- Automatic patch application from run-unica outputs.
