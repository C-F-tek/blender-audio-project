<!-- IA-CARMINE-MD-SPLIT: part -->
# full-toolbox-0-to-10-semi-automatic-procedure — parte 004 di 004

Sorgente indice: [`../full-toolbox-0-to-10-semi-automatic-procedure.md`](../full-toolbox-0-to-10-semi-automatic-procedure.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-003.md)

## Variant E - Evidence-only commit

After a full toolbox run, commit only compact Git-trackable evidence when useful:

```powershell
git add `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_python_line_count_$Stamp.csv" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_$Stamp.md"

git diff --cached --name-only
```

Must not include:

```text
output/**
*.db
*.sqlite
renders/**
```

## CLI merge commands

Ready PR:

```powershell
gh pr ready <PR_NUMBER> --repo C-F-tek/blender-audio-project
```

Squash merge with head protection:

```powershell
gh pr merge <PR_NUMBER> `
  --repo C-F-tek/blender-audio-project `
  --squash `
  --match-head-commit <HEAD_SHA> `
  --subject "<subject>" `
  --body "<body>"
```

Refresh master after merge:

```powershell
git switch master
git pull --ff-only origin master
git log --oneline -5
git status --short
```

## Final decision rules

Proceed when:

```text
validation reports passed
fatal_report_failure_count=0 when warning policy is used
patch_plan_count >= 1 when implementation is expected
bundle dry-run passed before apply
apply is explicit
post-apply git diff --check passed
status contains only intended source/docs changes
```

Stop when:

```text
syntax validation fails
validation contract fails
bundle builder has operation_count=0 unexpectedly
bundle runner reports errors
SQLite/persistent memory write is true without explicit memory PR
provider execution happened in a no-provider path
output/** appears in staged files
```

### Blender manual corpus default exclusion

The Blender manual generated corpus is not part of the default IA-Carmine full-toolbox/provider context.

Deleted/default-excluded corpus:

```text
Tools/npu/npu_blender_manual_chunks/**
Tools/npu/npu_blender_manual_index.md
Tools/npu/npu_blender_manual_manifest.json

Rationale:

Full-toolbox/provider runs must prioritize Tools/ai, Tools/validation, Tools/workflow,
runtime tool telemetry, repository consistency evidence, recommendations, patch plans,
memory inventory and tool capability manifests.

Blender manual chunks are large reference material and can dominate prompt/context
selection, reducing provider/toolbox signal quality.

Allowed use:

Regenerate/include Blender manual chunks only for Blender/API/manual-focused runs.
Do not include them in IA-Carmine provider/toolbox cloud handoff by default.
### GPU provider error hardening gate

Before trusting any long full-toolbox provider-backed run, the GPU supervised runner must pass the provider-error smoke.

Required validation:

```powershell
python -m py_compile .\Tools\ai\run_agent_gpu_deep_planning_supervised.py `
  .\Tools\validation\run_gpu_runner_provider_error_smoke.py

python .\Tools\validation\run_gpu_runner_provider_error_smoke.py `
  --repo-root . `
  --output .\output\validation\gpu_runner_provider_error_smoke.json `
  --markdown-output .\output\validation\gpu_runner_provider_error_smoke.md
```

The runner must serialize provider exceptions or empty responses as report data. It must never fail a planning round with `UnboundLocalError` for `raw_response`. Schema repair retry is allowed only when a non-empty provider response exists.

## Diagnostics and telemetry bundle invariants

Full-toolbox AI-to-AI handoff chunks must be deterministic by default.

Required semantic chunk policy:

```text
basename: full_toolbox_<STAMP>_cloud_semantic_deterministic
ollama: disabled
required flag: --no-ollama
```

Reason:

```text
Ollama summaries may be empty, truncated or stale. They are useful only as secondary verification, not as the primary cloud handoff source.
```

Repository consistency must not promote generated semantic chunk files into primary patch planning.

Generated evidence chunk paths such as:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*_cloud_semantic_chunks/**
docs/LOCAL_VALIDATION_EVIDENCE/*_cloud_semantic_deterministic_chunks/**
docs/LOCAL_VALIDATION_EVIDENCE/*_chunks/**
```

must be excluded from repository consistency findings or kept out of high-signal patch planning.

Runtime tool telemetry must distinguish:

```text
declared runtime tool requests
broker-executed tool calls
declared-but-not-executed requests
```

A GPU planner may declare tool requests without broker execution. That state is valid telemetry and must not appear as a missing or empty telemetry channel.

### Recursive AI packets root selection

The workload-quality gate accepts both:

```text
output/ai_packets
output/ai_packets/<DataStamp>
```

When the root folder is passed, every immediate timestamp folder under `output/ai_packets` is inspected. Only concrete workload report files are selected; packet directories are never passed as context files.


### Launcher directory variable contract

The root launcher reference `FULL_RUN_UNICA_TUTTO_SU_TUTTO.md` is the canonical executable reference for full-run variables.

Directory naming rule:

- PowerShell variable: `$OutputDir`
- Launcher parameter: `-OutputDir`
- Python directory argument: `--output-dir`
- Compact evidence variable/parameter: `$EvidenceDir` / `-EvidenceDir`

The full run must preserve the `TUTTO SU TUTTO` policy while keeping runtime output, compact evidence and AI packets explicitly separated.

### Production AI-to-AI communication bundle

For a completed full run, the standard production communication artifact is not only the decision-loop evidence.

The canonical AI-to-AI handoff is:

    docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md

This pair is the first bundle to send to the next AI/chat/operator session when continuing work from a completed local run.

The production communication set also includes:

    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.md
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.md
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.md
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_<STAMP>_cloud_semantic_deterministic_chunk_manifest.json
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_<STAMP>_cloud_semantic_deterministic_chunk_manifest.md

Decision-loop evidence remains required but partial:

    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_<STAMP>.json
    docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_<STAMP>.md

Operational rule:

    one completed full run -> one shared toolbox AI-to-AI bundle -> one telemetry/capability/chunk-manifest set -> optional evidence commit.

When the user asks to push telemetry/evidence after a full run, stage only files under docs/LOCAL_VALIDATION_EVIDENCE that match the run stamp and belong to this production communication set. Do not stage output/**.

### Full-run provider/bundle/broker acceptance

After a completed full run, inspect the production bundle and telemetry for these acceptance criteria:

    shared_toolbox_ai_to_ai_bundle_<STAMP>.md:
      patch_plan_summary_seen: True

    shared_toolbox_ai_to_ai_final_summary_<STAMP>.json:
      provider_diagnostics.provider_execution_seen: True
      provider_diagnostics.gpu_primary_advisory_succeeded: True or explicit recovered failure
      provider_diagnostics.deterministic_recovery_used: True when GPU/Ollama failed

    runtime_tool_usage_telemetry_<STAMP>.json:
      summary.tool_call_entry_count >= 3
      summary.executed_count >= 3
      summary.failed_count = 0
      summary.blocked_count = 0

Minimal broker bootstrap tools:

    check_python_syntax
    build_python_line_count_csv
    check_validation_report_contract

If GPU/Ollama primary advisory fails, the run may still pass by deterministic recovery, but the production bundle must expose the recovered provider failure explicitly.
