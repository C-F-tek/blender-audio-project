# Scripting context index

This file is the compact navigation layer for Blender/audio/video package scripts.

## Main context files

| Area | Context file | Role |
| --- | --- | --- |
| `Scripting` | `Scripting/TOOL_CONTEXT.md` | Scripting area overview. |
| `Scripting/v61b` | `Scripting/v61b/TOOL_CONTEXT.md` | Current working Blender reference package. |
| `Scripting/shared` | `Scripting/shared/TOOL_CONTEXT.md` | Shared utility extraction target. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync` | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/TOOL_CONTEXT.md` | Standalone Blender/YouTube package. |
| `Scripting/_template_audio_reactive_package` | `Scripting/_template_audio_reactive_package/TOOL_CONTEXT.md` | Template for future packages. |

## Related docs

| File | Role |
| --- | --- |
| `docs/SHARED_SCRIPTING_UTILITIES.md` | Shared utility extraction policy. |
| `docs/SCRIPT_SURFACE_CONTEXT.md` | Non-Tools surface map. |
| `docs/PACKAGE_CREATION_WORKFLOW.md` | Package creation workflow. |

## Usage

`Scripting/**` is application-domain code. Many scripts require Blender and `bpy`.

Do not run Blender, render, encode or generate media unless the operator explicitly requests that application-domain action.
