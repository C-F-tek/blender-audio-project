# Usage

## General workflow

1. Prepare or generate audio analysis data.
2. Configure paths in the Blender Python script.
3. Open Blender.
4. Run the script.
5. Inspect the generated scene.
6. Render test frames.
7. Tune parameters.
8. Render the final output.

## Audio-reactive workflow

The expected workflow is based on using audio-derived information to control visual parameters such as:

- object animation;
- camera movement;
- lighting intensity;
- material response;
- volumetric fog;
- scene timing;
- beat or onset reactions.

## Running scripts

Script execution method is not standardized yet. Possible methods include:

- Blender Text Editor;
- Blender command line;
- add-on installation;
- external automation.

The currently supported method must be verified per script.

## Inputs

Expected input types may include:

- `.wav` audio files;
- `.json` analysis files;
- Blender scene configuration values.

Exact input schema is not specified yet.

## Outputs

Possible outputs include:

- generated Blender scene objects;
- configured camera and lights;
- render-ready scene;
- frame sequence;
- video produced by external FFmpeg workflow.

Exact output contract is not specified yet.
