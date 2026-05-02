# Local Validation Evidence Bundle

- Generated at: `2026-05-02T19:41:25`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `False`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `5`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/validation/python_syntax_heavy_prototype_20260502-193942.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/analysis/code_interpreter_heavy_prototype_20260502-193942.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `112`

### `output/patch_specs/agent_review_code_patch_plan_heavy_prototype_20260502-193942.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_code_patch_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `30`
- Warnings: `['static recommendations capped at 30 of 80']`

### `output/validation/code_edit_proposal_heavy_prototype_20260502-193942_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_edit_proposal_smoke`
- Passed: `False`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Errors: `['code_edit_proposal_build.proposal must be a non-empty object']`

## Artifact manifest

- `output/validation/python_syntax_heavy_prototype_20260502-193942.json` exists=`True` size=`31633` suffix=`.json` preview_chars=`1500`
- `output/analysis/code_interpreter_heavy_prototype_20260502-193942.json` exists=`True` size=`1168235` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/agent_review_code_patch_plan_heavy_prototype_20260502-193942.json` exists=`True` size=`64237` suffix=`.json` preview_chars=`1500`
- `output/validation/code_edit_proposal_heavy_prototype_20260502-193942_smoke.json` exists=`True` size=`1086` suffix=`.json` preview_chars=`1056`

## Included artifact contents

### `output/analysis/code_interpreter_heavy_prototype_20260502-193942.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7244`
- SHA-256: `011bb1227e8eab6bcef3b473c11a71d02ab3e87b9e8bd18baea5489687f6614b`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `241`
- Parsed files: `241`
- Total lines: `63350`
- Total functions: `2087`
- Total classes: `76`
- Risk signals: `36`
- TODO/FIXME markers: `21`
- Recommendation count: `112`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` — `2197` lines, risk `high`
- `Tools/npu/run_dual_ai_pipeline.py` — `1773` lines, risk `high`
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines, risk `high`
- `Scripting/v61b_backgood/scene_tuning_panel.py` — `1097` lines, risk `high`
- `Scripting/v61b/animation.py` — `1079` lines, risk `high`
- `Scripting/v61b_backgood/animation.py` — `1019` lines, risk `high`
- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
- `Scripting/v61b_backgood/asset_setup.py` — `725` lines, risk `medium`
- `Scripting/v61b_backgood/physics_setup.py` — `720` lines, risk `medium`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `714` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Scripting/v61b/materials.py` — `657` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `628` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_selective_execution_plan.py` — `618` lines, risk `medium`
- `Tools/ai/build_repository_change_proposals.py` — `582` lines, risk `medium`
- `Tools/ai/build_ai_context_pack.py` — `575` lines, risk `medium`
- `Tools/ai/run_pipeline_dry_run_matrix.py` — `573` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `562` lines, risk `medium`

## Recommendations

