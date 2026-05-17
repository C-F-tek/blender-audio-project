# AI Orientation Map — 2026-05-09

## Purpose

Compact orientation map for an AI agent entering the repository after the heap/exchange lifecycle and patchkit merges.

This is not a replacement for source inspection. It is the first map to decide what to read next and which code owner to reuse.

## One-sentence model

IA-Carmine is a code-driven local-AI orchestration workbench where a controlled task enters a dynamic heap/exchange, runtime lanes cooperate through evidence and public events, and the final source-change product exits through deterministic validators, patchkit bundles and review PRs.

## Current baseline

```text
Merged baseline: master after PR #250
Runtime lifecycle: PR #249
Reusable patch boundary: PR #250
Current doc PR: #251
```

## First read path

Read in this order for current work:

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/README.md
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
Tools/ai/README.md
Tools/workflow/README.md
nearest target source file
```

## Mental model

```text
IN
  task Markdown
  stamp/run identity
  RepoPy gate
  inventories
  context pack
  agent state
  workload/capability evidence

LOOP / HEAP / EXCHANGE
  GPU1 / provider planner lane
  GPU0 / OpenVINO companion lane
  NPU / diagnostic microtask lane
  official adapter lane
  context/memory lane
  broker/tool evidence lane
  public exchange event stream

OUT
  heap exchange exit product
  concrete deterministic operation candidates
  lifecycle validator
  patchkit bundle or patch suggestion bridge
  review PR product
```

Entry and exit are controlled. The center is dynamic.

Do not reduce heap/exchange to a static chain. The run must provide context, evidence and lane registration; then the dynamic center may route/cooperate. The exit must still produce deterministic, reviewable product.

## Main owner map

| Responsibility | Code owner |
|---|---|
| Unified local AI run | `Tools/workflow/run_unified_local_ai_refactor.ps1` |
| Heap/exchange runtime entry | `Tools/ai/build_heap_exchange_runtime_entry.py` |
| Heap/exchange runtime exit | `Tools/ai/build_heap_exchange_runtime_exit.py` |
| Heap/exchange lifecycle validation | `Tools/validation/check_heap_exchange_runtime_lifecycle.py` |
| Heap/exchange smoke | `Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py` |
| Reusable patch bundle apply | `Tools/ai/patchkit/apply_patch_bundle.py` |
| Patchkit filesystem/encoding/newlines | `Tools/ai/patchkit/filesystem.py` |
| Patchkit anchors/text ops | `Tools/ai/patchkit/anchors.py` |
| Patchkit PowerShell helpers | `Tools/ai/patchkit/powershell.py` |
| Patchkit reports | `Tools/ai/patchkit/reports.py` |
| Patchkit smoke | `Tools/validation/run_patchkit_smoke.py` |
| Review PR preparation | `Tools/ai/prepare_review_pr.py` |
| Context pack | `Tools/ai/build_ai_context_pack.py` |
| Agent state packet | `Tools/ai/build_agent_state_packet.py` |
| Script/tool inventory | `Tools/validation/build_script_inventory.py` |
| Markdown inventory | `Tools/validation/build_markdown_inventory.py` |
| JSON/report contracts | `Tools/validation/check_validation_report_contracts.py` |
| Patch suggestion product | `Tools/ai/build_task_patch_suggestion_report.py` |
| Legacy patch suggestion apply | `Tools/ai/apply_patch_suggestion_bundle.py` |

Before creating a new script, check this table and the target package README.

## Current source-write rule

Preferred future source modification flow:

```text
read target source
write compact patchkit bundle
run patchkit --dry-run
run patchkit apply
run validators
inspect line counts
open/update review PR
```

Preferred bundle layout:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Do not create a new one-off patcher if patchkit operations can express the change.

## Patchkit command pattern

```powershell
python -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Current first-class patchkit operations:

```text
insert_after_invoke_checked
insert_before_marker
insert_after_marker
replace_once
append_once
assert_marker
assert_no_naked_throw
```

Current first-class validators:

```text
powershell_parser
python_compile
git_diff_check
```

## Run product classification

A full run may produce evidence but still fail as a product gate.

Valid successful product path:

```text
entry exists
runtime lanes available
runtime state events emitted
public exchange events emitted
exit product exists
concrete_operation_count > 0 when review PR product is requested
patchkit or patch bridge produces deterministic product
review PR product is created
```

Valid blocked state:

```text
entry/lane/public events are good
exit product has no concrete deterministic operation candidate
review PR product must not pretend success
```

Metadata-only patch drafts are not enough.

## Validation map

Heap/exchange lifecycle:

```powershell
python -m py_compile `
  .\Tools\ai\build_heap_exchange_runtime_entry.py `
  .\Tools\ai\build_heap_exchange_runtime_exit.py `
  .\Tools\validation\check_heap_exchange_runtime_lifecycle.py `
  .\Tools\validation\run_heap_exchange_runtime_lifecycle_smoke.py

python -m Tools.validation run_heap_exchange_runtime_lifecycle_smoke `
  --repo-root .
```

Patchkit:

```powershell
python -m py_compile `
  .\Tools\ai\patchkit\filesystem.py `
  .\Tools\ai\patchkit\anchors.py `
  .\Tools\ai\patchkit\powershell.py `
  .\Tools\ai\patchkit\reports.py `
  .\Tools\ai\patchkit\apply_patch_bundle.py `
  .\Tools\validation\run_patchkit_smoke.py

python -m Tools.validation run_patchkit_smoke `
  --repo-root .

git diff --check
```

Docs-only:

```powershell
python -m Tools.validation check_docs_links --repo-root . --output output/validation/docs_links.json
python -m Tools.validation check_file_line_limits --repo-root . --output output/validation/file_line_limits.json
git diff --check
```

## Guardrails

Never treat architecture docs as authorization to:

```text
merge without operator command
force-push
rewrite history
delete source
change secrets/permissions/billing/visibility
run Blender runtime
run FFmpeg runtime
commit output/**
commit indexAI/code_chunks/**
commit *.db / *.sqlite / renders/**
```

## What an AI should do when unsure

```text
1. Read the nearest source owner.
2. Read the newest compact task map.
3. Prefer existing validators and patchkit.
4. Produce evidence, not confidence language.
5. Mark stale/obsolete docs as historical instead of following them blindly.
6. Stop if the run exits without concrete deterministic product.
```
