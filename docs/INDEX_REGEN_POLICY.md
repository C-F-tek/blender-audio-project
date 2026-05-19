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
python -m Tools.npu build_project_ai_index
```

The NPU-focused code context files are:

```text
Tools/npu/context_artifacts/npu_code_context.md        # generated, ignored
Tools/npu/context_artifacts/npu_code_index.md          # generated, ignored
Tools/npu/context_artifacts/npu_code_manifest.json     # generated, ignored
Tools/npu/npu_code_chunks/
```

The NPU context generator script is:

```text
python -m Tools.npu build_npu_code_context
```

If the project application provides its own index-generation process, the application workflow is authoritative.

## When regeneration is required

Regenerate the indexes after changes to any of these areas:

- audio/scene workflow tools, such as `Tools/workflow/workflow_run/audio_analysis/analyze_cli.py`, `Tools/workflow/workflow_run/audio_analysis/summary_cli.py`, `Tools/workflow/workflow_run/scene_spec/cli.py`;
- any folder under `Scripting/`;
- any folder under `Tools/`;
- `Tools/npu/pipeline/` helper package modules or README;
- `Tools/validation/` validators;
- `Tools/workflow/` local runners;
- any file under `docs/` that affects project rules, workflow, or AI context;
- `AGENTS.md`;
- `README.md`;
- package templates;
- shared utility policies or shared utility code;
- JSON schema documentation;
- modular AI artifact pipeline modules under `Tools/ai/pipeline/`.

## When regeneration is optional

Regeneration is usually not required for:

- rendered media files;
- local output folders;
- temporary logs;
- files already excluded by the index generator;
- purely external notes not committed to the repository.

## Recommended pre-regeneration validation

Before committing regenerated indexes after a structural refactor, run the smallest relevant focused validation first.

For NPU helper package changes:

```powershell
python -m Tools.validation check_npu_pipeline_helper_tests --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
```

For broader source or workflow changes:

```powershell
python -m Tools.validation check_python_syntax --repo-root .
python -m Tools.validation check_ai_pipeline_modules --repo-root . --output .\output\validation\ai_pipeline_modules.json
python -m Tools.validation npu_pipeline_modules_check --repo-root . --output .\output\validation\npu_pipeline_modules.json
python -m Tools.validation check_npu_pipeline_helper_tests --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python -m Tools.validation check_npu_pipeline_docs --repo-root . --output .\output\validation\npu_pipeline_docs.json
python -m Tools.ai pipeline_dry_run_matrix --repo-root . --continue-on-error
python -m Tools.validation check_package_structure --repo-root .
python -m Tools.validation check_json_artifacts --repo-root .
```

For docs-only changes, the AI pipeline matrix can be skipped if no `Tools/ai/` files changed, but run documentation link checks when local execution is available:

```powershell
python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links.json
```

## Local/app regeneration

Preferred method:

```text
Run the index regeneration from the project application.
```

Fallback local commands from the repository root:

```powershell
python -m Tools.npu build_project_ai_index
python -m Tools.npu build_npu_code_context
```

Force project index rebuild when needed:

```powershell
python -m Tools.npu build_project_ai_index --force
```

## Auto-push after app regeneration

After the application regenerates indexes or technical JSON files, it can automatically commit and push the generated data by calling:

```powershell
python -m Tools.git auto_push_generated_artifacts
```

For a first integration test, use:

```powershell
python -m Tools.git auto_push_generated_artifacts -DryRun
```

To include full frame-by-frame analysis JSON files explicitly:

```powershell
python -m Tools.git auto_push_generated_artifacts -IncludeFullAnalysisJson
```

Full analysis JSON files are excluded by default because they may be large and should not be committed accidentally.

## Expected output

The index process may update:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
indexAI/project_code_chunks/
indexAI/README.md
Tools/npu/context_artifacts/npu_code_context.md        # generated, ignored
Tools/npu/context_artifacts/npu_code_index.md          # generated, ignored
Tools/npu/context_artifacts/npu_code_manifest.json     # generated, ignored
Tools/npu/npu_code_chunks/
```

Additional app-generated index files may also be updated depending on the local workflow.

## Git workflow after regeneration

Check state:

```powershell
git status
git diff --stat
```

If only generated AI indexes changed, commit the standard tracked files. NPU
`Tools/npu/context_artifacts/` outputs are generated local context and are
ignored by Git.

```powershell
git add indexAI/project_code_index.md `
        indexAI/project_code_manifest.json

git commit -m "chore: regenerate ai and npu indexes"
```

For a PR branch:

```powershell
git push origin <branch>
```

For master:

```powershell
git push origin master
```

If chunk files are tracked and changed, inspect them before adding.

Preferred automated local push when appropriate:

```powershell
python -m Tools.git auto_push_generated_artifacts
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
- After NPU helper package changes, inspect `Tools/npu/pipeline/README.md` and run focused NPU helper validation before runtime wiring.

## Current policy

Indexes must be rebuilt by the project app/local maintainer workflow whenever structural or workflow-relevant changes are made. After regeneration, the app may call `python -m Tools.git auto_push_generated_artifacts` to push generated technical data automatically.

For the current modular AI artifact pipeline and NPU helper package work, use `docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md` as the operational checklist.
