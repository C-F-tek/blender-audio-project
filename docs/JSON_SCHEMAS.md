# JSON Schemas

## Purpose

This document records known and expected JSON data structures used by the project.

## Current status

Formal JSON schemas are not specified yet.

The repository contains AI-oriented index and packet material under `indexAI/` and `Tools/npu/`. These files should be treated as structured context and inspected before automated modification.

## Expected JSON categories

| Category | Typical role | Status |
|---|---|---|
| audio analysis JSON | Technical audio data used by Blender scripts | not fully specified |
| track summary JSON | Compact track-level summary | not fully specified |
| music context JSON | Semantic and musical context for AI-assisted workflows | not fully specified |
| keyframe JSON | Animation and timing data for Blender | not fully specified |
| implementation draft JSON | AI-generated implementation plan | not fully specified |
| patch task packet JSON | Patch or service packet for AI workflows | not fully specified |
| project manifest JSON | File index or project code manifest | present in AI index areas |

## AI handling rules

- Never overwrite full analysis JSON files without explicit instruction.
- When producing derived summaries, write new files instead of replacing originals.
- Preserve unknown fields.
- Avoid destructive normalization.
- Mark inferred fields as assumptions.
- Prefer compact summaries for AI context while keeping originals intact.

## Recommended schema documentation format

For every confirmed JSON file type, document:

```text
File pattern:
Producer:
Consumer:
Required fields:
Optional fields:
Large fields:
Do not overwrite:
Notes:
```

## Next action

Inspect representative JSON files and convert this document from expected schema notes into confirmed schema documentation.
