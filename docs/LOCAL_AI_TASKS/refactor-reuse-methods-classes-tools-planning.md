# Refactor/reuse methods, classes and tools planning task

## Status

Stable local-AI planning task for IA-Carmine refactor/reuse work.

This task is intended for a full-run planning pass, not for automatic patch application.

## Objective

Analyze the repository code and produce a manual-review refactor/reuse plan for:

```text
duplicate methods/classes
reusable helper functions
base-class/superclass opportunities
project-tool promotion candidates
support-library extraction candidates
workflow/provider/telemetry utility centralization
code that should remain app-specific and not be promoted
The goal is a controlled mega patch plan, not a blind rewrite.

Current doctrine
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
telemetry accompanies evidence and patch plans for completeness

For this task, tutto includes code, docs, workflow scripts, validation tools, provider diagnostics, telemetry builders, memory/context lanes and Blender/audio application boundaries.

Hard requirements

The run must be review-only:

patch_application_performed=false
source_writes_performed=false

Do not:

apply patches automatically
perform source writes
run Blender
run FFmpeg
commit output/**
commit *.db or *.sqlite
commit indexAI/code_chunks/**
touch secrets, permissions, billing, visibility or deploy settings
merge to master
force-push or rewrite history
Required focus areas
Workflow and orchestration

Inspect for reusable workflow helpers across:

Tools/workflow/**
Tools/ai/**
Tools/validation/**
Tools/npu/**

Candidate themes:

report writing
manifest writing
path normalization
PowerShell command wrappers
provider diagnostic result normalization
telemetry summary assembly
bundle/final-summary assembly
patch-plan target hygiene
error/failure/blocked/degraded state propagation
Validation and report contracts

Inspect validator/report code for shared abstractions:

common report fields
schema_version/kind/repo_root/passed/errors/warnings
provider_execution_performed
patch_application_performed
source_writes_performed
blender_runtime_execution_performed
ffmpeg_execution_performed
JSON/Markdown paired output helpers
scoped report validation
warning policy ledgers
Provider and runtime diagnostics

Inspect provider-related code for extraction candidates, but do not promote provider execution by default.

Candidate reusable objects:

provider advisory state
provider failure reasons
degraded provider components
GPU/NPU timing summaries
real per-round elapsed_seconds extraction
workload quality lane routing
provider preflight normalization
Broker/tool promotion

Use docs/LOCAL_AI_TASKS/project-tool-registry.md and promotion docs to classify tools.

Do not promote these as broker-default tools:

Blender runtime tools
FFmpeg/audio encoding tools
Git write tools
patch apply tools
arbitrary shell execution tools
provider execution tools without explicit diagnostic-only contract
SQLite persistent write tools unless explicitly allowed
Blender/audio application boundary

Inspect Blender/audio files for reusable helper candidates, but keep app-specific runtime behavior separate.

Candidate extraction must preserve:

no Blender runtime during planning
no FFmpeg runtime during planning
no automatic behavior changes
manual-review patch plan only
Python string patch hygiene

Treat command-example cleanup and embedded Markdown/code fences as high-risk for multiline rewrites.

Do not introduce broad triple-quoted/raw multiline rewrites to fix command examples.

Prefer:

minimal one-line literal edits
POSIX-style relative examples such as ./Tools/...
explicit doubled backslashes when Windows path syntax must be preserved

Validate string/command-example changes with:

python -m py_compile
git diff --check
line counts
focused diff review
Required output

The full run should produce or update review artifacts containing:

recommendations
patch plan
review-only patch specs when supported
telemetry/capability/final-summary context
provider degradation notes if provider probes fail
source-write and patch-application flags
safe target list
unsafe/deferred target list
promotion/backlog notes
Acceptance criteria

A valid result must show:

patch_application_performed=false
source_writes_performed=false
provider state visible in telemetry/bundle/final summary
patch plan targets source/docs only when safe
no ordinary patch targets under docs/LOCAL_VALIDATION_EVIDENCE/**
no ordinary patch targets under output/**
no ordinary patch targets under indexAI/code_chunks/**
no generated/runtime artifacts committed as source

The patch plan must explicitly distinguish:

safe mechanical refactor
manual-review refactor
requires local runtime validation
requires Blender runtime validation
requires provider execution validation
defer/do not promote
Suggested command

Use the unified launcher from the repository root:

powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\Tools\workflow\run_unified_local_ai_refactor.ps1" `
  -TaskFile ".\docs\LOCAL_AI_TASKS\refactor-reuse-methods-classes-tools-planning.md" `
  -Full0To10 `
  -RunIntensity quick `
  -SkipGitSync `
  -NoBranch `
  -NoExecutionTail

Increase intensity only after the quick planning pass is inspectable from manifest, telemetry, bundle/final summary and patch plan.

Post-run handling

After the run:

Read the latest unified_local_ai_refactor_manifest.json.
Inspect provider diagnostics and workload quality reports.
Inspect decision loop recommendation and patch-plan counts.
Group evidence, patch plan, telemetry, capability manifest, full toolbox telemetry summary and AI-to-AI bundle/final summary.
Push runtime artifact bundle as a draft GitHub release asset or attach to PR; do not commit output/**.
Select a controlled patch subset manually.
Apply source/docs changes in a normal reviewed commit only after focused validation.
