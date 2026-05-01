# Workflow

## Purpose

This file is the root operational workflow for `IA-Carmine Local AI Orchestration Workbench`.

The GitHub repository slug is still `C-F-tek/blender-audio-project`, but the operational project is now broader than Blender/audio. The current workflow centers on local AI provider orchestration, validation, quality routing, compact evidence, and guarded multistep execution.

## Core principle

Work should move through small, explicit, validated tasks.

```text
read context
  -> build task-scoped context pack when useful
  -> choose one task
  -> define scope
  -> change minimal files
  -> run focused validation or explicit provider probes
  -> build post-validation AI work packet when useful
  -> build compact GitHub evidence bundle
  -> regenerate indexes when needed
  -> commit clear result
  -> share proof-of-work evidence
```

## Current provider-lane policy

```text
Ollama -> GPU/CUDA -> primary advisory provider
OpenVINO -> NPU -> probe / guardrail / decode diagnostic
```

Provider execution must be explicit. The preferred local workflow uses `-UsePrimaryAdvisoryProvider`, which activates Ollama/GPU only when the workload quality routing report confirms it as a usable primary advisory provider.

## Required reading before work

Read in this order:

```text
AGENTS.md
docs/README.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
Tools/npu/pipeline/README.md
Tools/validation/README.md
docs/EXECUTION_PLANS/README.md
```

For code changes, also read the nearest package/tool README and the target source file.

## Task lifecycle

### 1. Define the task

A task should have:

```text
goal
scope
files likely touched
validation commands
expected output
risk level
provider execution mode if any
```

For non-trivial tasks, create an execution plan under:

```text
docs/EXECUTION_PLANS/active/
```

For tasks where the relevant files are unclear, build a bounded context pack first:

```powershell
python .\Tools\ai\build_ai_context_pack.py --repo-root . --profile project_self_improvement
python .\Tools\validation\check_ai_context_pack_contract.py --repo-root . --pack .\output\ai_context_packs\project_self_improvement.json --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\project_self_improvement_context_pack_evidence.json --output .\output\validation\ai_context_pack_contract.json
```

### 2. Prepare repository

For master work:

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git status
git pull --rebase origin master
git status
```

For PR branch work:

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git fetch origin
git checkout <branch>
git pull --ff-only
git status
```

If the working tree is not clean before starting, stop and decide whether to commit, stash, or discard the existing changes.

### 3. Make a focused change

Rules:

```text
small scope
no unrelated formatting
no destructive rewrite of stable Blender packages
no generated full-analysis JSON edits
no runtime package migration without validation
no implicit provider/model execution behavior changes
```

### 4. Run focused validation

For most repository changes:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_docs_links.py --repo-root .
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
```

For NPU/helper/backend changes:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

For quality-based provider routing:

```powershell
python .\Tools\validation\check_ai_workload_report_quality.py --repo-root . --output .\output\validation\ai_workload_report_quality.json
python .\Tools\ai\build_workload_quality_lane_routing.py --repo-root . --output .\output\validation\ai_workload_quality_lane_routing.json --markdown-output .\output\validation\ai_workload_quality_lane_routing.md
python .\Tools\validation\check_npu_decode_quality_remediation.py --repo-root . --output .\output\validation\npu_decode_quality_remediation.json
```

### 5. Run the parallel GPU/NPU multistep workflow

Preferred full workflow for current core AI/backend work:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_parallel_ai_provider_multistep.ps1 `
  -Profile npu `
  -RunOllamaProbe `
  -RunNpuProbe `
  -RunNpuDecodeSmoke `
  -UsePrimaryAdvisoryProvider `
  -Basename parallel_gpu_npu_multistep_real_npu_v2 `
  -ProposalBasename parallel_gpu_npu_multistep_real_npu_v2_proposals `
  -EvidenceBasename parallel_gpu_npu_multistep_real_npu_v2_evidence
```

This workflow performs:

```text
Step 1 -> workload quality gate
Step 2 -> parallel provider probes / NPU decode smoke
Step 3 -> quality-based routing and NPU remediation report
Step 4 -> primary advisory packet/proposals using Ollama/GPU when confirmed
Step 5 -> compact GitHub evidence bundle
```

### 6. Build post-validation AI work packet directly

For a standalone advisory packet after manual tests:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1
```

Explicit primary advisory provider mode:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -UsePrimaryAdvisoryProvider
```

Legacy direct Ollama flag:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -UseOllama
```

Policy:

```text
advisory only
no auto-apply
no source modification
no provider execution unless explicitly requested
```

### 7. Build compact evidence instead of pasting long output

`output/` is ignored by Git. Use evidence bundles for review:

```powershell
python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename latest_ai_workflow_evidence
```

Then push:

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```

### 8. Regenerate indexes when needed

Regenerate after source, docs, workflow, validation or pipeline changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

### 9. Inspect changes

```powershell
git status
git diff --stat
```

If generated indexes changed, commit them intentionally.

### 10. Commit

Use concise commit messages:

```text
docs: update local ai orchestration workflow
feat(ai): add quality-based advisory routing
feat(workflow): add parallel gpu npu multistep runner
test: add real npu smoke evidence bundle
chore: regenerate ai and npu indexes
```

### 11. Push

For master:

```powershell
git push origin master
```

For a PR branch:

```powershell
git push origin <branch>
```

## Execution plans

Execution plans are used for multi-step work that should not live only in chat history.

Location:

```text
docs/EXECUTION_PLANS/
```

States:

```text
active      work currently planned or in progress
completed   work finished and validated
abandoned   work stopped intentionally
```

Folder/status consistency is enforced by:

```powershell
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
```

## AI-agent operating rule

AI agents should not treat conversation history as the only source of truth.

Durable project state should be written into:

```text
docs/
WORKFLOW.md
Tools/validation/
Tools/workflow/
docs/LOCAL_VALIDATION_EVIDENCE/
```

The compact evidence bundle is the preferred local handoff artifact after tests.

## Do not do without explicit approval

```text
delete files
rename the GitHub repository
rewrite Scripting/v61b/main_v61b.py
split Ready To Jazz monolith
change render output behavior
change FFmpeg final-output behavior
add dependencies
modify full frame-level analysis JSON
run heavy Blender/GPU workloads automatically
change schema-v6 report meanings
change NPU/Ollama provider execution behavior from explicit to implicit
```
