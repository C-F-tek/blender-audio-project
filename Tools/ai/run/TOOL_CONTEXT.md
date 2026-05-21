# Tools/ai/run context

## Role

`Tools/ai/run` is the canonical packaged entrypoint for IA-Carmine / Universo IA runs.

It is the public command behind:

```powershell
python -m Tools.ai run ...
```

This package is not just a command wrapper. It is the operator-facing entrypoint where request files, profiles, runtime lanes, evidence and final product classification meet.

Current runtime route:

```text
contractor_universe
```

There is no alternate runtime selector flag. Full smoke and legacy full-run wrappers
are not standalone product entry commands. They are downstream verification or
historical compatibility code, not public entry choices from this command.

## Mandatory model contracts

Before changing this area, read:

```text
docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
```

## Responsibilities

- Accept operator run profiles and request files.
- Route execution into maintained AI runtime packages.
- Keep the public run command stable while internal packages evolve.
- Preserve clear separation between command preview, runtime execution, evidence generation and final product artifacts.
- Preserve complete/full profile lane viability rules.
- Classify final state as product, no-op/non-applicable, blocked or unviable.
- Avoid turning provider prose, report existence or bundle existence into product success.

## Complete/full profile rule

In complete/full profiles, required core lanes are not optional.

```text
valid evidence -> viable
missing evidence -> unviable
failed evidence -> unviable
degraded -> unviable
unavailable -> unviable
```

`degraded` and `unavailable` do not satisfy full mode. They are failure/unviable states for a complete run unless the profile is explicitly partial/diagnostic and says so.

## Run lifecycle model

```text
operator request / request file
-> startup/preload/context
-> heap/exchange runtime entry
-> provider lane execution
-> runtime tool/broker evidence
-> validator evidence
-> heap/exchange runtime exit
-> product/no-op/blocked/unviable classification
-> compact evidence or product artifact
```

A run that skips lifecycle stages without explicit partial/diagnostic classification is not complete.

## Output role

Outputs depend on the selected profile. They may include:

```text
runtime reports
provider reports
runtime tool/broker reports
heap/exchange lifecycle artifacts
validation references
final readable products
code-product artifacts
full-run bundle ZIPs
blocked/unviable reason reports
```

These outputs must be classified. Raw output existence does not imply product success.

## Product classification

Use `docs/REAL_PRODUCT_RUN_MODEL.md`:

```text
evidence-only run -> useful diagnostics, not product
blocked product run -> valid safe exit, not product success
real product run -> concrete operation/product + validation + reviewable artifact
unviable full run -> required lane missing/failed/degraded/unavailable
```

## Command preview boundary

A command preview is not a completed run.

```text
command rendered != run executed
return code exists != product exists
output folder exists != product exists
bundle ZIP exists != product exists
provider text exists != product exists
```

A completed run requires output artifacts, return codes, lane evidence, validation/product classification and no unviable required lane in complete/full mode.

## Relationship to other packages

`Tools/ai/run` routes into the actual runtime/product packages. Important
internal packages and downstream validators:

```text
Tools/ai/contractor_universe/TOOL_CONTEXT.md
Tools/ai/heap_exchange/TOOL_CONTEXT.md
Tools/ai/heap_runtime/TOOL_CONTEXT.md
Tools/ai/provider_mesh/TOOL_CONTEXT.md
Tools/ai/provider_runtime_blackboard/TOOL_CONTEXT.md
Tools/ai/runtime_tool/TOOL_CONTEXT.md
Tools/ai/code_product/TOOL_CONTEXT.md
Tools/ai/patch_product/TOOL_CONTEXT.md
Tools/validation/real_product/TOOL_CONTEXT.md
```

## Guardrails

- Do not silently downgrade complete/full profiles to partial behavior.
- Do not use smoke/full-run validators as the product entry command.
- Do not add parallel runtime selector switches for competing run flows.
- Do not make GPU0/NPU/provider lanes optional by implementation convenience.
- Do not report full success with degraded or unavailable required lanes.
- Do not commit raw `output/**` from a run by default.
- Do not treat final readable output as apply-ready source change unless code/patch product boundaries pass.
- Inspect `Tools/ai/dispatch.py` and this package before changing the public run command.

## Extension notes

When run profile semantics change, update together:

```text
Tools/ai/run/TOOL_CONTEXT.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
Tools/validation/real_product/TOOL_CONTEXT.md
Tools/validation/runtime_universe/TOOL_CONTEXT.md
```
