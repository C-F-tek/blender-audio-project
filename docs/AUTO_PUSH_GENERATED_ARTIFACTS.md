# Auto Push Generated Artifacts

## Purpose

This document explains how the local application can automatically push regenerated technical artifacts to GitHub.

The application remains responsible for generating indexes, JSON summaries, AI context files, manifests, and technical notes. GitHub does not regenerate them.

After generation, the app can call:

```text
python -m Tools.git auto_push_generated_artifacts
```

The script stages selected generated-artifact paths, creates a commit only if changes exist, and pushes the current branch.

## Script path

```text
python -m Tools.git auto_push_generated_artifacts
```

## Basic usage

From the repository root:

```powershell
python -m Tools.git auto_push_generated_artifacts
```

With explicit path:

```powershell
python -m Tools.git auto_push_generated_artifacts -RepoPath "C:\Users\carmi\blender\blender-audio-project"
```

With custom message:

```powershell
python -m Tools.git auto_push_generated_artifacts -Message "chore: update app-generated indexes and contexts"
```

Dry run:

```powershell
python -m Tools.git auto_push_generated_artifacts -DryRun
```

Commit without push:

```powershell
python -m Tools.git auto_push_generated_artifacts -NoPush
```

## Default staged paths

By default, the script stages:

```text
indexAI
output/*_track_summary.json
output/*_music_context.json
output/*_analysis_ai_context.json
output/*_dual_ai_scene_plan.json
output/*_ai_implementation_draft.json
Tools/npu/npu_preflight_report.json
```

## Full analysis JSON policy

Full frame-by-frame analysis JSON files are excluded by default because they may be large and should not be overwritten or committed accidentally.

To include them explicitly:

```powershell
python -m Tools.git auto_push_generated_artifacts -IncludeFullAnalysisJson
```

This adds:

```text
output/*_analysis.json
output/*_analysis_blender_keyframes.json
```

## App integration pattern

Recommended app flow:

```text
1. Regenerate technical artifacts from the app.
2. Validate generated files.
3. Call `python -m Tools.git auto_push_generated_artifacts`.
4. Review GitHub commit if needed.
```

Example from PowerShell:

```powershell
# App regeneration step here
# App-owned regeneration command goes here; no tracked repository script is implied.

python -m Tools.git auto_push_generated_artifacts `
  -RepoPath "C:\Users\carmi\blender\blender-audio-project" `
  -Message "chore: update generated AI indexes and technical context"
```

## Safety behavior

The script:

- does not regenerate indexes;
- does not touch working Blender scripts unless they are explicitly passed in `-Paths`;
- does not commit if there are no staged changes;
- excludes full analysis JSON by default;
- pushes to the existing upstream branch when configured;
- sets upstream to `origin/current-branch` if missing.

## Custom paths

The app can pass a custom set of paths:

```powershell
python -m Tools.git auto_push_generated_artifacts `
  -Paths @("indexAI", "output/*_track_summary.json")
```

## AI rule

External AI assistants should not regenerate app-owned indexes automatically. They may add or improve this push script, but actual index generation remains controlled by the app/local workflow.
