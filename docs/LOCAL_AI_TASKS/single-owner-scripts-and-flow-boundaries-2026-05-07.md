# Single-owner scripts and flow boundaries — 2026-05-07

Status: active code-driven rule
Scope: scripts that must not be duplicated, bypassed or reimplemented as parallel entrypoints.

## Purpose

This document defines ownership boundaries. If a script owns a responsibility here, new code/docs must reuse or call it instead of duplicating its behavior.

## Hard rule

Do not create parallel scripts, runbooks or ad-hoc commands that bypass these owners unless the task is explicitly a focused diagnostic or a planned replacement.

When replacing an owner, update this document, the launcher runbook, package README and validation flow map in the same PR.

## Primary single owners

| Responsibility | Owner | Do not duplicate with |
|---|---|---|
| Operator launcher | `Tools/workflow/run_unified_local_ai_refactor.ps1` | New full-run, docs-run, provider-run or reset entrypoints. |
| Full-toolbox engine wrapper | `python -m Tools.workflow run_agent_review_full_toolbox_decision_loop` | New orchestration wrappers that skip the packaged engine. |
| Full-toolbox static foundation | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_engine.py` | Independent static-foundation runners. |
| Provider mesh and peer exchange orchestration | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py` | Standalone GPU1/GPU0/NPU production flows outside launcher. |
| Product/bundle/evidence finalization | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_product.py` | One-off final bundle or evidence runners for normal flows. |
| Workflow execution helpers | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py` | Repeated path/command/stamp helper logic. |
| Official local AI task adapter lane | `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | Parallel MD-to-packet adapter scripts. |
| Post-validation AI packet lane | `Tools/workflow/run_post_validation_ai_packet.ps1` | Separate repository_update_suggestions launchers. |
| Multistep provider lane | `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | Ad-hoc provider probe/advisory sequences. |
| Runtime tool broker | `ia_carmine/runtime/runtime_tool/agent_broker.py` | Direct provider tool execution bypassing broker. |
| AI peer exchange packet | `ia_carmine/providers/provider_mesh/peer_exchange_packet/cli.py` | Manual GPU1/GPU0/NPU exchange summaries. |
| GPU0 peer worker | `ia_carmine/providers/provider_mesh/gpu0_peer_companion_worker.py` | One-off GPU0 support scripts for production peer exchange. |
| Provider orchestrator | `ia_carmine/providers/provider_mesh/gpu_npu_parallel_orchestrator/cli.py` | New GPU/NPU orchestration loops. |
| GPU planner worker | `ia_carmine/providers/provider_mesh/gpu_deep_planning_supervised/cli.py` | New Ollama primary advisory workers. |
| Runtime tool usage evidence | `ia_carmine/runtime/runtime_tool/usage_evidence/cli.py` | Manual evidence counters. |
| Shared AI-to-AI bundle | `ia_carmine/context/agent_context/shared_toolbox_bundle/cli.py` | Parallel handoff bundle builders. |
| GitHub evidence bundle | `ia_carmine/product/repository_product/github_evidence_bundle.py` | Handwritten compact evidence aggregators. |
| Task patch suggestion report | `ia_carmine/product/patch_product/task_patch_suggestion_report.py` | Direct ad-hoc extraction from task MD. |
| Patch suggestion dry/apply | `ia_carmine/product/patch_product/patch_suggestion_bundle/cli.py` and `ia_carmine/product/patch_product/patch_suggestion_bundle/cli.py` | Direct source writes from suggestion JSON. |
| Review PR preparation | `ia_carmine/product/agent_review/review_pr_cli.py` | Ad-hoc staging/commit/push/PR scripts. |
| Product separation validation | `Tools/validation/patch_product/product_separation/cli.py` | Manual product-vs-evidence classification. |
| Python syntax validation | `python -m Tools.validation check_python_syntax` | Custom py_compile loops for product reports. |
| Report contract validation | `python -m Tools.validation check_validation_report_contract` | One-off JSON contract scans. |
| Markdown inventory | `Tools/validation/docs_hygiene/markdown_inventory/cli.py` | New Markdown scanners. |
| Script inventory | `Tools/validation/build_script_inventory.py` | New function/class/method inventory generators. |
| Docs link validation | `Tools/validation/check_docs_links.py` | New link checker wrappers. |
| Line limit report | `python -m Tools.validation check_file_line_limits` | New line-count enforcement scripts. |
| Semantic chunks | `Tools/npu/provider_mesh/semantic_code_chunks.py` | New generated code-chunk builders. |
| AI context pack | `ia_carmine/context/agent_context/ai_context_pack/cli.py` | New context-pack builders. |
| Agent state packet | `ia_carmine/context/agent_context/state_packet/cli.py` | New memory/state packet builders. |

## Allowed direct calls

Direct calls are allowed for focused smoke, unit-style validation, diagnostics, or local forensic inspection.

Direct calls are not allowed as replacement production workflows when the unified launcher already owns the flow.

## Flow boundary rules

```text
Provider tool requests must pass through agent_runtime_tool_broker.py.
Patch suggestions must pass through apply_patch_suggestion_bundle.py before source edits.
Review PR staging must pass through agent_review_prepare_pr.py.
Full-run operator commands must start at run_unified_local_ai_refactor.ps1.
Bundle/handoff artifacts must pass through the existing bundle builders.
Generated chunks, indexes, output reports and SQLite DB files are not source authority.
```

## Review checklist

Before adding a new script:

```text
1. Search this document for the target responsibility.
2. Search Tools/workflow, ia_carmine, Tools/validation and Tools/npu for an existing owner.
3. Reuse owner CLI/API when possible.
4. If a new script is still needed, define whether it is diagnostic-only, supporting, or new owner.
5. Update this document and the script census map.
```

## Non-owner helper status

A helper can exist without becoming an owner. Helper docs must say which owner calls it or which focused diagnostic it supports.
