# assets context

## Role

`assets/` contains project assets used by Blender/audio-reactive scene scripts. Assets are application inputs, not IA-Carmine runtime tools.

## How assets are used

Blender packages under `Scripting/**` may load assets through package configuration or scene setup modules. AI tooling may inspect asset paths for context, but asset files are not patch targets unless the task explicitly concerns asset organization or metadata.

## Rules

- Do not treat binary assets as source code.
- Do not rewrite or replace assets without explicit operator request.
- Do not commit generated render outputs here.
- Keep asset references configurable in package config modules.
- If an asset is large or generated, verify Git policy before staging.

## Relationship to scripts

Typical flow:

```text
assets/** -> Scripting package config -> Blender scene setup -> render output outside Git
```

Generated frames, videos and temporary exports belong outside versioned assets unless explicitly approved.
