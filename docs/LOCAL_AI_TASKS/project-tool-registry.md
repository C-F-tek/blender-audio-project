# Project Tool Registry

Status: stable registry seed
Scope: IA-Carmine local AI orchestration, validation, provider diagnostics, evidence production and Blender/audio application tools.
Source policy: derive entries from stable docs and current repository code, not from historical evidence bundles.

## Classification taxonomy

| Class | Meaning |
|---|---|
| PROJECT_TOOL | Stable project CLI/tool usable by humans or workflows. |
| BROKER_TOOL | Safe runtime broker tool allowed through `agent_runtime_tool_broker.py`. |
| FULL_RUN_EVIDENCE | Tool/report participating in production evidence bundle. |
| PROVIDER_DIAGNOSTIC | Probe/quality/diagnostic for GPU/Ollama/NPU/provider lane. |
| PATCH_PLAN_SUPPORT | Tool supporting recommendations, patch plans or validation. |
| MEMORY_LANE | Tool handling memory/context/state. |
| DOCS_MAINTENANCE | Documentation inventory, link, pruning or hygiene tool. |
| BLENDER_AUDIO_PIPELINE | Application-layer Blender/audio/render/encode tool. |
| LOCAL_UI_OR_MANUAL | Local/manual UI helper. |
| GIT_WRITE_TOOL | Tool capable of Git writes; never broker-default. |
| SUPPORT_LIBRARY | Library/helper module, not direct CLI entrypoint. |
| GENERATED_OR_CANDIDATE | Generated/candidate script, not yet promoted. |

## Registry fields

Each entry uses:

```text
path
tool_id
classification
current_status
broker_eligible
full_run_lane
provider_execution
source_writes
runtime_outputs
git_tracked_outputs
validation_command
guardrails
promotion_notes
```

## Global guardrails

```text
Do not promote Blender, FFmpeg or audio runtime tools to broker tools.
Do not use docs/LOCAL_VALIDATION_EVIDENCE/** as ordinary patch-plan targets.
Do not target output/**, indexAI/code_chunks/**, indexAI/project_code_chunks/** or renders/**.
Do not commit runtime artifacts, SQLite databases or generated patch bundles.
Broker tools must remain report-only unless explicit policy says otherwise.
Provider execution must be explicit and report-bound.
Patch application must remain explicit and manual-review gated.
```

