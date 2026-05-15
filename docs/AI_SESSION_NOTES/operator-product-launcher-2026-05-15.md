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

## Code product quality correction

The `operator_launcher_full_20260515-082944` product was not acceptable as a
final code product: it listed 15 matrix targets but 14 sections had no captured
diff. The good Day 0 reference remains the #300 artifact:
`C:\Users\carmi\Documents\aicarmine_heap_final_proposals_20260514-195340\CODE_PRODUCT_FULL_PATCH.md`,
about 4100 lines and 180k characters of actual diff/code.

Correction applied:

- `concrete_code_proposals` now means only targets with real worktree diff or
  new-file content;
- verified no-diff targets remain in `verified_targets` evidence;
- `CODE_PRODUCT_FULL_PATCH.md` renders only effective diff/code sections;
- the full code product renderer recaptures full worktree diffs when available
  instead of relying on truncated matrix sketches;
- intake detects truncation markers only when they are standalone payload markers,
  not when a source diff contains the marker string as code.

Follow-up run evidence:

- stamp: `operator_launcher_product_quality_20260515-0844`
- final status: `APPLY_REVIEW_READY`
- matrix target count: 15
- verified target count: 15
- effective code product count: 7
- final code product: 7 sections, 7 `diff --git` blocks, 0 placeholder sections
- intake result: 7/7 already integrated, 0 forward-safe sections, 0 needs-review sections.

## Empty code product handling

The launcher cycle check run produced a valid non-applicable
`CODE_PRODUCT_FULL_PATCH.md`: matrix passed, 15 targets were verified, but
`Effective code product count` was 0. The intake classifier now treats this as
`empty_code_product=true`, `passed=true`, `all_integrated=true`, with
apply-safe as a no-op and no source/patch/git writes.

This keeps malformed artifacts blocked while allowing an intentional "nothing
to apply" product to close cleanly through the launcher.

## Repo-wide refactor/OOB run correction

The launcher full run for a repo-wide refactor/OOB request initially produced an
empty effective code product because GPU1 repeated a non-allowlisted invented
path. GPU0/NPU and the deterministic gate rejected it correctly, but the final
operator artifact was not useful.

Correction applied:

- GPU1 refactor/OOB prompts now require `TARGET_FILES` copied verbatim from the
  source allowlist;
- refinement feedback blacklists rejected/non-allowlisted source references;
- repeated non-allowlisted references can terminate as `NO_PATCHABLE_TARGET`;
- the final code product renderer includes reviewable worktree source diffs
  under `Tools/`, `docs/`, and `config/` instead of relying only on matrix
  target sketches.

Follow-up run evidence:

- stamp: `operator_launcher_repo_refactor_oob_20260515-0950`
- final status: `APPLY_REVIEW_READY`
- matrix passed: true
- effective code product count: 5
- worktree extra product count: 2
- final code product: 5 sections, 5 `diff --git` blocks, no empty-product
  marker
- launcher intake/apply-safe: 5/5 already integrated, 0 forward-safe sections,
  0 needs-review sections, no source/patch/git writes.

Older temp artifact check:

- input: `C:\Users\carmi\AppData\Local\Temp\CODE_PRODUCT_FULL_PATCH.md`
- intake/apply-safe: 7/7 already integrated, 0 forward-safe sections,
  0 needs-review sections, no source/patch/git writes.
