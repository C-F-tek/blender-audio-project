# AI Pipeline Refactor Status

## Status

```text
modular_schedule_complete_pending_local_validation
```

This file is a stable status marker for human maintainers and AI agents.

The AI artifact pipeline has been modularized. The public CLI and schema-v6 report are intended to remain compatible, but local dry-run validation is still required after pulling the latest commits.

## Do not misinterpret this state

The modular split is not an abandoned half-refactor.

Current meaning:

```text
architecture split: complete
schema compatibility intent: preserved
local dry-run matrix: pending on workstation
AI/NPU index regeneration: required after validation
Blender runtime changes: not part of this refactor
```

## Machine-readable status

The Python status marker is:

```text
Tools/ai/pipeline/refactor_status.py
```

Use:

```python
from Tools.ai.pipeline.refactor_status import get_pipeline_refactor_status

status = get_pipeline_refactor_status()
```

## Required local validation

Run from repository root:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

Then regenerate indexes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Commit only generated index files when appropriate:

```powershell
git add Tools/npu/npu_code_context.md `
        Tools/npu/npu_code_index.md `
        Tools/npu/npu_code_manifest.json `
        indexAI/project_code_index.md `
        indexAI/project_code_manifest.json

git commit -m "chore: regenerate ai and npu indexes"
git push origin master
```

## Files changed by this refactor family

Primary entrypoint:

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
```

Documentation:

```text
docs/AI_PIPELINE_ARCHITECTURE.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
```

## Next safe actions

After local dry-run validation passes:

```text
1. regenerate AI/NPU indexes
2. commit generated index files
3. inspect dry-run matrix summary/schedule fields
4. continue with Markdown dry-run report output or richer lane policy
```
