# Blender Script Entry Points

## Purpose

This document identifies the scripts that should be inspected first when running or modifying the Blender workflow.

## Primary known entry point

| Script | Status | Role |
|---|---|---|
| `Scripting/v61b/main_v61b.py` | known from repository index | Primary Blender workflow script for the v61b scene pipeline. |

## Related documentation

| File | Role |
|---|---|
| `Scripting/v61b/README.md` | Folder-level notes for v61b. |
| `Scripting/v61b/SCENE_TUNING_GUIDE.md` | Existing scene tuning guide. |
| `docs/MODULE_MAP.md` | Repository module map. |
| `docs/DATA_FLOW.md` | Data flow overview. |

## Execution model

The exact execution model is not fully specified yet. Possible Blender execution methods include:

- running the script from Blender Text Editor;
- running Blender with a Python script argument;
- using a custom add-on panel;
- using a local automation wrapper.

## Required pre-run checks

Before running a Blender script:

1. Verify the Blender version.
2. Verify local paths for audio, JSON, and render output.
3. Verify that input JSON files exist.
4. Verify that the script does not depend on removed Blender API features.
5. Save or backup the current Blender scene.

## AI modification rules

- Inspect the actual entry-point script before suggesting patches.
- Do not assume the active entry point if multiple main scripts exist.
- Keep local file paths configurable.
- Report the resulting line count after modifying scripts.
- Prefer hotpatches for isolated experimental fixes.

## Not specified

- Definitive command-line invocation.
- Final list of all executable scripts.
- Add-on installation entry point.
- Supported Blender versions per script.
