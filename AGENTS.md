# AGENTS.md

Primary repository contract for AI assistants, local agents, automated review systems and GitHub-only assistants working on this repository.

## Mandatory first-read contract

Before planning, editing, validating, opening a PR or suggesting changes, the agent must read:

```text
AGENTS.md
CHATGPT.md
CONTEXT_INDEX.md
docs/README.md
docs/AI_DOCS_ENTRYPOINT.md
docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/CONTEXT_COVERAGE_STATUS.md
docs/DISPATCHER_CONTEXT_COVERAGE.md
Tools/CONTEXT_INDEX.md
```

Then open the nearest area/family `TOOL_CONTEXT.md`, the relevant `dispatch.py`, and the target source/document before making changes.

Historical runbooks under `docs/LOCAL_AI_TASKS/**` and session notes under `docs/AI_SESSION_NOTES/**` are background unless promoted into current contracts. They do not override the current model files, anti-ambiguity contract, model-to-code map, core lane completeness contract, context indexes, dispatcher coverage, source code, validation reports or explicit operator instruction.

## Repository identity

| Field | Value |
|---|---|
| Working title | `IA-Carmine Local AI Orchestration Workbench` |
| Repository | `C-F-tek/blender-audio-project` |
| Main language | Python |
| Active app model | `Universo IA` |
| Anti-ambiguity contract | `docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md` |
| Model-to-code bridge | `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` |
| Lane completeness contract | `docs/CORE_LANE_COMPLETENESS_CONTRACT.md` |
| Operator product entrypoint | `python -m Tools.ai run` |
| Dynamic workflow launcher | `python -m Tools.workflow run_unified_local_ai_refactor` |
| Main provider center | `Ollama / GPU1 / RTX 5080` |
| Coworker lane | `GPU0 / OpenVINO` |
| Micro-lane | `NPU / OpenVINO` |
| Deterministic authority | `CPU validators, brokered tools, source inspection` |
| Legacy domain | Blender audio-reactive scene automation |

The repository name is historical. Do not infer that Blender/audio is the current architectural boundary.

## Universo IA

The complete application is not a single model, single provider or single script. The complete application is the combination of all current models working together as **Universo IA** and concretized through dispatcher-owned tools.

```text
AI limitations / anti-ambiguity contract
+ heap/exchange useful model
+ standalone heap surface model
+ provider lanes unified mind model
+ real product run model
+ compact evidence model
+ patch/code product boundary model
+ core lane completeness contract
+ model-to-code map
= Universo IA
```

Read these as one system:

| Model | File | Meaning |
|---|---|---|
| AI limitations and anti-ambiguity contract | `docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md` | prevents context loss, invented architecture, smoke overfitting, optionalized lanes and completion-sounding claims without evidence |
| Model-to-code map | `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` | connects each model to code families, dispatcher commands, artifacts and validators |
| Core lane completeness contract | `docs/CORE_LANE_COMPLETENESS_CONTRACT.md` | complete/full runs require viable lane evidence; degraded equals unviable |
| Heap/exchange useful model | `docs/HEAP_EXCHANGE_USEFUL_MODEL.md` | controlled input, shared heap/exchange, evidence, deterministic exit |
| Standalone heap surface model | `docs/STANDALONE_HEAP_SURFACE_MODEL.md` | preload, memory, chunks, namespaces, tool catalog, broker, lanes, composer |
| Provider lanes unified mind model | `docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md` | Ollama/main provider, GPU0 coworker and NPU micro-lane as one operational mind with departments |
| Real product run model | `docs/REAL_PRODUCT_RUN_MODEL.md` | evidence-only, blocked and real product run states |
| Compact evidence model | `docs/COMPACT_EVIDENCE_MODEL.md` | raw runtime output vs compact Git-trackable evidence |
| Patch/code product boundary model | `docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md` | provider proposal, patch plan, code product, PatchKit, repo-patch-runner and reviewed apply boundaries |

A run, document, provider output or patch proposal is incomplete if it contradicts these models without source/validator evidence.

## AI limitation rule

A programming AI must not treat its chat context as project truth.

```text
chat memory != heap memory
status text != runtime evidence
provider prose != product
report existence != successful run
smoke pass != full product validation
activity != useful work
```

If evidence cannot be named, the correct status is `not proven`, not `done`.

