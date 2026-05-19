# Dispatcher context coverage

This document records the dispatcher-driven context pass.

## Purpose

The repository has many tools. Context documentation is therefore tracked by dispatcher and macro-family, not by pretending that every script has an individual hand-written page.

## Dispatchers inspected

| Dispatcher | Public command surface | Coverage status |
| --- | --- | --- |
| `Tools/ai/dispatch.py` | `python -m Tools.ai <tool>` | macro-families indexed |
| `Tools/validation/dispatch.py` | `python -m Tools.validation <tool>` | macro-families indexed |
| `Tools/workflow/dispatch.py` | `python -m Tools.workflow <tool>` | macro-families indexed |
| `Tools/npu/dispatch.py` | `python -m Tools.npu <tool>` | macro-families indexed |
| `Tools/docs/dispatch.py` | `python -m Tools.docs <tool>` | partially indexed |
| `Tools/git/dispatch.py` | `python -m Tools.git <tool>` | indexed |
| `Tools/repo_patch_runner/dispatch.py` | `python -m Tools.repo_patch_runner <tool>` | indexed |

## Navigation chain

```text
CONTEXT_INDEX.md
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

## Known non-complete items

| Family | Status | Reason |
| --- | --- | --- |
| `Tools/ai/repository_product/TOOL_CONTEXT.md` | stub | detailed remote edit was blocked; file exists as discoverability stub |
| `Tools/docs/_shared/TOOL_CONTEXT.md` | stub-missing | remote creation was blocked |
| `Tools/validation/heap_final_proposals/TOOL_CONTEXT.md` | stub-missing | remote creation was blocked |
| `Tools/TOOL_CONTEXT.md` | partial | area indexes now provide finer navigation |
| `Tools/ai/TOOL_CONTEXT.md` | partial | `Tools/ai/CONTEXT_INDEX.md` provides family navigation |
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
4. update this dispatcher coverage document if the family changes the coverage status.

## Guardrails

This document is documentation-only. It does not trigger runtime execution, provider execution, Blender execution, patch apply, merge, deploy or cleanup.
