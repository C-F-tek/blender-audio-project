# Scripting/shared

This folder is reserved for shared Blender scripting utilities that can be reused by multiple generated packages under `Scripting/`.

## Purpose

When a function, helper, panel, encoder, render profile, diagnostic tool, or configuration pattern becomes useful across more than one generated Blender package, it should be extracted from the package-specific folder and moved here.

`Scripting/v61b/` is currently the main source of mature reusable patterns.

## Candidate shared utilities from v61b

| Candidate | Current source | Shared role |
|---|---|---|
| FFmpeg encoding helper | `Scripting/v61b/encode_ffmpeg_v61b.py` | Generic image-sequence plus audio encoder. |
| Image sequence encoding helper | `Scripting/v61b/encode_image_sequence_v61b.py` | Reusable frame-sequence export/encoding helper. |
| Runtime/render profile logic | `Scripting/v61b/scene_tuning_panel.py` | Reusable preview/final/YouTube render profile logic. |
| Scene tuning panel pattern | `Scripting/v61b/scene_tuning_panel.py` | Reusable Blender UI pattern for package tuning. |
| Hot update pattern | `Scripting/v61b/hot_update_scene_v61b.py` | Reusable live scene update approach. |
| Diagnostics utilities | `Scripting/v61b/hotpatch/` | Reusable debugging and validation helpers. |

## Extraction rule

A utility should be moved or copied here when at least one of these is true:

- two or more packages need the same logic;
- a new package would otherwise duplicate v61b code;
- the function is not tied to one track or scene concept;
- the helper only needs configuration values to become generic;
- the code handles operational tasks such as rendering, encoding, paths, diagnostics, or UI controls.

## Required design for shared utilities

Shared utilities should avoid hardcoded package names such as `v61b` or track-specific names.

They should accept:

- package root path;
- config module or config object;
- audio path;
- analysis JSON path;
- image sequence directory;
- output video path;
- render profile name;
- optional Blender context.

## Current modules

| Module | Status |
|---|---|
| `path_utils.py` | Initial pure Python helper for project-root and path checks. |
| `json_io.py` | Initial pure Python helper for UTF-8 JSON reads/writes and small validation helpers. |
| `image_sequence.py` | Initial pure Python helper for frame sequence discovery and FFmpeg pattern generation. |
| `ffmpeg_encoder.py` | Initial pure Python FFmpeg command builder, dry-run by default. |
| `render_profiles.py` | Initial reusable encode profile definitions. |

## Suggested future modules

```text
Scripting/shared/
  README.md
  blender_compat.py
  config_model.py
  panel_base.py
  scene_update.py
  diagnostics.py
  hotpatch_base.py
  scene_registry.py
```

## AI rules

- Do not duplicate mature v61b helpers inside new packages without checking this folder.
- Before extracting code, remove v61b-specific names and paths.
- Keep shared utilities configurable and package-agnostic.
- Do not break the original v61b workflow during extraction.
- Prefer adding wrappers first, then migrating package code after Blender tests.

## Current status

Initial package-agnostic utilities have been extracted, but package migration is still incomplete. Existing working packages should remain unchanged until each shared replacement has independent validation and an optional adapter.
