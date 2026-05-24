# AI limitations and anti-ambiguity contract

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `CODE_PRODUCT_FULL_PATCH.md` is the final patch/code product; `PLAN_PRODUCT_FULL_PATCH.md` is the final recomposed GPU1 prompt/chat product, with pointer graph and recovery/congruence as technical attachments.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


## Status

Current mandatory contract for AI agents working inside IA-Carmine / Universo IA.

This document promotes lessons from historical failure notes into a canonical, required rule set.

Historical sources:

```text
docs/AI_SESSION_NOTES/provider-universe-failure-summary-2026-05-20.md
docs/AI_SESSION_NOTES/provider-universe-chat-failure-ledger-2026-05-20.md
```

## Purpose

The repository is large enough that an AI can lose context, invent architecture, overfit to narrow smokes, or treat activity as product.

This contract prevents that by forcing every AI to distinguish:

```text
concept
code implementation
runtime execution
provider evidence
tool evidence
validation evidence
product
blocked state
```

## Core limitation

An AI assistant is not the runtime.

```text
chat memory != heap memory
status text != runtime evidence
provider prose != product
report existence != successful run
smoke pass != full product validation
activity != useful work
```

## Mandatory anti-ambiguity rule

When an AI states that something works, is complete, is validated, or is ready, it must identify the evidence class:

```text
source file inspected
command output inspected
artifact path inspected
validator report inspected
runtime state inspected
provider report inspected
code/patch product inspected
```

If it cannot name the evidence, it must say `not proven`.

## No architecture invention rule

An AI must not invent a new architecture when current models already exist.

Current canonical models:

```text
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md
```

Before proposing architecture, inspect the model-to-code map and nearest source packages.

## Lane optionality failure

A common AI failure is to make lanes optional because a narrow run, smoke or provider output succeeded.

This is forbidden.

For complete/full profiles:

```text
missing required lane evidence -> unviable
degraded required lane -> unviable
unavailable required lane -> unviable
diagnostic-only required lane -> unviable unless the profile is explicitly diagnostic/partial
```

A full smoke must not pass if a required lane is missing, degraded, unavailable or diagnostic-only.

## Provider universe failure rule

Selected provider lanes are one provider universe, not unrelated helpers.

```text
Ollama/main provider
GPU0 coworker/reviewer
NPU micro-lane/auditor
CPU validators/tooling authority
```

If one selected required provider lane is non-operational in a complete/full profile, the provider universe is unviable. The run must not continue as if product progress exists.

Correct complete-run outcome:

```text
blocked_with_reason
no fake provider blocks
no invented proposal blocks
no diagnostic-only product success
no continued peer-lane work after provider-universe unviability
```

## Explicit operator config rule

Operator-facing Universo IA runtime parameters must enter through the canonical
CLI flags and be visible before execution. A missing required parameter stops
the run before provider execution.

Valid:

```text
python -m ia_carmine.cli run ...explicit flags...
python -m ia_carmine.cli run ...explicit flags... --print-effective-config
python -m ia_carmine.cli run --emit-expanded-command
```

Invalid:

```text
hidden/autoloaded JSON
operator config JSON as a parameter source
operator run profile/preset as a parameter source
environment-only provider defaults
runtime-invented model, URL, token, memory, RAG or tooling values
child commands relying on divergent local parameter values
```

The dry-run/effective-config report must expose:

```text
effective_universe_config
field_sources
expanded_heap_command
```

If a required operator-facing parameter is missing, the run must stop before
provider execution instead of filling a silent value.

## Smoke overfitting failure

A narrow smoke proves only the property it checks.

Invalid conclusion:

```text
smoke passed -> full runtime works
```

Valid conclusion:

```text
smoke passed -> the checked contract passed under the fixture/input used
```

Full smoke must ask:

```text
for each required core lane, where is its valid evidence?
```

## Activity vs product failure

Activity is not product.

These are not sufficient:

