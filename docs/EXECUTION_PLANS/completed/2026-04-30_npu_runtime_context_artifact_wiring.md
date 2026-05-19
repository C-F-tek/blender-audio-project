# NPU Runtime Context And Artifact Helper Wiring

## Status

completed

## Goal

Wire app-agnostic context-summary helpers and generated support-file write-planning helpers into `Tools/npu/run_dual_ai_pipeline.py` while preserving provider behavior, prompt prose, Blender runtime files and generated script policy.

## Scope

```text
Tools/npu/run_dual_ai_pipeline.py
Tools/validation/pipeline/npu_pipeline_modules_check/cli.py
Tools/npu/pipeline/README.md
docs/EXECUTION_PLANS/completed/2026-04-30_npu_runtime_context_artifact_wiring.md
docs/TECH_DEBT_TRACKER.md
```

## Out of scope

```text
Blender runtime files
Ready To Jazz
blender_compat.py adoption
provider runtime behavior
prompt text rewrite
context file generation behavior
full artifact writer runtime migration
full analysis JSON edits
hand-edited generated indexes
```

## Validation commands

```powershell
python -m Tools.workflow run_npu_pipeline_helper_validation
python -m Tools.workflow run_local_validation_after_refactor -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
python -m Tools.npu build_project_ai_index
python -m Tools.npu build_npu_code_context
git status
git diff --stat
```

## Progress log

- 2026-04-30: Started from clean `master` after PR #44 merged.
- 2026-04-30: Wired deterministic technical notes through `summarize_music_context`.
- 2026-04-30: Wired generated support-file writes through `PlannedArtifactWrite` and `write_planned_artifact`.
- 2026-04-30: Extended NPU helper smoke validation with runtime context-summary and artifact-write-planning checks using a temporary runtime root.
- 2026-04-30: Full local validation passed with `-MatrixWorkers 12 -RepeatCases 2`; report `output/local_validation/local_validation_20260430_203213.json`.
- 2026-04-30: Moved from `active/` to `completed/` after PR #45 was merged.

## Result

implemented, locally validated and merged

## Follow-up

A later context-file generation phase can inspect `build_music_context.py` and `build_ai_service_packet.py`. A later full artifact writer phase can cover primary generated draft/script/notes outputs, but broadening policy for `Tools/npu/` outputs must remain a separate decision. Provider adapters remain last.
