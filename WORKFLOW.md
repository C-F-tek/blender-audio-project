# Workflow

## Purpose

Root operational lifecycle for `IA-Carmine Local AI Orchestration Workbench`.

This file defines durable process and guardrails. It must not carry executable PowerShell command blocks because launcher flags, validation options and local paths change faster than root workflow policy.

Scenario-specific commands live in task runbooks under `docs/LOCAL_AI_TASKS/`. Tool-specific command catalogs are references after compact runbooks; do not treat oversized catalogs as primary operational entrypoints.

## Operational doctrine: TUTTO SU TUTTO

The full local-AI workflow is now whole-repository by default: **TUTTO SU TUTTO**.

A `-Full0To10` run must traverse every active lane that participates in project understanding, validation, provider diagnostics, broker telemetry, recommendations, patch planning, evidence and AI-to-AI handoff. `quick`, `balanced`, `deep` and `custom` are intensity profiles only; they change resource budgets, not workflow scope.

The scope of `tutto` may expand. When a new lane becomes stable, for example a new broker tool, registry validator, memory/context surface, repository-consistency check, provider diagnostic, CSV/count surface, file-line-limit report or evidence builder, it must be wired into the full-run contract or documented as explicitly excluded. Silent omission is a workflow defect.

Full0To10 is opt-out by lane: once selected, provider/probe/workload-quality, telemetry, discovery, index, CSV/count and file-line-limit lanes are included by default when relevant unless disabled with explicit `-No*` flags, diagnosed unavailable, represented as dry-run planned state or excluded by a documented operator decision.

Limitations are backlog to overcome, not reasons to skip available tools. A lane/tool is unavailable only when current code, telemetry, capability manifest, provider diagnostic or validator evidence says so.

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
docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
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
```

For code/provider/refactor work, also read the nearest tool/package README and the target source file.

## Current active work

Current compact operational bridge:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

Current branch state:

```text
master contains PR #187 unified launcher baseline
PR #193 updates operational docs from post-#187 code state
PR #192 is the next clean report-only foundation candidate
PR #191 is useful but diverged evidence to mine/regenerate/summarize
```

Do not infer bundle contents from file existence alone.

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
| 400-line/file-line-limit validation | `docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md` |
| Audio/media output guardrail | `docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md` |
| Tool discovery and promotion | `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md`, `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` |
| Markdown/script inventories | unified launcher runbook first; `Tools/validation/README.md` as catalog/reference |
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


Provider-capable Python preflight

Before provider/OpenVINO/NPU/GPU0 validation, verify that the selected Python is provider-capable, not only repository-validation-capable.

The launcher resolves Python through:

-PythonExe -> IA_CARMINE_PYTHON -> .venv -> venv -> python fallback

For OpenVINO GPU.0/NPU lanes, the selected interpreter must provide:

numpy
openvino
openvino-genai

Required local check:

$env:IA_CARMINE_PYTHON = "<repo>\.venv\Scripts\python.exe"
$env:PYTHONPATH = "<repo>"

& $env:IA_CARMINE_PYTHON -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; c=Core(); print(c.available_devices)"

A missing Python package is an environment-preflight failure, not GPU.0/NPU provider evidence. Do not interpret provider lane results until this preflight is green.
rn## Inventory policy

Use inventories before broad documentation or code refactors.

```text
Markdown inventory -> canonical docs, obsolete docs, generated/evidence docs, missing index review.
Script inventory -> scripts/tools, functions/classes/methods, descriptions, refactor discovery.
Python line-count and file-line-limit reports -> maintainability and split/refactor evidence.
Tool placement audit -> classifies canonical and non-canonical tools, including root scripts and Scripting/**.
Tool promotion guide -> defines project-tool, broker-tool and full-run-lane promotion requirements.
```

Do not commit inventory outputs from `output/**`. Commit compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` only when needed for review.

## Validation policy

For full workflow, provider, full-toolbox or code-refactor runs, prefer the unified launcher.

For focused validator work, use compact task docs first and large validator catalogs only as references.

The minimum validation evidence for a PR should state:

```text
which launcher/tool command was run
whether provider/runtime execution occurred
whether runtime broker telemetry was produced/absorbed
whether file-line-limit evidence was relevant or produced
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

## 400-line policy

Maintained documentation and source files must remain under 400 lines.

```text
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Validator:

```text
Tools/validation/check_file_line_limits.py
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```

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
400-line policy impact
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
file-line-limit evidence is available when maintainability is in scope
audio/media output is forbidden in normal AI/tooling runs
limitations are backlog to overcome, not tool-skip reasons
patch application remains explicit
long evidence is indexed by compact manifests
obsolete monolithic runbooks are not active entrypoints
```

