# Scripting/v61b

`Scripting/v61b/` is the current reference Blender package for complex audio-reactive scene generation in this repository.

It should be treated as a working production-oriented package and as the qualitative model for future generated packages.

This is application-domain runtime code. It must not be executed by normal local-AI run-unica validation unless an explicit Blender/audio/media task scopes it.

## Role in the project

`v61b` is the current reference for:

- modular Blender Python scripting;
- audio-reactive animation;
- configurable scene generation;
- camera, lighting, fog, material and physics orchestration;
- scene tuning and hotpatch workflows;
- image-sequence and FFmpeg encoding;
- structured object/collection registry patterns.

Future AI-generated Blender packages should use this folder as the expected depth and structure reference unless a simpler prototype is explicitly requested.

## Main entry point

```text
main_v61b.py
```

The entry point performs the following high-level sequence:

1. resolve script path and reload known modules;
2. validate analysis JSON and audio input;
3. load frame-level analysis data;
4. clear and configure the Blender scene;
5. configure render and world settings;
6. add the audio strip;
7. create camera, floor, backdrop and lights;
8. import/create hero and secondary assets;
9. create aura, rings, ribbons, variants, atmosphere, mist and physics accents;
10. animate the scene from the analysis frames;
11. classify scene structure;
12. register the tuning panel;
13. print the render/encoding summary.

## Important files

| File or folder | Role |
|---|---|
| `main_v61b.py` | Main package entry point. |
| `config.py` | Workflow configuration and local path defaults. |
| `io_utils.py` | JSON loading, input validation and Blender sequencer/audio helpers. |
| `scene_utils.py` | Scene cleanup helpers. |
| `camera_setup.py` | Camera and target creation. |
| `world_setup.py` | World, floor, backdrop and light setup. |
| `asset_setup.py` | Hero and secondary asset setup. |
| `materials.py` | Material and shader-node construction. |
| `atmosphere_setup.py` | Aura, rings, ribbons, atmosphere cube, mist and related objects. |
| `fog_dynamics.py` | Fog behavior and audio-reactive dynamics. |
| `fog_filaments.py` | Fog filament helper logic. |
| `physics_setup.py` | Physical accents and force-field style structures. |
| `animation.py` | Main audio-reactive animation mapping. |
| `render_setup.py` | Render and physics configuration. |
| `scene_tuning_panel.py` | Blender UI tuning panel and profile logic. |
| `encode_image_sequence_v61b.py` | Image-sequence encoding workflow. |
| `encode_ffmpeg_v61b.py` | FFmpeg command builder and encoder. |
| `hotpatch/` | Focused runtime patches and diagnostics. |
| `spaziotempo/core/registry.py` | Scene layer, collection and feature registry. |
| `spaziotempo/core/collections.py` | Object classification and collection organization helpers. |

## Refactoring policy

Do not destructively refactor this package only to move code into shared modules.

Correct migration order:

1. create a shared module under `Scripting/shared/`;
2. validate the shared module independently;
3. add an optional adapter if needed;
4. test the package in Blender;
5. migrate one call site at a time.

## Extraction candidates

| Source | Candidate shared utility |
|---|---|
| `io_utils.py` | `Scripting/shared/json_io.py`, `Scripting/shared/blender_compat.py` |
| `encode_ffmpeg_v61b.py` | `Scripting/shared/ffmpeg_encoder.py`, `image_sequence.py`, `render_profiles.py` |
| `encode_image_sequence_v61b.py` | `Scripting/shared/image_sequence.py` |
| `render_setup.py` | `Scripting/shared/render_profiles.py` |
| `scene_tuning_panel.py` | `Scripting/shared/panel_base.py`, `render_profiles.py` |
| `hotpatch/common.py` | `Scripting/shared/hotpatch_base.py`, `diagnostics.py` |
| `spaziotempo/core/registry.py` | Shared scene registry pattern for future packages. |

## Runtime notes

- Keep audio, JSON, render output and FFmpeg paths configurable through `config.py` or adapters.
- Mark Blender-version-sensitive code clearly.
- Keep render output mode and encoding mode separate.
- Keep artistic behavior changes separate from infrastructure refactors.
- Keep hotpatches focused and reversible.
- Do not run Blender render, FFmpeg encode/mux or audio/media output from normal AI/tooling validation.

## Encoding notes

The current package contains FFmpeg support for image-sequence encoding. This logic should eventually become shared and profile-based, but existing scripts should remain operational until the shared encoder is validated.

## 400-line policy

Maintained package docs and source files follow the repository 400-line policy.

```text
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Large existing scripts are technical debt and should be split only through focused package work, not during unrelated AI/tooling documentation updates.

## AI generation guidance

When an AI system edits `v61b`:

1. read `AGENTS.md` and current operational docs;
2. read this README;
3. inspect the target source file;
4. avoid broad rewrites;
5. preserve current entry points;
6. report changed files, purpose, risks, tests and line counts;
7. document any Blender-version assumption;
8. state whether Blender/FFmpeg/media runtime was not run or was explicitly scoped.

## Not specified

A full function-level index is not manually maintained here. Use the project code index generators, script inventory, line-count and file-line-limit reports when detailed symbol-level context is required.