- `code_static_001` `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_002` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected
- `code_static_003` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_004` `Scripting/v61b/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_005` `Scripting/v61b/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_006` `Scripting/v61b/config.py` risk `medium`: medium-size Python module
- `code_static_007` `Scripting/v61b/encode_ffmpeg_v61b.py` risk `medium`: large functions detected, static risk calls detected
- `code_static_008` `Scripting/v61b/encode_image_sequence_v61b.py` risk `medium`: complex functions detected
- `code_static_009` `Scripting/v61b/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_010` `Scripting/v61b/hotpatch/accent_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_011` `Scripting/v61b/hotpatch/diagnostics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_012` `Scripting/v61b/hotpatch/fog_patch.py` risk `medium`: large functions detected
- `code_static_013` `Scripting/v61b/hotpatch/hero_material_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_014` `Scripting/v61b/hotpatch/render_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_015` `Scripting/v61b/main_v61b.py` risk `medium`: large functions detected
- `code_static_016` `Scripting/v61b/materials.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_017` `Scripting/v61b/physics_setup.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_018` `Scripting/v61b/render_setup.py` risk `medium`: large functions detected, complex functions detected
- `code_static_019` `Scripting/v61b/scene_tuning_panel.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_020` `Scripting/v61b/scene_utils.py` risk `medium`: complex functions detected
- `code_static_021` `Scripting/v61b_backgood/animation.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_022` `Scripting/v61b_backgood/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_023` `Scripting/v61b_backgood/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_024` `Scripting/v61b_backgood/encode_image_sequence_v61b.py` risk `medium`: complex functions detected
- `code_static_025` `Scripting/v61b_backgood/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_026` `Scripting/v61b_backgood/hotpatch/hero_material_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_027` `Scripting/v61b_backgood/hotpatch/render_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_028` `Scripting/v61b_backgood/main_v61b.py` risk `medium`: large functions detected
- `code_static_029` `Scripting/v61b_backgood/materials.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_030` `Scripting/v61b_backgood/physics_setup.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_031` `Scripting/v61b_backgood/render_setup.py` risk `medium`: large functions detected, complex functions detected
- `code_static_032` `Scripting/v61b_backgood/scene_tuning_panel.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_033` `Scripting/v61b_backgood/scene_utils.py` risk `medium`: complex functions detected
- `code_static_034` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_035` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_036` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_037` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_038` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_039` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_040` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/patch_specs/agent_review_code_patch_plan_heavy_prototype_20260502-193942.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `22836`
- SHA-256: `53bf42e9eeff35e0695e767a2002b213f77780715d5efa095f7de1da8a1c2185`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Review Code Patch Plan

- Passed: `True`
- Apply mode: `report_only_manual_review_code_patch_plan`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `30`
- Contract-drift plan count: `0`
- Static-code plan count: `30`

## Inputs

- `code_contract_drift_report`: `output/validation/code_contract_drift.json`
- `line_count_csv`: `output/validation/python_line_count_heavy_prototype_20260502-193942.csv`
- `line_count_csv_loaded`: `True`
- `code_interpreter_report`: `output/analysis/code_interpreter_heavy_prototype_20260502-193942.json`
- `code_interpreter_report_loaded`: `True`

## Plans

### `code_static_001`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `high`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py`
- Rationale: Static code interpreter recommendation `code_static_001` flagged `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` for manual review: large Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 2197 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_002`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/shared/image_sequence.py`
- Rationale: Static code interpreter recommendation `code_static_002` flagged `Scripting/shared/image_sequence.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 161 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_003`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `high`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/animation.py`
- Rationale: Static code interpreter recommendation `code_static_003` flagged `Scripting/v61b/animation.py` for manual review: large Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 1079 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_004`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/asset_setup.py`
- Rationale: Static code interpreter recommendation `code_static_004` flagged `Scripting/v61b/asset_setup.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 725 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_005`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/atmosphere_setup.py`
- Rationale: Static code interpreter recommendation `code_static_005` flagged `Scripting/v61b/atmosphere_setup.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 554 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_006`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/config.py`
- Rationale: Static code interpreter recommendation `code_static_006` flagged `Scripting/v61b/config.py` for manual review: medium-size Python module.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 439 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_007`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/encode_ffmpeg_v61b.py`
- Rationale: Static code interpreter recommendation `code_static_007` flagged `Scripting/v61b/encode_ffmpeg_v61b.py` for manual review: large functions detected, static risk calls detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 399 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_008`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/encode_image_sequence_v61b.py`
- Rationale: Static code interpreter recommendation `code_static_008` flagged `Scripting/v61b/encode_image_sequence_v61b.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 395 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_009`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/fog_dynamics.py`
- Rationale: Static code interpreter recommendation `code_static_009` flagged `Scripting/v61b/fog_dynamics.py` for manual review: large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 392 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_010`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/hotpatch/accent_patch.py`
- Rationale: Static code interpreter recommendation `code_static_010` flagged `Scripting/v61b/hotpatch/accent_patch.py` for manual review: large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 301 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_011`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/hotpatch/diagnostics.py`
- Rationale: Static code interpreter recommendation `code_static_011` flagged `Scripting/v61b/hotpatch/diagnostics.py` for manual review: large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 286 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_012`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/hotpatch/fog_patch.py`
- Rationale: Static code interpreter recommendation `code_static_012` flagged `Scripting/v61b/hotpatch/fog_patch.py` for manual review: large functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 133 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_013`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/hotpatch/hero_material_patch.py`
- Rationale: Static code interpreter recommendation `code_static_013` flagged `Scripting/v61b/hotpatch/hero_material_patch.py` for manual review: large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 395 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_014`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/hotpatch/render_patch.py`
- Rationale: Static code interpreter recommendation `code_static_014` flagged `Scripting/v61b/hotpatch/render_patch.py` for manual review: large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 206 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_015`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/main_v61b.py`
- Rationale: Static code interpreter recommendation `code_static_015` flagged `Scripting/v61b/main_v61b.py` for manual review: large functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 200 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_016`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Scripting/v61b/materials.py`
- Rationale: Static code interpreter recommendation `code_static_016` flagged `Scripting/v61b/materials.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, 
```

