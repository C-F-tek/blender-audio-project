# Workflow

## Purpose

Root operational lifecycle for `IA-Carmine Local AI Orchestration Workbench`.

This file defines durable process and guardrails. It must not carry executable PowerShell command blocks because launcher flags, validation options and local paths change faster than root workflow policy.

Scenario-specific commands live in task runbooks under `docs/LOCAL_AI_TASKS/`. Tool-specific commands live next to the tool package, for example `Tools/validation/README.md` and `Tools/npu/pipeline/README.md`.

## Operational doctrine: TUTTO SU TUTTO

The full local-AI workflow is now whole-repository by default: **TUTTO SU TUTTO**.

A `-Full0To10` run must traverse every active lane that participates in project understanding, validation, provider diagnostics, broker telemetry, recommendations, patch planning, evidence and AI-to-AI handoff. `quick`, `balanced`, `deep` and `custom` are intensity profiles only; they change resource budgets, not workflow scope.

The scope of `tutto` may expand. When a new lane becomes stable, for example a new broker tool, registry validator, memory/context surface, repository-consistency check, provider diagnostic or evidence builder, it must be wired into the full-run contract or documented as explicitly excluded. Silent omission is a workflow defect.

Full0To10 is opt-out by lane: once selected, provider/probe/workload-quality, telemetry, discovery, index and CSV/count lanes are included by default unless disabled with explicit `-No*` flags, diagnosed unavailable, represented as dry-run planned state or excluded by a documented operator decision.

## Canonical lifecycle

```text
read contract
  -> classify task
  -> build inventories/context when useful
  -> choose one scope
  -> change minimal files
  -> validate locally when available
  -> build compact evidence or patch bundle when needed
  -> record provider/runtime/media side-effect status
  -> open/update PR
  -> human review / merge
```

## Required reading

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
README.md
WORKFLOW.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/WORKFLOW_HELPER_SCRIPTS_POLICY.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
Tools/validation/README.md
```

For code/provider/refactor work, also read the nearest tool/package README and the target source file.

## Current active work

```text
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Mode: review-only until explicit human instruction
```

The compact operational bridge is:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

The bundle is not committed to the repository. Do not infer its contents from file existence alone.

## Canonical local AI workflow

The active local AI workflow entrypoint is:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Use the runbook for current `-Full0To10`, `-RunIntensity`, interactive, reset, provider, memory, patch-spec, evidence and validation examples.

Legacy monolithic 0-to-10 scripts/runbooks are not an active operator path. Historical details belong in git history or compact evidence, not in parallel maintained entrypoints.

## Command placement policy

Root workflow and README files are descriptive. They should link to command owners instead of copying executable command blocks.

| Command family | Canonical owner |
|---|---|
| Full local AI / 0-to-10 launcher commands | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Launcher manifest fields | `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Current operational bridge | `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` |
| Current code/tool/evidence flow | `docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` |
| Refactor/reuse planning | `docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md` |
| Recent telemetry baseline | `docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` |
| Runtime broker telemetry resolved context | `docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` |
| Audio/media output guardrail | `docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md` |
| Tool discovery and promotion | `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md`, `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` |
| Markdown/script inventories | `Tools/validation/README.md` and unified launcher runbook |
| NPU helper validation | `Tools/npu/pipeline/README.md` |
| Patch-spec workflow | `docs/PATCH_SPEC_WORKFLOW.md` |
| Local checkout/bootstrap notes | `docs/LOCAL_AI_RUN_BOOTSTRAP.md` |

If a command becomes outdated, update the owning runbook/tool README only. Do not duplicate it into root docs.

## Provider policy

```text
Full0To10 -> provider/probe/workload-quality lanes included by default unless explicitly disabled or diagnosed unavailable
Ollama -> GPU/CUDA -> primary advisory provider lane for Full0To10 when available and quality-gated
OpenVINO -> NPU -> probe / guardrail / decode diagnostic lane for Full0To10 when available
Blender/audio/media runtime -> application target, frozen unless explicitly scoped
```