## Core lane viability rule

For complete/full profiles, required core lanes are not optional and `degraded` is not acceptable as success.

```text
valid evidence -> viable
missing evidence -> unviable
failed evidence -> unviable
degraded -> unviable
unavailable -> unviable
```

A full smoke must fail if a required lane lacks valid evidence. A partial/diagnostic smoke may report degraded/unavailable lanes, but it must not be named or treated as full.

## Mental model

```text
IN
  operator request / task Markdown
  context indexes and source refs
  preload surfaces
  tool catalog
  memory/chunk surfaces

UNIVERSO IA / HEAP / EXCHANGE
  shared runtime state
  exchange events
  Ollama main planner/synthesis center
  GPU0 coworker/reviewer lane
  NPU microtask/audit lane
  brokered tool execution
  CPU validator authority

OUT
  blocked reason
  diagnostic evidence
  recommendation evidence
  concrete operation candidate
  code/patch product
  reviewable product
```

The center is dynamic. The entry and exit must stay controlled, observable and deterministic.

## Provider departments

| Department | Role | Must produce |
|---|---|---|
| Ollama / main provider | central reasoning, planning, synthesis, candidate generation | structured recommendation/proposal evidence |
| GPU0 / coworker lane | peer review, OpenVINO/helper workload, discrepancy checks | observable peer evidence, contradiction/refinement notes |
| NPU / micro-lane | microtask/tool/device provider and diagnostic support | compact micro-provider/audit reports |
| CPU / validators | deterministic authority | pass/fail/blocked reports |

Ollama is the main center, but not an unchecked source-write authority. GPU0 is not decoration; it must leave observable evidence when selected. NPU is a real bounded micro-task/tool/device provider when selected, but it remains support/micro and must not be reported as the primary semantic provider.

## Canonical command surfaces

Use dispatcher-owned commands instead of launching scattered files by path:

```powershell
python -m Tools.ai <tool> [args...]
python -m Tools.validation <tool> [args...]
python -m Tools.workflow <tool> [args...]
python -m Tools.npu <tool> [args...]
python -m Tools.docs <tool> [args...]
python -m Tools.git <tool> [args...]
python -m Tools.repo_patch_runner <tool> [args...]
```

Area and family navigation:

```text
Tools/CONTEXT_INDEX.md
Tools/ai/CONTEXT_INDEX.md
Tools/validation/CONTEXT_INDEX.md
Tools/workflow/CONTEXT_INDEX.md
Tools/npu/CONTEXT_INDEX.md
Tools/docs/CONTEXT_INDEX.md
Tools/git/CONTEXT_INDEX.md
Tools/repo_patch_runner/CONTEXT_INDEX.md
```

For model-to-code navigation, use:

```text
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Product and evidence rules

Do not call evidence a product.

```text
task Markdown = input
provider answer = evidence
runtime report = evidence
recommendation = planning evidence
metadata-only patch spec = not product
candidate operation = possible product input
code/patch product = reviewable product
blocked reason = valid non-product exit
```

A real product path requires:

```text
concrete operation
target files identified
change strategy or diff present
validation path present
review artifact or blocked reason explicit
```

If source writes are expected, `changed_count > 0` must be true or the run must be classified as blocked/non-product.

## Compact evidence policy

Raw runtime output is not documentation by default.

Do not commit by default:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
*.sqlite-wal
*.sqlite-shm
raw checkpoints
large generated chunk folders
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```

Allowed when intentional and small enough to review:

```text
source files
tests
small documentation
selected compact evidence
reviewed patch/code product docs
```

For evidence publication, read `docs/COMPACT_EVIDENCE_MODEL.md` first.

## Source-write boundaries

PatchKit/code-product/repo-patch-runner paths are deterministic application boundaries, not authorization layers.

Preferred source-change path:

```text
read target source
produce compact candidate/code/patch product
run dry validation when available
apply through reviewed product boundary when explicitly scoped
run targeted validators
inspect line counts for code/script files
commit only intended files
```

PatchKit bundle pattern:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Standard PatchKit commands:

```powershell
python -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Agents must not claim local application or validation until terminal/output evidence is available.

## Markdown coherence policy

This repository uses compact Markdown as an operational surface.

```text
active .md file <= 500 lines
preferred active runbook <= 400 lines
```

When a maintained Markdown file exceeds the limit, keep the original as a compact index and split details into a sibling folder named exactly like the file, including `.md`:

```text
<file>.md/
  part-001.md
  part-002.md
