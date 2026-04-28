# Inputs

This folder stores compact package input files.

## Expected files

| File | Role |
|---|---|
| `track_summary.json` | Compact technical summary of the audio track. |
| `music_context.json` | Semantic or musical context for AI-assisted scene generation. |
| `input_schema.json` | Local schema notes for expected input fields. |
| `audio.wav` | Optional local placeholder name for the audio file. |

Large full-analysis JSON files may live outside this package. If so, document their path in the package README and `config.py`.

## Rule

Do not overwrite full analysis JSON files without explicit instruction.