Provider execution is explicit when the operator selects `-Full0To10` or a provider mode/flag. It is not an additional per-lane opt-in after Full0To10 is selected.

A full 0-to-10 run must not silently degrade if provider quality routing is missing. It must build workload quality routing evidence or fail clearly; dry-run may mark the routing report as planned.

## Audio/media output policy

Normal AI/tooling workflows are report/evidence workflows, not media-generation workflows.

Forbidden unless explicitly scoped as application-domain runtime work:

```text
audio playback
audio export
WAV/MP3/AAC conversion
FFmpeg encode or mux operation
Blender render
video generation
media output side effect
```

If a non-application run produces audio/media output, classify it as a guardrail breach and record:

```text
phase
tool
path
tracked/ignored state
how to disable it
```

Detailed policy:

```text
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

## Preflight policy

Before local execution, the operator should verify:

```text
correct branch
fast-forward sync where appropriate
clean or intentionally dirty working tree
Python interpreter/venv selection
PYTHONPATH rooted at repository root
ignored output/cache/state files not staged
```

The unified launcher resolves Python through `-PythonExe`, `IA_CARMINE_PYTHON`, `.venv`, `venv` and fallback `python`. It also sets `PYTHONPATH` to the repository root.

## Inventory policy

Use inventories before broad documentation or code refactors.

```text
Markdown inventory -> canonical docs, obsolete docs, generated/evidence docs, missing index review.
Script inventory -> scripts/tools, functions/classes/methods, descriptions, refactor discovery.
Tool placement audit -> classifies canonical and non-canonical tools, including root scripts and Scripting/**.
Tool promotion guide -> defines project-tool, broker-tool and full-run-lane promotion requirements.
```

Do not commit inventory outputs from `output/**`. Commit compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` only when needed for review.

## Validation policy

For full workflow, provider, full-toolbox or code-refactor runs, prefer the unified launcher.

For focused validator work, use `Tools/validation/README.md` as the command catalog.

The minimum validation evidence for a PR should state:

```text
which launcher/tool command was run
whether provider/runtime execution occurred
whether runtime broker telemetry was produced/absorbed
whether audio/media output occurred
where the manifest/report/evidence is located
whether patch application occurred
what remains unvalidated locally
```

## Evidence and patch bundles

Compact evidence belongs under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Full local reports remain ignored under `output/**` unless a compact Git-trackable evidence artifact is intentionally generated.

Patch application remains manual-review-only unless the user explicitly requests apply. Patch-spec generation may be requested through the unified launcher, but source application must remain a separate reviewed action.

## Index regeneration

Regenerate generated indexes only after structural source/doc/workflow changes when the index is required for review or the next run.

Generated index files are not manually maintained source. Do not hand-edit generated chunks or manifests.

## Guardrails

Do not do without explicit approval:

```text
delete files
force-push or rewrite history
merge to master/protected branch
change secrets, permissions, billing or visibility
deploy production
run heavy Blender/GPU workloads outside an explicitly selected full/provider workflow
run audio playback/export, FFmpeg encode/mux, Blender render or media generation
change provider/model execution from Full0To10 opt-out semantics to silent opt-in
```

Never commit:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
raw checkpoints
large full analysis JSON outside compact evidence policy
generated audio/video/media output
```

## PR report contract

Every PR should state:

```text
changed files
purpose
script line counts for created/modified scripts
validation run or missing
provider/runtime execution status
runtime broker telemetry status
audio/media output status
risk
follow-up
```

## Acceptance criteria for workflow docs

```text
root docs are command-free
commands live in owning runbooks/tool READMEs
unified launcher remains the active local-AI entrypoint
Full0To10 remains opt-out by lane, not opt-in per capability
runtime broker telemetry is surfaced when relevant
audio/media output is forbidden in normal AI/tooling runs
patch application remains explicit
long evidence is indexed by compact manifests
obsolete monolithic runbooks are not active entrypoints
```