```

Use repository tools for structural Markdown hygiene when available:

```powershell
python -m Tools.docs refactor_markdown_splits --repo-root . --migrate-legacy-splits --split-monolithic
```

Do not use fragile Windows PowerShell `Set-Content` snippets for Unicode Markdown. Prefer PatchKit or Python UTF-8 read/write helpers.

## Code length policy

Hard limit for maintained code/script files:

```text
Python/PowerShell/scripts/source code: <= 400 lines per maintained source file
```

When modifying code, report resulting line count for every created or modified code/script file.

Existing oversized files are technical debt; split progressively when touching that area for a code task.

## Provider-capable `.venv` rule

Before provider, GPU0, NPU, OpenVINO or run-unica validation, verify the repository Python environment:

```powershell
$env:IA_CARMINE_PYTHON = "<repo>\.venv\Scripts\python.exe"
$env:PYTHONPATH = "<repo>"
& $env:IA_CARMINE_PYTHON -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; c=Core(); print(c.available_devices)"
```

Expected IA-Carmine workstation visibility:

```text
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

If dependencies are missing, classify as `provider_python_environment_missing_dependency`, not as GPU0/NPU provider failure. GPU.1 may be visible through OpenVINO, but it is reserved for CUDA/Ollama and must not receive OpenVINO workload.

## Production-grade tool promotion rule

A new capability is not complete when code is merely inserted.

Every added or changed tool/lane must move through the production path before it is called done:

```text
implemented code
-> wired into dispatcher/entrypoint according to scope
-> visible in context docs or CLI/help/runbook
-> environment preflight documented when relevant
-> emits compact evidence
-> appears in manifest/report/evidence surfaces when relevant
-> understood by validators or explicitly marked diagnostic
-> has viable evidence in complete/full profiles
```

Do not stop at an internal helper, isolated smoke script or hidden command.

## TUTTO SU TUTTO / run-unica rule

TUTTO SU TUTTO means intelligent combined use of all relevant mapped tools/scripts inside the complete run-unica flow.

It does not mean executing every script blindly. It means the run can discover, select, coordinate, validate and report every applicable capability from the maps while respecting guardrails, provider availability, evidence quality and explicit `-No*` opt-outs.

`RunIntensity quick|balanced|deep|custom` changes budget, rounds, context limits, token limits and keep-alive only. It must not reduce the semantic perimeter.

## Allowed by default

```text
read files
inspect repository structure
add/update non-destructive documentation
add report-only validators and inventory tools
create manual-review patch specs/bundles
run focused local validation when execution is available
open/update PRs without merging
```

## Requires explicit human approval

```text
delete files
force-push
rewrite history
merge to master/protected branch
change secrets, permissions, billing or visibility
deploy production
rename repository
run long Blender renders or heavy GPU workloads outside an explicitly selected full/provider workflow
change provider/model execution semantics
add dependencies
move package entrypoints
rewrite large Blender scripts
modify full frame-level analysis JSON
```

## Never commit

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
*.sqlite-wal
*.sqlite-shm
raw checkpoints
large full analysis JSON outside compact evidence policy
indexAI/code_chunks/** unless explicitly requested as compact generated index evidence
```

## Refactoring rules

```text
prefer existing helpers before creating new ones
keep path/JSON/provider/evidence logic app-agnostic when practical
keep generated indexes out of source-level refactors
keep artistic scene behavior separate from infrastructure refactors
do not migrate Blender packages broadly unless explicitly scoped
centralize execution through broker/registry/validator/evidence surfaces instead of duplicating per-runner logic
```

## Reporting contract

For code/script changes report:

```text
changed files
purpose
resulting line count for every created/modified script
validation performed or missing
provider/runtime execution status
risks
follow-up recommendations
```

A workflow change is incomplete unless it produces compact evidence or clearly states which checks are missing.

## Conflict rule

When docs, source, evidence and user request disagree:

```text
1. stop relying on the conflicting text;
2. inspect current source and dispatcher;
3. inspect current validators/evidence;
4. update the smallest current map or context file;
5. report unresolved conflict instead of inventing certainty.
```
