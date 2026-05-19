# _template_audio_reactive_package context

## Role

`Scripting/_template_audio_reactive_package` is the template/scaffold area for future audio-reactive Blender packages.

It should guide new package generation without changing existing working packages such as `Scripting/v61b`.

## Intended use

Use this area when creating a new track-specific or concept-specific Blender package. The template should encourage separation of concerns:

```text
main entrypoint
configuration
audio mapping
scene object creation
materials
lighting/camera
animation
render settings
encoding
diagnostics
package README
```

## Boundaries

- A template is not a production package until instantiated and validated.
- Do not use template files to override working package behavior.
- Do not commit generated media outputs from template experiments.
- Keep paths configurable and avoid workstation-specific hardcoding where practical.

## Relationship to shared utilities

New packages created from this template should check `Scripting/shared` before duplicating reusable helpers for JSON, paths, image sequences, FFmpeg, render profiles or diagnostics.

## Validation expectations

For a generated package based on this template:

```text
python compile/import checks for pure helpers
Blender smoke for bpy-dependent scene code
FFmpeg command preview for encode helpers
package README with entrypoint, inputs and outputs
```
