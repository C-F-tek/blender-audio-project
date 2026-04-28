# indexAI/patch_library

## Purpose

This folder stores AI-oriented patch artifacts, task packets, service capsules, and implementation notes.

## Typical content

- Patch plans.
- Implementation drafts.
- Service capsules.
- GPU or NPU task packets.
- Generated notes for future coding sessions.

## Handling rules

- Treat every file as a planning artifact unless explicitly marked as executable source.
- Inspect target source files before applying any generated patch.
- Preserve historical patch artifacts unless cleanup is requested.
- Prefer adding new dated or named artifacts instead of overwriting previous ones.
- Mark assumptions clearly.

## Review checklist

Before applying a patch artifact:

1. Identify target files.
2. Confirm target files exist.
3. Check whether the artifact is current.
4. Apply only the relevant changes.
5. Test in Blender when the patch touches scene code.
6. Update documentation if the workflow changes.

## Not specified

- Artifact retention policy.
- Formal naming convention.
- Required JSON schema for task packets.
