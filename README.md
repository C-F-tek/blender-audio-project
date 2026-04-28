# blender-audio-project

Python project for Blender scripting, audio-reactive scene generation, AI-assisted visual package creation, and experimental visual production workflows.

## Author

Carmine Faiola

LinkedIn: https://it.linkedin.com/in/carmine-faiola-12471a183

## License

MIT License. See `LICENSE`.

## Project status

Work in progress. The repository is a technical workspace for Blender scene automation, audio-driven visual production, AI-assisted package generation, and future local AI/NPU/GPU-assisted workflows.

## Scope

The project is intended to support:

- audio analysis and compact track summaries;
- Blender Python scripting;
- procedural scene generation;
- audio-reactive animation logic;
- camera, light, fog, material, object, and render tuning;
- JSON-based intermediate data from audio analysis;
- AI-generated or AI-refined Blender script packages;
- versioned package development;
- future local AI-assisted generation and validation.

## Repository structure

| Path | Description |
|---|---|
| `analyze_wav.py` | Audio analysis tool. |
| `build_track_summary.py` | Compact summary builder for analysis data. |
| `normalize_scene_spec.py` | Scene-spec normalization tool. |
| `Scripting/` | Workspace for Blender script packages generated or refined from audio-analysis data. |
| `Scripting/v61b/` | Current quality reference for complex Blender scene scripting. |
| `Scripting/_template_audio_reactive_package/` | Template for future AI-generated audio-reactive Blender packages. |
| `Scripting/shared/` | Target area for reusable non-destructive shared utilities. |
| `Tools/npu/` | Local AI, NPU, context-building, and review tooling. |
| `Tools/repo_patch_runner/` | Structured repository patch tooling. |
| `indexAI/` | AI indexes, manifests, context, and patch artifacts. |
| `docs/` | Technical documentation. |
| `examples/` | Future examples and usage notes. |
| `.github/` | GitHub templates. |

## Documentation index

Start here:

- `AGENTS.md`
- `docs/README.md`
- `docs/PROJECT_OVERVIEW.md`
- `docs/MODULE_MAP.md`
- `docs/DATA_FLOW.md`
- `docs/AI_GENERATED_PACKAGE_STANDARD.md`
- `docs/PACKAGE_CREATION_WORKFLOW.md`
- `docs/QUALITY_GATE.md`
- `docs/SHARED_SCRIPTING_UTILITIES.md`
- `docs/LOCAL_AI_WORKFLOW.md`
- `docs/PROJECT_AUDIT.md`

## Package workflow

New serious Blender packages should start from:

```text
Scripting/_template_audio_reactive_package/
```

and be copied to a project-specific folder such as:

```text
Scripting/track_name_visual_concept/
```

`Scripting/v61b/` remains the reference for richer scene complexity and scripting ambition.

## Documentation policy

Information that is not confirmed by code or tests must remain marked as `not specified`.

Working code should not be broken for premature refactoring. Shared utilities should be extracted additively and tested before existing packages are migrated.
