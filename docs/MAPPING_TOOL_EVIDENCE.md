# Mapping tool evidence

## Purpose

This is the surface entrypoint for repository mapping runs and compact evidence publication.

Use it when the repository changes enough that area-level `TOOL_CONTEXT.md` files are not sufficient, or when an AI agent must discover every script/tool family from current source instead of chat memory.

## Current decision

The mapping run is optional and operator-scheduled. It is not required before continuing documentation work.

Reason:

```text
full mapping is slow, PowerShell-heavy and only useful when the operator explicitly wants a refreshed evidence snapshot
```

Until the operator chooses to run it, documentation work should continue from:

```text
current source files
current dispatchers
existing TOOL_CONTEXT.md files
operator-provided inventory baseline
GitHub-readable repository files
```

## Canonical procedure

Detailed task/procedure:

```text
docs/LOCAL_AI_TASKS/mapping-tool-evidence-publishing-2026-05-19.md
```

Related inventory task:

```text
docs/LOCAL_AI_TASKS/exhaustive-script-surface-inventory-2026-05-19.md
```

## Operator-only command policy

The mapping launch block is intentionally a long manual operator command. It is not a new maintained repository tool, not a production launcher, and not something to promote into source code only because it is lengthy.

Reason:

```text
mapping commands are local, occasional, environment-sensitive and evidence-oriented
```

They are useful to refresh repository maps, generate compact evidence and then return to documentation work. They are not useful as permanent application/runtime scripts inside the repo.

If this process becomes frequent, create a small maintained wrapper only after the input/output contract stabilizes. Until then, keep the long command in documentation as an operator procedure.

## Execution rule

Run mapping and compact-evidence generation only when explicitly scheduled by the operator. If a partial PowerShell state is missing variables such as `$RepoRoot`, `$Stamp`, `$RawDir`, `$EvidenceDir`, `$RunLog`, `$EvidenceJsonPath` or `$EvidenceMdPath`, stop and restart from a complete script/block later.

Do not block normal documentation updates while waiting for a mapping run.

## Local raw outputs

Raw mapping outputs stay local under:

```text
output/validation/mapping/
```

Do not commit raw `output/**` by default.

## Git-trackable evidence outputs

If the operator runs the mapping pass, publish only compact evidence summaries under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/mapping_tool_results_<stamp>.md
docs/LOCAL_VALIDATION_EVIDENCE/mapping_tool_results_<stamp>.json
docs/LOCAL_VALIDATION_EVIDENCE/mapping_tool_results_latest.md
docs/LOCAL_VALIDATION_EVIDENCE/mapping_tool_results_latest.json
```

## Mapping tools

Recommended mapping pass when explicitly scheduled:

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

After a future mapping pass:

1. keep raw outputs under `output/validation/mapping/`;
2. create compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`;
3. commit only compact evidence and documentation updates;
4. return to updating `TOOL_CONTEXT.md` files from the discovered gaps.

Without a fresh mapping pass, continue directly with `TOOL_CONTEXT.md` and surface-document updates using current source inspection.

## Guardrails

This mapping pass is documentation/evidence only. Do not run Blender, FFmpeg, providers, patch apply, deploy, force-push, merge or cleanup as part of mapping.