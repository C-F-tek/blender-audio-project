# Index Regeneration Policy

## Purpose

This document defines when and how the project AI indexes must be regenerated.

The indexes are part of the AI operating context. When they are stale, AI systems may miss new files, package templates, documentation, workflow rules, or code changes.

## Primary index files

The primary generated project indexes are:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
indexAI/project_code_chunks/
```

The generator is:

```text
Tools/npu/build_project_ai_index.py
```

## When regeneration is required

Regenerate the indexes after changes to any of these areas:

- root Python tools, such as `analyze_wav.py`, `build_track_summary.py`, `normalize_scene_spec.py`;
- any folder under `Scripting/`;
- any folder under `Tools/`;
- any file under `docs/` that affects project rules, workflow, or AI context;
- `AGENTS.md`;
- `README.md`;
- `.github/workflows/`;
- package templates;
- shared utility policies or shared utility code;
- JSON schema documentation;
- validation scripts.

## When regeneration is optional

Regeneration is usually not required for:

- rendered media files;
- local output folders;
- temporary logs;
- files already excluded by the index generator;
- purely external notes not committed to the repository.

## Manual command

From the repository root:

```powershell
python .\Tools\npu\build_project_ai_index.py --force
```

or with the Python executable used by the project:

```powershell
py .\Tools\npu\build_project_ai_index.py --force
```

## Expected output

The command should update:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
indexAI/project_code_chunks/
indexAI/README.md
```

## Git workflow

After regeneration:

```powershell
git status
git add indexAI/project_code_index.md indexAI/project_code_manifest.json indexAI/project_code_chunks indexAI/README.md
git commit -m "chore: regenerate project AI indexes"
git push
```

## Automated workflow

A GitHub Actions workflow may regenerate the primary indexes automatically when relevant files change. If the workflow is unavailable or fails, run the manual command locally.

## AI rules

- Before making analysis based on repository structure, check whether `indexAI/project_code_manifest.json` is stale.
- If new files were created or important files changed, request or perform index regeneration.
- Do not treat stale indexes as complete project truth.
- Prefer direct file inspection when the index is older than recent repository changes.
- If index regeneration cannot be executed by the current environment, document that limitation and provide the exact local command.

## Current policy

Indexes must be rebuilt whenever structural or workflow-relevant changes are made.
