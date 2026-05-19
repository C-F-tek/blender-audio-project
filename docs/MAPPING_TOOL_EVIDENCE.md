# Mapping tool evidence

## Purpose

This is the surface entrypoint for repository mapping runs and compact evidence publication.

Use it when the repository changes enough that area-level `TOOL_CONTEXT.md` files are not sufficient, or when an AI agent must discover every script/tool family from current source instead of chat memory.

## Canonical procedure

Detailed task/procedure:

```text
docs/LOCAL_AI_TASKS/mapping-tool-evidence-publishing-2026-05-19.md
```

Related inventory task:

```text
docs/LOCAL_AI_TASKS/exhaustive-script-surface-inventory-2026-05-19.md
```

## Local raw outputs

Raw mapping outputs stay local under:

```text
output/validation/mapping/
```

Do not commit raw `output/**` by default.

## Git-trackable evidence outputs

Publish only compact evidence summaries under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/mapping_tool_results_<stamp>.md
docs/LOCAL_VALIDATION_EVIDENCE/mapping_tool_results_<stamp>.json
```

## Mapping tools

Recommended mapping pass:

```powershell
python -m Tools.validation build_script_inventory
python -m Tools.docs tool_root_inventory
python -m Tools.docs repo_tool_surface_audit
python -m Tools.docs tool_package_family_audit
python -m Tools.docs module_duplication_audit
python -m Tools.validation build_markdown_inventory
python -m Tools.validation check_package_structure
python -m Tools.validation check_python_syntax
```

## Current inventory baseline

Latest operator-provided local inventory:

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

## Follow-up

After each mapping pass:

1. keep raw outputs under `output/validation/mapping/`;
2. create compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`;
3. commit only compact evidence and documentation updates;
4. return to updating `TOOL_CONTEXT.md` files from the discovered gaps.

## Guardrails

This mapping pass is documentation/evidence only. Do not run Blender, FFmpeg, providers, patch apply, deploy, force-push, merge or cleanup as part of mapping.
