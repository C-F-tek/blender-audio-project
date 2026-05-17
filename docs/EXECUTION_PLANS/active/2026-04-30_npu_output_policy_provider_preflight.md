# NPU Output Policy And Provider Preflight Wiring

## Status

active

## Goal

Chain the next two NPU core/backend milestones after context and artifact write-planning wiring:

```text
exact legacy runtime output policy
provider preflight report normalization
```

## Scope

```text
Tools/npu/pipeline/artifact_paths.py
Tools/npu/pipeline/providers.py
Tools/npu/pipeline/__init__.py
Tools/npu/run_dual_ai_pipeline.py
Tools/validation/check_npu_pipeline_modules.py
Tools/validation/test_npu_pipeline_helpers.py
Tools/npu/pipeline/README.md
docs/TECH_DEBT_TRACKER.md
docs/MODULE_MAP.md
docs/DATA_FLOW.md
```

## Out of scope

```text
Blender runtime changes
Ready To Jazz migration
provider/model execution adapters
prompt text rewrite
context file generation behavior changes
full analysis JSON mutation
hand-edited generated indexes
```

## Validation commands

```powershell
python -m Tools.workflow run_npu_pipeline_helper_validation
python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links.json
python -m Tools.npu build_project_ai_index
python -m Tools.npu build_npu_code_context
git diff --check
```

Full local validation remains recommended before merge:

```powershell
python -m Tools.workflow run_local_validation_after_refactor -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
```

## Risk level

medium

## Progress log

- 2026-04-30: Created this plan for the combined output-policy and preflight-normalization phase.
- 2026-04-30: Added exact legacy dual-AI runtime output policy helpers.
- 2026-04-30: Added provider preflight normalization that does not execute providers.
- 2026-04-30: Wired the dual-AI runtime to validate legacy output writes and normalize NPU preflight reports.
- 2026-04-30: Focused NPU helper validation passed.
- 2026-04-30: Full local validation passed with `-MatrixWorkers 12 -RepeatCases 2`; report: `output/local_validation/local_validation_20260430_204657.json`.
- 2026-04-30: Regenerated AI/NPU indexes.

## Future task notes

- A later phase can create a small runtime-output manifest report that lists every written legacy/generated artifact from a run.
- Provider execution adapters should remain last; next provider-side work should be response/result normalization and failure reporting, not model calls.
- `build_ai_service_packet.py` still owns additional packet outputs and can receive exact output policy coverage in a separate focused pass.

## Result

Implemented and locally validated on branch `codex/npu-output-policy-provider-preflight`.

## Follow-up

Open a PR and keep provider execution adapters for a later phase.
