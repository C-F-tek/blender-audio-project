# Core lane completeness contract

## Status

Current normative contract for complete IA-Carmine / Universo IA runs and full smoke coverage.

This file exists to prevent documentation ambiguity where a programming AI treats required runtime lanes as optional, silently drops them from full runs, or weakens full-smoke validation into a partial smoke.

## Core rule

In complete profiles, core lanes are not optional by interpretation.

For complete/full profiles, every required core lane must produce valid evidence.

```text
valid evidence -> lane viable
missing evidence -> lane unviable
failed evidence -> lane unviable
degraded lane -> unviable
unavailable lane -> unviable
```

`degraded` is not an acceptable success state for a complete run or full smoke. It is equivalent to `unviable` for completeness.

## Complete-run semantic perimeter

A complete IA run must preserve the full semantic perimeter:

```text
request/task input
startup/preload context
heap/exchange entry
provider lanes
runtime tool/broker lane
validation lane
heap/exchange exit
product or blocked classification
compact evidence
```

Budget, intensity or profile tuning may reduce depth, token count, rounds or timeouts. It must not remove the semantic perimeter.

## Required core lanes

For complete product-oriented runs, these lanes must be viable:

| Lane | Required viable evidence |
| --- | --- |
| Request/input lane | request file, operator task, task ingress contract or equivalent input artifact |
| Startup/preload lane | context pack, memory reload, transient context or equivalent startup context evidence |
| Heap/exchange lane | runtime entry, peer/runtime manifest, exchange/lifecycle evidence, runtime exit |
| Ollama/main provider lane | provider execution evidence and structured provider output |
| GPU0 coworker lane | Ollama GPU0/Vulkan peer workload evidence plus review/refinement evidence when selected by complete profile |
| NPU micro-lane | OpenVINO NPU microtask/audit evidence when selected by complete profile |
| Runtime tool/broker lane | broker/tool usage evidence, capability manifest, tool loop evidence or explicit no-tool full-profile contract |
| CPU/validator lane | validation reports for selected product/runtime contracts |
| Product boundary lane | code/patch product, explicit no-op/non-applicable product, or blocked product reason |
| Compact evidence lane | compact evidence summary or selected evidence artifact |

If a complete profile cannot make a required lane viable, the run is not complete. It must fail or produce an explicit blocked/unviable result.

## Full smoke rule

A full smoke must not pass by omitting required lanes.

A full smoke may pass only if every required core lane has valid evidence.

These states must fail a full smoke:

```text
missing lane evidence
failed lane evidence
degraded lane
unavailable lane
provider-only prose with no structured evidence
preflight-only success
bundle-only success
artifact-exists-only success
```

A partial/diagnostic smoke may report degraded/unavailable lanes, but it must name itself partial/diagnostic. It must not be called full.

## Invalid documentation/programming patterns

Do not write docs or code that implies:

```text
GPU0 is optional because Ollama ran
NPU is optional because CPU validators ran
degraded is acceptable in complete/full mode
unavailable is acceptable in complete/full mode
provider reports are enough without runtime/tool/validator evidence
preflight passed means product exists
full-run bundle exists means product exists
full smoke means whichever lanes happened to run
quick/balanced/deep changes project perimeter
missing lane can be ignored without failing completeness
```

## Viability examples

```text
Ollama unavailable -> complete run unviable
GPU0 Ollama/Vulkan visible but no verified workload -> complete run unviable for provider-lane completeness
NPU unavailable when selected by complete profile -> complete run unviable
validator unavailable -> product cannot claim validated success
code product empty -> no-op/non-applicable or blocked product, not apply-ready
```

## Required artifact language

Reports and docs should use precise state words:

```text
viable
unviable
executed
validated
failed
blocked
not_applicable
partial_profile
```

Use `degraded` only as diagnostic detail. For complete/full pass/fail semantics, degraded means unviable.

Avoid vague words such as:

```text
ok
complete
handled
available
done
ready
```

unless the report also names the exact evidence that proves the claim.

## Relationship to Universo IA models

This contract protects the coexistence of the core models:

```text
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
```

A programming AI must not simplify one model by deleting another. The application is the coexistence of the models.

## Code/tool areas affected

```text
ia_carmine/runtime/run/
ia_carmine/providers/provider_mesh/
ia_carmine/runtime/provider_runtime_blackboard/
ia_carmine/runtime/runtime_tool/
ia_carmine/runtime/heap_exchange/
ia_carmine/runtime/heap_runtime/
ia_carmine/product/code_product/
ia_carmine/product/patch_product/
Tools/validation/real_product/
Tools/validation/provider_mesh/
Tools/validation/runtime_tool/
Tools/validation/heap_runtime/
Tools/validation/patch_product/
```

## Validator expectation

When a validator claims full coverage, it must check lane viability, not just artifact existence.

Required full-smoke question:

```text
for each required core lane, where is its valid evidence?
```

If that question cannot be answered with concrete evidence, the full smoke is not full and must fail.
