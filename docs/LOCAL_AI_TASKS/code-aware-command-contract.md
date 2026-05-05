# Code-aware command contract

This document summarizes executable command contracts visible in current code.
Root docs should link here or to canonical runbooks instead of duplicating long command blocks.

## Python argparse contracts

| Script | Args |
|---|---|
| `Tools/ai/agent_memory_routing_policy.py` | `--broker-request-output, --clear-operational, --markdown-output, --memory-search-limit, --objective, --operational-query, --output, --persistent-query, --profile, --promotion-candidate, --remember-note, --repo-root` |
| `Tools/ai/agent_review_warning_policy.py` | `--decision-report, --final-report, --markdown-output, --min-patch-plans, --min-recommendations, --output, --repo-root, --report-file` |
| `Tools/ai/agent_runtime_sqlite_memory.py` | `--action, --allow-persistent-write, --confirm, --content, --database, --limit, --markdown-output, --output, --persistent-database, --query, --repo-root, --request-id, --role, --scope, --summary, --tag` |
| `Tools/ai/agent_runtime_tool_broker.py` | `--dry-run, --markdown-output, --output, --repo-root, --request-file, --stamp, --timeout-seconds, --tool-output-dir` |
| `Tools/ai/analyze_gpu_npu_run_sync.py` | `--markdown-output, --orchestrator, --output, --repo-root` |
| `Tools/ai/apply_full0to10_auto_refactor_patch_specs.py` | `--apply, --markdown-output, --max-specs, --output, --patch-specs, --repo-root` |
| `Tools/ai/apply_full0to10_markdown_split_patch_specs.py` | `--apply-shadow, --markdown-output, --max-specs, --output, --patch-specs, --repo-root, --shadow-root` |
| `Tools/ai/build_agent_agnostic_tool_inventory.py` | `--markdown-output, --max-items-per-category, --max-tools, --output, --repo-root, --root` |
| `Tools/ai/build_agent_memory_inventory.py` | `--markdown-output, --max-memory-chars, --max-policy-items, --max-preview-records, --max-sqlite-tables, --memory-db, --memory-db-limit, --memory-jsonl, --objective, --output, --repo-root` |
| `Tools/ai/build_agent_review_code_patch_plan.py` | `--code-contract-drift-report, --code-interpreter-report, --line-count-csv, --markdown-output, --output, --repo-root` |
| `Tools/ai/build_agent_review_evidence_sufficiency.py` | `--markdown-output, --output, --refined-proposals, --refined-review, --repo-root, --report-file` |
| `Tools/ai/build_agent_review_patch_bundle.py` | `--basename, --markdown-output, --output, --output-dir, --patch-plan, --repo-root, --stamp, --write-bundle` |
| `Tools/ai/build_agent_review_patch_plan.py` | `--evidence, --markdown-output, --max-patch-plans, --orchestrator, --output, --repo-root` |
| `Tools/ai/build_agent_state_packet.py` | `--include-file, --max-memory-chars, --max-record-chars, --memory-db, --memory-db-limit, --memory-jsonl, --memory-note, --objective, --output-dir, --packet-name, --repo-root, --save-inputs-to-memory-db` |
| `Tools/ai/build_agent_transient_request_context.py` | `--markdown-output, --max-chars-per-file, --max-raw-files, --memory-note, --objective, --output, --raw-file, --repo-root, --report-file` |
| `Tools/ai/build_ai_context_pack.py` | `--basename, --evidence-basename, --evidence-dir, --max-file-chars, --max-total-chars, --no-evidence, --output-dir, --profile, --repo-root` |
| `Tools/ai/build_analysis_input_bundle.py` | `--exclude-dir, --include-extension, --input, --markdown-output, --max-file-chars, --max-total-chars, --output, --repo-root` |
| `Tools/ai/build_code_edit_proposal_from_plan.py` | `--code-patch-plan, --edit-kind, --markdown-output, --output, --plan-id, --repo-root, --unified-diff` |
| `Tools/ai/build_code_interpreter_report.py` | `--exclude-dir, --input, --markdown-output, --output, --repo-root` |
| `Tools/ai/build_code_patch_artifact_pack.py` | `--code-patch-plan, --docs-followup, --markdown-output, --output, --repo-root` |
| `Tools/ai/build_code_patch_docs_followup.py` | `--code-patch-plan, --markdown-output, --output, --repo-root` |
| `Tools/ai/build_deterministic_recommendations.py` | `--evidence, --gpu-report, --markdown-output, --max-recommendations, --orchestrator, --output, --patch-plan-orchestrator-output, --repo-root, --tool-report` |
| `Tools/ai/build_dry_run_matrix_evidence_bundle.py` | `--basename, --matrix-report, --output-dir, --repo-root, --validation-report` |
| `Tools/ai/build_full0to10_accelerator_control.py` | `--no-external-probes, --output, --output-dir, --repo-root, --request, --timeout-seconds` |
| `Tools/ai/build_full0to10_auto_refactor_plan.py` | `--markdown-output, --output, --patch-specs-output, --repo-root, --scan-root` |
| `Tools/ai/build_full0to10_effective_use_optimization.py` | `--db, --no-external-probes, --output, --output-dir, --repo-root, --request, --timeout-seconds` |
| `Tools/ai/build_full0to10_final_product_quality_package.py` | `--output, --output-dir, --run-root` |
| `Tools/ai/build_full0to10_final_tool_product.py` | `--no-external-probes, --output, --output-dir, --repo-root, --request, --timeout-seconds` |
| `Tools/ai/build_full0to10_hardware_tool_capability.py` | `--markdown-output, --no-external-probes, --output, --repo-root, --timeout-seconds` |
| `Tools/ai/build_full0to10_light_profile_promotion.py` | `--output, --output-dir, --run-report` |
| `Tools/ai/build_full0to10_memory_visibility_assertion.py` | `--output, --output-dir, --repo-root` |
| `Tools/ai/build_full0to10_provider_execution_bridge.py` | `--allow-provider-generation, --no-external-probes, --operator-intent, --output, --output-dir, --repo-root, --request, --timeout-seconds` |
| `Tools/ai/build_full0to10_provider_governor.py` | `--allow-provider-generation, --no-external-probes, --operator-intent, --output, --output-dir, --repo-root, --request, --strict-permit, --timeout-seconds` |
| `Tools/ai/build_full0to10_provider_invocation_plan.py` | `--allow-provider-generation, --no-external-probes, --operator-intent, --output, --output-dir, --repo-root, --request, --timeout-seconds` |
| `Tools/ai/build_full0to10_provider_telemetry_semantic_validation.py` | `--output, --output-dir, --run-root` |
| `Tools/ai/build_full0to10_provider_tool_feedback_loop.py` | `--output, --output-dir, --run-root` |
| `Tools/ai/build_full0to10_quality_gate.py` | `--markdown-output, --output, --patch-specs, --repo-root` |
| `Tools/ai/build_full0to10_quality_stack_summary.py` | `--markdown-output, --output, --repo-root, --search-root` |
| `Tools/ai/build_full0to10_repo_quality_packet.py` | `--allow-output-outside-output, --input, --max-files, --output, --output-dir, --output-file, --repo-root, --request, --tool, --write-output` |
| `Tools/ai/build_full0to10_run_manifest.py` | `--markdown-output, --output, --repo-root, --scan-root, --workers` |
| `Tools/ai/build_full0to10_runtime_tool_registry.py` | `--markdown-output, --output, --repo-root` |
| `Tools/ai/build_full0to10_track_input_contract.py` | `--max-candidates, --output, --output-dir, --repo-root, --require-inputs, --track-name` |
| `Tools/ai/build_full_context_golden_proposals.py` | `--markdown-output, --output, --repo-root, --source-report` |
| `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | `--budget-minutes, --bundle-validation-passed, --decision-loop, --evidence-to-commit, --files-per-round, --gpu-npu-sync, --gpu-report, --markdown-output, --max-chars-per-file, --max-context-files, --max-new-tokens, --m...` |
| `Tools/ai/build_github_evidence_bundle.py` | `--artifact, --basename, --chunk-large-files-lines, --max-included-artifact-chars, --max-included-artifacts, --no-auto-include-related-artifacts, --output-dir, --recursive-artifact-root, --recursive-include-unstamped, ...` |
| `Tools/ai/build_gpu_repair_failure_recommendation.py` | `--gpu-report, --markdown-output, --orchestrator, --output, --repo-root` |
| `Tools/ai/build_local_ai_enrichment_plan.py` | `--basename, --markdown-output, --objective, --output, --profile, --repo-root, --task-file` |
| `Tools/ai/build_megalithic_review_pr_draft.py` | `--base-branch, --markdown-output, --output, --proposals, --review, --title-prefix` |
| `Tools/ai/build_music_intermediates.py` | `--analysis-json, --output-dir` |
| `Tools/ai/build_patch_specs_from_proposals.py` | `--basename, --max-proposals, --output-dir, --proposal, --repo-root` |
| `Tools/ai/build_refactor_duplication_audit.py` | `--bundle-smoke-report, --code-interpreter-report, --input-audit-report, --line-count-report, --markdown-output, --max-candidates, --memory-routing-report, --output, --python-syntax-report, --repo-root, --report, --roo...` |
| `Tools/ai/build_repository_change_proposals.py` | `--basename, --output-dir, --profile, --repo-root, --report-file` |
| `Tools/ai/build_repository_consistency_map.py` | `--markdown-output, --max-detail-items, --max-snippet-chars, --output, --repo-root, --workers` |
| `Tools/ai/build_runtime_tool_capability_manifest.py` | `--markdown-output, --output, --repo-root, --tool-usage` |
| `Tools/ai/build_runtime_tool_usage_telemetry.py` | `--broker-report, --decision-loop, --gpu-npu-sync, --gpu-report, --markdown-output, --max-entries, --orchestrator, --output, --repo-root, --stamp` |
| `Tools/ai/build_selective_execution_plan.py` | `--context-pack-evidence, --context-pack-evidence-md, --dry-run-evidence, --execution-plan-dir, --markdown-output, --output, --provider-evidence, --repo-root, --tech-debt, --validation-report-contract` |
| `Tools/ai/build_semantic_evidence_chunks.py` | `--basename, --chunk-max-chars, --chunk-output-dir, --chunk-overlap-lines, --no-ollama, --ollama-host, --ollama-keep-alive, --ollama-max-input-chars, --ollama-model, --ollama-timeout-seconds, --output-dir, --repo-root,...` |
| `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | `--architecture-md, --artifact, --basename, --chunk-large-files-lines, --code-interpreter-report, --contract-replay-report, --gpu-report, --include-missing-optional, --max-included-artifact-chars, --max-included-artifa...` |
| `Tools/ai/build_workload_quality_lane_routing.py` | `--context-file, --markdown-output, --output, --quality-report, --repo-root` |
| `Tools/ai/check_local_resource_lanes.py` | `--markdown-output, --model, --output, --parallel, --probe-ollama-generate, --repo-root, --require-lane, --skip-gpu, --skip-npu, --skip-ollama, --timeout` |
| `Tools/ai/check_npu_provider_environment.py` | `--markdown-output, --npu-python, --output, --repo-root, --timeout-seconds` |
| `Tools/ai/enrich_github_evidence_bundle_code_plan.py` | `--bundle, --markdown-output, --output, --repo-root` |
| `Tools/ai/full0to10_memory_tool.py` | `--db, --embedding-model, --embedding-provider, --limit, --markdown-output, --mode, --namespace, --ollama-url, --output, --path, --query, --text, --title` |
| `Tools/ai/full0to10_runtime_tool.py` | `--args-file, --args-json, --output, --repo-root` |
| `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` | `--artifact, --basename, --max-included-artifact-chars, --max-included-artifacts, --no-auto-include-related-artifacts, --output-dir, --repo-root, --report, --selected-chunks-evidence` |
| `Tools/ai/merge_ai_candidates.py` | `--input, --limit, --output` |
| `Tools/ai/patch_unified_launcher_light_full0to10.py` | `--apply, --backup-dir, --launcher, --repo-root, --report` |
| `Tools/ai/pipeline/cli.py` | `--agent-state-packet, --analysis-json, --build-chunks, --build-music-summary, --continue-on-error, --dry-run, --gpu-command, --guardrail-auto-remediate, --guardrail-max-passes, --no-guardrail-auto-remediate, --no-npu-...` |
| `Tools/ai/promote_patch_spec_draft.py` | `--basename, --draft, --output-dir, --replacement-plan, --repo-root` |
| `Tools/ai/refine_megalithic_review_signals.py` | `--markdown-output, --output, --proposal-output, --proposals, --review` |
| `Tools/ai/replay_gpu_planner_json_contract.py` | `--gpu-report, --markdown-output, --output, --repo-root` |
| `Tools/ai/review_agent_memory.py` | `--fail-on-risk, --markdown-output, --memory-db, --memory-db-limit, --memory-jsonl, --output, --repo-root` |
| `Tools/ai/review_wave_entrypoints.py` | `--output, --repo-root, --target` |
| `Tools/ai/run_agent_gpu_deep_planning_review.py` | `--budget-minutes, --context-root, --evidence, --files-per-round, --keep-alive, --markdown-output, --max-chars-per-file, --max-context-files, --max-new-tokens, --max-rounds, --objective, --ollama-base-url, --ollama-mod...` |
| `Tools/ai/run_agent_gpu_deep_planning_supervised.py` | `--budget-minutes, --checkpoint-dir, --context-root, --disable-runtime-tool-bootstrap, --enable-runtime-tool-broker, --evidence, --files-per-round, --include-npu-auditor, --keep-alive, --markdown-output, --max-chars-pe...` |
| `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` | `--budget-minutes, --checkpoint-dir, --context-root, --disable-runtime-tool-bootstrap, --enable-runtime-tool-broker, --evidence, --files-per-round, --gpu-markdown-output, --gpu-output, --gpu-runner-direct-runtime-tool-...` |
| `Tools/ai/run_agent_review_decision_loop.py` | `--bridge-orchestrator-output, --evidence, --gpu-report, --markdown-output, --max-patch-plans, --max-recommendations, --min-patch-plans, --min-recommendations, --orchestrator, --output, --patch-plan-markdown, --patch-p...` |
| `Tools/ai/run_local_provider_probe.py` | `--model, --output, --repo-root, --run-npu, --run-ollama, --timeout` |
| `Tools/ai/run_megalithic_repo_review.py` | `--file-sample-limit, --include-all-code, --include-all-docs, --include-index, --include-output, --include-raw, --include-sqlite-memory, --markdown-output, --max-chars-per-file, --max-files, --max-raw-files, --max-sqli...` |
| `Tools/ai/run_npu_decode_smoke_diagnostic.py` | `--device, --max-new-tokens, --max-prompt-len, --min-response-len, --model-dir, --output, --prompt, --python-exe, --repo-root, --run-npu, --text-output, --timeout` |
| `Tools/ai/run_npu_gpu_deep_review_auditor.py` | `--context-output, --disable-npu-tool-fallback, --gpu-review, --markdown-output, --max-context-chars, --max-new-tokens, --max-npu-tool-requests, --max-prompt-chars, --max-runtime-tool-context-chars, --metadata-only, --...` |
| `Tools/ai/run_pipeline_dry_run_matrix.py` | `--continue-on-error, --markdown-output, --matrix-workers, --output, --output-dir, --repeat-cases, --repo-root` |
| `Tools/ai/select_semantic_code_chunks.py` | `--chunks, --markdown-output, --max-chunks, --max-excerpt-chars, --max-total-chars, --no-code, --output, --path-boost, --query, --repo-root` |
| `Tools/ai/smart_ai_gatekeeper.py` | `--artifact-dir, --context-packet, --current-attempt, --max-repair-attempts, --output, --repair-output, --target-file` |
| `Tools/ai/suggest_repository_updates.py` | `--basename, --context-file, --extra-context, --extra-report, --max-context-chars, --model, --output-dir, --profile, --repo-root, --report-file, --use-ollama` |
| `Tools/ai/summarize_full0to10_light_evidence.py` | `--markdown-output, --output, --run-report` |
| `Tools/ai/validate_ai_artifacts.py` | `--allow-errors, --artifact-dir, --capsules-dir, --output, --package-dir, --repo-root` |
| `Tools/docs/apply_md_code_coherence_refactor.py` | `--apply, --doc-line-limit, --max-lines, --repo-root, --report` |
| `Tools/docs/build_code_aware_md_coherence.py` | `--markdown-output, --max-lines, --max-markdown-finding-rows, --output, --repo-root` |
| `Tools/docs/split_large_markdown.py` | `--apply, --include-evidence, --markdown-output, --max-lines, --output, --repo-root, --scope` |
| `Tools/npu/build_ai_service_packet.py` | `--analysis, --analysis-ai-context, --blender-keyframes-json, --dual-plan, --music-context, --npu-notes, --npu-status, --track-stem, --track-summary` |
| `Tools/npu/build_blender_manual_context.py` | `--ensure-only, --limit-files, --manual-root` |
| `Tools/npu/build_music_context.py` | `--analysis, --analysis-ai-context, --blender-keyframes-json, --compact-json, --ollama-model, --run-ollama, --scene-file, --segment-seconds, --track-summary` |
| `Tools/npu/build_npu_knowledge_broker_packet.py` | `--adapter-manifest, --context-pack, --markdown-output, --max-candidates, --objective, --output, --repo-root, --selected-chunks` |
| `Tools/npu/build_project_ai_index.py` | `--force, --max-chunk-chars` |
| `Tools/npu/build_provider_result_report.py` | `--inline-json, --model, --no-json-parse, --output, --payload, --provider, --repo-root, --use-samples` |
| `Tools/npu/build_runtime_output_manifest.py` | `--extra-path, --output, --provider-execution-performed, --repo-root, --track-stem` |
| `Tools/npu/build_semantic_code_chunks.py` | `--dry-run, --manifest, --output, --repo-root, --source-dir` |
| `Tools/npu/npu_guardrail_service.py` | `--device, --hard-fail, --input, --max-chars, --model-dir, --output, --python-exe, --recursive, --soft-fail, --strict, --write-action-queue` |
| `Tools/npu/run_dual_ai_pipeline.py` | `--analysis, --analysis-ai-context, --asset-inventory, --blender-keyframes-json, --compact-json, --creative-model, --force-npu, --include-manual, --max-new-tokens, --npu-chunk-tokens, --npu-final-tokens, --npu-model-di...` |
| `Tools/npu/run_npu_artifact_reviewer.py` | `--device, --input, --max-workers, --output` |
| `Tools/npu/run_npu_review.py` | `--chunk-chars, --chunk-dir, --chunk-overlap-chars, --context, --device, --domain, --engine, --keep-ollama-model, --keep-ollama-server, --max-chunk-tokens, --max-chunks, --max-context-chars, --max-new-tokens, --max-pro...` |
| `Tools/npu/run_ollama_music_agent.py` | `--base-url, --context-json, --fallback-context-json, --keep-alive, --keep-model, --keep-server, --max-new-tokens, --model, --out-json, --out-md, --temperature` |
| `Tools/repo_patch_runner/apply_repo_mods.py` | `--dry-run, --no-backup, --repo-root, --show-diff, --spec, --write` |
| `Tools/validation/apply_docs_contract_drift_fixes.py` | `--apply, --markdown-output, --output, --repo-root` |
| `Tools/validation/build_full_python_line_count_markdown.py` | `--csv, --output, --repo-root, --report-output, --stamp` |
| `Tools/validation/build_markdown_inventory.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/build_python_line_count_csv.py` | `--csv-output, --exclude-dir, --include-default-excludes, --markdown-output, --repo-root, --report-output, --timestamped` |
| `Tools/validation/build_script_inventory.py` | `--csv-output, --markdown-max-rows, --markdown-output, --output, --repo-root` |
| `Tools/validation/check_agent_memory_policy.py` | `--memory-db, --output, --repo-root` |
| `Tools/validation/check_ai_context_pack_contract.py` | `--evidence, --output, --pack, --repo-root` |
| `Tools/validation/check_ai_dry_run_matrix_cases.py` | `--min-case-count, --output, --repo-root` |
| `Tools/validation/check_ai_dry_run_matrix_contract.py` | `--matrix-report, --output, --repo-root` |
| `Tools/validation/check_ai_dry_run_matrix_outputs.py` | `--matrix-report, --output, --repo-root` |
| `Tools/validation/check_ai_model_json.py` | `--output, --repo-root` |
| `Tools/validation/check_ai_pipeline_modules.py` | `--output, --repo-root` |
| `Tools/validation/check_ai_pipeline_report_contract.py` | `--output, --repo-root, --report, --require-dry-run` |
| `Tools/validation/check_ai_workload_report_quality.py` | `--include-missing-known-reports, --output, --repo-root, --report, --report-dir` |
| `Tools/validation/check_artifact_domain_registry.py` | `--output, --repo-root` |
| `Tools/validation/check_blender_shared_compat_smoke.py` | `--output, --output-dir, --repo-root, --require-blender` |
| `Tools/validation/check_code_contract_drift.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/check_core_activation_agnostic_contract.py` | `--markdown-output, --output, --repo-root, --workflow` |
| `Tools/validation/check_docs_contract_drift.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/check_docs_links.py` | `--exclude, --output, --repo-root` |
| `Tools/validation/check_dry_run_matrix_evidence_bundle.py` | `--evidence, --output, --repo-root` |
| `Tools/validation/check_execution_plan_status.py` | `--output, --repo-root` |
| `Tools/validation/check_full0to10_bundle_contracts.py` | `--bundle, --evidence-dir, --markdown-output, --output, --repo-root` |
| `Tools/validation/check_full0to10_generated_artifact_quarantine.py` | `--output, --repo-root` |
| `Tools/validation/check_full_context_golden_docs_contract.py` | `--output, --repo-root` |
| `Tools/validation/check_full_context_golden_proposals.py` | `--min-proposals, --output, --proposal, --repo-root` |
| `Tools/validation/check_generated_artifact_path_policy.py` | `--allowed-exact-path, --allowed-prefix, --artifact-report, --output, --path, --repo-root` |
| `Tools/validation/check_generated_blender_script_policy.py` | `--output, --path, --repo-root` |
| `Tools/validation/check_generated_python_policy.py` | `--output, --path, --repo-root` |
| `Tools/validation/check_github_evidence_bundle.py` | `--bundle, --output, --repo-root` |
| `Tools/validation/check_json_artifacts.py` | `--exclude, --include-index-ai, --max-size-mb, --output, --repo-root` |
| `Tools/validation/check_local_ai_adapter_manifest.py` | `--manifest, --output, --repo-root` |
| `Tools/validation/check_local_ai_enrichment_plan.py` | `--output, --plan, --repo-root` |
| `Tools/validation/check_markdown_line_limits.py` | `--include-evidence, --markdown-output, --max-lines, --output, --repo-root, --scope` |
| `Tools/validation/check_md_code_coherence.py` | `--max-high, --max-lines, --max-medium, --output, --repo-root, --report` |
| `Tools/validation/check_npu_decode_quality_remediation.py` | `--output, --quality-report, --repo-root` |
| `Tools/validation/check_npu_knowledge_broker_packet.py` | `--max-candidates, --min-candidates, --output, --packet, --repo-root` |
| `Tools/validation/check_npu_pipeline_docs.py` | `--output, --repo-root` |
| `Tools/validation/check_npu_pipeline_helper_tests.py` | `--output, --repo-root` |
| `Tools/validation/check_npu_pipeline_modules.py` | `--output, --repo-root` |
| `Tools/validation/check_package_structure.py` | `--output, --repo-root, --strict` |
| `Tools/validation/check_patch_spec_drafts.py` | `--manifest, --output, --repo-root, --spec` |
| `Tools/validation/check_provider_result_parsing.py` | `--output, --repo-root` |
| `Tools/validation/check_python_syntax.py` | `--exclude, --output, --repo-root` |
| `Tools/validation/check_refactor_status_consistency.py` | `--output, --repo-root` |
| `Tools/validation/check_repository_change_proposals.py` | `--output, --proposal, --repo-root` |
| `Tools/validation/check_reviewed_patch_specs.py` | `--manifest, --output, --repo-root, --spec` |
| `Tools/validation/check_selected_semantic_chunks.py` | `--bundle, --evidence-output, --markdown-output, --max-total-chars, --output, --repo-root` |
| `Tools/validation/check_selective_execution_plan.py` | `--output, --plan, --repo-root` |
| `Tools/validation/check_validation_report_contract.py` | `--output, --repo-root, --report-dir, --report-file, --require-recommended` |
| `Tools/validation/run_agent_memory_routing_policy_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_agent_review_code_patch_plan_smoke.py` | `--output, --repo-root, --report` |
| `Tools/validation/run_agent_review_decision_loop_smoke.py` | `--markdown-output, --output, --repo-root, --timeout-seconds` |
| `Tools/validation/run_agent_review_evidence_sufficiency_smoke.py` | `--markdown-output, --output, --refined-proposals, --refined-review, --repo-root, --report-file, --timeout-seconds, --tool-markdown-output, --tool-output` |
| `Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py` | `--markdown-output, --output, --repo-root, --workflow` |
| `Tools/validation/run_agent_review_patch_bundle_builder_smoke.py` | `--markdown-output, --output, --repo-root, --timeout-seconds` |
| `Tools/validation/run_agent_review_patch_plan_full_validation.py` | `--bundle-basename, --bundle-validation-output, --docs-links-output, --evidence, --evidence-output-dir, --expect-fallback, --git-timeout-seconds, --markdown-output, --min-patch-plans, --orchestrator, --output, --patch-...` |
| `Tools/validation/run_agent_review_patch_plan_smoke.py` | `--evidence, --expect-fallback, --markdown-output, --min-patch-plans, --orchestrator, --output, --repo-root, --timeout-seconds, --tool-markdown-output, --tool-output` |
| `Tools/validation/run_agent_review_warning_policy_smoke.py` | `--markdown-output, --output, --repo-root, --timeout-seconds` |
| `Tools/validation/run_agent_runtime_tool_broker_smoke.py` | `--dry-run, --markdown-output, --output, --repo-root` |
| `Tools/validation/run_agnostic_ai_tools_smoke_matrix.py` | `--dry-run, --include-ollama-live, --include-workflow, --markdown-output, --memory-db, --ollama-max-new-tokens, --output, --repo-root, --timeout-seconds, --work-dir` |
| `Tools/validation/run_agnostic_context_stack_smoke.py` | `--dry-run, --markdown-output, --memory-db, --objective, --output, --repo-root, --timeout-seconds, --work-dir` |
| `Tools/validation/run_ai_workload_quality_report_dir_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_ai_workload_report_quality_stamp_scoped_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_code_edit_proposal_smoke.py` | `--output, --proposal, --repo-root` |
| `Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_full0to10_accelerator_control_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_auto_refactor_planner_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_bundle_contracts_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_controlled_refactor_applier_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_effective_use_optimization_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_final_product_import_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_final_product_quality_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_final_tool_product_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_hardware_tool_capability_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_light_evidence_only_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_light_profile_mega_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_light_profile_promotion_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_manifest_gate_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_markdown_shadow_guard_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_markdown_split_shadow_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_memory_visibility_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_openvino_device_visibility_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_provider_execution_bridge_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_provider_governor_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_provider_invocation_plan_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_provider_telemetry_semantic_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_provider_tool_feedback_loop_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_quality_gate_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_quality_stack_preflight_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_quality_supervisor_safety_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_quality_supervisor_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_repo_quality_inputpath_normalization_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_repo_quality_packet_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_repo_quality_wrapper_diagnostics_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_runtime_memory_tool_registry_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_sqlite_embedding_hybrid_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_sqlite_memory_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_startup_track_input_guard_smoke.py` | `--repo-root` |
| `Tools/validation/run_full0to10_track_input_contract_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_full0to10_workflow_exit_code_guard_smoke.py` | `--repo-root` |
| `Tools/validation/run_full_toolbox_deterministic_chunks_telemetry_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_gpu_planner_json_contract_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_gpu_runner_provider_error_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py` | `--markdown-output, --output, --repo-root, --timeout-seconds` |
| `Tools/validation/run_npu_runtime_tool_context_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_npu_runtime_tool_execution_smoke.py` | `--markdown-output, --output, --repo-root, --timeout-seconds, --tool-output-dir` |
| `Tools/validation/run_npu_runtime_tool_fallback_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_npu_tool_request_contract_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_provider_empty_response_diagnostics_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_refactor_duplication_audit_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_repository_consistency_map_smoke.py` | `--map-report, --markdown-output, --output, --repo-root, --timeout-seconds, --workers` |
| `Tools/validation/run_runtime_sqlite_persistent_write_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_runtime_tool_feedback_loop_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_runtime_tool_guidance_fallback_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_schema_repair_context_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_schema_repair_retry_bootstrap_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_schema_repair_retry_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_startup_check_cli_contract_smoke.py` | `--markdown-output, --output, --repo-root` |
| `Tools/validation/run_substantive_planning_smoke.py` | `--markdown-output, --min-patch-plans, --min-recommendations, --min-substantive, --output, --patch-plan, --recommendations, --repo-root` |
| `Tools/validation/run_unified_full0to10_supervisor_gate_smoke.py` | `--repo-root, --work-dir` |
| `Tools/validation/run_unified_launcher_lightfull0to10_smoke.py` | `--repo-root` |
| `Tools/workflow/ai_runtime_diagnostics.py` | `--json-out, --md-out, --track-stem` |
| `Tools/workflow/smart_ai_context.py` | `--include-file, --max-capsule-chars, --max-packet-chars, --output-dir, --repo-root, --task, --track-stem` |
| `Tools/workflow/startup_check.py` | `--json, --output, --project, --repo-root, --root, --text-output` |
| `Tools/workflow/workflow_debug.py` | `--interval, --json, --no-write-probe, --watch` |
| `analyze_wav.py` | `--fps, --gamma-high, --gamma-low, --gamma-mid, --high-max, --hop-length, --low-max, --mid-max, --n-fft, --ollama-model, --output-dir, --run-ollama-agent, --skip-music-context, --smooth-high, --smooth-low, --smooth-mid...` |
| `build_track_summary.py` | `--analysis-json, --out-json, --skip-music-context` |

