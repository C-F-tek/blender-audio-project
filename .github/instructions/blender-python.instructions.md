---
applyTo: "Scripting/**/*.py"
---

# Blender Python Instructions

Use these rules when editing Blender-facing Python files under `Scripting/`.

## Scope

This repository targets Blender audio-reactive scene generation. Blender packages may be versioned, generated, or track-specific.

## Required checks before editing

- Read the nearest package `README.md`.
- Inspect the target Python file.
- Check whether the logic already exists in `Scripting/shared/`.
- For `Scripting/v61b/`, preserve current public entry points and workflow order.

## Blender-specific rules

- Do not import `bpy` inside pure shared utilities unless the file is explicitly Blender-specific.
- Keep object creation, material creation, animation, render setup and encoding separate when practical.
- Keep audio strip creation and sequencer cleanup behind helper functions.
- Isolate Blender-version-sensitive behavior in compatibility helpers.
- Avoid broad rewrites of working scene packages.
- Do not assume a node type exists across Blender versions; provide a fallback or mark as not tested.
- Keep paths configurable through `config.py` or a config object.
- Preserve frame range and audio sync semantics.

## v61b policy

`Scripting/v61b/` is the current stable reference package.

Allowed:

- small fixes;
- additive adapters;
- comments explaining compatibility;
- optional use of tested shared helpers.

Avoid:

- changing `main_v61b.py` orchestration order without a clear runtime reason;
- moving modules out of the package before validation;
- changing artistic behavior while doing infrastructure refactor.

## Validation

For syntax-only changes:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
```

For package changes:

```powershell
python .\Tools\validation\check_package_structure.py --repo-root .
```

Runtime Blender behavior still requires Blender validation or clear manual test notes.
