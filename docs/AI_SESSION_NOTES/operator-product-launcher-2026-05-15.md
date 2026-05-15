# Operator product launcher - 2026-05-15

## Decision

Added a small operator-facing launcher surface over the existing heap profile
runner and `CODE_PRODUCT_FULL_PATCH.md` intake.

## Purpose

The launcher lets the operator choose:

- input Markdown request;
- target repo directory;
- intermediate run-output root;
- final Documents/output root;
- heap intensity profile;
- final code-product artifact for review/apply.

It does not replace `run_heap_runtime_context_closure.py` or the profile builder.
It builds on the existing profile file and uses `analyze_code_product_artifact.py`
for deterministic review and safe apply.

## Files

```text
Tools/ai/operator_product_launcher_core.py
Tools/ai/operator_product_launcher.py
Tools/validation/run_operator_product_launcher_smoke.py
```

## Guardrail

Source writes happen only when the operator presses Apply Safe or passes
`--apply-safe`. Application still goes through the code-product intake classifier
and only applies sections already classified as safe forward-applicable.

## Broker classifier follow-up

The full run exposed a broker regression from coarse aggregation of child
`source_writes_performed` / `patch_application_performed` flags. The fix stays
in `Tools/ai/agent_runtime_tool_broker.py`: child writes under
`output/validation/.../fixture_repo` are fixture evidence, generated
report/artifact outputs under `output/` or `docs/LOCAL_VALIDATION_EVIDENCE/`
are not promoted to real repo source writes, and real patch/git/source writes
still remain guardrail-relevant unless explicitly authorized.

Full run evidence:

- stamp: `operator_launcher_full_20260515-082944`
- final status: `APPLY_REVIEW_READY`
- code execution matrix: passed
- concrete code proposal count: 15
- final product package: `C:\Users\carmi\Documents\aicarmine_operator_launcher_codex_full_operator_launcher_full_20260515-082944\aicarmine_heap_final_proposals_20260515-083004`
- code product intake result: 1 broker patch already integrated, 0 forward-safe sections, 14 manual-review/no-diff sections.
