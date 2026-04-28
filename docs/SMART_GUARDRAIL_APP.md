# Smart Guardrail App

## Purpose

The smart guardrail layer supervises the AI artifact pipeline without directly modifying source code or raw analysis JSON files.

It acts as a lightweight control app around the workflow:

1. review the scripts that produce first-wave WAV artifacts;
2. build or refresh deterministic intermediates;
3. build smart AI context;
4. run the NPU-light guardrail;
5. emit action queues for fixes or enrichment;
6. repeat only auto-safe passes during the same run;
7. keep Python/code corrections as reviewable requests.

## First-wave review

`Tools/ai/review_wave_entrypoints.py` reviews:

- `analyze_wav.py`;
- `build_track_summary.py`.

It emits:

```text
output/ai_pipeline/wave_entrypoint_review.json
```

The report contains:

- score per entrypoint;
- attention flags;
- useful notes;
- future guardrail hints;
- suggested actions;
- remediation requests for future workflow steps.

This does not modify the reviewed files.

## Guardrail remediation requests

`Tools/npu/npu_guardrail_service.py` now emits structured requests, including:

| action_type | Meaning |
|---|---|
| `fix_python_code` | A focused Python/code correction should be requested. Manual review required. |
| `enrich_intermediate_data` | Intermediate JSON should be enriched with metadata useful to downstream AI. |
| `create_compact_summary` | Large artifacts should be summarized before NPU/light review. |
| `rerun_context_selection` | Smart context should be rebuilt with better capsules or task targeting. |
| `multi_pass_review` | A second review pass is recommended. |
| `parameterize_path` | Local paths should be moved to config or marked local-only. |

The queue is written to:

```text
output/ai_pipeline/npu_guardrail_action_queue.json
```

## Multi-pass behavior

`Tools/ai/run_parallel_artifact_pipeline.py` can consume the action queue and repeat only auto-safe stages:

- `enrich_intermediates`;
- `smart_context_generation`;
- `compact_context_generation`;
- `guardrail_second_pass`;
- `wave_entrypoint_review`.

Python/code fixes are intentionally not auto-applied. They remain reviewable requests.

## Recommended command

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py `
  --repo-root . `
  --analysis-json .\output\Feel_The_Light_analysis.json `
  --track-stem "Feel The Light" `
  --review-wave-entrypoints `
  --build-music-summary `
  --build-chunks `
  --smart-context `
  --npu-guardrail `
  --guardrail-auto-remediate `
  --guardrail-max-passes 2 `
  --validate
```

## Safety model

- Raw WAV-derived analysis JSON remains read-only.
- First-wave script review is diagnostic only.
- NPU guardrail is soft-fail by default.
- Auto-remediation only reruns deterministic or context-building steps.
- Code changes require review and an explicit patch step.
