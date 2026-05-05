# Track input contract

Il warning startup sui track inputs non deve restare testo libero.

## Input richiesti

- `analysis_json`;
- `music_context_json`;
- `blender_keyframes_json`.

## Default

Mancanza input = warning.

## Strict

Con `-RequireTrackInputs` nel wrapper startup guard, la mancanza diventa errore.

## Output

```text
full0to10_track_input_contract.json
full0to10_track_input_contract.md
full0to10_track_input_template.json
```