```text
child process exists
CPU/GPU/NPU usage rises
JSON file is written
console status updates
provider text appears
runtime output folder exists
bundle ZIP exists
```

A product requires the conditions defined in:

```text
docs/REAL_PRODUCT_RUN_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
```

## Provider text failure

Provider output must become structured evidence before it can affect product decisions.

Invalid:

```text
provider says it reviewed -> accepted review
provider says patch is ready -> apply-ready patch
provider says validation passed -> validation passed
```

Valid:

```text
provider report with structured fields
broker/tool evidence when tools were requested
validator report for validation claims
code/patch product for source-change claims
```

## Diagnostic-only failure

Diagnostic-only output is useful evidence, but not product progress.

Examples:

```text
GPU0 device visibility only
NPU timeout report
NPU diagnostic-only report
provider empty response diagnostic
runtime debug lab output
file reference classification
```

A diagnostic-only artifact must not satisfy a product lane unless the profile explicitly says diagnostic/partial.

## Context overload failure

Large generated context can become mechanical CPU work instead of useful AI reasoning.

Do not push enormous generated Markdown or raw chunk dumps into live provider paths as a substitute for retrieval.

Preferred pattern:

```text
compact refs
bounded excerpts
SQLite/FTS/chunk lookup
brokered retrieval when detail is needed
compact evidence summary
```

## Evidence boundary failure

Generated runtime evidence must not become maintained source context unless compacted and intentionally indexed.

Do not commit by default:

```text
output/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
large generated chunk folders
```

Use:

```text
docs/COMPACT_EVIDENCE_MODEL.md
```

## Source-write failure

An AI must not move from idea to source write directly.

Required boundary:

```text
evidence
-> patch/code plan
-> concrete candidate
-> code/patch product
-> reviewed apply boundary
-> validation
-> commit/review
```

Use:

```text
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
```

## Completion-language rule

Avoid completion-sounding language unless full evidence exists.

Do not say:

```text
done
complete
ready
works
validated
fixed
full
```

unless the response identifies the exact source, artifact, validator or run evidence.

Prefer:

```text
updated documentation only
validated by fixture smoke only
not end-to-end proven
blocked pending full run
source not inspected
runtime not executed
provider not proven
```

## Operator block audit counter

When the operator has to stop Codex/OpenAI agent behavior because it is gaming
the script instead of doing the requested task, the failure must be recorded in
the active audit surfaces.

Update at minimum:

```text
README.md
docs/AI_SESSION_NOTES/provider-universe-chat-failure-ledger-2026-05-20.md
```

The counter must distinguish:

```text
operator-aligned fixes kept in source/docs
operator blocks required
repeated-code regressions
misleading/Codex lie evidence
systemic product-lie evidence
systemic product-lie severity score
```

Repeated-code regression means Codex reintroduces a code shape, field, gate,
wrapper or report surface that the operator already rejected or that was
already deleted in the current work window.

The count is part of the evidence of Codex operator unreliability. It is not a
runtime success metric and must not be used to claim progress.

`provider_execution_performed=false` does not prove that a command was static
or harmless. Resource/provider preflights, including lane availability checks,
must expose separate mechanics counters when they touch runtime services or
device enumeration:

```text
resource_mechanics_performed
resource_probe_performed
mechanical_not_static_read
operator_authorization_required
```

If Codex hides this distinction, the severity/incompetence counters above must
be updated instead of explaining the event away.

## Required behavior when unsure

```text
1. Read AGENTS.md.
2. Read this contract.
3. Read docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md.
4. Open nearest TOOL_CONTEXT.md.
5. Inspect dispatch.py and source.
6. Classify missing evidence as not proven or unviable.
7. Do not invent architecture or optionalize lanes.
8. Update docs only when ambiguity is found.
```

## Rule for future agents

Do not treat selected provider lanes as background helpers.

In complete/full runs, selected provider lanes are part of one provider universe. If a required lane is failed, unavailable, degraded or diagnostic-only, the complete run is unviable and must stop or block with reason.
