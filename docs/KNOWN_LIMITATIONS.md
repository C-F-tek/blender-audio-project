# Known Limitations

## Current limitations

- Formal installation process is not specified.
- Blender version compatibility is not fully specified.
- External Python dependencies are not fully specified.
- Input JSON schemas are not fully specified.
- Automated tests are not specified.
- Release process is not specified.
- Example scenes are not yet documented.

## Technical risks

- Blender API changes can break node creation or render settings.
- Local absolute paths can reduce portability.
- Large generated files may not be suitable for Git.
- Audio analysis data may be too large for manual review.
- Rendering results may vary between GPU, CPU, codecs, and platforms.

## Recommended improvements

- Add minimal reproducible examples.
- Add script-level headers with inputs and outputs.
- Add compatibility notes per Blender version.
- Add a data schema for audio analysis JSON files.
- Add a render workflow guide.
