# Module Map

## Purpose

Compact repository area map for `IA-Carmine Local AI Orchestration Workbench`.

Use this file to locate areas. Use the code-driven maps for behavior, ownership and validation flow.

## Required current maps

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Do not use this module map as proof of active behavior when source code or the owner maps say otherwise.

## Repository areas

| Area | Role | Operational status |
|---|---|---|
| `Tools/workflow/` | Local workflow launchers and helper shells. | Unified launcher is canonical. Other scripts are supporting/diagnostic unless owner maps say otherwise. |
| `Tools/ai/` | AI orchestration, provider diagnostics, context, memory, telemetry, evidence, heap/exchange, patchkit, patch suggestion and handoff tools. | Use owner map before adding or calling scripts directly. |
| `Tools/ai/patchkit/` | Reusable controlled patch bundle application infrastructure. | Preferred deterministic source-write boundary for reviewed bundles. |
| `Tools/validation/` | Non-invasive validators, smokes and report-contract checks. | Use validator cycle map to choose checks. |
| `Tools/npu/` | NPU/OpenVINO/Ollama support, context builders and runtime helpers. | Provider/runtime work must stay evidence-bound and launcher-integrated. |
| `Tools/npu/pipeline/` | App-agnostic NPU helper package. | Helper contracts and planned/runtime-free modules unless explicitly wired by code. |
| `Tools/repo_patch_runner/` | Legacy structured patch runner tooling. | Explicit/manual-review before apply; patchkit is preferred for reusable bundles. |
| `docs/` | Stable documentation contracts and project state. | Prefer compact code-driven maps over historical runbooks. |
| `docs/LOCAL_AI_TASKS/` | Active task runbooks, maps and historical handoffs. | Current maps define active behavior; historical files are context only. |
| `docs/LOCAL_VALIDATION_EVIDENCE/` | Compact Git-trackable evidence snapshots. | Review artifacts, not source docs. |
| `indexAI/` | Generated AI-oriented indexes/context/patch material. | Generated context; do not hand-refactor as source. |
| `patch_specs/` | Patch specification artifacts and patchkit bundle specs/fragments when selected. | Review-only unless explicit apply path is authorized. |
| `Scripting/` | Blender/audio application-domain packages. | Not part of normal AI/tooling run unless scoped. |
| `Scripting/v61b/` | Current reference Blender workflow. | Application-domain quality reference; avoid destructive broad refactors. |
| `Scripting/shared/` | Shared Blender/application utilities. | Use only for scoped application-domain refactor. |
| `examples/` | Examples and small fixtures. | Keep reproducible and compact. |
| root scripts | Historical/application helpers such as audio analysis and scene spec normalization. | Inspect before editing; not local-AI entrypoints. |

## Canonical active owners

| Responsibility | Owner |
|---|---|
| Operator launcher | `Tools/workflow/run_unified_local_ai_refactor.ps1` |
| Full-toolbox engine | `Tools/workflow/run_agent_review_full_toolbox_decision_loop.py` and packaged modules. |
| Provider mesh | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py` |
| Runtime broker | `Tools/ai/agent_runtime_tool_broker.py` |
| Heap/exchange runtime entry | `Tools/ai/build_heap_exchange_runtime_entry.py` |
| Heap/exchange runtime exit product | `Tools/ai/build_heap_exchange_runtime_exit.py` |
| Heap/exchange lifecycle validation | `Tools/validation/check_heap_exchange_runtime_lifecycle.py` and `Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py` |
| Patchkit bundle application | `Tools/ai/patchkit/apply_patch_bundle.py` |
| Patchkit smoke | `Tools/validation/run_patchkit_smoke.py` |
| AI-to-AI bundle | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` |
| Task Markdown patch suggestion authoring | `Tools/ai/create_task_patch_suggestion_markdown.py` |
| Task Markdown patch suggestion report | `Tools/ai/build_task_patch_suggestion_report.py` |
| Patch suggestion dry/apply | `Tools/ai/apply_patch_suggestion_bundle.py` and `Tools/ai/patch_suggestion_bundle/cli.py` |
| Generated patch specs review bridge | `Tools/ai/apply_generated_patch_specs_for_review_pr.py` |
| Patch suggestion product separation | `Tools/validation/check_patch_suggestion_product_separation.py` |
| Product PR chain smoke | `Tools/validation/run_full0to10_product_pr_chain_smoke.py` |
| Review PR preparation | `Tools/ai/prepare_review_pr.py` |
| Validator/smoke selection | `docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md` |

Full table:

```text
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
```

## Current Markdown-to-review-PR product path

```text
docs/LOCAL_AI_TASKS/<task>.md
  -> unified launcher
  -> context pack / agent state / workload evidence
  -> build_heap_exchange_runtime_entry.py
  -> dynamic heap/exchange provider/tool/broker/validator center
  -> patch suggestion bridge or generated patch specs bridge
  -> build_heap_exchange_runtime_exit.py
  -> check_heap_exchange_runtime_lifecycle.py
  -> patchkit or deterministic patch suggestion application
  -> prepare_review_pr.py
  -> GitHub PR for manual review
```

Code-driven facts:

```text
ReviewPrIncludePath remains supported for explicit/manual allowlists.
prepare_review_pr.py can auto-discover include paths from apply reports with `--auto-include-from-apply-report` plus `--apply-report`.
prepare_review_pr.py supports `--draft-pr` only when explicitly paired with `--create-pr`.
metadata-only patch drafts are not enough for product success.
```

## Obsolete / monolithic flag

Treat a script or document as historical/superseded when it duplicates a current owner or preserves an older monolithic flow.

Typical flags:

```text
starts a normal full workflow outside run_unified_local_ai_refactor.ps1
runs provider tool requests outside agent_runtime_tool_broker.py
stages/commits/opens PRs outside prepare_review_pr.py
applies suggestions outside apply_patch_suggestion_bundle.py or patchkit
contains copied launcher commands instead of linking the runbook
uses extensionless Markdown split folders
exceeds file-size policy without a compact index
claims automatic path discovery or draft PR creation not present in code
claims product success without heap/exchange exit and lifecycle evidence when that lane is selected
```

Mark obsolete first. Delete/prune only under an explicit documentation-pruning task.

## Run-unica doctrine

```text
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = intensity, not scope
-No* flags = explicit opt-out only
NoStrictRealRunActivation = diagnostics only, not full product mode
```

Promoted lanes must expose manifest, phase report, telemetry, capability, evidence or bundle visibility.

## Application-domain boundary

Blender/audio runtime is an application domain over the local AI workbench.

Normal local-AI/tooling/doc/provider flows must not run:

```text
Blender render
FFmpeg encode/mux
audio playback/export
media generation
```

unless explicitly scoped as application-domain runtime work.

## Generated output policy

Never commit by default:

```text
output/**
*.db
*.sqlite
*.sqlite3
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```

Commit compact evidence only when useful and intentionally selected:

```text
docs/LOCAL_VALIDATION_EVIDENCE/**
```

## Editing guidance

Before adding or changing code/docs:

```text
1. read the target file
2. inspect existing owner/helper
3. prefer reuse
4. make smallest safe change
5. run focused validation when available
6. report validation gaps
```

A full function-level module index is not manually maintained here. Generate it from script inventory, line-count CSV and function/class/method inventory when needed.
