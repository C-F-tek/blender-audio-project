---
applyTo: "Tools/ai/**/*.py,Tools/npu/**/*.py,indexAI/**/*.md,indexAI/**/*.json,docs/*AI*,docs/*NPU*"
---

# AI/NPU Pipeline Instructions

Use these rules when editing AI artifact generation, local NPU/GPU workflow, project indexing, smart context, validators, or generated AI context documentation.

## Core model

The AI pipeline is additive. It should support the Blender workflow without replacing stable runtime packages.

Preferred lanes:

```text
CPU -> parsing, compact context, deterministic validation
NPU -> short review, warning detection, scoring, guardrails
GPU -> optional heavy generation or planning
```

## Editing rules

- Do not rewrite full analysis JSON files.
- Do not treat `indexAI/` as primary hand-edited source unless the file is explicitly curated.
- Preserve deterministic fallback behavior.
- Keep provider/runtime code separate from prompts.
- Keep prompt construction separate from validators.
- Keep artifact writers separate from pipeline orchestration.
- Keep generated context compact and traceable to source files.
- Record assumptions in generated reports or notes.

## Preferred future split

Large AI/NPU orchestrators should move toward:

```text
Tools/npu/pipeline/config.py
Tools/npu/pipeline/context_builder.py
Tools/npu/pipeline/prompts.py
Tools/npu/pipeline/providers.py
Tools/npu/pipeline/validators.py
Tools/npu/pipeline/artifact_writer.py
Tools/npu/pipeline/runner.py
```

Preserve current CLI behavior while splitting.

## Index regeneration

After structural or documentation changes, regenerate indexes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## Validation

Use:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

AI artifact dry run:

```powershell
python .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate --dry-run --write-dry-run-report
```
