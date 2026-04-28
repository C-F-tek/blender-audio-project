# Documentation

This folder contains the main technical documentation for `blender-audio-project`.

## Recommended reading order

1. `PROJECT_OVERVIEW.md`
2. `MODULE_MAP.md`
3. `DATA_FLOW.md`
4. `BLENDER_SCRIPT_ENTRYPOINTS.md`
5. `AI_REPOSITORY_MANIFEST.md`
6. `AI_PROMPTS.md`
7. `AI_GENERATED_PACKAGE_STANDARD.md`
8. `PACKAGE_CREATION_WORKFLOW.md`
9. `QUALITY_GATE.md`
10. `REVIEW_CHECKLIST.md`
11. `SHARED_SCRIPTING_UTILITIES.md`
12. `AUDIO_ANALYSIS_PIPELINE.md`
13. `JSON_SCHEMAS.md`
14. `RENDER_WORKFLOW.md`
15. `FFMPEG_WORKFLOW.md`
16. `LOCAL_AI_WORKFLOW.md`
17. `INSTALLATION.md`
18. `USAGE.md`
19. `COMPATIBILITY.md`
20. `KNOWN_LIMITATIONS.md`
21. `DEVELOPER_GUIDE.md`

## Documentation groups

### Project context

- `PROJECT_OVERVIEW.md`
- `MODULE_MAP.md`
- `DATA_FLOW.md`
- `DEVELOPER_GUIDE.md`

### AI-assisted workflow

- `AI_REPOSITORY_MANIFEST.md`
- `AI_PROMPTS.md`
- `AI_GENERATED_PACKAGE_STANDARD.md`
- `PACKAGE_CREATION_WORKFLOW.md`
- `QUALITY_GATE.md`
- `REVIEW_CHECKLIST.md`
- `LOCAL_AI_WORKFLOW.md`

Machine-readable AI metadata is stored in:

```text
../indexAI/ai_manifest.json
```

### Shared utilities and non-destructive extraction

- `SHARED_SCRIPTING_UTILITIES.md`

### Blender workflow

- `BLENDER_SCRIPT_ENTRYPOINTS.md`
- `AUDIO_ANALYSIS_PIPELINE.md`
- `RENDER_WORKFLOW.md`

### Data and encoding

- `JSON_SCHEMAS.md`
- `FFMPEG_WORKFLOW.md`

### Setup and operations

- `INSTALLATION.md`
- `USAGE.md`
- `COMPATIBILITY.md`
- `KNOWN_LIMITATIONS.md`

## Documentation style

The documentation is explicit and structured. Unknown information is marked as `not specified` instead of being inferred without evidence.

## AI usage

AI systems should read `../AGENTS.md` first, then this documentation index, then `AI_REPOSITORY_MANIFEST.md`, `MODULE_MAP.md`, `DATA_FLOW.md`, `AI_GENERATED_PACKAGE_STANDARD.md`, `PACKAGE_CREATION_WORKFLOW.md`, `QUALITY_GATE.md`, and `REVIEW_CHECKLIST.md` before creating or editing generated Blender packages.
