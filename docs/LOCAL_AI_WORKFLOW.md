# Local AI Workflow

## Purpose

This document records the intended direction for moving parts of the Blender script-generation workflow from external AI assistance toward a local AI-assisted pipeline.

## Current workflow

At the current stage, the workflow is generally:

```text
Audio input
  -> technical analysis
  -> JSON files and compact context
  -> external AI assistance such as Codex or GPT
  -> generated Blender script package
  -> stored under Scripting/
  -> manual or assisted refinement
```

## Target direction

The future objective is to perform more of the script-generation and review loop locally, when hardware and model quality allow it.

Candidate local components:

- local project indexing;
- local compact context generation;
- local JSON summarization;
- local Blender-aware code generation;
- local patch planning;
- local patch validation;
- NPU-assisted review where useful;
- GPU-assisted model execution where required.

## Repository areas involved

| Area | Role |
|---|---|
| `Scripting/` | Destination for generated Blender script packages. |
| `Tools/npu/` | Local AI, NPU, context-building, and review tooling. |
| `indexAI/` | Project index, manifests, compact context, and patch materials. |
| `indexAI/patch_library/` | Generated plans, service capsules, and task packets. |
| `docs/` | Stable documentation for human and AI orientation. |

## Desired local pipeline

```text
WAV/audio data
  -> analysis JSON
  -> compact music and technical context
  -> local AI planner
  -> implementation plan
  -> patch generator
  -> validation against repo index
  -> generated Blender package under Scripting/
  -> Blender test run
  -> render and FFmpeg workflow
```

## Requirements for safe local generation

- A reliable project index.
- Clear target files.
- Clear JSON schema or documented assumptions.
- Patch validation before writing files.
- No destructive overwrite of source or analysis data.
- Explicit logging of generated files.
- Manual review for major scene-generation changes.

## AI rules

- Treat local AI output as draft material until validated.
- Keep generated packages separated by track, concept, or version.
- Do not merge unrelated generated packages automatically.
- Preserve full analysis JSON files.
- Prefer compact summaries for model input.
- Record assumptions in generated implementation notes.

## Not specified

- Final local model choice.
- Final NPU or GPU runtime.
- Final prompt format.
- Final patch schema.
- Final validation command.
