# Scripting/shared context

## Role

`Scripting/shared` is the target area for reusable scripting utilities shared by Blender/audio/video packages. It should contain package-neutral helpers for paths, JSON, image sequences, FFmpeg, render profiles, diagnostics, Blender compatibility and hotpatch conventions.

This area exists to reduce duplication without destabilizing working scene packages.

## Expected responsibilities

```text
path utilities
JSON read/write helpers
image sequence scanning
FFmpeg command construction
render profile data models
Blender compatibility wrappers
diagnostics/report helpers
hotpatch base conventions
scene registry helpers
```

## Extraction policy

Working package code has priority over abstraction.

Correct extraction flow:

```text
identify duplicated behavior in a working package
add package-neutral helper under Scripting/shared
validate helper independently
add optional adapter in target package
migrate package use only after successful validation
```

Do not move code out of `Scripting/v61b` or another working package directly.

## Validation expectations

- Pure Python helpers: `python -m py_compile` and fixture test.
- FFmpeg helpers: command preview and short encode test when practical.
- Blender wrappers: import-safety outside Blender plus Blender smoke where `bpy` is required.
- Render profile helpers: verify generated settings/commands.
- Hotpatch helpers: run only on copied or controlled scene/test inputs.

## Boundaries

- Shared utilities should not depend on package-specific config globals directly.
- Use adapters to convert package config into shared dataclasses or explicit arguments.
- Do not commit generated frames, renders or videos.
- Avoid broad refactors without package-level rollback paths.

## Related docs

`docs/SHARED_SCRIPTING_UTILITIES.md` is the detailed extraction plan and policy for this area.
