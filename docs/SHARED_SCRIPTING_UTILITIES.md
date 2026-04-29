# Shared Scripting Utilities

## Purpose

This document defines how reusable Blender, FFmpeg, JSON, path, diagnostics and rendering utilities should be extracted into `Scripting/shared/`.

The goal is to reduce duplication across generated packages without destabilizing working scenes.

## Core principle

Working package code has priority over abstraction.

`Scripting/v61b/` is a working reference model and must not be destructively refactored only to make utilities global. Shared extraction must happen in small, additive steps.

## Required extraction workflow

1. Identify reusable behavior in an existing package.
2. Copy or reimplement the behavior under `Scripting/shared/` with package-neutral naming.
3. Remove hardcoded package names and workstation-specific defaults from the shared version.
4. Keep the original package unchanged.
5. Validate the shared module independently.
6. Add an optional adapter in the target package.
7. Test inside Blender or with the relevant CLI workflow.
8. Migrate package usage only after successful validation.
9. Document changed files, assumptions, risks and tests.

A duplicated working helper is acceptable until the shared replacement is validated.

## Target shared modules

| Module | Responsibility |
|---|---|
| `Scripting/shared/path_utils.py` | Project-root discovery, path normalization, safe output directory creation. |
| `Scripting/shared/json_io.py` | UTF-8 JSON loading/writing, schema-light validation, clear error messages. |
| `Scripting/shared/blender_compat.py` | Blender-version-sensitive API wrappers: sequencer, nodes, object properties, scene cleanup. |
| `Scripting/shared/image_sequence.py` | Frame discovery, numbering, gap detection, FFmpeg input pattern generation. |
| `Scripting/shared/ffmpeg_encoder.py` | FFmpeg discovery, command construction, dry-run command preview, execution helpers. |
| `Scripting/shared/render_profiles.py` | CPU/GPU/YouTube render and encode profile definitions. |
| `Scripting/shared/config_model.py` | Dataclass-based configuration models and adapters from package config modules. |
| `Scripting/shared/diagnostics.py` | Common diagnostics, reporting and environment checks. |
| `Scripting/shared/hotpatch_base.py` | Common hotpatch runner conventions and patch result reporting. |
| `Scripting/shared/panel_base.py` | Blender UI panel registration and reusable tuning-panel patterns. |
| `Scripting/shared/scene_registry.py` | Reusable scene layer, collection and feature registry patterns. |

## Minimum first implementation

The first safe extraction should be small and testable:

```text
Scripting/shared/path_utils.py
Scripting/shared/json_io.py
Scripting/shared/image_sequence.py
```

These modules do not need to import `bpy`, so they can be tested with normal Python before Blender integration.

## Blender compatibility helpers

Blender API compatibility should be isolated. Do not scatter version-specific fallback code across scene modules.

Candidate wrappers:

```python
clear_sequence_editor(scene)
create_sound_strip(scene, audio_path, frame_start=1, channel=1)
safe_create_node(nodes, preferred_type, fallback_type=None)
safe_set_scene_sync_audio(scene)
safe_remove_object(obj)
```

Use this layer for differences such as sequencer API changes or removed/renamed shader nodes.

## FFmpeg and render profile helpers

Encoding should be represented as data plus command generation.

Suggested models:

```python
@dataclass(frozen=True)
class EncodeProfile:
    name: str
    codec: str
    preset: str
    quality_args: tuple[str, ...]
    color_args: tuple[str, ...]
    audio_args: tuple[str, ...]

@dataclass(frozen=True)
class EncodeJob:
    ffmpeg: Path
    input_pattern: str
    audio_path: Path
    output_path: Path
    fps: float
    first_frame: int
    frame_count: int
    profile: EncodeProfile
```

The current CPU SVT-AV1 and GPU NVENC workflows can become named profiles.

## Configuration helpers

Existing package configs can remain global for compatibility, but shared utilities should not depend on package globals directly.

Recommended adapter pattern:

```python
def render_config_from_module(cfg) -> RenderConfig:
    return RenderConfig(
        fps=float(getattr(cfg, "FPS_OVERRIDE", 0) or 30),
        output_mode=str(getattr(cfg, "RENDER_OUTPUT_MODE", "IMAGE_SEQUENCE")),
        resolution_x=int(getattr(cfg, "RESOLUTION_X", 3840)),
        resolution_y=int(getattr(cfg, "RESOLUTION_Y", 2160)),
    )
```

## Scene registry helpers

The v61b `spaziotempo/core/registry.py` approach is a good model: use data to describe layers, collections, feature ownership and object classification.

Future packages should prefer:

```text
feature name
  -> layer
  -> collection
  -> owning module
  -> hotpatch target
```

This makes AI patches safer because the target module is explicit.

## Extraction candidates

| Source file | Candidate shared behavior | Target |
|---|---|---|
| `Scripting/v61b/io_utils.py` | JSON loading, input existence checks, sequencer/audio strip compatibility | `json_io.py`, `blender_compat.py` |
| `Scripting/v61b/encode_ffmpeg_v61b.py` | FFmpeg discovery, image-sequence detection, audio offset, CPU/GPU profiles | `ffmpeg_encoder.py`, `image_sequence.py`, `render_profiles.py` |
| `Scripting/v61b/encode_image_sequence_v61b.py` | Image sequence handling and export conventions | `image_sequence.py` |
| `Scripting/v61b/render_setup.py` | Render engine/profile configuration | `render_profiles.py` |
| `Scripting/v61b/scene_tuning_panel.py` | Tuning panel registration and profile application | `panel_base.py`, `render_profiles.py` |
| `Scripting/v61b/hotpatch/common.py` | Hotpatch utility patterns | `hotpatch_base.py`, `diagnostics.py` |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py` | YouTube CPU/GPU encode presets | `ffmpeg_encoder.py`, `render_profiles.py` |

## Migration rules for existing packages

- Do not move code out of `v61b` directly.
- Do not rename existing package entry points during utility extraction.
- Do not change artistic scene behavior while extracting infrastructure helpers.
- Do not add shared imports to a working package until the shared module has been tested.
- Prefer adapters that preserve the package's existing public function names.
- Migrate one concern at a time.
- Keep rollback simple.

## Rules for new packages

New generated packages should check `Scripting/shared/` before duplicating:

- JSON loading;
- path resolution;
- audio strip creation;
- image sequence scanning;
- FFmpeg command creation;
- render profile selection;
- diagnostics;
- project manifests.

Package-specific visual decisions should remain in the package.

## Validation requirements

| Utility type | Minimum validation |
|---|---|
| Pure Python utility | `python -m py_compile` and a small fixture test. |
| FFmpeg utility | command preview plus a short encode test. |
| Blender compatibility wrapper | Blender manual run or headless import where possible. |
| Render profile helper | verify output settings in Blender and generated command. |
| Hotpatch helper | run on a copied scene or controlled test scene. |

## Current status

`Scripting/shared/` is the correct target for reusable code, but full migration is not complete. Existing working package code should remain untouched until each shared replacement is tested.
