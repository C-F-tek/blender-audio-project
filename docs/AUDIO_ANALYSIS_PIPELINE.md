# Audio Analysis Pipeline

## Purpose

This document describes the expected role of audio analysis in the Blender scene-generation workflow.

## Conceptual pipeline

```text
WAV audio
  -> technical audio analysis
  -> rhythm, intensity, frequency-band, beat, onset, and segment data
  -> JSON analysis files
  -> Blender scene parameters
```

## Expected analysis outputs

The project may use analysis data for:

- duration and frame range;
- sample rate and timing;
- estimated BPM;
- low, mid, and high band activity;
- beat or onset markers;
- segment-level intensity;
- camera modulation;
- material and light modulation;
- fog and atmosphere changes.

## Input files

| Input | Status | Notes |
|---|---|---|
| WAV file | expected | Exact local path is configurable. |
| Existing analysis JSON | expected | Schema not fully specified. |
| Music context JSON | possible | Used by AI-assisted planning workflows. |

## Output files

| Output | Status | Notes |
|---|---|---|
| audio analysis JSON | expected | Do not overwrite without explicit instruction. |
| track summary JSON | possible | Used as compact context. |
| music context JSON | possible | Used by AI tools or script generation. |
| keyframe JSON | possible | Used to map analysis data to Blender animation. |

## AI rules

- Treat analysis JSON files as valuable generated data.
- Do not reduce full frame-level JSON into a lossy version unless requested.
- For AI work, prefer compact summaries while preserving original files.
- Document every assumed JSON field.
- Do not invent schema fields without marking them as assumed.

## Not specified

- Canonical JSON schema.
- Canonical analysis command.
- Canonical output folder.
- Required audio format beyond WAV-oriented workflow.
