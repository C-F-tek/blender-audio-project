# AI Prompt Templates

## Purpose

This file provides reusable prompts for AI assistants working on this repository.

Use these prompts with the repository context from:

- `AGENTS.md`
- `docs/AI_REPOSITORY_MANIFEST.md`
- `indexAI/ai_manifest.json`
- `docs/QUALITY_GATE.md`

## General rules for every prompt

The assistant must:

1. inspect target files before editing;
2. avoid destructive rewrites unless explicitly requested;
3. keep paths configurable;
4. preserve generated analysis JSON files;
5. mark unverified assumptions as `not specified`;
6. report changed files, tests, risks, and line counts for scripts.

## Prompt: repository technical audit

```text
You are reviewing the blender-audio-project repository.

Read AGENTS.md, README.md, docs/README.md, docs/MODULE_MAP.md, docs/DATA_FLOW.md, docs/QUALITY_GATE.md, and docs/AI_REPOSITORY_MANIFEST.md.

Task:
- identify inconsistencies between documentation and code;
- identify missing or stale developer documentation;
- identify Blender compatibility risks;
- identify AI workflow risks;
- propose focused patches only.

Output:
- summary;
- findings grouped by severity;
- affected files;
- proposed patch plan;
- tests to run;
- assumptions marked as not specified when unverified.
```

## Prompt: Blender compatibility patch

```text
You are patching Blender Python compatibility in blender-audio-project.

Read the target script completely before editing.

Task:
- identify Blender API calls or node types that may be removed or renamed;
- patch the smallest safe area;
- preserve existing visual intent;
- add compatibility comments only where useful.

Constraints:
- do not rewrite unrelated functions;
- keep local paths configurable;
- do not delete generated data;
- report resulting line count for modified scripts.

Output:
- changed files;
- compatibility issue fixed;
- Blender version tested or not specified;
- tests performed;
- risks.
```

## Prompt: generate a new audio-reactive package

```text
You are creating a new Blender audio-reactive package.

Read:
- AGENTS.md
- docs/AI_GENERATED_PACKAGE_STANDARD.md
- docs/PACKAGE_CREATION_WORKFLOW.md
- docs/QUALITY_GATE.md
- Scripting/_template_audio_reactive_package/README.md

Input:
- audio analysis JSON path;
- compact track summary path;
- music context path, if available;
- visual concept;
- target package folder.

Task:
- create a new package by following the template structure;
- keep paths configurable;
- add audio strip loading when a WAV path is provided;
- map low/mid/high/onset/beat features to scene behavior;
- avoid destructive changes to existing packages.

Output:
- created files;
- resulting line count for scripts;
- scene design summary;
- configuration values;
- validation checklist;
- untested areas.
```

## Prompt: review an AI implementation draft

```text
You are reviewing an AI-generated implementation draft for blender-audio-project.

Read:
- AGENTS.md
- docs/AI_REPOSITORY_MANIFEST.md
- docs/QUALITY_GATE.md
- the draft JSON;
- every target file referenced by the draft.

Task:
- validate whether referenced target files exist;
- reject broad destructive patches;
- identify missing audio, render, path, and Blender compatibility details;
- convert the draft into a safe patch plan.

Output:
- accepted changes;
- rejected changes with reason;
- missing files;
- safe patch order;
- tests to run.
```

## Prompt: documentation synchronization

```text
You are synchronizing documentation in blender-audio-project.

Read:
- README.md
- AGENTS.md
- docs/README.md
- docs/MODULE_MAP.md
- docs/DATA_FLOW.md
- CONTRIBUTING.md
- CHANGELOG.md

Task:
- update stale paths;
- add missing links;
- keep the default branch as master unless repository settings change;
- ensure AI-facing documents reference the correct manifests and quality gates;
- mark unverified information as not specified.

Output:
- files updated;
- reason for each update;
- assumptions;
- tests performed.
```
