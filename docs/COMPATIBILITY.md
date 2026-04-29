# Compatibility

## Blender

Blender 5.1.1 has passed a focused no-render smoke for `Scripting/shared/blender_compat.py` on Windows.

Validated scope:

```text
set_render_fps
set_frame_range_from_seconds
safe_create_noise_texture_node
clear_sequence_editor
create_sound_strip
safe_set_scene_sync_audio
```

The project should document compatibility per script, especially when Blender API changes affect node types, render settings, or EEVEE and Cycles options.

## Python

Python version is tied to the Blender version in most workflows.

External Python interpreter compatibility is not specified yet.

## Operating systems

Known workstation context may include Windows-based Blender usage, but cross-platform support is not specified yet.

## Known compatibility risk areas

- removed or renamed Blender shader nodes;
- render engine enum changes;
- EEVEE and Cycles API differences;
- local absolute paths;
- GPU and CPU render configuration differences;
- audio strip and VSE API changes.
- local add-ons compiled for a different Blender Python version.

## Known local add-on issue

Blender 5.1.1 startup logs currently report that Animation Nodes was compiled for Python 3.11 while Blender uses Python 3.13. This did not block the `blender_compat.py` smoke test, but it should be disabled or updated before treating background Blender logs as clean.

## Documentation rule

Do not mark a Blender version as supported until it has been tested.
