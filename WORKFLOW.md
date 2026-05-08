# Workflow

## Purpose

Root operational lifecycle for `IA-Carmine Local AI Orchestration Workbench`.

This file defines durable process and guardrails. It must not carry executable PowerShell command blocks because launcher flags, validation options and local paths change faster than root workflow policy.

## First rule: read, inspect, reuse, then change

Before proposing or editing:

```text
read current source/canonical docs
inspect existing owners and nearby helpers
reuse existing scripts/helpers first
propose the smallest safe change
then modify docs/source
```

Canonical rule:

```text
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
```

## Operational doctrine: TUTTO SU TUTTO

A `-Full0To10` run must traverse every active lane that participates in project understanding, validation, provider diagnostics, broker telemetry, recommendations, patch planning, evidence and AI-to-AI handoff.

```text
Full0To10 = whole-repository active-lane perimeter
quick/balanced/deep/custom = intensity, not reduced scope
-No* flags = explicit opt-out only
```

The scope of `tutto` may expand. When a new lane becomes stable, it must be wired into the full-run contract or explicitly excluded with rationale. Silent omission is a workflow defect.

## Code-driven reading order

Use this order unless a task file says otherwise:

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
Tools/workflow/README.md
Tools/ai/README.md
Tools/validation/README.md
nearest package/tool README
target source/doc file
```

Historical handoffs and generated evidence are context only. They do not override current source code, owner maps, launcher manifests or validation evidence.

## Canonical lifecycle

```text
read contract and source
  -> classify task
  -> reuse existing owner script/helper
  -> choose flow variant
  -> change minimal files
  -> run focused validation when available
  -> build compact evidence or patch bundle when needed
  -> record provider/runtime/media side-effect status
  -> open/update PR
  -> human review / merge
```

## Active local AI workflow

The active local AI workflow entrypoint is:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Normal workflows must not bypass the single-owner scripts.

Owner and flow maps:

```text
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
```

## Obsolete / historical monolithic runbook flag

Legacy monolithic 0-to-10 scripts or runbooks are not active operator entrypoints when they duplicate the unified launcher or owner maps.

Mark a document as historical/superseded when:

```text
it duplicates launcher commands instead of linking the runbook
it starts from an internal helper as normal operator flow
it predates strict real-run activation or provider mesh ownership
it claims automatic review PR behavior not implemented in code
it treats generated evidence as a canonical source doc
it exceeds the active Markdown line budget and has no compact index
```

Preferred replacement wording:

```text
Status: historical / superseded by the unified launcher and code-driven maps.
Current entrypoint: docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md.
Current source-derived behavior: docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md.
```

Do not delete historical docs automatically. Mark obsolete first, then prune only under an explicit documentation-pruning task.

## Command placement policy

Root workflow and README files are descriptive. They should link to command owners instead of copying executable command blocks.

| Command family | Canonical owner |
|---|---|
| Full local AI / 0-to-10 launcher commands | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Launcher manifest fields | `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Code-derived behavior | `docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md` |
| Script ownership | `docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md` |
| Data-flow variants | `docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md` |
| Validator/smoke cycles | `docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md` |
| Patch suggestion final phase | `docs/LOCAL_AI_TASKS/patch-suggestion-bundle-final-phase.md` |
| Tool discovery and promotion | `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md`, `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` |
| Markdown/script inventories | unified launcher runbook first; `Tools/validation/README.md` as catalog/reference |

If a command becomes outdated, update the owning runbook/tool README only. Do not duplicate it into root docs.

## Provider policy

```text
Full0To10 -> provider/probe/workload-quality lanes included by default unless explicitly disabled or diagnosed unavailable
GPU1/Ollama/RTX 5080 -> primary advisory lane when selected and quality-gated
GPU0/OpenVINO -> companion peer worker and tool-request producer
NPU/OpenVINO -> non-blocking micro/tool-support and diagnostics lane
Blender/audio/media runtime -> application target, frozen unless explicitly scoped
```

Provider execution is explicit when the operator selects `-Full0To10` or a provider mode/flag. It is not an additional per-lane opt-in after Full0To10 is selected.

For single-phase diagnostics, use `-NoStrictRealRunActivation` to prevent accidental full-lane promotion.

## Provider-capable Python preflight

Before provider/OpenVINO/NPU/GPU0 validation, verify the selected Python is provider-capable.

Resolution order is documented in the launcher contract. The selected interpreter must provide:

```text
numpy
openvino
openvino-genai
```

Expected IA-Carmine workstation device visibility:

```text
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

A missing Python package is an environment-preflight failure, not GPU0/NPU provider evidence.

## Inventory policy

Use inventories before broad documentation or code refactors.

```text
Markdown inventory -> canonical docs, obsolete docs, generated/evidence docs, missing index review
Script inventory -> scripts/tools, functions/classes/methods, descriptions, refactor discovery
Python line-count and file-line-limit reports -> maintainability and split/refactor evidence
Tool placement audit -> canonical and non-canonical tool classification
```

Do not commit inventory outputs from `output/**`. Commit compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` only when needed for review.

## Validation policy

For full workflow, provider, full-toolbox or code-refactor runs, prefer the unified launcher.

For focused validator work, use:

```text
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Minimum PR evidence should state:

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

## Markdown and code size policy

Maintained files must remain reviewable.

```text
preferred active runbook <= 400 lines
active Markdown hard threshold <= 500 lines
maintained source/script target <= 400 lines
```

Markdown split layout is exact:

```text
path/name.md
path/name.md/part-001.md
path/name.md/part-002.md
```

Policies:

```text
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/md-split-folder-naming-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```

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
indexAI/code_chunks/** unless explicitly requested as generated evidence
```

## PR report contract

Every PR should state:

```text
changed files
purpose
script line counts for created/modified scripts
file-size policy impact
validation run or missing
provider/runtime execution status
runtime broker telemetry status
audio/media output status
risk
follow-up
```

## Acceptance criteria for workflow docs

```text
root docs are command-light and owner-linked
commands live in owning runbooks/tool READMEs
unified launcher remains the active local-AI entrypoint
single-owner scripts are not duplicated or bypassed
Full0To10 remains opt-out by lane, not opt-in per capability
runtime broker telemetry is surfaced when relevant
file-line-limit evidence is available when maintainability is in scope
audio/media output is forbidden in normal AI/tooling runs
limitations are backlog to overcome, not tool-skip reasons
patch application remains explicit
long evidence is indexed by compact manifests
obsolete monolithic runbooks are flagged historical, not active
```
