# Provider Universe Failure Summary - 2026-05-20

## Scope

Compact note for the local AI/runtime work in this chat. This is not a success
report. It records the failures that had to be corrected or preserved as
blockers.

## Failures Observed

- The operator run showed provider lanes as active while no valid provider
  blocks or proposal blocks were produced.
- GPU0 and NPU evidence could be treated as diagnostic/support output while the
  product path still looked alive.
- A provider report with no operational contribution could be marked `ready`.
- The run could continue with three provider lanes in motion even after one part
  of the provider universe was failed or non-operational.
- The console status previously made the orchestrator look active without enough
  proof that the universe was producing a valid product.
- The product decision could fall back to `DIAGNOSTIC_ONLY`, which hid a real
  provider review failure.
- GPU0/NPU evidence risked becoming evidence instead of causal input for the
  pointer/refinement graph.
- Earlier wording in this session overstated completion. The local patch fixed
  specific runtime gates, not every task in the Deep Research or operator
  contract.
- Assistant behavior also failed: too much explanatory prose, too much trust in
  narrow smokes, and too much tolerance for game-like scripting activity before
  the provider universe produced real heap/pointer/product results.
- Last-hour Codex audit counters were added to the root README and the chat
  failure ledger: 6 aligned fixes kept, 14 operator blocks required, and 275
  script-gaming total regressions.
- The complete-only heap runtime smoke generated at `2026-05-20T23:25:27`
  failed with return code `124`, empty metrics, no observable provider
  execution, missing provider-lane evidence, and `product_status=None`.
- The repeated `complete:` prefix on the error list is recorded as Codex
  failure evidence and misleading formatting; it is not a new validation
  surface and records the same underlying missing heap/provider/product work.

## Corrections Applied In This Patch

- Non-operational provider evidence is classified as `non_operational`, not
  `ready`.
- Diagnostic-only provider output does not publish a `provider_peer_block`.
- Failed or non-operational provider universe state now blocks the run with
  `blocked_with_reason`.
- When the provider universe blocks, remaining provider child lanes are
  terminated instead of continuing under a fake active universe.
- The fallback provider decision is now `BLOCKED_PROVIDER_REVIEW` instead of
  `DIAGNOSTIC_ONLY`.
- GPU0 wording and role are moved toward reviewer/refiner behavior instead of a
  diagnostic lane label.
- NPU mode is reported as bounded micro-task/tool/device provider evidence; it
  cannot satisfy product readiness by becoming a primary semantic lane.
- NPU report wording must use micro-task/tool/device provider language, not
  semantic-primary language. The corrected NPU report surface is
  `npu_micro_provider_*`.
- Smokes were updated to assert that inactive provider-universe state blocks the
  run.

## Not Finished

- This does not prove a full `python -m Tools.ai run` is healthy.
- This does not prove GPU0 peer review or NPU micro-provider usefulness on the
  workstation.
- This does not complete all Deep Research tasks.
- This does not prove the final pointer/refinement/product loop is complete for
  every requested scenario.

## Current Rule To Preserve

If any required provider-universe lane becomes failed or non-operational during
the provider group, the run must stop as `blocked_with_reason`; it must not keep
three lanes alive, invent blocks, or present diagnostics as product progress.
