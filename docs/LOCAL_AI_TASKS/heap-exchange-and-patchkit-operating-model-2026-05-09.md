# Heap/Exchange and Patchkit Operating Model — 2026-05-09

## Status

Canonical post-merge operating note for the heap/exchange lifecycle and reusable patchkit boundary.

Merged baseline:

```text
PR #249 feat(ai): add heap exchange runtime lifecycle
PR #250 feat(ai): add reusable patchkit for controlled bundles
```

## Code-driven source of truth

Read source before extending docs or workflows.

Primary files:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/ai/build_heap_exchange_runtime_entry.py
Tools/ai/build_heap_exchange_runtime_exit.py
Tools/validation/check_heap_exchange_runtime_lifecycle.py
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
Tools/ai/patchkit/apply_patch_bundle.py
Tools/ai/patchkit/filesystem.py
Tools/ai/patchkit/anchors.py
Tools/ai/patchkit/powershell.py
Tools/ai/patchkit/reports.py
Tools/validation/run_patchkit_smoke.py
```

## Mental model

The unified run is not a fixed linear script pretending to be intelligence.

Use this boundary model:

```text
IN
  controlled task Markdown
  run identity
  RepoPy/PYTHONPATH gate
  inventories/context/agent-state
  capability and workload evidence

LOOP / HEAP / EXCHANGE
  shared dynamic knowledge surface
  GPU1 primary advisory/provider lane
  GPU0 OpenVINO companion/helper lane
  NPU microtask/diagnostic lane
  official adapter
  context/memory lane
  broker/tool evidence lane
  validators/CPU authority
  public event stream

OUT
  heap exchange exit product
  concrete deterministic operation candidates
  lifecycle validation
  unified chain contract
  patchkit/apply bridge
  review PR product
```

The center is dynamic. The entry and exit are controlled.

## Heap/exchange rule

The heap is the active knowledge surface.

Do not micromanage GPU1/GPU0/NPU/provider interaction as a static chain. The run enters the heap/exchange with enough context and capability evidence; inside that space, registered lanes may cooperate according to runtime routing and evidence quality.

What must stay deterministic:

```text
entry evidence exists
lane availability is recorded
public exchange events are emitted
runtime state is written
exit product is evaluated
concrete patch product is required before review PR product
failure reasons are explicit
```

## Runtime lifecycle artifacts

Entry writes:

```text
output/ai_packets/<stamp>/heap_exchange_runtime_entry.json
output/ai_packets/<stamp>/heap_exchange_runtime_entry.md
output/ai_packets/<stamp>/heap_exchange_runtime_state.jsonl
```

Exit writes:

```text
output/ai_packets/<stamp>/heap_exchange_runtime_exit_product.json
output/ai_packets/<stamp>/heap_exchange_runtime_exit_product.md
```

Observer/public exchange writes:

```text
output/local_ai_runs/*<stamp>*_observer/ai_public_events.jsonl
```

Lifecycle validator writes:

```text
output/validation/heap_exchange_runtime_lifecycle_<stamp>.json
output/validation/heap_exchange_runtime_lifecycle_<stamp>.md
```

## Expected lane roles

| Lane | Role |
|---|---|
| `gpu0` | OpenVINO companion/helper workload and evidence lane. |
| `gpu1` | Reserved/provider lane, normally CUDA/Ollama side. |
| `npu` | Microtask/diagnostic/support lane. |
| `ollama_provider` | Primary advisory/provider evidence lane. |
| `official_adapter` | Task interpretation and official local AI adapter lane. |
| `context_memory` | Context pack, agent state and memory handoff lane. |

The lane set may expand, but new lanes must be mapped, guarded, observable and evidence-producing before being treated as active.

## Exit policy

For review-PR/product runs, metadata-only drafts are not enough.

Required before a review PR product:

```text
operation_count > 0
concrete_operation_count > 0
changed_count > 0 when source writes are expected
manual_review_items may exist but cannot be the only product
```

Valid blocked state:

```text
heap/exchange exit has no concrete deterministic operation candidate
```

This is not a crash. It means the dynamic center entered and observed lanes correctly, but did not produce concrete patch product.

## Patchkit rule

Patchkit is the deterministic OUT boundary for source modifications.

Future patch bundles should not create one-off patcher scripts unless the patchkit operation set is insufficient. Prefer a declarative core patch bundle:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Apply with the reusable runner:

```powershell
python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Patchkit owns:

```text
backup
encoding/BOM preservation
newline preservation without Windows CRCRLF corruption
in-memory dry-run chain simulation
idempotency markers
PowerShell Invoke-Checked anchors
marker insertions
exact replacements
PowerShell parser validation
Python compile validation
git diff --check
JSON/Markdown reports
line count reporting
```

## Bundle schema v1

Example:

```json
{
  "schema_version": 1,
  "kind": "codemod_patch_bundle",
  "operations": [
    {
      "operation": "insert_after_invoke_checked",
      "target": "Tools/workflow/run_unified_local_ai_refactor.ps1",
      "label": "Build AI workload quality routing report",
      "marker": "IA-CARMINE-EXAMPLE-BEGIN",
      "content_file": "fragments/example.ps1"
    }
  ],
  "validators": [
    "powershell_parser",
    "python_compile",
    "git_diff_check"
  ]
}
```

Supported first operations:

```text
insert_after_invoke_checked
insert_before_marker
insert_after_marker
replace_once
append_once
assert_marker
assert_no_naked_throw
```

## Development rule for future changes

Prefer this progression:

```text
read source/code owners
write focused core patch bundle
run patchkit dry-run
run patchkit apply
run targeted validators
inspect line counts
open review PR
```

Do not paste long PowerShell/Python patches into chat when a patchkit bundle can carry the same change safely.

## Validation commands

Heap/exchange lifecycle:

```powershell
python -m py_compile `
  .\Tools\ai\build_heap_exchange_runtime_entry.py `
  .\Tools\ai\build_heap_exchange_runtime_exit.py `
  .\Tools\validation\check_heap_exchange_runtime_lifecycle.py `
  .\Tools\validation\run_heap_exchange_runtime_lifecycle_smoke.py

python .\Tools\validation\run_heap_exchange_runtime_lifecycle_smoke.py `
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

python .\Tools\validation\run_patchkit_smoke.py `
  --repo-root .

git diff --check
```

## Guardrails

Patchkit does not bypass review.

Still forbidden unless explicitly approved:

```text
merge to master by automation
force-push
rewrite history
delete source files
change secrets, permissions, billing or visibility
run Blender/FFmpeg runtime
commit output/**
commit indexAI/code_chunks/**
commit *.db / *.sqlite / renders/**
```

## Open roadmap after this model

Potential next safe steps:

```text
extend patchkit with write_file and JSON-field operations
add patchkit bundle validator independent from apply
make generated patch specs emit patchkit bundle.json directly
connect heap/exchange exit product to patchkit bundle detection
add memory/context namespace manifest as heap input/output surface
expand broker/tool capability map consumed by context packs
```
