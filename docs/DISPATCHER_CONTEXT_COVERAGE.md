# Dispatcher context coverage

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `CODE_PRODUCT_FULL_PATCH.md` is the final patch/code product; `PLAN_PRODUCT_FULL_PATCH.md` is the final recomposed GPU1 prompt/chat product, with pointer graph and recovery/congruence as technical attachments.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


This document records the dispatcher-driven context pass.

## Purpose

The repository has many tools. Context documentation is tracked by dispatcher and macro-family, not by pretending that every script has an individual hand-written page.

Dispatcher coverage is a support layer for the anti-ambiguity, lane completeness and IA Universe model-to-code contracts:

```text
docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

Use those contracts first when you need to decide whether a command, smoke, artifact or lane is proof. Use this document to verify dispatcher and family coverage.

## Dispatchers inspected

| Dispatcher | Public command surface | Coverage status |
| --- | --- | --- |
| `ia_carmine/dispatch.py` | `python -m ia_carmine.cli <tool>` | macro-families indexed |
| `Tools/validation/dispatch.py` | `python -m Tools.validation <tool>` | macro-families indexed |
| `Tools/workflow/dispatch.py` | `python -m Tools.workflow <tool>` | macro-families indexed |
| `Tools/npu/dispatch.py` | `python -m Tools.npu <tool>` | macro-families indexed |
| `Tools/docs/dispatch.py` | `python -m Tools.docs <tool>` | partially indexed |
| `Tools/git/dispatch.py` | `python -m Tools.git <tool>` | indexed |
| `Tools/repo_patch_runner/dispatch.py` | `python -m Tools.repo_patch_runner <tool>` | indexed |

## Navigation chain

```text
CONTEXT_INDEX.md
-> docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
-> docs/CORE_LANE_COMPLETENESS_CONTRACT.md
-> docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
-> docs/CONTEXT_COVERAGE_STATUS.md
-> Tools/CONTEXT_INDEX.md
-> Tools/<area>/CONTEXT_INDEX.md
-> Tools/<area>/<family>/TOOL_CONTEXT.md
-> Tools/<area>/dispatch.py
-> source package
```

## Complete-enough coverage

Current strategy marks a family `complete-enough` when it has:

```text
nearest context file
index linkage
coverage status entry
source/dispatcher fallback instruction
```

This is enough for orientation. It is not an exhaustive source audit.

Internal RAG context commands are covered by the `ia_carmine/context/agent_context`
macro-family and validation coverage is under `Tools/validation/agent_context`.

## Known non-complete items

| Family | Status | Reason |
| --- | --- | --- |
| `ia_carmine/product/repository_product/TOOL_CONTEXT.md` | stub | detailed remote edit was blocked; file exists as discoverability stub |
| `Tools/docs/_shared/TOOL_CONTEXT.md` | stub-missing | remote creation was blocked |
| `Tools/validation/heap_final_proposals/TOOL_CONTEXT.md` | stub-missing | remote creation was blocked |
| `Tools/TOOL_CONTEXT.md` | partial | area indexes now provide finer navigation |
| `ia_carmine/TOOL_CONTEXT.md` | partial | `ia_carmine/CONTEXT_INDEX.md` provides family navigation |
| `Tools/validation/TOOL_CONTEXT.md` | partial | `Tools/validation/CONTEXT_INDEX.md` provides family navigation |
| `Tools/workflow/TOOL_CONTEXT.md` | partial | `Tools/workflow/CONTEXT_INDEX.md` provides family navigation |
| `Tools/npu/TOOL_CONTEXT.md` | partial | `Tools/npu/CONTEXT_INDEX.md` provides family navigation |

## Operator decision on mapping

Full mapping is optional and operator-scheduled. It is not required before normal documentation work.

The current known inventory baseline is:

```text
script_count: 1479
syntax_warning_count: 0
ai_tool: 652
validator: 450
workflow_runner: 148
npu_or_provider_tool: 96
blender_application_script: 78
script: 50
git_helper: 5
```

## Update rule

When a dispatcher adds a new public tool family:

1. add or update the nearest `TOOL_CONTEXT.md`;
2. update the area `CONTEXT_INDEX.md`;
3. update `docs/CONTEXT_COVERAGE_STATUS.md`;
4. update `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` if the family changes model-to-code meaning;
5. update this dispatcher coverage document if the family changes coverage status.

## Guardrails

This document is documentation-only. It does not trigger runtime execution, provider execution, Blender execution, patch apply, merge, deploy or cleanup.
