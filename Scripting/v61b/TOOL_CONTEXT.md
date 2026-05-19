# Scripting/v61b context

## Role

`Scripting/v61b` is the current working Blender package/reference scene for the Spaziotempo audio-reactive visual pipeline. It contains the main scene builder, render configuration, animation, material/atmosphere/physics modules, hotpatches and encoding helpers.

This is not an AI tool package. It is project/product scripting that may be inspected or patched by IA-Carmine tooling.

## Main entrypoints

### Scene generation

```text
main_v61b.py
```

Runs inside Blender with `bpy` available. It loads the configured analysis JSON and audio path, creates/clears the scene, configures render/world/audio, imports assets, creates atmosphere/physics elements, animates the scene and prints a render summary.

### Hot update

```text
hot_update_scene_v61b.py
```

Used for targeted scene updates/hotpatch-like workflows. Treat as Blender-context code.

### Encoding

```text
encode_image_sequence_v61b.py
encode_ffmpeg_v61b.py
```

Used after frame rendering to encode image sequences with audio. These scripts include frame detection and audio sync concerns and may use Blender context where applicable.

## Key package families

```text
animation.py                  -> audio-reactive animation orchestration
asset_setup.py                -> primary/secondary asset setup
atmosphere_setup.py           -> aura, fog, ribbons, rings, particles
camera_setup.py               -> camera rig
config.py / config_parts/     -> package configuration
fog_dynamics.py               -> fog dynamics
materials.py / materials_parts/ -> material and shader setup
physics_setup.py              -> physics accents
render_setup.py               -> render and engine configuration
scene_tuning_panel.py         -> Blender UI tuning panel
spaziotempo/**                -> structured scene registry/core/features
hotpatch/**                   -> targeted patch modules
```

## Runtime assumptions

- Blender with `bpy` is required for scene modules.
- Config paths control audio, analysis JSON, render output and frame sequence output.
- `main_v61b.py` can be opened in Blender Text Editor and launched with `Alt+P`.
- Encoding scripts expect rendered frames and a valid audio file.

## Safety rules

- Do not destructively refactor `v61b` just to extract shared code.
- Keep working artistic behavior stable unless the change is explicitly requested.
- Extract reusable utilities additively into `Scripting/shared` first.
- Preserve public function names when adding adapters.
- Validate pure Python helpers with normal Python and Blender-facing changes inside Blender.
- Do not commit generated frames, videos, caches or render outputs.

## Relationship to shared utilities

`docs/SHARED_SCRIPTING_UTILITIES.md` defines the migration policy: working package code has priority over abstraction. `Scripting/shared` is the target for reusable path, JSON, image sequence, FFmpeg, render profile, diagnostics and compatibility helpers, but migration should happen only after tests.
