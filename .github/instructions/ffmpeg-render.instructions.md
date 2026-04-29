---
applyTo: "Scripting/**/*encode*.py,Scripting/**/*ffmpeg*.py,docs/*FFMPEG*,docs/*RENDER*"
---

# FFmpeg and Render Instructions

Use these rules when editing image-sequence encoding, FFmpeg command builders, render profile code, or render documentation.

## General rules

- Keep render settings separate from final video encoding.
- Always make frame rate explicit.
- Always make start frame explicit.
- Always make audio path explicit.
- Always make output path explicit.
- Preserve audio/frame synchronization when renders start from a frame greater than 1.
- Use explicit pixel format and color metadata for YouTube/public video targets.
- Prefer command preview/dry-run before execution.

## Shared extraction direction

Reusable encoding logic should move toward:

```text
Scripting/shared/image_sequence.py
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
```

Existing package encoders should not be broken while shared utilities are introduced.

## CPU/GPU profile notes

- CPU SVT-AV1 should remain available for high-quality, consistent YouTube uploads.
- GPU NVENC profiles should remain available for speed tests and iteration.
- Keep YouTube-safe color flags explicit.
- Do not assume GPU output is visually identical to CPU output on YouTube.

## Validation

For syntax:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
```

For image sequence metadata, prefer using or extending:

```text
Scripting/shared/image_sequence.py
```

A full encode should be tested on a short frame range before production use.
