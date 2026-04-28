# Render Workflow

## Purpose

This document describes the expected rendering stage of the Blender audio-reactive workflow.

## High-level render flow

```text
Configured Blender scene
  -> test render
  -> frame sequence render
  -> review frames
  -> encode video with external tool
```

## Render inputs

- Blender scene generated or tuned by Python.
- Camera and animation timeline.
- Lighting and material configuration.
- Output path for frames.
- Frame rate and resolution.

## Render outputs

- Image sequence.
- Optional preview render.
- Final encoded video generated outside Blender.

## Recommended practice

- Render a small frame range first.
- Verify background, fog, lights, camera, and object motion.
- Use consistent color management.
- Keep render output paths configurable.
- Avoid committing large render outputs to Git unless explicitly required.

## AI rules

- Do not assume final render settings without reading the active script.
- Document any change to resolution, FPS, engine, denoise, motion blur, or output path.
- Keep CPU/GPU render assumptions separate from FFmpeg encoding assumptions.

## Not specified

- Canonical render engine.
- Canonical resolution.
- Canonical frame rate.
- Canonical output directory.
- Canonical color-management profile.
