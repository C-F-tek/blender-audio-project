# ia_carmine/product/code_product context

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


## Role

`ia_carmine/product/code_product` owns code-product artifact handling: interpreter reports, edit proposals, patch artifact packs, docs follow-up, full-run bundle ZIPs and `CODE_PRODUCT_FULL_PATCH.md` intake.

This area turns validated code/diff evidence into reviewable artifacts. It must not confuse provider prose, runtime evidence or bundle transport with apply-ready code.

It concretizes:

```text
docs/REAL_PRODUCT_RUN_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Main responsibilities

- Build code interpreter reports.
- Convert reviewed plans into code edit proposals.
- Build patch artifact packs and docs follow-up artifacts.
- Build full-run bundle ZIPs as transport/export artifacts.
- Analyze `CODE_PRODUCT_FULL_PATCH.md` sections.
- Classify code-product sections as already integrated, safe-applicable, blocked, evidence-only, no-op or manual-review.
- Support reviewed safe application only through explicit operator action or downstream apply boundary.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m ia_carmine.cli build_code_interpreter_report ...
python -m ia_carmine.cli build_code_edit_proposal_from_plan ...
python -m ia_carmine.cli build_code_patch_artifact_pack ...
python -m ia_carmine.cli build_code_patch_docs_followup ...
python -m ia_carmine.cli code_product_artifact_intake ...
python -m ia_carmine.cli analyze_code_product_artifact ...
python -m ia_carmine.cli assemble_heap_final_readable_product ...
python -m ia_carmine.cli full_run_bundle_zip ...
```

## Code-product states

A `CODE_PRODUCT_FULL_PATCH.md` section should be classified explicitly:

```text
real diff/code present -> review/apply candidate
already integrated -> no-op but valid
verified target with no diff -> evidence only
missing/truncated payload -> blocked/manual review
empty product -> explicit no-op/non-applicable state
metadata only -> non-product/evidence-only unless paired with real operation
```

## Bundle boundary

`full_run_bundle_zip` is a transport/export artifact.

It may package useful product/evidence material, but it is not automatically an apply-ready source-change product.

```text
bundle exists != product exists
bundle includes evidence != apply-ready patch
bundle includes code product -> review classification still required
```

## Guardrails

- `CODE_PRODUCT_FULL_PATCH.md` is not valid merely because it exists.
- Empty or diagnostic artifacts must not be presented as apply-ready code.
- Safe apply should be explicit and review-driven.
- Source writes must be reported accurately.
- Do not commit generated runtime bundles unless explicitly Git-trackable.
- Do not treat ZIP/export artifacts as source modifications.

## Relationship to heap/matrix

```text
provider proposal -> heap evidence
lab/matrix diff/code -> code product source
code product intake -> review/apply classification
PatchKit/repo-patch-runner/manual apply -> explicit apply boundary
```

The code product should be derived from concrete diff/code captured by matrix/lab or reviewed patch evidence.

## Validation expectations

Relevant validation areas:

```powershell
python -m Tools.validation run_code_product_artifact_intake_smoke ...
python -m Tools.validation run_generated_patch_specs_empty_product_smoke ...
python -m Tools.validation check_review_pr_final_product_contract ...
python -m Tools.validation check_review_pr_product_readiness ...
```

## Extension notes

When adding a new code-product format, update parser, report rendering and smoke coverage together. Add validation under `Tools/validation/code_product`, `Tools/validation/patch_product` or `Tools/validation/real_product` when applicability changes.
