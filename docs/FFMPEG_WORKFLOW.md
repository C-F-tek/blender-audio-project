# FFmpeg Workflow

## Purpose

This document describes the expected external video encoding stage after Blender rendering.

## Conceptual flow

```text
Rendered image sequence
  + WAV audio
  -> FFmpeg command
  -> final video file
```

## Common inputs

- Image sequence rendered by Blender.
- Original or mastered WAV audio file.
- Target frame rate.
- Codec and quality settings.
- Output video path.

## CPU encoding profile

A CPU encoding workflow may use AV1 through `libsvtav1` with a limited thread count.

Recommended fields to document per command:

- input frame pattern;
- start frame number;
- frame rate;
- audio file path;
- codec;
- preset;
- CRF or quality value;
- pixel format;
- color metadata;
- thread count;
- output path.

## GPU encoding profile

A GPU encoding workflow may use NVIDIA NVENC where available.

Recommended fields to document per command:

- selected GPU;
- codec;
- preset;
- rate-control mode;
- quality setting;
- pixel format;
- output path.

## Known risk areas

- Different results between local player and online processing platforms.
- Background or transparency handling.
- Color metadata mismatch.
- Pixel format incompatibility.
- Codec support differences.

## AI rules

- Do not assume CPU and GPU outputs are visually equivalent.
- Keep CPU and GPU scripts separate when settings differ.
- Preserve audio bitrate and frame rate explicitly.
- Document tested commands and observed output behavior.

## Not specified

- Canonical final encoding command.
- Canonical target bitrate.
- Canonical codec for publication.