### `output/analysis/code_interpreter_heavy_prototype_20260502-193942.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1168235`
- SHA-256: `48406554fcb99c52c82844337bdc39d960ed3336010808db5f6e8ba5ab160a7c`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-02T19:40:01",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 241,
  "parsed_file_count": 241,
  "total_lines": 63350,
  "total_functions": 2087,
  "total_classes": 76,
  "total_risk_signals": 36,
  "total_todos": 21,
  "top_imports": [
    {
      "module": "config",
      "count": 596
    },
    {
      "module": "Tools",
      "count": 474
    },
    {
      "module": "pathlib",
      "count": 178
    },
    {
      "module": "__future__",
      "count": 177
    },
    {
      "module": "typing",
      "count": 153
    },
    {
      "module": "json",
      "count": 124
    },
    {
      "module": "argparse",
      "count": 109
    },
    {
      "module": "datetime",
      "count": 74
    },
    {
      "module": "report_utils",
      "count": 68
    },
    {
      "module": "sys",
      "count": 64
    },
    {
      "module": "bpy",
      "count": 54
    },
    {
      "module": "common",
      "count": 49
    },
    {
      "module": "dataclasses",
      "count": 40
    },
    {
      "module": "re",
      "count": 31
    },
    {
      "module": "pipeline",
      "count": 28
    },
    {
      "module": "materials",
      "count": 27
    },
    {
      "module": "agent_state",
      "count": 26
    },
    {
      "module": "math",
      "count": 23
    },
    {
      "module": "subprocess",
      "count": 19
    },
    {
      "module": "models",
      "count": 16
    },
    {
      "module": "os",
      "count": 15
    },
    {
      "module": "io_utils",
      "count": 14
    },
    {
      "module": "scene_utils",
      "count": 13
    },
    {
      "module": "artifact_contracts",
      "count": 13
    },
    {
      "module": "atmosphere_setup",
      "count": 12
    },
    {
      "module": "hashlib",
      "count": 12
    },
    {
      "module": "reports",
      "count": 12
    },
    {
      "module": "defaults",
      "count": 11
    },
    {
      "module": "mathutils",
      "count": 10
    },
    {
      "module": "asset_setup",
      "count": 10
    },
    {
      "module": "time",
      "count": 10
    },
    {
      "module": "runner",
      "count": 9
    },
    {
      "module": "spaziotempo",
      "count": 9
    },
    {
      "module": "npu_runtime",
      "count": 9
    },
    {
      "module": "artifact_paths",
      "count": 9
    },
    {
      "module": "path_utils",
      "count": 8
    },
    {
      "module": "lighting_patch",
      "count": 8
    },
    {
      "module": "registry",
      "count": 8
    },
    {
      "module": "ast",
      "count": 8
    },
    {
      "module": "concurrent",
      "count": 8
    }
  ],
  "largest_files": [
    {
      "path": "Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py",
      "line_count": 2197,
      "risk": "high"
    },
    {
      "path": "Tools/npu/run_dual_ai_pipeline.py",
      "line_count": 1773,
      "risk": "high"
    },
    {
      "path": "Scripting/v61b/scene_tuning_panel.py",
      "line_count": 1262,
      "risk": "high"
    },
    {
      "path": "Scripting/v61b_backgood/scene_tuning_panel.py",
      "line_count": 1097,
      "risk": "high"
    },
    {
      "path": "Scripting/v61b/animation.py",
      "line_count": 1079,
      "risk": "high"
    },
    {
      "path": "Scripting/v61b_backgood/animation.py",
      "line_count": 1019,
      "risk": "high"
    },
    {
      "path": "Scripting/v61b/physics_setup.py",
      "line_count": 737,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b/asset_setup.py",
      "line_count": 725,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b_backgood/asset_setup.py",
      "line_count": 725,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b_backgood/physics_setup.py",
      "line_count": 720,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_review.py",
      "line_count": 714,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/build_music_context.py",
      "line_count": 711,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b/materials.py",
      "line_count": 657,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/run_npu_review.py",
      "line_count": 628,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/check_npu_pipeline_modules.py",
      "line_count": 627,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_selective_execution_plan.py",
      "line_count": 618,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_repository_change_proposals.py",
      "line_count": 582,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_ai_context_pack.py",
      "line_count": 575,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_pipeline_dry_run_matrix.py",
      "line_count": 573,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_patch_plan.py",
      "line_count": 562,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b/atmosphere_setup.py",
      "line_count": 554,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/suggest_repository_updates.py",
      "line_count": 551,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/agent_state.py",
      "line_count": 544,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b_backgood/atmosphere_setup.py",
      "line_count": 543,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_megalithic_repo_review.py",
      "line_count": 519,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b_backgood/materials.py",
      "line_count": 513,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_code_patch_plan.py",
      "line_count": 499,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/ai_pipeline_report_contracts.py",
      "line_count": 497,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/npu_guardrail_service.py",
      "line_count": 490,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/refine_megalithic_review_signals.py",
      "line_count": 489,
      "risk": "medium"
    }
  ],
  "risk_summary": {
    "low": 129,
    "high": 6,
    "medium": 106
  },
  "recommendation_count": 112,
  "recommendations": [
    {
      "id": "code_static_001",
      "target_file": "Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py",
      "risk": "high",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\ready_to_jazz_wow_youtube_profiles_audio_sync\\main_ready_to_jazz_wow_youtube.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_002",
      "target_file": "Scripting/shared/image_sequence.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\shared\\image_sequence.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_003",
      "target_file": "Scripting/v61b/animation.py",
      "risk": "high",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\animation.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_004",
      "target_file": "Scripting/v61b/asset_setup.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\asset_setup.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_005",
      "target_file": "Scripting/v61b/atmosphere_setup.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\atmosphere_setup.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_006",
      "target_file": "Scripting/v61b/config.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\config.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_007",
      "target_file": "Scripting/v61b/encode_ffmpeg_v61b.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large functions detected",
        "static risk calls detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\encode_ffmpeg_v61b.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-ro
```

### `output/validation/code_contract_drift.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `6496`
- SHA-256: `91b7fdb0129d81b348052a028fc7e4beed953d3f3747b679a338930b465d438b`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "code_contract_drift",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_manual_review_only",
  "drift_count": 0,
  "lane_policy": {
    "cpu": "validators, contract analyzers, packet/proposal builders and orchestration run here by default",
    "gpu_cuda": "Ollama/GPU may produce advisory workload reports only through explicit provider commands",
    "npu": "OpenVINO/NPU may produce probe/knowledge-broker metadata or workload reports only through explicit provider commands"
  },
  "checks": [
    {
      "path": "Tools/workflow/run_local_ai_core_tool_activation.ps1",
      "contract": "local_ai_core_tool_activation_guardrails",
      "owner_lane": "cpu_orchestration",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "exists": true,
      "ok": true,
      "required_term_count": 7,
      "recommended_term_count": 3,
      "missing_required_terms": [],
      "missing_recommended_terms": [],
      "forbidden_terms_present": [],
      "forbidden_global_terms_present": [],
      "allowed_global_forbidden_terms_present": [],
      "errors": [],
      "warnings": [],
      "safe_actions": []
    },
    {
      "path": "Tools/validation/check_ai_workload_report_quality.py",
      "contract": "ai_workload_quality_gate_report_contract",
      "owner_lane": "cpu_validation",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "exists": true,
      "ok": true,
      "required_term_count": 8,
      "recommended_term_count": 2,
      "missing_required_terms": [],
      "missing_recommended_terms": [],
      "forbidden_terms_present": [],
      "forbidden_global_terms_present": [],
      "allowed_global_forbidden_terms_present": [],
      "errors": [],
      "warnings": [],
      "safe_actions": []
    },
    {
      "path": "Tools/ai/workload_quality.py",
      "contract": "workload_quality_fail_closed_routing",
      "owner_lane": "cpu_validation",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "exists": true,
      "ok": true,
      "required_term_count": 7,
      "recommended_term_count": 2,
      "missing_required_terms": [],
      "missing_recommended_terms": [],
      "forbidden_terms_present": [],
      "forbidden_global_terms_present": [],
      "allowed_global_forbidden_terms_present": [],
      "errors": [],
      "warnings": [],
      "safe_actions": []
    },
    {
      "path": "Tools/ai/suggest_repository_updates.py",
      "contract": "packet_builder_quality_approved_context_only",
      "owner_lane": "cpu_packet_builder",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "exists": true,
      "ok": true,
      "required_term_count": 6,
      "recommended_term_count": 2,
      "missing_required_terms": [],
      "missing_recommended_terms": [],
      "forbidden_terms_present": [],
      "forbidden_global_terms_present": [],
      "allowed_global_forbidden_terms_present": [],
      "errors": [],
      "warnings": [],
      "safe_actions": []
    },
    {
      "path": "Tools/ai/build_repository_change_proposals.py",
      "contract": "repository_proposals_quality_gate_evidence",
      "owner_lane": "cpu_proposal_builder",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "exists": true,
      "ok": true,
      "required_term_count": 6,
      "recommended_term_count": 2,
      "missing_required_terms": [],
      "missing_recommended_terms": [],
      "forbidden_terms_present": [],
      "forbidden_global_terms_present": [],
      "allowed_global_forbidden_terms_present": [],
      "errors": [],
      "warnings": [],
      "safe_actions": []
    },
    {
      "path": "Tools/npu/run_npu_review.py",
      "contract": "npu_review_metadata_sidecar",
      "owner_lane": "npu_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "npu"
      ],
      "exists": true,
      "ok": true,
      "required_term_count": 7,
      "recommended_term_count": 2,
      "missing_required_terms": [],
      "missing_recommended_terms": [],
      "forbidden_terms_present": [],
      "forbidden_global_terms_present": [],
      "allowed_global_forbidden_terms_present": [],
      "errors": [],
      "warnings": [],
      "safe_actions": []
    },
    {
      "path": "Tools/validation/check_docs_contract_drift.py",
      "contract": "docs_contract_drift_report_only",
      "owner_lane": "cpu_validation",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "exists": true,
      "ok": true,
      "required_term_count": 6,
      "recommended_term_count": 2,
      "missing_required_terms": [],
      "missing_recommended_terms": [],
      "forbidden_terms_present": [],
      "forbidden_global_terms_present": [],
      "allowed_global_forbidden_terms_present": [
        "OpenVINO GPU primary lane",
        "provider execution by default"
      ],
      "errors": [],
      "warnings": [],
      "safe_actions": []
    },
    {
      "path": "Tools/validation/apply_docs_contract_drift_fixes.py",
      "contract": "docs_contract_drift_explicit_fixer",
      "owner_lane": "cpu_validation_explicit_docs_fixer",
      "consumed_by_lanes": [
        "cpu"
      ],
      "exists": true,
      "ok": true,
      "required_term_count": 7,
      "recommended_term_count": 2,
      "missing_required_terms": [],
      "missing_recommended_terms": [],
      "forbidden_terms_present": [],
      "forbidden_global_terms_present": [],
      "allowed_global_forbidden_terms_present": [],
      "errors": [],
      "warnings": [],
      "safe_actions": []
    }
  ],
  "safe_actions": [],
  "guardrails": {
    "code_report_only": true,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "blender_runtime_touched": false,
    "full_analysis_json_touched": false,
    "sqlite_db_touched": false,
    "npu_promoted_to_advisory": false,
    "openvino_gpu_primary_lane": false
  }
}

