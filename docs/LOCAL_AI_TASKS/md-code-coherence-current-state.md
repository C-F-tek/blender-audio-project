# MD/code coherence current state

## Scope

- Markdown scanned: `443`
- Python scripts scanned: `582`
- PowerShell scripts scanned: `44`
- Finding count: `525`
- By severity: `{"high": 45, "low": 167, "medium": 313}`

## Finding classes

- `stale-or-historical`: `242`
- `unknown`: `77`
- `placeholder-template`: `65`
- `active-current`: `45`
- `ambiguous-basename-reference`: `35`
- `historical-or-handoff`: `20`
- `stale-or-future`: `16`
- `chatgpt-advisory-or-handoff`: `13`
- `local-absolute-path`: `8`
- `patch-bundle-template`: `2`
- `evidence-only`: `2`

## Finding kinds

- `markdown_reference_missing`: `491`
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
| markdown_reference_missing | `docs/AI_ONBOARDING.md` | `Scripting/shared/config_model.py` | active-current |
| markdown_reference_missing | `docs/AI_ONBOARDING.md` | `Scripting/shared/diagnostics.py` | active-current |
| markdown_reference_missing | `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` | `Tools/validation/check_generated_automation_script_policy.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `Scripting/shared/diagnostics.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `Scripting/shared/panel_base.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `Scripting/shared/scene_utils.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `Tools/lib/scene_spec.py` | active-current |
| markdown_reference_missing | `docs/MODULE_MAP.md` | `spaziotempo/core/registry.py` | active-current |
| markdown_reference_missing | `docs/PROJECT_AUDIT.md` | `spaziotempo/core/registry.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `Tools/lib/scene_spec.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `spaziotempo/core/registry.py` | active-current |
| markdown_reference_missing | `docs/REFACTORING_AND_REUSE_PLAN.md` | `src/spaziotempo_audio/scene_spec.py` | active-current |
| markdown_reference_missing | `docs/SHARED_SCRIPTING_UTILITIES.md` | `Scripting/shared/config_model.py` | active-current |
| markdown_reference_missing | `docs/SHARED_SCRIPTING_UTILITIES.md` | `Scripting/shared/diagnostics.py` | active-current |
| markdown_reference_missing | `docs/SHARED_SCRIPTING_UTILITIES.md` | `Scripting/shared/hotpatch_base.py` | active-current |
| markdown_reference_missing | `docs/SHARED_SCRIPTING_UTILITIES.md` | `Scripting/shared/panel_base.py` | active-current |
| markdown_reference_missing | `docs/SHARED_SCRIPTING_UTILITIES.md` | `Scripting/shared/scene_registry.py` | active-current |
| markdown_reference_missing | `docs/SHARED_SCRIPTING_UTILITIES.md` | `spaziotempo/core/registry.py` | active-current |
| markdown_reference_missing | `Scripting/README.md` | `Scripting/shared/diagnostics.py` | active-current |
| markdown_reference_missing | `Tools/repo_patch_runner/README.md` | `Scripting/example.py` | active-current |
| active_markdown_over_line_budget | `Tools/validation/README.md` | `Tools/validation/README.md` | active-current |
| markdown_reference_missing | `Tools/validation/README.md` | `alidation/check_ai_workload_report_quality.py` | active-current |
| active_markdown_over_line_budget | `Tools/npu/npu_music_chunks/chunk_001_music_overview.md` | `Tools/npu/npu_music_chunks/chunk_001_music_overview.md` | active-current |
| markdown_reference_missing | `Scripting/v61b/PROJECT_STRUCTURE.md` | `spaziotempo/features/water.py` | active-current |
| markdown_reference_missing | `Scripting/v61b/README.md` | `Scripting/shared/hotpatch_base.py` | active-current |
| markdown_reference_missing | `Scripting/v61b/README.md` | `Scripting/shared/panel_base.py` | active-current |
| markdown_reference_missing | `indexAI/scene_scripts/new_plan_luca_vera_master_scene_bundle/README.md` | `/new_plan_luca_vera_master_scene_builder_candidate.py` | active-current |
| markdown_reference_missing | `indexAI/scene_scripts/parameters_luca_vera_premaster_master_scene_bundle/README.md` | `/parameters_luca_vera_premaster_master_scene_builder_candidate.py` | active-current |
| markdown_reference_missing | `indexAI/scene_scripts/phazzah_luca_vera_master_scene_bundle/README.md` | `/phazzah_luca_vera_master_scene_builder_candidate.py` | active-current |
| markdown_reference_missing | `indexAI/scene_scripts/ready_to_jazz_luca_vera_master_scene_bundle/README.md` | `/ready_to_jazz_luca_vera_master_scene_builder_candidate.py` | active-current |
| markdown_reference_missing | `docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-001.md` | `Tools/validation/example.py` | active-current |
| markdown_reference_missing | `docs/CODE_CONSULTATION_REPORT/part-001.md` | `Tools/validation/check_docs_paths.py` | active-current |
| markdown_reference_missing | `docs/LOCAL_AI_TASKS/markdown-line-budget-policy.md` | `alidation/check_markdown_line_limits.py` | active-current |
| markdown_reference_missing | `docs/LOCAL_AI_TASKS/project-tool-registry.md` | `Tools/ai/build_python_line_count_csv.py` | active-current |
| markdown_reference_missing | `docs/PROJECT_AI_CONSCIOUSNESS/part-001.md` | `Scripting/shared/config_model.py` | active-current |
| markdown_reference_missing | `docs/PROJECT_AI_CONSCIOUSNESS/part-001.md` | `Scripting/shared/diagnostics.py` | active-current |
| markdown_reference_missing | `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md` | `scripts/validate_after_patch.ps1` | active-current |
| markdown_reference_missing | `docs/LOCAL_AI_TASKS/full0to10-repo-quality/06-inputpath-normalization.md` | `Tools/a.ps1` | active-current |
| markdown_reference_missing | `docs/LOCAL_AI_TASKS/full0to10-repo-quality/06-inputpath-normalization.md` | `Tools/b.py` | active-current |
| markdown_reference_missing | `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/02-zip-01-tools.md` | `Dest01/run_patch_bundle.py` | active-current |
| markdown_reference_missing | `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md` | `Dest02/run_patch_bundle.py` | active-current |
| markdown_reference_missing | `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md` | `Dest03/run_patch_bundle.py` | active-current |
| markdown_reference_missing | `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md` | `Tools/ai_core/json_utils.py` | active-current |
