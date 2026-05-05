# MD/code coherence current state

## Scope

- Markdown scanned: `443`
- Python scripts scanned: `582`
- PowerShell scripts scanned: `44`
- Finding count: `805`
- By severity: `{"high": 261, "low": 163, "medium": 381}`

## Finding classes

- `stale-or-historical`: `329`
- `active-current`: `261`
- `unknown`: `81`
- `placeholder-template`: `65`
- `historical-or-handoff`: `36`
- `stale-or-future`: `16`
- `chatgpt-advisory-or-handoff`: `13`
- `patch-bundle-template`: `2`
- `evidence-only`: `2`

## Finding kinds

- `markdown_reference_missing`: `771`
- `markdown_python_command_missing_script`: `13`
- `markdown_powershell_flag_not_in_param_block`: `8`
- `markdown_python_flag_not_in_argparse`: `8`
- `markdown_powershell_command_missing_script`: `3`
- `active_markdown_over_line_budget`: `2`

## Operational decision

Do not bulk-fix all findings blindly.
Use high findings first for active commands and missing scripts.
Historical/evidence-only references must be demoted or described as historical, not recreated as fake active files.

## Top high findings

| Kind | Document | Target | Classification |
|---|---|---|---|
| markdown_reference_missing | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | `ools/ai/build_repository_consistency_map.py` | active-current |
| markdown_reference_missing | `guida_git_github_blender_audio_project.md` | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py` | active-current |
| markdown_reference_missing | `docs/AI_GENERATED_PACKAGE_STANDARD.md` | `config.py` | active-current |
| markdown_reference_missing | `docs/AI_GENERATED_PACKAGE_STANDARD.md` | `encode_ffmpeg.py` | active-current |
| markdown_reference_missing | `docs/AI_GENERATED_PACKAGE_STANDARD.md` | `main.py` | active-current |
| markdown_reference_missing | `docs/AI_ONBOARDING.md` | `Scripting/shared/config_model.py` | active-current |
| markdown_reference_missing | `docs/AI_ONBOARDING.md` | `Scripting/shared/diagnostics.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `artifact_contracts.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `cli.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `compat.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `defaults.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `guardrail_models.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `models.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `orchestrator.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `preflight.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `remediation.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `runner.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `scheduler.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `schema_report.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_ARCHITECTURE.md` | `steps.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `artifact_contracts.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `defaults.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `guardrail_models.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `orchestrator.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `preflight.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `remediation.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `scheduler.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `schema_report.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `steps.py` | active-current |
| markdown_reference_missing | `docs/COMPATIBILITY.md` | `blender_compat.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `artifact_contracts.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `check_ai_pipeline_modules.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `cli.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `compat.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `defaults.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `guardrail_models.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `models.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `orchestrator.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `preflight.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `refactor_status.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `remediation.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `run_pipeline_dry_run_matrix.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `runner.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `scheduler.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `schema_report.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `steps.py` | active-current |
| markdown_reference_missing | `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` | `build_markdown_inventory.py` | active-current |
| markdown_reference_missing | `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` | `build_script_inventory.py` | active-current |
| markdown_reference_missing | `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` | `Tools/validation/check_generated_automation_script_policy.py` | active-current |
| markdown_reference_missing | `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` | `generated_python_policy.py` | active-current |
| markdown_reference_missing | `docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md` | `blender_compat.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `Scripting/shared/diagnostics.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `Scripting/shared/panel_base.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `Scripting/shared/scene_utils.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `Tools/lib/scene_spec.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `blender_compat.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `config.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `encode_ffmpeg_v61b.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `encode_image_sequence_v61b.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `ffmpeg_encoder.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `hotpatch_base.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `image_sequence.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `io_utils.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `json_io.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `main_v61b.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `render_profiles.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `render_setup.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `scene_tuning_panel.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `scene_utils.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `spaziotempo/core/registry.py` | active-current |
| markdown_reference_missing | `docs/PATCH_SPEC_WORKFLOW.md` | `apply_repo_mods.py` | active-current |
| markdown_reference_missing | `docs/PROJECT_AUDIT.md` | `spaziotempo/core/registry.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `Tools/lib/scene_spec.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `blender_compat.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `check_python_syntax.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `config.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `ffmpeg_encoder.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `image_sequence.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `json_io.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `render_profiles.py` | active-current |
