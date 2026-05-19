# ready_to_jazz_wow_youtube_profiles_audio_sync context

## Role

This package is a standalone Blender/YouTube rendering workflow for a Ready To Jazz WOW scene. It includes a main Blender script, render profile choices and final encoding with audio/frame synchronization.

This package is product scripting, not IA-Carmine infrastructure.

## Primary entrypoint

```text
main_ready_to_jazz_wow_youtube.py
```

Open this file in Blender and run it from the Text Editor when generating the scene.

## Render profiles

The package README documents named profiles such as:

```text
HD_PREVIEW
HD_INTERMEDIATE
HD_FINAL
2K_PREVIEW
2K_INTERMEDIATE
2K_FINAL
```

The script uses profile data to control resolution, quality and motion blur settings.

## Encoding workflow

```text
render image sequence -> detect first rendered frame -> compute audio offset -> ffmpeg encode
```

The audio offset rule is:

```text
offset_seconds = (first_frame - 1) / FPS
```

This keeps the WAV aligned when rendering starts from a frame other than 1.

## Boundaries

- Keep package-specific visual decisions inside this package.
- Do not replace it with shared utilities until equivalent behavior is validated.
- Do not commit generated frames or encoded videos.
- Use shared utilities only through adapters after validation.

## Related files

```text
README.md
INSTALL_LOCATION.txt
render_profiles_reference.py
encode_final_youtube.py
```

## Relationship to Scripting/shared

Reusable concepts such as FFmpeg command construction, image sequence scanning and render profile modeling may later move toward `Scripting/shared`, but this package should remain stable while extraction is tested.
