# AI Pipeline Refactor Status

## Status

```text
modular_schedule_complete_subordinate_to_unified_launcher
```

This file is a stable status marker for human maintainers and AI agents.

The AI artifact pipeline has been modularized. The public CLI and schema-v6 report are intended to remain compatible, but the pipeline is now a subordinate implementation lane inside the wider unified local-AI workflow.

## Current interpretation

The modular split is not an abandoned half-refactor.

Current meaning:

```text
architecture split: complete
schema compatibility intent: preserved
direct dry-run matrix: focused validation only
Full0To10 proof: requires unified launcher evidence plus telemetry/capability handoff
file-line evidence: required when pipeline maintainability is in scope
AI/NPU index regeneration: local-only follow-up when explicitly required
Blender runtime changes: not part of this refactor
```

A dry-run matrix is not a full run. It proves planned/dry-run pipeline behavior only. It does not prove provider execution, runtime broker execution, capability availability, patch application state or source-write state.

## Machine-readable status

The Python status marker is:

```text
Tools/ai/pipeline/refactor_status.py
```

Use from code when needed:

```python
from Tools.ai.pipeline.refactor_status import get_pipeline_refactor_status

status = get_pipeline_refactor_status()
```

## Validation ownership

Current broad command examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Focused validator references are allowed, but large validator catalogs are not first operational entrypoints.

Broad local-AI validation should route through the unified launcher. Focused direct validation is appropriate only when changing or debugging the AI artifact pipeline itself.

Local validation should report:

```text
launcher mode/profile/flags when launcher was used
pipeline dry-run report path when focused pipeline validation was used
manifest path when launcher was used
phase_status / phase_reports when launcher was used
whether telemetry/capability/final-summary surfaces were produced
whether file-line-limit evidence was produced when maintainability is in scope
whether provider execution occurred
whether patch application occurred
whether source writes occurred
```

## Full-run evidence requirement

If this refactor status contributes to recommendations, patch plans or patch specs in a full-run context, the handoff must include:

```text
pipeline report or compact evidence
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
file-line-limit report when maintainability is in scope
```

Telemetry is the completeness accessory. It does not replace the pipeline report; it explains whether the related lanes executed, failed, were blocked, degraded, disabled or planned-only.

## 400-line policy

Maintained pipeline source and documentation follow the hard 400-line policy.

```text
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Validator:

```text
Tools/validation/check_file_line_limits.py
```

## Files changed by this refactor family

Primary focused entrypoint:

```text
Tools/ai/run_parallel_artifact_pipeline.py
```

Modular implementation:

```text
Tools/ai/pipeline/defaults.py
Tools/ai/pipeline/models.py
Tools/ai/pipeline/runner.py
Tools/ai/pipeline/compat.py
Tools/ai/pipeline/artifact_contracts.py
Tools/ai/pipeline/cli.py
Tools/ai/pipeline/preflight.py
Tools/ai/pipeline/steps.py
Tools/ai/pipeline/scheduler.py
Tools/ai/pipeline/orchestrator.py
Tools/ai/pipeline/schema_report.py
Tools/ai/pipeline/guardrail_models.py
Tools/ai/pipeline/remediation.py
Tools/ai/pipeline/refactor_status.py
```

Validation helpers:

```text
Tools/validation/check_ai_pipeline_modules.py
Tools/ai/run_pipeline_dry_run_matrix.py
Tools/validation/check_file_line_limits.py
```

Documentation:

```text
docs/AI_PIPELINE_ARCHITECTURE.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```

## Safe next actions

```text
1. Validate focused pipeline behavior locally only when the pipeline changes.
2. Use the unified launcher for broad local-AI validation.
3. Keep dry-run matrix evidence clearly marked as planned-only.
4. Include file-line evidence when maintainability is in scope.
5. Regenerate AI/NPU indexes only when a scoped local task requires it.
6. Do not commit output/**, SQLite DBs or raw local reports.
7. Do not push to master or merge from this status document.
8. Continue richer lane policy only after manifest, report and telemetry surfaces are clear.
```

## Guardrails

Do not infer from this status marker that it is safe to:

```text
run providers implicitly
run Blender or FFmpeg
apply patches automatically
queue patch specs for GitHub Action automatically
commit generated indexes without explicit validation context
push to master
merge to protected branches
claim Full0To10 success from dry-run matrix alone
skip file-line evidence when maintainability is in scope
```