## PowerShell parameter contracts

| Script | Parameters |
|---|---|
| `Tools/git/auto_push_generated_artifacts.ps1` | `-DryRun, -IncludeFullAnalysisJson, -Message, -NoPush, -Paths, -RepoPath` |
| `Tools/git/auto_push_generated_data.ps1` | `-Branch, -DryRun, -FullProject, -IncludeAllGenerated, -IncludeDocs, -IncludeOutputJson, -Message, -PullFirst, -RepoPath` |
| `Tools/npu/run_npu_context.ps1` | `-BuildOnly, -CreativeModel, -DualPhase, -Engine, -IncludeManual, -OllamaModel, -ReviewDomain, -RunDualAI, -RunOllamaMusicAgent, -SkipDualNpu, -SkipDualOllama, -SkipFinal, -TechnicalModel` |
| `Tools/workflow/install_weekly_local_ai_reset_task.ps1` | `-At, -DayOfWeek, -Force, -IncludeGeneratedIndexReset, -IncludeMemoryReset, -Install, -RetentionDays, -TaskName` |
| `Tools/workflow/repair_full_toolbox_datastamp_doc.ps1` | `-DocPath` |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1` | `-BudgetMinutes, -EvidenceDir, -FilesPerRound, -KeepAlive, -MaxCharsPerFile, -MaxContextFiles, -MaxNewTokens, -MaxPatchPlans, -MaxRecommendations, -MaxRounds, -MinPatchPlans, -MinRecommendations, -NpuAuditorEveryRounds...` |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1` | `-BudgetMinutes, -EvidenceDir, -FilesPerRound, -KeepAlive, -MaxCharsPerFile, -MaxContextFiles, -MaxNewTokens, -MaxRounds, -MinPatchPlans, -MinRecommendations, -NpuAuditorEveryRounds, -NpuAuditorTimeoutSeconds, -NpuFina...` |
| `Tools/workflow/run_ai_cycle_startup_preflight.ps1` | `-EnableNpuProviderEnvironmentCheck, -EvidenceDir, -ExtraArtifact, -ExtraReport, -InputAuditReport, -MaxIncludedArtifactChars, -MaxIncludedArtifacts, -Objective, -OutputRoot, -RepoRoot, -SkipCodeInterpreter, -SkipGpuCo...` |
| `Tools/workflow/run_docs_md_refactor_10min.ps1` | `-AllowDirty, -DryRun, -LaunchRunner, -NoBranch, -SkipGitSync, -Stamp, -TaskBranch` |
| `Tools/workflow/run_full0to10_accelerator_control.ps1` | `-NoExternalProbes, -OutputDir, -RepoRoot, -Request, -TimeoutSeconds` |
| `Tools/workflow/run_full0to10_auto_refactor_apply.ps1` | `-Apply, -ForwardedArgs, -MaxSpecs, -OutputDir, -PatchSpecs, -RepoRoot, -true` |
| `Tools/workflow/run_full0to10_auto_refactor_plan.ps1` | `-OutputDir, -RepoRoot, -WritePatchSpecs` |
| `Tools/workflow/run_full0to10_download_md_line_budget_chain.ps1` | `-ApplyDocSplit, -DownloadsDir, -RepoRoot, -UseAllInOne, -env` |
| `Tools/workflow/run_full0to10_effective_use_optimization.ps1` | `-Db, -NoExternalProbes, -OutputDir, -RepoRoot, -Request, -TimeoutSeconds` |
| `Tools/workflow/run_full0to10_final_tool_product.ps1` | `-NoExternalProbes, -OutputDir, -RepoRoot, -Request, -TimeoutSeconds` |
| `Tools/workflow/run_full0to10_hardware_tool_capability_probe.ps1` | `-NoExternalProbes, -OutputDir, -RepoRoot, -TimeoutSeconds` |
| `Tools/workflow/run_full0to10_light_evidence_only.ps1` | `-MaxRepoQualityFiles, -NoExternalProbes, -OutputDir, -RepoRoot, -SkipFinalProduct, -SkipMarkdownLineCheck, -Strict, -TimeoutSeconds, -TrackName` |
| `Tools/workflow/run_full0to10_light_profile_gate.ps1` | `-OutputDir, -RepoRoot, -RunReport, -Strict` |
| `Tools/workflow/run_full0to10_manifest_contract_gate.ps1` | `-Bundle, -EvidenceDir, -OutputDir, -RepoRoot, -Workers` |
| `Tools/workflow/run_full0to10_markdown_split_shadow.ps1` | `-ApplyShadow, -ForwardedArgs, -MaxSpecs, -OutputDir, -PatchSpecs, -RepoRoot, -ShadowRoot, -true` |
| `Tools/workflow/run_full0to10_provider_execution_bridge.ps1` | `-AllowProviderGeneration, -NoExternalProbes, -OperatorIntent, -OutputDir, -RepoRoot, -Request, -TimeoutSeconds` |
| `Tools/workflow/run_full0to10_provider_governor.ps1` | `-AllowProviderGeneration, -NoExternalProbes, -OperatorIntent, -OutputDir, -RepoRoot, -Request, -TimeoutSeconds` |
| `Tools/workflow/run_full0to10_provider_invocation_plan.ps1` | `-AllowProviderGeneration, -NoExternalProbes, -OperatorIntent, -OutputDir, -RepoRoot, -Request, -TimeoutSeconds` |
| `Tools/workflow/run_full0to10_quality_gate.ps1` | `-OutputDir, -PatchSpecs, -RepoRoot` |
| `Tools/workflow/run_full0to10_quality_stack_preflight.ps1` | `-NoExternalProbes, -OutputDir, -PatchSpecs, -RepoRoot, -TimeoutSeconds` |
| `Tools/workflow/run_full0to10_repo_quality_packet.ps1` | `-AllowOutputOutsideOutput, -DiagnosticsOnly, -InputPath, -MaxFiles, -OutputDir, -OutputFile, -RepoRoot, -Request, -Tool, -WriteOutput` |
| `Tools/workflow/run_full0to10_startup_check_guard.ps1` | `-OutputDir, -RepoRoot, -RequireTrackInputs, -StrictExit, -TrackName` |
| `Tools/workflow/run_full0to10_track_input_contract.ps1` | `-MaxCandidates, -OutputDir, -RepoRoot, -RequireInputs, -TrackName` |
| `Tools/workflow/run_full_memory_tool_regeneration.ps1` | `-ClearOperational, -EvidenceDir, -MaxIncludedArtifactChars, -MaxIncludedArtifacts, -Objective, -OutputRoot, -Profile, -RepoRoot, -SkipBroker, -SkipBundle, -SkipCodeInterpreter, -Stamp, -TimeoutSeconds` |
| `Tools/workflow/run_local_ai_core_tool_activation.ps1` | `-DryRun, -GenerateMacroPatchDrafts, -Objective, -RepoRoot, -RunMegalithicReview, -RunName, -TaskFile, -UseExplicitProviders, -UseOllamaForMegalithicReview` |
| `Tools/workflow/run_local_ai_markdown_task.ps1` | `-AllowDirty, -DryRun, -NoBranch, -OutputDir, -RunnerCommand, -SkipGitSync, -TaskBranch, -TaskFile` |
| `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | `-AgentStateBasename, -AgentStateMaxMemoryChars, -AgentStateObjective, -Basename, -BuildAgentStatePacket, -BuildContextPack, -BuildEnrichmentPlan, -BuildEvidence, -BuildSelectedChunksEvidence, -BuildSemanticChunks, -Ch...` |
| `Tools/workflow/run_local_validation_after_refactor.ps1` | `-BuildAiPacket, -ContinueOnError, -LogDir, -MatrixWorkers, -OllamaModel, -RepeatCases, -RepoRoot, -SkipPull, -UseOllama, -true` |
| `Tools/workflow/run_npu_pipeline_helper_validation.ps1` | `-OutputDir, -RepoRoot, -TrackStem` |
| `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | `-Basename, -ContextFile, -EvidenceBasename, -MaxContextChars, -Model, -OutputDir, -Profile, -ProposalBasename, -RepoRoot, -ReportFile, -RunNpuDecodeSmoke, -RunNpuProbe, -RunOllamaProbe, -UsePrimaryAdvisoryProvider` |
| `Tools/workflow/run_post_validation_ai_packet.ps1` | `-Basename, -ContextFile, -MaxContextChars, -Model, -OutputDir, -Profile, -ProposalBasename, -RepoRoot, -ReportFile, -UseOllama, -UsePrimaryAdvisoryProvider` |
| `Tools/workflow/run_unified_full0to10_quality_supervisor.ps1` | `-AllowGitSyncBranching, -ForwardedArgs, -Model, -NoBranch, -NoExternalProbes, -OutputDir, -PatchSpecs, -RepoRoot, -RunIntensity, -RunLauncher, -SkipGitSync, -SkipLauncher` |
| `Tools/workflow/run_unified_full0to10_with_contract_gate.ps1` | `-Bundle, -DryRun, -EvidenceDir, -ForwardedArgs, -GateOutputDir, -Model, -NoBranch, -RepoRoot, -RunIntensity, -SkipGitSync, -SkipLauncher` |
| `Tools/workflow/run_unified_light_full0to10_profile.ps1` | `-MaxRepoQualityFiles, -NoExternalProbes, -OutputDir, -RepoRoot, -SkipFinalProduct, -Strict, -TimeoutSeconds, -TrackName` |
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | `-AgentStateMaxMemoryChars, -AiPacketsDir, -AiPacketsRoot, -AllowDirty, -ApplyReset, -BudgetMinutes, -BuildEvidence, -BuildWorkloadQualityReport, -ConfirmResetText, -ContextPackMaxFileChars, -ContextPackMaxTotalChars, ...` |
| `Tools/workflow/startup_preflight.ps1` | `-Detail, -Name, -Status` |
| `workflow_gui.ps1` | `-DebugMode, -SkipStartupCheck` |
| `workflow_shell.ps1` | `-DebugMode, -SkipStartupCheck` |
