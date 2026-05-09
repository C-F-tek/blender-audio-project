# AGENTS.md

Primary repository contract for AI assistants, local agents, automated review systems and GitHub-only assistants working on this repository.

## Mandatory contract

Before planning, editing, validating, opening a PR or suggesting changes, the agent must:

1. read `AGENTS.md`;
2. read `CHATGPT.md` and `CHATGPT/README.md` when resuming ChatGPT-assisted, local-AI, full-toolbox or handoff-driven work;
3. read `docs/README.md` for the current documentation index;
4. read `docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md` for the current IN -> dynamic heap/exchange -> deterministic OUT operating model;
5. read `docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md` for the compact AI first-orientation map;
6. read `docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md` when documentation appears conflicting or stale;
7. read `docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md` when classifying, deleting, splitting or refactoring old docs/index/discovery surfaces;
8. read `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` for the current code/state bridge when present;
9. read `docs/MAIN_RUNTIME_ARCHITECTURE.md` when working on runtime, provider, broker, validator, telemetry or workflow architecture;
10. read `docs/LOCAL_AI_RUN_BOOTSTRAP.md` when working from or delegating to a local checkout;
11. read `docs/LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md` before converting patch-note suggestions into source edits;
12. follow hard guardrails unless the human explicitly approves a normally restricted action;
13. inspect the target source/document before proposing or applying a patch;
14. report conflicts between the request, code, docs, evidence and guardrails before modifying files.

## Repository identity

| Field | Value |
|---|---|
| Working title | `IA-Carmine Local AI Orchestration Workbench` |
| Repository | `C-F-tek/blender-audio-project` |
| Main language | Python |
| Active architecture | Shared runtime heap / blackboard, provider-lane orchestration, broker execution, semantic tools registry, deterministic CPU validators, telemetry/evidence workflows |
| Primary provider lane | `GPU1 / Ollama / RTX 5080 -> primary advisory planner/worker` |
| Secondary provider lane | `GPU0 / OpenVINO -> coworker/helper peer worker and tool-request producer` |
| Microtask provider lane | `NPU / OpenVINO -> microtask responder, support lane, probe and diagnostics` |
| Current source-write boundary | `Tools/ai/patchkit/apply_patch_bundle.py` for reviewed patchkit bundles when operations can express the change |
| Legacy domain | Blender audio-reactive scene automation |

The repository name is historical. Do not infer that Blender/audio is the current architectural boundary.

