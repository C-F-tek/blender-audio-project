# Local Validation Evidence Bundle

- Generated at: `2026-05-02T20:53:16`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `False`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `3`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/analysis/gpu_npu_run_sync_20260502-195523.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Artifact manifest

- `output/analysis/gpu_npu_run_sync_20260502-195523.json` exists=`True` size=`2309` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/analysis/gpu_npu_run_sync_20260502-195523.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1277`
- SHA-256: `46dbb4d2ef797fad17d4d5fc827978bb2f35477aa562b8ce5afc8eddba26d75f`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `0`
- `npu_audit_count`: `5`
- `npu_audit_success_count`: `5`
- `npu_audit_round_coverage`: `0.0`
- `avg_gpu_round_seconds`: `0.0`
- `p50_gpu_round_seconds`: `0.0`
- `p90_gpu_round_seconds`: `0.0`
- `avg_npu_audit_seconds`: `124.8`
- `p50_npu_audit_seconds`: `122.0`
- `p90_npu_audit_seconds`: `130.0`
- `npu_to_gpu_avg_duration_ratio`: `0.0`
- `gpu_elapsed_seconds`: `706.195`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`

## Suggested balanced profile

- `npu_auditor_every_rounds`: `4`
- `max_concurrent_npu_audits`: `1`
- `npu_auditor_timeout_seconds`: `420`
- `npu_max_context_chars`: `8000`
- `npu_max_prompt_chars`: `1200`
- `npu_max_new_tokens`: `384`
- `npu_final_wait_seconds`: `180`
- `gpu_max_new_tokens`: `3600`
- `gpu_files_per_round`: `8`
- `gpu_max_chars_per_file`: `6000`

## Reasoning

- NPU audits are usable; tune cadence rather than disabling the lane.
- GPU JSON contract hardening should be tested before increasing GPU token budget further.


