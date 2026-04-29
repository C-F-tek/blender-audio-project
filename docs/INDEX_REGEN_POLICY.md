# Index Regeneration Policy

## Purpose

This document defines when the project AI indexes should be considered stale and rebuilt by the project application or by the maintainer's local workflow.

The indexes are part of the AI operating context. When they are stale, AI systems may miss new files, package templates, documentation, workflow rules, or code changes.

## Ownership

Index regeneration is owned by the project application/local workflow, not by GitHub Actions and not by external assistants.

External AI assistants should only:

- detect when indexes may be stale;
- report that regeneration is recommended;
- avoid treating stale indexes as complete truth;
- inspect live repository files directly when needed.

The maintainer or the application performs the actual regeneration.

## Primary index files

The primary generated project indexes are:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
indexAI/project_code_chunks/
```

The project code generator script is:

```text
Tools/npu/build_project_ai_index.py
```

The NPU-focused code context files are:

```text
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
Tools/npu/npu_code_chunks/
```

The NPU context generator script is:

```text
Tools/npu/build_npu_code_context.py
```

If the project application provides its own index-generation process, the application workflow is authoritative.

## When regeneration is required

Regenerate the indexes after changes to any of these areas:

- root Python tools, such as `analyze_wav.py`, `build_track_summary.py`, `normalize_scene_spec.py`;
- any folder under `Scripting/`;
- any folder under `Tools/`;
- any file under `docs/` that affects project rules, workflow, or AI context;
- `AGENTS.md`;
- `README.md`;
- package templates;
- shared utility policies or shared utility code;
- JSON schema documentation;
- validation scripts;
- modular AI artifact pipeline modules under `Tools/ai/pipeline/`.

## When regeneration is optional

Regeneration is usually not required for:

- rendered media files;
- local output folders;
- temporary logs;
- files already excluded by the index generator;
- purely external notes not committed to the repository.

## Recommended pre-regeneration validation

Before committing regenerated indexes after a structural refactor, run:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

For docs-only changes, the AI pipeline matrix can be skipped if no `Tools/ai/` files changed, but it is recommended after the current modular AI pipeline refactor.

## Local/app regeneration

Preferred method:

```text
Run the index regeneration from the project application.
```

Fallback local commands from the repository root:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Force project index rebuild when needed:

```powershell
python .\Tools\npu\build_project_ai_index.py --force
```

## Auto-push after app regeneration

After the application regenerates indexes or technical JSON files, it can automatically commit and push the generated data by calling:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\git\auto_push_generated_artifacts.ps1
```

For a first integration test, use:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\git\auto_push_generated_artifacts.ps1 -DryRun
```

To include full frame-by-frame analysis JSON files explicitly:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\git\auto_push_generated_artifacts.ps1 -IncludeFullAnalysisJson
```

Full analysis JSON files are excluded by default because they may be large and should not be committed accidentally.

## Expected output

The index process may update:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
indexAI/project_code_chunks/
indexAI/README.md
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
Tools/npu/npu_code_chunks/
```

Additional app-generated index files may also be updated depending on the local workflow.

## Git workflow after regeneration

Check state:

```powershell
git status
git diff --stat
```

If only generated AI/NPU indexes changed, commit the standard tracked files:

```powershell
git add Tools/npu/npu_code_context.md `
        Tools/npu/npu_code_index.md `
        Tools/npu/npu_code_manifest.json `
        indexAI/project_code_index.md `
        indexAI/project_code_manifest.json

git commit -m "chore: regenerate ai and npu indexes"
git push origin master
```

If chunk files are tracked and changed, inspect them before adding.

Preferred automated local push when appropriate:

```powershell
.\Tools\git\auto_push_generated_artifacts.ps1
```

## GitHub Actions policy

Do not regenerate app-owned indexes automatically with GitHub Actions unless the maintainer explicitly changes this policy.

Indexes are generated by the app/local workflow because the application may apply project-specific rules, exclusions, metadata, and context formatting that should remain authoritative.

## AI rules

- Before making analysis based on repository structure, check whether `indexAI/project_code_manifest.json` may be stale.
- If new files were created or important files changed, state that app-side index regeneration is recommended.
- Do not regenerate app-owned indexes unless explicitly requested and technically possible in the current environment.
- Do not add automatic GitHub workflows for app-owned indexes unless explicitly requested.
- Do not treat stale indexes as complete project truth.
- Prefer direct file inspection when the index is older than recent repository changes.
- After AI artifact pipeline changes, inspect `docs/AI_PIPELINE_REFACTOR_STATUS.md` before interpreting pipeline state.

## Current policy

Indexes must be rebuilt by the project app/local maintainer workflow whenever structural or workflow-relevant changes are made. After regeneration, the app may call `Tools/git/auto_push_generated_artifacts.ps1` to push generated technical data automatically.

For the current modular AI artifact pipeline refactor, use `docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md` as the operational checklist.
