# Track input warning resolution

Il warning:

```text
missing: analysis_json, music_context_json, blender_keyframes_json
```

viene risolto tramite contract e template.

## Regola

Il warning non blocca di default il Full0To10 perché alcuni loop sono code/tool
only. Può diventare blocker quando la run è track/blender oriented.

## Strumento

```text
Tools/workflow/run_full0to10_track_input_contract.ps1
```
