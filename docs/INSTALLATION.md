# Installation

## Repository clone

```powershell
git clone https://github.com/C-F-tek/blender-audio-project.git
cd blender-audio-project
```

## Blender setup

Open Blender and run the target Python script from the `Scripting/` folder.

A formal add-on installation process is not specified yet.

## Python dependencies

External Python dependencies are not specified yet.

## Local assets

Some workflows may require:

- WAV audio files;
- JSON analysis files;
- render output folders;
- Blender project files.

Exact paths should be configured locally and should not be assumed globally valid.

## Recommended local workflow

1. Clone the repository.
2. Open Blender.
3. Inspect the script path under `Scripting/`.
4. Adjust local paths for audio, JSON, and output folders.
5. Run the script from Blender.
6. Review console output and generated scene elements.