```

### `docs/LOCAL_AI_TASKS/gpu-npu-balanced-run-profile.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3594`
- SHA-256: `f50b4a7456e6d48a7a3512b79c3cf1ad0664dfbc01f187119d4fc57ed9f16247`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Balanced Run Profile

## Purpose

Balanced profile proposal for complete local AI-to-AI runs when the GPU planner advances much faster than the NPU checkpoint auditor.

The goal is not perfect lockstep. The goal is useful NPU checkpoint coverage without blocking GPU progress or leaving NPU audits too stale.

## Reference run observation

Reference run:

```text
project_complete_20260502-195523
```

Observed behavior:

```text
GPU planner completed 24 rounds
NPU checkpoint auditor completed 5 audits
NPU audits succeeded
GPU output still ended with repair_attempt_failed
```

Interpretation:

```text
NPU is useful as a sampled checkpoint auditor, not as a per-round synchronous reviewer.
```

## Baseline complete-run parameters

Previous project-complete run used:

```text
--budget-minutes 30
--max-rounds 24
--files-per-round 10
--max-context-files 240
--max-chars-per-file 8000
--max-new-tokens 4800
--npu-auditor-every-rounds 4
--max-concurrent-npu-audits 1
--npu-auditor-timeout-seconds 600
--npu-max-context-chars 12000
--npu-max-prompt-chars 1500
--npu-max-new-tokens 512
--npu-final-wait-seconds 120
```

## Balanced profile candidate

Use this profile for the next comparative complete run after JSON-contract integration is available:

```text
--budget-minutes 30
--max-rounds 20
--files-per-round 8
--max-context-files 220
--max-chars-per-file 6000
--max-new-tokens 3600
--npu-auditor-every-rounds 3
--max-concurrent-npu-audits 1
--npu-auditor-timeout-seconds 420
--npu-max-context-chars 8000
--npu-max-prompt-chars 1200
--npu-max-new-tokens 384
--npu-final-wait-seconds 180
```

## Rationale

GPU-side changes:

```text
slightly smaller file batches
slightly smaller per-file context
lower max-new-tokens than 4800
fewer max rounds
```

Expected effect:

```text
less prompt echo pressure
less malformed long JSON
more compact GPU responses
less runaway round count
```

NPU-side changes:

```text
smaller context budget
smaller prompt budget
smaller decode budget
shorter per-audit timeout
longer final wait
```

Expected effect:

```text
faster NPU checkpoint completion
less chance that final NPU audits are still draining after GPU completion
better end-of-run audit inclusion
```

Cadence:

```text
npu-auditor-every-rounds 3
```

Expected effect:

```text
more frequent checkpoint coverage than every 4 rounds, while still avoiding per-round lockstep.
```

## Guardrails

```text
NPU remains non-blocking
NPU remains checkpoint/audit/support lane
NPU is not promoted to primary advisory
OpenVINO GPU is not used as primary lane
no provider/model setting changes first
no patch auto-apply
no source writes through patch runner
no Blender runtime execution
raw output/** remains local only
compact bundle remains required
```

## Required analysis tool

Use:

```powershell
python .\Tools\ai\analyze_gpu_npu_run_sync.py `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_<STAMP>_orchestrator.json" `
  --output ".\output\analysis\gpu_npu_run_sync_<STAMP>.json" `
  --markdown-output ".\output\analysis\gpu_npu_run_sync_<STAMP>.md"
```

The sync analysis report must be included in the evidence bundle for any future complete run that changes GPU/NPU cadence parameters.

## Success criteria

A balanced run is better if:

```text
GPU JSON contract failures decrease
context_echo_detected is separated from raw parse failure
NPU audit success remains true
NPU audit coverage improves or remains useful
final bundle includes NPU audit evidence and sync analysis
fallback patch-plan remains available when GPU recommendations are empty
```

```

### `output/ai_pipeline/project_complete_20260502-195523_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `20138`
- SHA-256: `fdf74c5801328d125e3d5d7bbb422b25f0ebb4327d487b85648685e7fc59a3e9`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-02T20:09:33",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 706.195,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 668.685,\n  \"round_count\": 24,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"empty_recommendations_reason\": \"repair_attempt_failed\",\n  \"evidence_ready_for_manual_patch_count\": 12,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "repair_attempt_failed",
  "gpu_evidence_ready_for_manual_patch_count": 12,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "gpu_summary": {
    "passed": true,
    "round_count": 24,
    "recommendation_count": 0,
    "raw_recommendation_candidate_count": 0,
    "filtered_recommendation_count": 0,
    "json_parse_error_count": 16,
    "repair_attempt_count": 18,
    "empty_recommendations_reason": "repair_attempt_failed",
    "evidence_ready_for_manual_patch_count": 12,
    "recommended_next_layer": "build_agent_review_patch_plan.py",
    "decision": {
      "ready_for_patch_plan": false,
      "ready_count": 0,
      "needs_more_context_count": 0,
      "fallback_patch_plan_recommended": true,
      "npu_auditor_non_blocking": true,
      "npu_unusable_or_failed_count": 0,
      "npu_audit_success_count": 0,
      "npu_auditor_disabled_reason": "",
      "recommended_next_layer": "build_agent_review_patch_plan.py",
      "manual_review_required": true
    }
  },
  "checkpoint_dir": "output/ai_pipeline/project_complete_20260502-195523_checkpoints",
  "npu_audit_count": 5,
  "npu_audit_success_count": 5,
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-02T19:58:59",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "600",
        "--max-context-chars",
        "4000",
        "--max-prompt-chars",
        "1500",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-02T20:01:07",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "gpu_review_blocked": false
    },
    {
      "round": 4,
      "checkpoint": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_004.json",
      "audit_output": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_004_npu_async_audit.json",
      "started_at": "2026-05-02T20:01:09",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "600",
        "--max-context-chars",
        "4000",
        "--max-prompt-chars",
        "1500",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-02T20:03:19",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_004_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_004_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "gpu_review_blocked": false
    },
    {
      "round": 8,
      "checkpoint": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_008.json",
      "audit_output": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_008_npu_async_audit.json",
      "started_at": "2026-05-02T20:03:21",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "600",
        "--max-context-chars",
        "4000",
        "--max-prompt-chars",
        "1500",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-02T20:05:23",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_008_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_008_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": tru
```

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
