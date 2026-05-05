# MD/code coherence current state

## Scope

- Markdown scanned: `451`
- Python scripts scanned: `555`
- PowerShell scripts scanned: `44`
- Finding count: `2395`
- By severity: `{"high": 1590, "low": 143, "medium": 662}`

## Finding classes

- `active-current`: `1590`
- `stale-or-historical`: `650`
- `unknown`: `143`
- `historical-or-handoff`: `12`

## Finding kinds

- `markdown_reference_missing`: `1782`
- `markdown_python_command_missing_script`: `507`
- `markdown_powershell_command_missing_script`: `104`
- `active_markdown_over_line_budget`: `2`

## Operational decision

Do not bulk-fix all findings blindly.
Use high findings first for active commands and missing scripts.
Historical/evidence-only references must be demoted or described as historical, not recreated as fake active files.

## Top high findings

| Kind | Document | Target | Classification |
|---|---|---|---|
| markdown_reference_missing | `AGENTS.md` | `patches/00_check_repo_ready.py` | active-current |
| markdown_reference_missing | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | `/Tools/ai/some_tool.py` | active-current |
| markdown_reference_missing | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | `/Tools/validation/some_smoke.py` | active-current |
| markdown_reference_missing | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | `/Tools/workflow/some_runner.ps1` | active-current |
| markdown_reference_missing | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | `/Tools/workflow/some_script.ps1` | active-current |
| markdown_reference_missing | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | `ools/ai/build_repository_consistency_map.py` | active-current |
| markdown_powershell_command_missing_script | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | `/Tools/workflow/some_runner.ps1` | active-current |
| markdown_reference_missing | `guida_git_github_blender_audio_project.md` | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py` | active-current |
| markdown_reference_missing | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | `/Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1` | active-current |
| markdown_reference_missing | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | `/Tools/workflow/run_unified_local_ai_refactor.ps1` | active-current |
| markdown_python_command_missing_script | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | `/output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` | active-current |
| markdown_powershell_command_missing_script | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | `/Tools/workflow/run_unified_local_ai_refactor.ps1` | active-current |
| markdown_powershell_command_missing_script | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | `/Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1` | active-current |
| markdown_reference_missing | `CHATGPT/next-chat-handoff-2026-05-05-post-broker-runtime-telemetry.md` | `/Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1` | active-current |
| markdown_reference_missing | `CHATGPT/next-chat-handoff-2026-05-05-post-broker-runtime-telemetry.md` | `/Tools/workflow/run_unified_local_ai_refactor.ps1` | active-current |
| markdown_reference_missing | `docs/AI_CHUNKING_STRATEGY.md` | `/Tools/npu/build_semantic_code_chunks.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_CHUNKING_STRATEGY.md` | `/Tools/npu/build_semantic_code_chunks.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_CHUNKING_STRATEGY.md` | `/Tools/npu/build_semantic_code_chunks.py` | active-current |
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
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/ai/run_parallel_artifact_pipeline.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/ai/run_pipeline_dry_run_matrix.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/validation/check_ai_pipeline_modules.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/validation/check_python_syntax.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `artifact_contracts.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `defaults.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `guardrail_models.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `orchestrator.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `preflight.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `remediation.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `scheduler.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `schema_report.py` | active-current |
| markdown_reference_missing | `docs/AI_PIPELINE_OPTIMIZATION.md` | `steps.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/ai/run_parallel_artifact_pipeline.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/ai/run_parallel_artifact_pipeline.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/ai/run_parallel_artifact_pipeline.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/ai/run_pipeline_dry_run_matrix.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/validation/check_python_syntax.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/validation/check_ai_pipeline_modules.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_PIPELINE_OPTIMIZATION.md` | `/Tools/ai/run_pipeline_dry_run_matrix.py` | active-current |
| markdown_reference_missing | `docs/AI_SMART_POLICY.md` | `/Tools/ai/review_agent_memory.py` | active-current |
| markdown_reference_missing | `docs/AI_SMART_POLICY.md` | `/Tools/validation/check_agent_memory_policy.py` | active-current |
| markdown_reference_missing | `docs/AI_SMART_POLICY.md` | `/Tools/validation/check_generated_artifact_path_policy.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_SMART_POLICY.md` | `/Tools/validation/check_generated_artifact_path_policy.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_SMART_POLICY.md` | `/Tools/ai/review_agent_memory.py` | active-current |
| markdown_python_command_missing_script | `docs/AI_SMART_POLICY.md` | `/Tools/validation/check_agent_memory_policy.py` | active-current |
| markdown_reference_missing | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/Tools/git/auto_push_generated_artifacts.ps1` | active-current |
| markdown_reference_missing | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/your_app_regenerate_indexes.ps1` | active-current |
| markdown_powershell_command_missing_script | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/Tools/git/auto_push_generated_artifacts.ps1` | active-current |
| markdown_powershell_command_missing_script | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/Tools/git/auto_push_generated_artifacts.ps1` | active-current |
| markdown_powershell_command_missing_script | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/Tools/git/auto_push_generated_artifacts.ps1` | active-current |
| markdown_powershell_command_missing_script | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/Tools/git/auto_push_generated_artifacts.ps1` | active-current |
| markdown_powershell_command_missing_script | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/Tools/git/auto_push_generated_artifacts.ps1` | active-current |
| markdown_powershell_command_missing_script | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/Tools/git/auto_push_generated_artifacts.ps1` | active-current |
| markdown_powershell_command_missing_script | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/Tools/git/auto_push_generated_artifacts.ps1` | active-current |
| markdown_powershell_command_missing_script | `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` | `/Tools/git/auto_push_generated_artifacts.ps1` | active-current |
| markdown_reference_missing | `docs/COMPATIBILITY.md` | `blender_compat.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `/Tools/ai/run_pipeline_dry_run_matrix.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `/Tools/npu/build_npu_code_context.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `/Tools/npu/build_project_ai_index.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `/Tools/validation/check_ai_pipeline_modules.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `/Tools/validation/check_json_artifacts.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `/Tools/validation/check_package_structure.py` | active-current |
| markdown_reference_missing | `docs/DEVELOPER_GUIDE.md` | `/Tools/validation/check_python_syntax.py` | active-current |