## Broker tools

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/ai/agent_runtime_tool_broker.py` | `agent_runtime_tool_broker` | `BROKER_TOOL;SUPPORT_LIBRARY` | stable dispatcher | n/a dispatcher | broker runtime lane | no | no | caller-defined JSON/MD reports | none directly | `python -m py_compile .\Tools\ai\agent_runtime_tool_broker.py` | allowlist-only; no arbitrary shell | Keep as broker gate, not as generic executor. |
| `Tools/validation/check_python_syntax.py` | `check_python_syntax` | `BROKER_TOOL;FULL_RUN_EVIDENCE` | stable | yes | baseline validation | no | no | `output/validation/python_syntax*.json` | compact evidence only | `python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax.json` | report-only | Keep in minimal broker bootstrap. |
| `Tools/ai/build_python_line_count_csv.py` | `build_python_line_count_csv` | `BROKER_TOOL;FULL_RUN_EVIDENCE` | stable | yes | inventory evidence | no | no | CSV inventory | optional compact CSV evidence | `python -m py_compile .\Tools\ai\build_python_line_count_csv.py` | exclude venv/cache/runtime dirs | Useful for size/regression tracking. |
| `Tools/validation/check_validation_report_contract.py` | `check_validation_report_contract` | `BROKER_TOOL;FULL_RUN_EVIDENCE` | stable | yes | report contract validation | no | no | `output/validation/validation_report_contract.json` | compact evidence only | `python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json` | report-only | Required before committing evidence. |
| `Tools/ai/build_agent_memory_inventory.py` | `build_agent_memory_inventory` | `BROKER_TOOL;MEMORY_LANE;FULL_RUN_EVIDENCE` | stable | yes | memory inventory | no | no by default | `output/ai_pipeline/*memory_inventory*.json` | compact evidence only | `python -m py_compile .\Tools\ai\build_agent_memory_inventory.py` | read-only unless explicit policy | Do not enable persistent writes by default. |
| `Tools/ai/build_agent_agnostic_tool_inventory.py` | `build_agent_agnostic_tool_inventory` | `BROKER_TOOL;FULL_RUN_EVIDENCE` | stable | yes | tool inventory | no | no | `output/ai_pipeline/*tool_inventory*.json` | compact evidence only | `python -m py_compile .\Tools\ai\build_agent_agnostic_tool_inventory.py` | report-only | Keep feeding tool-placement audits. |
| `Tools/ai/build_agent_transient_request_context.py` | `build_agent_transient_request_context` | `BROKER_TOOL;PATCH_PLAN_SUPPORT` | stable | yes | transient request context | no | no | `output/ai_pipeline/*transient_request_context*.json` | compact evidence only | `python -m py_compile .\Tools\ai\build_agent_transient_request_context.py` | no source writes | Useful as task-context lane. |
| `Tools/validation/run_gpu_planner_json_contract_smoke.py` | `run_gpu_planner_json_contract_smoke` | `BROKER_TOOL;PROVIDER_DIAGNOSTIC` | stable smoke | yes | GPU JSON contract smoke | no | no | `output/validation/*gpu_planner_json_contract*.json` | compact evidence only | `python -m Tools.validation run_gpu_planner_json_contract_smoke --repo-root . --output .\output\validation\gpu_planner_json_contract_smoke.json` | no real provider call | Keep provider-free. |
| `Tools/ai/build_code_interpreter_report.py` | `build_code_interpreter_report` | `BROKER_TOOL;FULL_RUN_EVIDENCE` | stable | yes | static code-interpreter report | no | no | `output/ai_pipeline/*code_interpreter*.json` | compact evidence only | `python -m py_compile .\Tools\ai\build_code_interpreter_report.py` | report-only | Do not execute arbitrary code. |
| `Tools/validation/check_local_ai_adapter_manifest.py` | `check_local_ai_adapter_manifest` | `BROKER_TOOL;FULL_RUN_EVIDENCE` | stable | yes | adapter manifest/telemetry contract | no | no | `output/validation/*adapter_manifest*.json` | compact evidence only | `python -m Tools.validation check_local_ai_adapter_manifest --repo-root . --manifest <manifest.json> --output .\output\validation\adapter_manifest_contract.json` | report-only | Validates local AI task manifests and telemetry output declarations. |
| `python -m Tools.ai build_refactor_duplication_audit` | `build_refactor_duplication_audit` | `BROKER_TOOL;PATCH_PLAN_SUPPORT` | stable | yes | refactor evidence | no | no | `output/ai_pipeline/*duplication_audit*.json` | compact evidence only | `python -m py_compile .\Tools\ai\refactor_duplication_audit\cli.py` | report-only | Feed patch plans, do not apply them. |

## Full-run and evidence tools

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/ai/build_runtime_tool_usage_telemetry.py` | `build_runtime_tool_usage_telemetry` | `FULL_RUN_EVIDENCE` | stable | candidate if report-only | runtime tool telemetry | no | no | `output/validation/runtime_tool_usage_telemetry_*.json` | `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_*.json/.md` | `python -m py_compile .\Tools\ai\build_runtime_tool_usage_telemetry.py` | preserve broker reports; no output commit | Required for broker evidence completeness. |
| `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | `build_shared_toolbox_ai_to_ai_bundle` | `FULL_RUN_EVIDENCE;PATCH_PLAN_SUPPORT` | stable | candidate if report-only | AI-to-AI production bundle | no | no | `output/analysis/shared_toolbox_ai_to_ai_final_summary_*.json` | `docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_*.json/.md` | `python -m py_compile .\Tools\ai\build_shared_toolbox_ai_to_ai_bundle.py` | compact only; no raw output dump | Must expose provider advisory degradation. |
| `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | `build_full_toolbox_run_telemetry_summary` | `FULL_RUN_EVIDENCE` | stable | candidate if report-only | run telemetry summary | no | no | `output/analysis` or requested output | `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_*.json/.md` | `python -m py_compile .\Tools\ai\build_full_toolbox_run_telemetry_summary.py` | report-only | Reads GPU/NPU sync report; does not compute timings itself. |
| `Tools/ai/analyze_gpu_npu_run_sync.py` | `analyze_gpu_npu_run_sync` | `PROVIDER_DIAGNOSTIC;FULL_RUN_EVIDENCE` | stable | candidate if report-only | GPU/NPU sync diagnostics | no | no | `output/validation/*gpu_npu*sync*.json/.md` | compact evidence only | `python -m py_compile .\Tools\ai\analyze_gpu_npu_run_sync.py` | must prefer `rounds[*].elapsed_seconds` | Primary source for GPU round timing metrics. |
| `Tools/ai/build_github_evidence_bundle.py` | `build_github_evidence_bundle` | `FULL_RUN_EVIDENCE;DOCS_MAINTENANCE` | stable | no by default | evidence bundle builder | no | writes evidence docs | `docs/LOCAL_VALIDATION_EVIDENCE/*` | compact bundle JSON/MD | `python -m py_compile .\Tools\ai\build_github_evidence_bundle.py` | never copy raw heavy output | Manual/evidence stage only. |
| `Tools/validation/check_github_evidence_bundle.py` | `check_github_evidence_bundle` | `FULL_RUN_EVIDENCE;VALIDATION` | stable | yes if report-only | evidence validation | no | no | `output/validation/*bundle*_validation.json` | compact validation evidence | `python -m Tools.validation check_github_evidence_bundle --repo-root . --bundle <bundle.json> --output .\output\validation\bundle_validation.json` | report-only | Required before versioning bundles. |

## Provider diagnostics

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/ai/run_local_provider_probe.py` | `run_local_provider_probe` | `PROVIDER_DIAGNOSTIC` | stable | no by default | provider probe | yes when requested | no | `output/validation/local_provider_probe.json/.md` | compact evidence only | `python -m py_compile .\Tools\ai\run_local_provider_probe.py` | explicit provider diagnostics only | Safe diagnostic, but not default broker. |
| `Tools/ai/check_local_resource_lanes.py` | `check_local_resource_lanes` | `PROVIDER_DIAGNOSTIC;PROJECT_TOOL` | stable | no by default | resource-lane precheck | optional probe | no | `output/validation/local_ai_resource_lanes*.json/.md` | compact evidence only | `python -m Tools.ai check_local_resource_lanes --repo-root . --parallel --output .\output\validation\local_ai_resource_lanes.json` | probe flags explicit | Good local preflight tool. |
| `Tools/ai/check_npu_provider_environment.py` | `check_npu_provider_environment` | `PROVIDER_DIAGNOSTIC;PROJECT_TOOL` | stable | no | NPU environment precheck | may inspect provider environment | no | `output/validation/npu_provider_environment.json/.md` | compact evidence only | `python -m Tools.ai check_npu_provider_environment --repo-root . --output .\output\validation\npu_provider_environment.json` | no NPU promotion | Keep diagnostic only. |
| `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` | `run_agent_gpu_npu_parallel_orchestrator` | `PROJECT_TOOL;PROVIDER_DIAGNOSTIC` | stable | no | full GPU/NPU orchestrator | yes explicit | no | `output/ai_pipeline/*orchestrator*.json/.md` | compact evidence only | `python -m py_compile .\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py` | no patch apply; no Blender | Manual/full-run entry, not broker. |
| `Tools/ai/run_agent_gpu_deep_planning_supervised.py` | `run_agent_gpu_deep_planning_supervised` | `PROJECT_TOOL;PROVIDER_DIAGNOSTIC;PATCH_PLAN_SUPPORT` | stable | no | GPU planner lane | yes explicit | no | `output/ai_pipeline/*parallel_gpu*.json/.md` | compact evidence only | `python -m py_compile .\Tools\ai\run_agent_gpu_deep_planning_supervised.py` | provider errors must serialize valid JSON | GPU/Ollama advisory lane. |
| `Tools/validation/check_ai_workload_report_quality.py` | `check_ai_workload_report_quality` | `PROVIDER_DIAGNOSTIC;VALIDATION` | stable | candidate if report-only | workload-quality gate | no | no | `output/validation/*workload_quality*.json` | compact evidence only | `python -m py_compile .\Tools\validation\check_ai_workload_report_quality.py` | report-only | Quality gate for provider outputs. |
| `Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py` | `run_orchestrator_gpu_runtime_tool_routing_smoke` | `PROVIDER_DIAGNOSTIC;BROKER_TOOL` | smoke | candidate | broker/provider routing smoke | no real provider by default | no | `output/validation/*routing_smoke*.json` | compact evidence only | `python -m py_compile .\Tools\validation\run_orchestrator_gpu_runtime_tool_routing_smoke.py` | smoke only | Keep as broker telemetry follow-up. |
| `Tools/validation/run_npu_runtime_tool_execution_smoke.py` | `run_npu_runtime_tool_execution_smoke` | `PROVIDER_DIAGNOSTIC;BROKER_TOOL` | smoke | candidate | NPU runtime smoke | no real provider by default | no | `output/validation/*npu_runtime_tool_execution*.json` | compact evidence only | `python -m py_compile .\Tools\validation\run_npu_runtime_tool_execution_smoke.py` | smoke only | Keep report-only. |

## Patch-plan support

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/ai/build_deterministic_recommendations.py` | `build_deterministic_recommendations` | `PATCH_PLAN_SUPPORT;FULL_RUN_EVIDENCE` | stable | no by default | deterministic recommendations | no | no | `output/patch_specs` or requested report | compact evidence only | `python -m py_compile .\Tools\ai\build_deterministic_recommendations.py` | forbidden target prefixes enforced | Keep anti-evidence target hygiene. |
| `Tools/ai/build_agent_review_patch_plan.py` | `build_agent_review_patch_plan` | `PATCH_PLAN_SUPPORT` | stable | no by default | patch-plan generation | no | no | `output/patch_specs/agent_review_patch_plan.json/.md` | compact evidence only | `python -m py_compile .\Tools\ai\build_agent_review_patch_plan.py` | review-only; no apply | Canonical patch-plan builder. |
| `Tools/ai/build_patch_notes_quality_product.py` | `build_patch_notes_quality_product` | `PATCH_PLAN_SUPPORT;FULL_RUN_EVIDENCE` | active product builder | no by default | patch notes quality product | no | no | `docs/LOCAL_VALIDATION_EVIDENCE/patch_notes_quality_product_*.json/.md`; operational FTS under `output/**` | compact evidence JSON/MD | `python -m Tools.validation run_patch_notes_quality_product_smoke --repo-root .` | report-only; manual review required; no provider call by builder | Reuses patch-plan quality IO/FTS/scoring surfaces and consumes runtime telemetry/capability evidence. |
| `Tools/ai/build_agent_review_code_patch_plan.py` | `build_agent_review_code_patch_plan` | `PATCH_PLAN_SUPPORT` | stable | no | code patch-plan lane | no | no | `output/patch_specs/*code_patch_plan*.json/.md` | compact evidence only | `python -m py_compile .\Tools\ai\build_agent_review_code_patch_plan.py` | no automatic apply | Manual review required. |
| `Tools/ai/build_code_edit_proposal_from_plan.py` | `build_code_edit_proposal_from_plan` | `PATCH_PLAN_SUPPORT` | stable | no | code edit proposal | no | no | `output/patch_specs/*code_edit_proposal*.json` | compact evidence only | `python -m py_compile .\Tools\ai\build_code_edit_proposal_from_plan.py` | proposal-only | Never apply directly. |
| `Tools/ai/build_code_patch_artifact_pack.py` | `build_code_patch_artifact_pack` | `PATCH_PLAN_SUPPORT;FULL_RUN_EVIDENCE` | stable | no | artifact pack | no | writes artifact pack | output artifact pack | compact evidence only | `python -m py_compile .\Tools\ai\build_code_patch_artifact_pack.py` | no source writes unless explicit | Keep packs out of Git unless policy allows. |
| `Tools/validation/run_agent_review_patch_plan_smoke.py` | `run_agent_review_patch_plan_smoke` | `PATCH_PLAN_SUPPORT;VALIDATION` | stable smoke | yes if report-only | patch-plan smoke | no | no | `output/validation/agent_review_patch_plan_smoke*.json/.md` | compact evidence only | `python -m Tools.validation run_agent_review_patch_plan_smoke --repo-root . --orchestrator <report> --evidence <evidence> --output .\output\validation\agent_review_patch_plan_smoke.json` | smoke only | Validates fallback/plan contract. |
| `Tools/validation/run_agent_review_patch_plan_full_validation.py` | `run_agent_review_patch_plan_full_validation` | `PATCH_PLAN_SUPPORT;VALIDATION` | stable | no by default | full patch-plan validation | no | no | `output/validation/*patch_plan_full_validation*.json` | compact evidence only | `python -m py_compile .\Tools\validation\run_agent_review_patch_plan_full_validation.py` | no apply | Manual validation stage. |

## Documentation maintenance

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/validation/build_markdown_inventory.py` | `build_markdown_inventory` | `DOCS_MAINTENANCE;FULL_RUN_EVIDENCE` | stable | yes if report-only | markdown inventory | no | no | `output/validation/*markdown_inventory*.json/.md` | compact evidence only | `python -m py_compile .\Tools\validation\build_markdown_inventory.py` | report-only | Canonical MD inventory. |
| `Tools/validation/check_docs_links.py` | `check_docs_links` | `DOCS_MAINTENANCE;VALIDATION` | stable | yes if report-only | docs link validation | no | no | `output/validation/*docs_links*.json` | compact evidence only | `python -m py_compile .\Tools\validation\check_docs_links.py` | no network unless explicit | Keep local/static by default. |
| `Tools/validation/build_script_inventory.py` | `build_script_inventory` | `FULL_RUN_EVIDENCE;DOCS_MAINTENANCE` | stable | yes if report-only | script inventory | no | no | `output/validation/*script_inventory*.json` | compact evidence only | `python -m py_compile .\Tools\validation\build_script_inventory.py` | report-only | Helps discover candidate tools. |
| `python -m Tools.docs build_code_aware_md_coherence` | `build_code_aware_md_coherence` | `DOCS_MAINTENANCE;FULL_RUN_EVIDENCE` | very good tool; stable report builder | yes if report-only | MD/code coherence report | no | no | `output/validation/md_code_coherence_report*.json/.md` | compact evidence only | `python -m py_compile .\Tools\docs\_shared\code_aware_md_coherence_core.py -m Tools.docs code_aware_md_coherence_cli` | report-only; classify historical/template refs before pruning | Very good tool: proved useful for reducing MD/code false positives and guiding safe pruning. |
| `Tools/docs/apply_md_code_coherence_refactor.py` | `apply_md_code_coherence_refactor` | `DOCS_MAINTENANCE` | very good tool; stable generated-doc refresher | no by default | generated MD summaries | no | writes selected docs | `docs/LOCAL_AI_TASKS/code-aware-*.md`; `docs/LOCAL_AI_TASKS/md-code-coherence-current-state.md` | generated docs only | `python -m py_compile .\Tools\docs\apply_md_code_coherence_refactor.py` | path-explicit commits only; no output/** commit | Very good tool: regenerates compact code-aware docs from validated report state. |
| `Tools/validation/check_md_code_coherence.py` | `check_md_code_coherence` | `DOCS_MAINTENANCE;VALIDATION` | very good tool; stable threshold gate | yes if report-only | MD/code coherence validation | no | no | `output/validation/md_code_coherence_check*.json` | compact evidence only | `python -m py_compile .\Tools\validation\check_md_code_coherence.py` | threshold-based; do not treat historical refs as active blockers | Very good tool: useful as controlled gate after mapper/report improvements. |
| `python -m Tools.docs split_large_markdown` | `split_large_markdown` | `DOCS_MAINTENANCE` | very good tool; controlled line-budget splitter | no by default | Markdown line-budget maintenance | no | writes selected Markdown stubs/parts when --apply | source docs and split manifests | generated split docs only | `python -m py_compile .\Tools\docs\_shared\large_markdown_splitter_core.py -m Tools.docs split_large_markdown_cli` | exact scopes only; no blind broad split; no evidence/output commit | Very good tool: safe for keeping large Markdown navigable with stub + part layout. |

## Workflow tools

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | `run_unified_local_ai_refactor` | `PROJECT_TOOL;LOCAL_UI_OR_MANUAL` | stable active entrypoint | no | unified local run launcher | explicit by flags | no by default | `output/**` phase reports | compact evidence only | PowerShell parser validation | no commit/push/merge; no Blender | Canonical operator entrypoint. |
| `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | `run_local_ai_task_via_pipeline` | `PROJECT_TOOL;FULL_RUN_EVIDENCE;PATCH_PLAN_SUPPORT` | stable adapter | no | official Markdown task adapter | explicit by flags | no | `output/local_ai_runs/**`; compact evidence when selected | compact evidence only | PowerShell parser validation | no patch apply; no Blender/FFmpeg; no output commit | Builds packet/proposals/patch-specs/telemetry/evidence for Markdown tasks. |
| `Tools/workflow/run_local_ai_task_via_pipeline/*.ps1` | `local_ai_task_via_pipeline_modules` | `SUPPORT_LIBRARY;FULL_RUN_EVIDENCE` | stable internal modules | no | official adapter internals | inherited from adapter flags | no | caller-defined | none directly | PowerShell parser validation | helper-only; no standalone promotion | Reuse before adding another adapter/helper. |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1` | `run_agent_review_full_toolbox_decision_loop` | `PROJECT_TOOL;FULL_RUN_EVIDENCE;LOCAL_UI_OR_MANUAL` | stable wrapper | no | full toolbox decision loop | explicit by flags | no | `output/**` decision/evidence reports | compact evidence only | PowerShell parser + Python compile/static smoke | no patch apply | Public PS shell wrapper; Python engine is the only implementation path. |
| `python -m Tools.workflow run_agent_review_full_toolbox_decision_loop` | `run_agent_review_full_toolbox_decision_loop_python_entrypoint` | `PROJECT_TOOL;FULL_RUN_EVIDENCE` | stable Python entrypoint | no | full toolbox decision loop | explicit by forwarded flags | no | inherited from Python engine package | compact evidence only | `python -m py_compile` | no patch apply | Preserves public CLI and runs the packaged Python engine as the single implementation. |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_*.py` | `run_agent_review_full_toolbox_decision_loop_python_package` | `SUPPORT_LIBRARY;FULL_RUN_EVIDENCE` | active package | no | full toolbox decision loop internals | inherited from entrypoint flags | no | caller-defined reports, telemetry, final product, path policy | compact evidence only | `python -m py_compile` | no patch apply | Responsibility split for static foundation, provider mesh, final product/bundle/telemetry and shared helpers. |
| `python -m Tools.workflow startup_check` | `startup_check` | `PROJECT_TOOL;PROVIDER_DIAGNOSTIC` | stable | candidate if report-only | startup diagnostics | optional checks | no | `output/validation/*startup_check*.json` | compact evidence only | `python -m py_compile .\Tools\workflow\startup_check_core\cli.py -m Tools.workflow report` | no source writes | Promote as core startup diagnostic. |
| `Tools/workflow/startup_preflight.ps1` | `startup_preflight` | `PROJECT_TOOL;LOCAL_UI_OR_MANUAL` | stable wrapper | no | startup wrapper | explicit by called checks | no | `output/validation/**` | compact evidence only | PowerShell parser validation | wrapper only | Document after `python -m Tools.workflow startup_check`. |
| `Tools/workflow/ai_runtime_diagnostics.py` | `ai_runtime_diagnostics` | `PROVIDER_DIAGNOSTIC;PROJECT_TOOL` | candidate | no | runtime diagnostics | optional | no | `output/validation/**` | compact evidence only | `python -m py_compile .\Tools\workflow\ai_runtime_diagnostics.py` | diagnostic only | Good preflight candidate. |
| `python -m Tools.workflow workflow_shell` | `workflow_shell` | `LOCAL_UI_OR_MANUAL` | manual | no | none | operator-driven | possible via commands | operator-defined | none | manual smoke only | interactive shell | Never broker. |
| `python -m Tools.workflow workflow_shell_with_push` | `workflow_shell_with_push` | `LOCAL_UI_OR_MANUAL;GIT_WRITE_TOOL` | manual unsafe | no | none | operator-driven | possible | operator-defined | Git commits/pushes | manual only | Git writes | Never broker or unattended. |
| `Tools/workflow/git_auto_push.py` | `git_auto_push` | `GIT_WRITE_TOOL` | manual unsafe | no | none | no | Git writes | Git state | commits/pushes | manual only | explicit operator command | Never include in automated full-run. |

## NPU tools

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/npu/run_npu_review.py` | `run_npu_review` | `PROVIDER_DIAGNOSTIC;PROJECT_TOOL` | candidate | no | NPU review lane | yes explicit | no | `output/**` NPU reports | compact evidence only | `python -m py_compile .\Tools\npu\run_npu_review.py` | NPU advisory only | Do not promote to primary advisor. |
| `Tools/npu/pipeline/*.py` | `npu_pipeline_modules` | `SUPPORT_LIBRARY;PROVIDER_DIAGNOSTIC` | internal library | no | NPU pipeline support | called by wrappers | no | caller-defined | none directly | `python -m py_compile <module>` | support library | Document API before promotion. |

## Blender/audio application tools

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/workflow/audio_analysis/analyze_cli.py` | `audio_analysis` | `BLENDER_AUDIO_PIPELINE;PROJECT_TOOL` | stable | no | audio analysis workflow | no | writes analysis output | `output/*analysis*.json` | none by default | `python -m py_compile .\Tools\workflow\audio_analysis\analyze_cli.py` | no broker; no runtime artifacts committed | Canonical workflow audio analyzer. |
| `Tools/workflow/audio_analysis/summary_cli.py` | `audio_summary` | `BLENDER_AUDIO_PIPELINE;PROJECT_TOOL` | stable | no | audio summary workflow | no | writes summary output | `output/*summary*.json/.md` | none by default | `python -m py_compile .\Tools\workflow\audio_analysis\summary_cli.py` | no broker; no runtime artifacts committed | Canonical workflow audio summary builder. |
| `Scripting/v61b/main_v61b.py` | `main_v61b` | `BLENDER_AUDIO_PIPELINE;PROJECT_TOOL` | stable runtime | no | Blender scene generation | no provider | Blender scene/render side effects | renders/output/manual | none by default | `python -m py_compile .\Scripting\v61b\main_v61b.py` | do not run Blender implicitly | Manual runtime only. |
| `Scripting/v61b/encode_image_sequence_v61b.py` | `encode_image_sequence_v61b` | `BLENDER_AUDIO_PIPELINE;PROJECT_TOOL` | stable runtime | no | encode workflow | no | FFmpeg side effects | rendered video | none by default | `python -m py_compile .\Scripting\v61b\encode_image_sequence_v61b.py` | do not run FFmpeg implicitly | Manual runtime only. |
| `Scripting/v61b/encode_ffmpeg_v61b.py` | `encode_ffmpeg_v61b` | `BLENDER_AUDIO_PIPELINE;PROJECT_TOOL` | stable runtime | no | encode workflow | no | FFmpeg side effects | rendered video | none by default | `python -m py_compile .\Scripting\v61b\encode_ffmpeg_v61b.py` | do not run FFmpeg implicitly | Manual runtime only. |
| `Scripting/v61b/hot_update_scene_v61b.py` | `hot_update_scene_v61b` | `BLENDER_AUDIO_PIPELINE;GENERATED_OR_CANDIDATE` | candidate | no | manual Blender utility | no | Blender scene side effects | manual | none | `python -m py_compile .\Scripting\v61b\hot_update_scene_v61b.py` | manual only | Needs explicit promotion doc. |
| `Scripting/v61b/scene_tuning_panel.py` | `scene_tuning_panel` | `LOCAL_UI_OR_MANUAL;BLENDER_AUDIO_PIPELINE` | candidate UI | no | manual UI | no | Blender UI/runtime | manual | none | `python -m py_compile .\Scripting\v61b\scene_tuning_panel.py` | UI/manual only | Never broker. |

## Support libraries

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/ai/pipeline/*.py` | `ai_pipeline_modules` | `SUPPORT_LIBRARY` | internal | no | imported by AI tools | caller-dependent | caller-dependent | caller-defined | none directly | `python -m py_compile <module>` | no standalone promotion without CLI | Keep as implementation modules. |
| `Tools/ai/code_interpreter_report/*.py` | `code_interpreter_report_modules` | `SUPPORT_LIBRARY;FULL_RUN_EVIDENCE` | internal | no | static code report internals | no | no | caller-defined | none directly | `python -m py_compile .\Tools\ai\code_interpreter_report\*.py` | helper-only | Implementation split for `build_code_interpreter_report.py`. |
| `Tools/ai/repository_consistency_map/*.py` | `repository_consistency_map_modules` | `SUPPORT_LIBRARY;FULL_RUN_EVIDENCE` | internal | no | repository consistency internals | no | no | caller-defined | none directly | `python -m py_compile .\Tools\ai\repository_consistency_map\*.py` | helper-only | Implementation split for `build_repository_consistency_map.py`. |
| `Tools/ai/_shared/workload_quality.py` | `workload_quality` | `SUPPORT_LIBRARY;PROVIDER_DIAGNOSTIC` | internal | no | workload quality support | no | no | caller-defined | none directly | `python -m py_compile .\Tools\ai\_shared\workload_quality.py` | support-only | Used by quality routing. |
| `Tools/ai/schema_repair/` | `schema_repair_context` | `SUPPORT_LIBRARY;PROVIDER_DIAGNOSTIC` | internal | no | schema repair support | no | no | caller-defined | none directly | `python -m py_compile .\Tools\ai\schema_repair/` | do not run repair without raw provider response | Keep provider-error paths safe. |
| `Tools/ai/agent_memory/policy.py` | `agent_memory_policy` | `SUPPORT_LIBRARY;MEMORY_LANE` | internal | no | memory policy | no | no | caller-defined | none directly | `python -m py_compile .\Tools\ai\agent_memory/policy.py` | memory write policy explicit | Support-only. |
| `Tools/validation/_shared/report_utils.py` | `report_utils` | `SUPPORT_LIBRARY;VALIDATION` | internal | no | report writing support | no | caller-dependent | caller-defined | none directly | `python -m py_compile .\Tools\validation\_shared\report_utils.py` | helper only | Shared validation/report helper. |

## Promotion backlog

| path | tool_id | classification | current_status | broker_eligible | full_run_lane | provider_execution | source_writes | runtime_outputs | git_tracked_outputs | validation_command | guardrails | promotion_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Tools/workflow/_shared/project_awareness.py` | `project_awareness` | `FULL_RUN_EVIDENCE;SUPPORT_LIBRARY` | candidate | no | context support | no | no | output context reports | compact evidence only | `python -m py_compile .\Tools\workflow\_shared\project_awareness.py` | report-only | Promote after stable CLI documented. |
| `python -m Tools.workflow smart_ai_context` | `smart_ai_context` | `FULL_RUN_EVIDENCE;SUPPORT_LIBRARY` | candidate | no | context support | no | no | output context reports | compact evidence only | `python -m py_compile .\Tools\workflow\smart_ai_context_core\cli.py` | report-only | Promote after stable CLI documented. |
| `Tools/workflow/_shared/artifact_consult.py` | `artifact_consult` | `FULL_RUN_EVIDENCE;SUPPORT_LIBRARY` | candidate | no | artifact consultation | no | no | output context reports | compact evidence only | `python -m py_compile .\Tools\workflow\_shared\artifact_consult.py` | do not dump raw heavy artifacts | Promote after output limits documented. |
| `Tools/workflow/_shared/asset_inventory.py` | `asset_inventory` | `BLENDER_AUDIO_PIPELINE;FULL_RUN_EVIDENCE` | candidate | no | asset inventory | no | no | asset inventory reports | compact evidence only | `python -m py_compile .\Tools\workflow\_shared\asset_inventory.py` | no renders committed | Candidate for audio/asset docs. |
| `Tools/workflow/_shared/scene_brief.py` | `scene_brief` | `BLENDER_AUDIO_PIPELINE;PATCH_PLAN_SUPPORT` | candidate | no | scene brief | no | no | scene brief reports | compact evidence only | `python -m py_compile .\Tools\workflow\_shared\scene_brief.py` | no Blender runtime | Candidate for scene planning. |
