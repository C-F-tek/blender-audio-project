from __future__ import annotations

KNOWN_MARKDOWN_TEMPLATES: dict[str, str] = {
    "docs/README.md": """# Documentation Index

## Status

Compact repository documentation index.

Canonical root contract:

```text
../AGENTS.md
```

Current docs-side router:

```text
AI_DOCS_ENTRYPOINT.md
```

## Current first-read path

```text
../AGENTS.md
../CHATGPT.md
../CHATGPT/README.md
README.md
AI_DOCS_ENTRYPOINT.md
LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

## Active maps

| Area | Document |
|---|---|
| Runtime architecture | `MAIN_RUNTIME_ARCHITECTURE.md` |
| Local AI workflow | `LOCAL_AI_WORKFLOW.md` |
| Data flow | `DATA_FLOW.md` |
| JSON/report schemas | `JSON_SCHEMAS.md` |
| Patch-spec workflow | `PATCH_SPEC_WORKFLOW.md` |
| Project status | `PROJECT_STATUS_POINT.md` |
| AI docs entrypoint | `AI_DOCS_ENTRYPOINT.md` |
| Tooling index | `../tools/ai/README.md`, `../tools/workflow/README.md`, `../tools/validation/README.md` |

## Policy

Keep this file compact. Do not add competing first-read orders here.
""",
    "docs/PATCH_SPEC_WORKFLOW.md": """# Patch Spec Workflow

## Status

Compact required workflow bridge for patch-spec and PatchKit work.

This file is required by AI context-pack startup and is intentionally a routing
document. It does not authorize source writes by itself.

## Source-write boundary

Current controlled source-write mechanisms:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.py
patch_specs/<bundle>/fragments/*.ps1
tools/ai/patchkit/apply_patch_bundle.py
tools/ai/generated_patch_specs_apply.py
```

Patch notes, proposal ledgers and generated summaries are review inputs only.
They must become deterministic patch operations or branch diffs before source
files are modified.

## Standard local sequence

```powershell
$RepoPy = (Resolve-Path .\\.venv\\Scripts\\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy .\\Tools\\ai\\patchkit\\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\\patch_specs\\<bundle>\\bundle.json `
  --dry-run

& $RepoPy .\\Tools\\ai\\patchkit\\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\\patch_specs\\<bundle>\\bundle.json
```

## Required validation posture

```text
inspect current source
verify target files exist
avoid output/**, renders/**, *.db, *.sqlite, indexAI/code_chunks/**
run py_compile or focused validator when Python changes
run git diff --check
report resulting line counts for scripts/code
record unavailable/degraded provider lanes as evidence, not success
```

## Read next

```text
../AGENTS.md
AI_DOCS_ENTRYPOINT.md
LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
../patch_specs/README.md
../tools/ai/patchkit/apply_patch_bundle.py
```
""",
    "docs/PROJECT_STATUS_POINT.md": """# Project Status Point

## Status

Compact current status checkpoint for IA-Carmine repository self-improvement.

## Current project identity

```text
IA-Carmine Local AI Orchestration Workbench
```

The active architecture is the local AI orchestration workbench: heap/exchange
runtime, provider lanes, broker/tool execution, memory/context preload,
validators, evidence bundles and patch/review product lanes.

## Current runtime target

```text
IN -> preload/context/memory/tool state -> heap/exchange loop -> deterministic OUT
```

## Product expectation

A successful product run must produce concrete reviewable output, not only
evidence. Proposal chunks must reference real repository paths and must not be
placeholder/TODO/stub content.
""",
    "docs/DATA_FLOW.md": """# Data Flow

## Status

Compact active data-flow contract.

## Runtime flow

```text
operator task / task Markdown
  -> required docs/context initializer
  -> real product preflight
  -> tool catalog + repo docs + semantic chunks + memory inventory
  -> startup task-file / heap input
  -> heap blackboard / exchange state
  -> provider lanes and deterministic tools
  -> proposal chunks / patch specs / evidence
  -> composer / review product / final package
```

## Failure rule

A degraded context preload may continue only when artifact usefulness is
recorded explicitly. A final product must fail honestly when no concrete
proposal/patch output exists.
""",
    "docs/LOCAL_AI_WORKFLOW.md": """# Local AI Workflow

## Status

Compact workflow contract for local AI runs.

## Canonical product path

```text
tools/workflow/run_unified_real_product_pr.ps1
```

## Heap/context closure path

```text
ia_carmine/runtime/heap_context_closure/cli.py
```

The heap closure path must perform:

```text
required context file initialization
real product preflight
startup docs/memory/tool/context reload
heap runtime execution
composer/export closure
```

## Python environment

```powershell
$RepoPy = (Resolve-Path .\\.venv\\Scripts\\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path
```
""",
    "docs/JSON_SCHEMAS.md": """# JSON Schemas

## Status

Compact schema orientation for IA-Carmine reports.

## Common report fields

```text
schema_version
kind
generated_at
repo_root
passed
errors
warnings
provider_execution_performed
patch_application_performed
source_writes_performed
```

## Context preload fields

```text
tool_executions
effective_passed
artifact_useful
input_ready_before_heap
startup_task_file
required_context_files_json
tool_catalog
memory_inventory
operational_memory
transient_request_context
ai_context_pack
semantic_chunks
repo_docs
```

## Contract rule

When a tool continues after partial failure, it must record the degraded
requirement and the artifact usefulness explicitly.
""",
}