## Canonical reading order

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/README.md
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
CHATGPT/next-chat-handoff-*.md                 # when present and relevant
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md                 # local checkout only
README.md
WORKFLOW.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
docs/LOCAL_AI_TASKS/md-coherence-only-github-pass-2026-05-06.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/patch-notes-quality-product-2026-05-07.md
docs/LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
Tools/ai/README.md
Tools/workflow/README.md
Tools/validation/README.md
nearest package/tool README
target file
```

For full toolbox, refactor, provider or 0-to-10 local AI runs, the active entrypoint is:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

## Markdown coherence policy

This repository uses compact Markdown as an operational surface.

Hard rule for maintained Markdown:

```text
active .md file <= 500 lines
preferred active runbook <= 400 lines
```

When a maintained Markdown file exceeds 500 lines:

```text
keep the original file as a compact index
create a sibling folder named exactly like the file, including .md: <file>.md/
move detailed content into <file>.md/part-001.md, part-002.md, ...
keep each part <= 500 lines
link all parts from the compact index
```

Generated evidence may exceed 500 lines only when it has compact JSON/Markdown manifest, summary or index and is not used as a primary entrypoint.

Markdown cleanup rules:

```text
update canonical docs before adding parallel runbooks
mark stale docs as superseded/historical/delete-candidate before removal
do not commit output/**, indexAI/code_chunks/**, *.db, *.sqlite, renders/** or generated media
never treat generated indexes/evidence as maintained source docs
```

Current compact operational state:

```text
Baseline: master after PR #251 merge
Primary launcher: Tools/workflow/run_unified_local_ai_refactor.ps1
Current operating model: docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
AI orientation map: docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
Documentation panorama/staleness map: docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
Repository hygiene procedure: docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md
Capability map: docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
Parameter map: docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
Docs bridge: docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
Main runtime architecture: docs/MAIN_RUNTIME_ARCHITECTURE.md
Patchkit boundary: Tools/ai/patchkit/apply_patch_bundle.py
Current mode: code-driven, docs-first updates unless source changes are explicitly scoped
Review posture: no merge to master unless explicitly requested
```

The earlier broker telemetry gap is resolved/historical unless a new regression is found. Use `docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` and newer telemetry evidence for the recent baseline.

## Main runtime architecture target

The primary runtime target is:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Operational meaning:

```text
provider lanes advise, help, classify or respond through explicit roles
broker unico executor is the execution gateway for registered tools
semantic tools registry is the capability source of truth
deterministic validators on CPU remain local pass/fail authority
telemetry/event stream records executed, skipped, degraded and blocked phases
```

Current runtime boundary:

```text
IN = controlled task/context/capability entry
LOOP = dynamic heap/exchange where GPU1/GPU0/NPU/provider lanes cooperate
OUT = deterministic exit product, lifecycle validation, patchkit bundle or review PR
```

Architecture targets do not authorize source writes, provider execution, patch application, Blender runtime, FFmpeg runtime, commit, push, merge or delete by themselves.

## Patch suggestion ledger policy

A patch-notes quality product is a proposal ledger, not executable code.

```text
patch_notes_quality_product_<stamp>.json = review input
summary.proposal_core = compact bundle handoff ledger
patchkit bundle / branch diff = reviewed implementation artifact
```

Agents must not convert ledger entries directly into source writes. Review order is:

```text
1. python_python
2. python_doc
3. doc_doc
4. doc_python
```

Before patching any suggestion:

```text
refresh against current master
verify source/target still exists
verify missing imports/symbols are still missing
reject generated-evidence noise and placeholder fenced-code paths
use a small reviewed patchkit bundle or branch diff
run py_compile/smoke/git diff --check
```

If a suggestion is stale, record it as stale evidence when useful and do not patch it.

## Patchkit source-write policy

Future long, delicate or repeated patch work should centralize the modification core in a repository-native patchkit bundle when patchkit operations can express the change:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Standard apply path:

```powershell
python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Patchkit is not an authorization layer. It is a deterministic application boundary. Human/operator scope, branch policy and guardrails still apply.

## Remote-AI PatchKit handoff policy

When an AI does not have local terminal access, PatchKit remains the preferred controlled route for large local changes.

The AI should produce:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*
local dry-run command
local apply command
local validation commands
expected touched files and line-count reporting requirement
```

The AI must not claim local application or validation until the user returns terminal output.

The local operator applies:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

& $RepoPy .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Remote handoff bundles must be idempotent where practical, use stable anchors or guarded delete markers and include validators when possible.

## Code length policy

Hard limit for maintained code/script files:

```text
Python/PowerShell/scripts/source code: <= 400 lines per maintained source file
```

When modifying code, report resulting line count for every created or modified code/script file.

Existing oversized files are technical debt; split them progressively when touching that area for a code task.

## AI session notes

`docs/AI_SESSION_NOTES/` stores compact Markdown notes from long AI-assisted sessions.

Rules:

```text
keep notes factual and compact
record decisions, validation outcomes, blockers and next actions
do not paste private reasoning
do not let notes override AGENTS.md, source, validation reports or canonical docs
promote stable principles into canonical docs/LOCAL_AI_TASKS or contract docs
```

## Provider and peer-exchange posture

Canonical production roles:

```text
GPU1 / Ollama / RTX 5080 = mandatory primary advisory planner/worker
GPU0 / OpenVINO = companion peer worker and tool-request producer
NPU = micro-fast task assistant and lightweight tool-support lane
deterministic scripts = heavy audit and validation authority
runtime tool broker = controlled tool execution for GPU1, GPU0 and NPU requests
broker unico executor = target central execution gateway for registered tools
semantic tools registry = target capability source of truth
telemetry/event stream = target visibility surface for executed, skipped, degraded and blocked phases
```

GPU1/Ollama must execute the primary advisory lane for real 0Full10/run-unica execution unless explicitly disabled by an operator flag or classified as unavailable/degraded by evidence.

GPU0 is not complete when it only performs preflight, smoke, final workload evidence or passive support. GPU0 must move toward peer-worker behavior:

```text
GPU1 planner/worker task packet
  -> GPU0 companion execution
  -> GPU0 response/evidence packet
  -> optional GPU0 tool requests
  -> runtime broker execution for GPU0 requests
  -> non-blocking NPU micro/tool-support signal
  -> runtime broker execution for NPU requests when present
  -> GPU1 planner/auditor consumption
  -> final telemetry, bundle and gate evidence
```

When `IA_CARMINE_GPU0_COMPANION_MODEL_DIR` is configured, GPU0 may run OpenVINO GenAI tasks on GPU.0. When no companion model is configured, GPU0 may still produce numeric, static, tool-request or report-only evidence, but the run must classify missing semantic companion mode explicitly.

NPU should not be the heavy audit authority when deterministic validators already cover the product. Preferred NPU role:

```text
micro-fast task support
small checkpoint review
provider/device diagnostics
structured helper output
tool-intelligence support when cheap and available
```

Heavy audit, report validation and acceptance decisions stay with deterministic repository scripts unless a task explicitly requests NPU semantic review.
NPU tool-support output must stay non-blocking, broker-controlled and visible in telemetry/bundle evidence when provider lanes are selected.

## Provider-capable `.venv` rule

Before running provider, GPU0, NPU, OpenVINO or 0Full10/run-unica validation, agents must verify:

```powershell
$env:IA_CARMINE_PYTHON = "<repo>\.venv\Scripts\python.exe"
$env:PYTHONPATH = "<repo>"
& $env:IA_CARMINE_PYTHON -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; c=Core(); print(c.available_devices)"
```

Required OpenVINO/GPU0/NPU packages:

```text
numpy
openvino
openvino-genai
```

Expected IA-Carmine workstation visibility:

```text
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

If `.venv` is missing dependencies, classify as `provider_python_environment_missing_dependency`, not as GPU0/NPU provider failure. GPU.1 may be visible through OpenVINO, but it is reserved for CUDA/Ollama and must not receive OpenVINO workload.

## Production-grade tool promotion rule

A new capability is not complete when code is merely inserted.

Every added or changed tool/lane must move through the production path before it is called done:

```text
implemented code
  -> wired into the canonical operator entrypoint
  -> visible in CLI/help/runbook/operator docs
  -> environment preflight documented when dependencies/providers matter
  -> activated by intended profile or explicit flag
  -> emits compact JSON/Markdown evidence
  -> appears in phase_status / phase_reports or equivalent manifest surfaces
  -> is understood by contract validators
  -> is included in evidence/bundle/handoff when relevant
  -> has unavailable/degraded/disabled classification when it cannot run
```

Do not stop at an internal module, helper function, isolated smoke script or hidden command.

For 0Full10/run unica, promoted lanes must be included by default unless disabled by explicit operator flags or classified as unavailable/degraded through manifest, telemetry, phase reports or validator evidence.

## TUTTO SU TUTTO / 0Full10 run-unica rule

TUTTO SU TUTTO means intelligent combined use of all relevant mapped tools/scripts inside the complete 0Full10 run-unica flow.

It does not mean executing every script blindly. It means the run unica can discover, select, coordinate, validate and report every applicable capability from the maps while respecting guardrails, provider availability, evidence quality and explicit `-No*` opt-outs.

```text
mapped capability
  -> lane selection
  -> preflight / availability classification
  -> execution or explicit skip/degraded state
  -> deterministic validation when applicable
  -> telemetry/evidence/bundle publication
  -> recommendation, patch-plan or review-PR product when requested
```

0Full10 is the run unica: complete 0-to-10 workflow over the whole active project perimeter.

`-Full0To10` is a compatibility/shortcut CLI flag when present in the launcher. It must not be treated as a magic source of semantics. Its behavior should remain expressible as explicit lane composition:

```text
task input
run identity
real-run activation
intensity/budget
provider lanes
evidence lanes
patch/review lanes
explicit -No* opt-outs
```

A valid 0Full10/run-unica execution includes every major phase unless the operator disables a phase explicitly with a `-No*` flag.

Expected by default:

```text
pipeline adapter ufficiale eseguito
packet/proposals generati
GPU1/Ollama primary advisory executed or explicitly classified degraded
GPU0 companion/peer evidence present when configured or explicitly classified degraded
NPU micro-fast/tool-support diagnostics present when available
patch specs creati e validati
workload quality routing presente
context pack presente
SQLite memory IN/OUT presente quando non disabilitata
heap/exchange runtime entry presente
heap/exchange runtime state presente
heap/exchange runtime exit product presente quando product lanes are selected
heap/exchange lifecycle validator presente quando product lanes are selected
runtime broker report absorbed into telemetry
patch_application_performed=false unless an explicit reviewed patch boundary is selected
```

As the main runtime architecture lands, 0Full10 should progressively expose:

```text
blackboard state report
broker unico executor report
semantic tools registry snapshot
deterministic validators / CPU authority summary
telemetry/event stream summary
GPU1/GPU0/NPU lane status reports
```

Future tools become part of TUTTO SU TUTTO only after they are mapped, wired, guarded, observable and evidence-producing. Architecture targets are expansion space, not current execution claims.

`-RunIntensity quick|balanced|deep|custom` changes budget, rounds, context limits, token limits and keep-alive only. It must not reduce the 0Full10 semantic perimeter.

A missing full-run lane is valid only when one of these is true:

```text
explicit -No* disabler is present
manifest/report records unavailable-tool or provider failure
-DryRun records the phase as planned but not executed
```

## Important folders

| Path | Meaning |
|---|---|
| `CHATGPT/` | Lightweight handoff notes. |
| `docs/AI_SESSION_NOTES/` | Compact session notes and decisions. |
| `Tools/ai/` | AI orchestration, provider probes, evidence bundles, heap/exchange lifecycle helpers and patch-plan tooling. |
| `Tools/ai/patchkit/` | Reusable controlled patch-bundle application helpers. |
| `Tools/workflow/` | Local workflow runners and post-validation packet generation. |
| `Tools/npu/` | NPU/OpenVINO support and diagnostics. |
| `Tools/validation/` | Non-invasive validators and inventory builders. |
| `docs/` | Stable documentation contracts and project state. |
| `docs/MAIN_RUNTIME_ARCHITECTURE.md` | Main runtime topology and blackboard/broker/registry/validator/telemetry contract. |
| `docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md` | Current runtime operating model. |
| `docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md` | Compact first-orientation map for AI agents. |
| `docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md` | Automated hygiene/refactor/delete allowlist procedure. |
| `indexAI/` | Generated indexes/context/patch material. Do not hand-refactor as source. |
| `Scripting/` | Blender application-domain packages; frozen for core/backend work unless scoped. |

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
run long Blender renders or heavy GPU workloads
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
raw checkpoints
large full analysis JSON outside compact evidence policy
indexAI/code_chunks/** unless explicitly requested as generated index evidence
```

## Patch delivery policy

For long, multi-file or delicate changes, especially on workflow, broker, memory, GPU/NPU provider or runner code, prefer repository-native patchkit bundles when supported:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Patchkit bundles must be idempotent where possible, create backups when writing, block on failed validators, report resulting line counts for modified scripts and never commit automatically.

For remote AI sessions without local terminal access, PatchKit is the official handoff format for large controlled changes:

```text
AI authors bundle + local commands
user runs dry-run/apply/validators locally
user returns output
AI continues from real terminal evidence
```

ZIP patch bundles remain acceptable for external/manual transfer when repository-native patchkit cannot express the change. ZIP-internal names such as `README.md`, bundle runner script and `patches/` are bundle members, not repository-tracked source paths.

Patch-note products and `summary.proposal_core` ledgers are not patch bundles. They must be converted into reviewed patchkit bundles or branch diffs before any source write.

## Refactoring rules

```text
prefer existing helpers before creating new ones
keep path/JSON/provider/evidence logic app-agnostic when practical
keep generated indexes out of source-level refactors
keep artistic scene behavior separate from infrastructure refactors
do not migrate Blender packages broadly unless explicitly scoped
when implementing the main runtime architecture, centralize execution through broker/registry/validator/telemetry surfaces instead of duplicating per-runner logic
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
