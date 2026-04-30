# Generated Python Policy Layer

## Status

completed

## Goal

Add a generic generated Python policy layer that improves AI guardrails without tying policy to Blender, audio or any single input/output workflow.

## Scope

- Add reusable generated Python syntax and hazard checks.
- Add a CLI validator with deterministic in-memory samples.
- Compose the Blender generated-script validator on top of the generic Python layer.
- Include the new validator in local validation workflow and AI-friendly docs.
- Regenerate AI/NPU indexes after structural and documentation changes.

## Out of scope

- No Blender runtime package changes.
- No migration of `Scripting/shared/blender_compat.py` into packages.
- No generated analysis JSON rewrites.
- No external dependency, database or CI workflow addition.

## Files likely touched

```text
AGENTS.md
Tools/validation/generated_python_policy.py
Tools/validation/check_generated_python_policy.py
Tools/validation/check_generated_blender_script_policy.py
Tools/validation/README.md
Tools/workflow/run_local_validation_after_refactor.ps1
docs/AI_SMART_POLICY.md
docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
docs/MODULE_MAP.md
docs/PROJECT_AI_CONSCIOUSNESS.md
docs/QUALITY_GATE.md
indexAI/project_code_index.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

## Validation commands

```powershell
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## Risk level

low

## Progress log

- 2026-04-30: Added generic generated Python policy samples and composed Blender adapter over the generic layer.
- 2026-04-30: Focused generated Python, Blender adapter and syntax validations passed locally.
- 2026-04-30: Full local runner passed with the new generated Python policy step, dry-run matrix, docs links, JSON/package validation and AI/NPU index regeneration.

## Result

completed. Generic generated Python policy now sits between the generic generated-file policy engine and application-specific adapters.

## Follow-up

Use the generated Python policy as the base for future application adapters, keeping input-domain checks separate.
