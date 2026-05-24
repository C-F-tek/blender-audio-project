# Tools context index

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `FINAL_PRODUCT` is single: text, code, or text+code. `PLAN_PRODUCT_FULL_PATCH.md` is its text/prose surface; `CODE_PRODUCT_FULL_PATCH.md` is its code/diff surface only when verified code exists. GPU1 emits causal `FINAL_PRODUCT_DELTA` records; blocked status is runtime/gate classification, not GPU1 output.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


## Purpose

This directory contains the operator-facing and AI-facing tool surface for IA-Carmine. The post-refactor convention is to avoid launching scattered legacy files directly and to prefer package dispatchers:

```powershell
python -m Tools.<area> <tool> [tool args...]
```

The shared dispatcher implementation is `Tools/tool_dispatch.py`. Area dispatchers map stable tool names to concrete package CLIs or controlled PowerShell wrappers.

## Areas

| Area | Context file | Canonical command surface | Role |
| --- | --- | --- | --- |
| `ia_carmine` | `ia_carmine/TOOL_CONTEXT.md` | `python -m ia_carmine.cli <tool>` | Heap runtime, provider lanes, context/memory, code product, patch product, AI-to-AI bundle artifacts. |
| `Tools/validation` | `Tools/validation/TOOL_CONTEXT.md` | `python -m Tools.validation <tool>` | Validators, smoke tests, gates, contracts, readiness checks. |
| `Tools/workflow` | `Tools/workflow/TOOL_CONTEXT.md` | `python -m Tools.workflow <tool>` | Operator workflow wrappers, GUI/shell surfaces, startup and orchestration scripts. |
| `Tools/npu` | `Tools/npu/TOOL_CONTEXT.md` | `python -m Tools.npu <tool>` | NPU/provider mesh support, context builders, music/code/manual packets. |
| `Tools/docs` | `Tools/docs/TOOL_CONTEXT.md` | `python -m Tools.docs <tool>` | Documentation hygiene, repo/tool surface audit, Markdown split/coherence helpers. |
| `Tools/git` | `Tools/git/TOOL_CONTEXT.md` | `python -m Tools.git <tool>` | Controlled Git helper wrappers for generated artifacts/data. |
| `Tools/repo_patch_runner` | `Tools/repo_patch_runner/TOOL_CONTEXT.md` | `python -m Tools.repo_patch_runner <tool>` | Controlled repository patch runner utilities. |

## Operational model

The intended flow is not a linear script chain. The tool surface supports a shared runtime universe:

```text
request -> startup context/memory reload -> heap blackboard -> brokered tools
-> provider lanes -> validation/matrix/lab -> code product or blocked diagnosis
```

For new work, prefer reusing an existing area dispatcher and package. Do not create new top-level one-off scripts when a package-owned CLI can be added under an existing area.

## Mapping and evidence entrypoint

When the tool surface changes, or when a context/documentation pass must be driven by current repository facts, use:

```text
docs/MAPPING_TOOL_EVIDENCE.md
docs/LOCAL_AI_TASKS/mapping-tool-evidence-publishing-2026-05-19.md
docs/LOCAL_AI_TASKS/exhaustive-script-surface-inventory-2026-05-19.md
```

Raw mapping outputs stay under `output/validation/mapping/`. Only compact summaries should be promoted to `docs/LOCAL_VALIDATION_EVIDENCE/`.

## Contract sources

Root `CHATGPT.md` is the canonical operating contract for this repository. `CHATGPT/README.md` remains an advisory handoff folder for earlier architecture notes and should not override the root contract.

## Safety defaults

Do not commit runtime artifacts, databases, render outputs, or ignored generated folders:

```text
output/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```

Use generated evidence bundles or session notes only when they are explicitly intended to be Git-trackable documentation.