```

### `output/validation/python_line_count_heavy_prototype_20260502-193942.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `12741`
- SHA-256: `0f9d06a571cd01fc82dfbeba2de603ecc451407e09592f6300b635b27736d531`
- Content included: `True`
- Content truncated: `True`

```text
File,Lines
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py,2197
Tools/npu/run_dual_ai_pipeline.py,1773
old script legacy/spaziotempo_asset_visual_v61.py,1513
Scripting/v61b/scene_tuning_panel.py,1262
Tools/workflow/workflow_state.py,1230
old script legacy/spaziotempo_asset_visual_v6.py,1174
Scripting/v61b_backgood/scene_tuning_panel.py,1097
Scripting/v61b/animation.py,1079
Scripting/v61b_backgood/animation.py,1019
old script legacy/spaziotempo_album_visual_v5.py,969
Tools/workflow/gui/workflow_gui.py,738
Scripting/v61b/physics_setup.py,737
Scripting/v61b/asset_setup.py,725
Scripting/v61b_backgood/asset_setup.py,725
Scripting/v61b_backgood/physics_setup.py,720
Tools/ai/run_agent_gpu_deep_planning_review.py,714
Tools/npu/build_music_context.py,711
old script legacy/spaziotempo_album_visual_v3.py,710
Scripting/v61b/materials.py,657
Tools/npu/run_npu_review.py,628
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_selective_execution_plan.py,618
Tools/workflow/workflow_debug.py,607
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/build_ai_context_pack.py,575
Tools/ai/run_pipeline_dry_run_matrix.py,573
Tools/ai/build_agent_review_patch_plan.py,562
Scripting/v61b/atmosphere_setup.py,554
Tools/ai/suggest_repository_updates.py,551
Tools/ai/agent_state.py,544
Scripting/v61b_backgood/atmosphere_setup.py,543
Tools/ai/run_megalithic_repo_review.py,519
Scripting/v61b_backgood/materials.py,513
Tools/ai/build_agent_review_code_patch_plan.py,499
Tools/validation/ai_pipeline_report_contracts.py,497
Tools/npu/npu_guardrail_service.py,490
Tools/ai/refine_megalithic_review_signals.py,489
Tools/validation/run_agent_review_patch_plan_full_validation.py,487
Tools/validation/run_agnostic_ai_tools_smoke_matrix.py,483
Tools/ai/run_agent_gpu_deep_planning_supervised.py,478
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py,471
normalize_scene_spec.py,469
Tools/validation/check_reviewed_patch_specs.py,446
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/ai/build_code_interpreter_report.py,437
Tools/npu/build_project_ai_index.py,436
Tools/validation/check_ai_context_pack_contract.py,425
Tools/npu/ollama_runtime.py,422
Tools/workflow/gui/components/storage_dashboard.py,422
Tools/workflow/scene_brief.py,419
Tools/ai/build_patch_specs_from_proposals.py,414
Tools/ai/run_npu_gpu_deep_review_auditor.py,411
Tools/ai/build_agent_agnostic_tool_inventory.py,408
Tools/npu/build_npu_code_context.py,402
Tools/validation/check_github_evidence_bundle.py,401
Tools/validation/check_patch_spec_drafts.py,400
Scripting/v61b/encode_ffmpeg_v61b.py,399
Tools/ai/build_dry_run_matrix_evidence_bundle.py,398
Tools/ai/build_agent_memory_inventory.py,397
Scripting/v61b/encode_image_sequence_v61b.py,395
Scripting/v61b/hotpatch/hero_material_patch.py,395
Scripting/v61b_backgood/hotpatch/hero_material_patch.py,395
Tools/ai/build_agent_review_evidence_sufficiency.py,394
Scripting/v61b/fog_dynamics.py,392
Tools/ai/build_full_context_golden_proposals.py,392
Tools/validation/check_code_contract_drift.py,392
Tools/workflow/gui/components/artifact_browser.py,390
Scripting/v61b_backgood/encode_image_sequence_v61b.py,376
indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py,369
Tools/npu/generated_blender_script_candidate.py,369
Tools/npu/generated_blender_script_candidate_FristNear.py,369
Tools/validation/check_repository_change_proposals.py,366
Tools/validation/test_npu_pipeline_helpers.py,359
Scripting/v61b_backgood/config.py,358
Tools/ai/build_local_ai_enrichment_plan.py,357
Tools/npu/build_ai_service_packet.py,355
Tools/workflow/project_awareness.py,353
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/npu/build_npu_knowledge_broker_packet.py,327
Tools/npu/build_blender_manual_context.py,326
Tools/workflow/workflow_shell.py,324
Tools/validation/check_dry_run_matrix_evidence_bundle.py,321
Tools/workflow/gui/workflow_gui_modern.py,319
Tools/validation/check_local_ai_adapter_manifest.py,317
Tools/ai/build_music_intermediates.py,314
Tools/ai/run_npu_decode_smoke_diagnostic.py,314
Tools/ai/agent_memory_policy.py,307
Tools/validation/check_full_context_golden_proposals.py,307
Tools/ai/build_analysis_input_bundle.py,304
Scripting/v61b/hotpatch/accent_patch.py,301
Tools/npu/pipeline/providers.py,297
Tools/ai/select_semantic_code_chunks.py,291
Tools/validation/check_ai_pipeline_modules.py,290
Scripting/v61b/hotpatch/diagnostics.py,286
Tools/workflow/startup_check.py,284
Tools/ai/build_agent_transient_request_context.py,283
Tools/validation/run_agent_review_patch_plan_smoke.py,283
Tools/workflow/gui/components/session_overview.py,278
Scripting/v61b/render_setup.py,270
Tools/validation/check_full_context_golden_docs_contract.py,270
Scripting/v61b_backgood/render_setup.py,267
Tools/workflow/ai_runtime_diagnostics.py,267
Tools/ai/build_code_patch_docs_followup.py,266
Tools/validation/check_ai_workload_report_quality.py,260
Tools/validation/check_docs_contract_drift.py,259
Tools/ai/build_code_patch_artifact_pack.py,258
analyze_wav.py,257
Tools/validation/run_agnostic_context_stack_smoke.py,256
Tools/ai/build_code_edit_proposal_from_plan.py,250
Tools/ai/build_megalithic_review_pr_draft.py,245
Scripting/v61b_backgood/fog_dynamics.py,240
Tools/ai/review_wave_entrypoints.py,240
Tools/npu/run_ollama_music_agent.py,238
Tools/validation/check_selective_execution_plan.py,238
Tools/ai/smart_ai_gatekeeper.py,232
Tools/ai/enrich_github_evidence_bundle_code_plan.py,231
Tools/validation/check_ai_dry_run_matrix_outputs.py,230
Tools/validation/check_npu_knowledge_broker_packet.py,229
Tools/validation/build_python_line_count_csv.py,225
Tools/ai/workload_quality.py,222
Tools/validation/check_generated_artifact_path_policy.py,222
Scripting/v61b/spaziotempo/core/registry.py,221
Tools/workflow/smart_ai_context.py,219
Tools/ai/artifact_domain_registry.py,217
Tools/validation/generated_file_policy.py,217
Tools/ai/code_patch_plan_common.py,216
Tools/ai/github_evidence_bundle_reports.py,211
Tools/ai/github_evidence_bundle_markdown.py,209
Tools/validation/check_local_ai_enrichment_plan.py,209
Tools/validation/check_core_activation_agnostic_contract.py,207
Scripting/v61b/hotpatch/render_patch.py,206
Scripting/v61b_backgood/hotpatch/render_patch.py,206
Tools/validation/run_agent_review_evidence_sufficiency_smoke.py,204
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py,203
Tools/validation/run_code_edit_proposal_smoke.py,203
Tools/ai/code_edit_proposal_helpers.py,201
Tools/validation/run_agent_review_code_patch_plan_smoke.py,201
Scripting/v61b/main_v61b.py,200
Tools/ai/validate_ai_artifacts.py,200
Scripting/v61b/world_setup.py,198
Tools/ai/pipeline/steps.py,197
Tools/validation/generated_python_policy.py,197
Tools/ai/check_npu_provider_environment.py,189
Tools/validation/check_validation_report_contract.py,187
Tools/ai/build_workload_quality_lane_routing.py,186
Tools/workflow/git_auto_push.py,186
Tools/ai/pipeline/remediation.py,185
Tools/validation/check_ai_dry_run_matrix_cases.py,183
Tools/workflow/gui/components/action_panel.py,183
Tools/ai/run_local_provider_probe.py,182
Tools/workflow/gui/components/live_output_panel.py,182
Scripting/v61b_backgood/main_v61b.py,181
Tools/workflow/gui/workflow_gui_with_push.py,181
Scripting/v61b_backgood/world_setup.py,174
Tools/validation/check_generated_blender_script_policy.py,173
Scripting/shared/image_sequence.py,161
Tools/npu/npu_runtime.py,160
Scripting/v61b/fog_filaments.py,159
Tools/validation/check_npu_decode_quality_remediation.py,159
Tools/npu/pipeline/__init__.py,157
Tools/ai/github_evidence_bundle_io.py,153
Tools/ai/pipeline/models.py,152
Scripting/v61b/hotpatch/lighting_patch.py,150
Tools/validation/check_refactor_status_consistency.py,149
Tools/npu/build_runtime_output_manifest.py,148
Tools/npu/build_provider_result_report.py,147
Tools/validation/check_blender_shared_compat_smoke.py,147
Tools/ai/github_evidence_bundle_decisions.py,146
Tools/workflow/artifact_consult.py,144
Tools/ai/build_github_evidence_bundle.py,142
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/validation/check_docs_links.py,141
Scripting/shared/blender_compat.py,140
Scripting/shared/ffmpeg_encoder.py,134
Tools/ai/github_evidence_bundle_artifacts.py,134
Scripting/shared/render_profiles.py,133
Scripting/v61b/hotpatch/fog_patch.py,133
Scripting/v61b/spaziotempo/core/collections.py,132
Tools/validation/check_json_artifacts.py,132
Tools/ai/model_json.py,130
Tools/ai/build_agent_state_packet.py,128
Tools/npu/pipeline/artifact_paths.py,127
Tools/npu/run_npu_artifact_reviewer.py,127
Scripting/v61b_backgood/hotpatch/accent_patch.py,125
Tools/npu/pipeline/reports.py,125
Tools/validation/check_agent_memory_policy.py,125
Tools/validation/check_generated_python_policy.py,125
Scripting/v61b_backgood/hotpatch/fog_patch.py,124
Tools/validation/check_execution_plan_status.py,123
Tools/validation/check_ai_model_json.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/validation/check_package_structure.py,117
Tools/workflow/workflow_shell_with_push.py,117
build_track_summary.py,113
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/validation/check_python_syntax.py,105
Tools/ai/pipeline/preflight.py,104
Scripting/v61b/hotpatch/runner.py,103
Scripting/shared/path_utils.py,102
Tools/ai/pipeline/runner.py,102
Tools/npu/pipeline/prompts.py,99
Scripting/v61b/scene_utils.py,97
Scripting/v61b_backgood/scene_utils.py,97
Tools/ai/pipeline/guardrail_models.py,97
Tools/validation/check_npu_pipeline_docs.py,96
Tools/workflow/gui/components/st_theme.py,92
Scripting/v61b/hotpatch/common.py,91
Scripting/v61b_backgood/hotpatch/common.py,91
Tools/npu/build_semantic_code_chunks.py,91
Scripting/shared/json_io.py,88
Tools/ai/pipeline/artifact_contracts.py,86
Scripting/v61b_backgood/hotpatch/lighting_patch.py,85
Tools/npu/pipeline/validators.py,84
Tools/validation/check_provider_result_parsing.py,83
Scripting/v61b/io_utils.py,81
Scripting/v61b_backgood/io_utils.py,81
Tools/npu/pipeline/fixtures.py,80
Scripting/_template_audio_reactive_package/main.py,79
Scripting/_template_audio_reactive_package/encode_ffmpeg.py,75
Tools/npu/pipeline/context_builder.py,75
Tools/ai/pipeline/reports.py,74
Tools/ai/pipeline/compat.py,73
Tools/ai/pipeline/refactor_status.py,70
Tools/npu/pipeline/runner.py,70
Tools/ai/review_agent_memory.py,69
Tools/npu/pipeline/migration_readiness.py,68
Tools/ai/pipeline/scheduler.py,66
Tools/ai/run_parallel_artifact_pipeline.py,65
Tools/validation/check_ai_pipeline_report_contract.py,65
Tools/validation/check_artifact_domain_registry.py,64
Scripting/v61b/hot_update_scene_v61b.py,63
Scripting/v61b_backgood/hot_update_scene_v61b.py,61
Tools/npu/pipeline/io_utils.py,61
Scripting/v61b_backgood/hotpatch/runner.py,60
Tools/validation/check_npu_pipeline_helper_tests.py,59
Tools/npu/pipeline/artifact_writer.py,56
Tools/ai/merge_ai_candidates.py,53
Tools/npu/pipeline/legacy_compat.py,52
Scripting/_template_audio_reactive_package/audio_mapping.py,51
Scripting/v61b/reload_utils.py,51
Tools/ai/pipeline/cli.py,50
Tools/validation/report_utils.py,50
Scripting/_template_audio_reactive_package/config.py,49
Scripting/_template_audio_reactive_package/materials.py,35
Tools/ai/pipeline/orchestrator.py,31
Scripting/v61b/camera_setup.py,29
Scripting/v61b_backgood/camera_setup.py,29
Scripting/_template_audio_reactive_package/camera.py,26
Scripting/_template_audio_reactive_package/render_settings.py,26
Scripting/_template_audio_reactive_package/lighting.py,23
Tools/ai/pipeline/__init__.py,23
Scripting/_template_audio_reactive_package/scene_objects.py,21
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/render_profi
```

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
