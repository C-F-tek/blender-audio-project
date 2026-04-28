# Blender Audio Project

This repository provides a framework for automatically generating and animating Blender scenes in response to music or audio tracks. Starting from an audio file, the system analyzes the waveform, extracts features, produces a track summary, classifies the overall mood, and uses that information to drive procedurally generated 3D scenes, lights, cameras, and special effects in Blender.

## How It Works

The pipeline consists of several steps:

1. **Audio Analysis** – Tools like `analyze_wav.py` compute beats, tempo, frequency bands and other features from the input `.wav` or `.mp3` file. The results are saved as a JSON file (`analysis.json`).
2. **Track Summary** – `build_track_summary.py` creates a condensed representation of the track (`track_summary.json` or `compact_track_summary.json`), capturing key segments and transitions. The summarization step also includes a new **classification** stage, which assigns broad scene types (e.g., "Calm", "Energetic", "Tension") based on the audio features.
3. **Scene Specification** – Based on the classification and summary, a high-level scene specification is generated. This describes which scene modules to use (e.g., camera, lighting, atmosphere), durations, transitions, and any story or mood cues.
4. **Normalization** – `normalize_scene_spec.py` ensures the specification conforms to required formats and adds defaults.
5. **Blender Execution** – The Python scripts under `Scripting/v61b/` orchestrate Blender. They assemble objects, apply materials and physics, animate parameters (such as camera motion or fog density) in sync with the audio, and render frames. Version `v61b` adds modules for atmosphere, water, lens effects, physics, and improved camera control. It also contains a reusable `shared` package for common tasks and a template to guide development of new audio-reactive packages.

## Repository Layout

```
.
├── analyze_wav.py            – Analyze audio files and generate feature JSON.
├── build_track_summary.py    – Produce a compact summary and classification.
├── normalize_scene_spec.py   – Normalize and validate scene specifications.
├── Scripting/
│   ├── v61b/                 – Current Blender package with orchestrator and modules.
│   │   ├── orchestrator.py   – Main entrypoint for generating scenes.
│   │   ├── modules/          – Submodules for camera, lighting, atmosphere, physics, etc.
│   │   ├── shared/           – Code shared across modules.
│   │   └── _template_audio_reactive_package/ – Template for creating new packages.
│   └── ... (other versions)
├── docs/
│   ├── PROJECT_OVERVIEW.md   – Project goals and architecture.
│   ├── DATA_FLOW.md          – Detailed pipeline description.
│   └── MODULE_MAP.md         – Summary of modules and their responsibilities.
└── examples/                 – Sample audio files and specs.
```

## Extending and Contributing

- **Develop new modules** – Use the `_template_audio_reactive_package` under `Scripting/v61b/` as a starting point. The template contains a checklist for writing a README, describing the agent’s context, outlining the implementation plan, and verifying the behavior with tests and a sample scene.
- **Update documentation** – When scripts or APIs change, make sure to update the files in `docs/`. In particular, revise `DATA_FLOW.md` when adding new pipeline stages (such as the classification step introduced in version v61b).
- **Don’t break existing workflows** – The orchestrator script depends on specific keys in the summary and scene specification JSON files. When modifying those files or adding modules, preserve existing keys and add new fields under clearly named sections. Document all assumptions and defaults.

See `docs/INSTALLATION.md` and `docs/USAGE.md` for environment setup and running instructions.
