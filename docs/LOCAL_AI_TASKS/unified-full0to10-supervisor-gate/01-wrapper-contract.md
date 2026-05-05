# Wrapper contract

Il wrapper accetta parametri principali del launcher:

```text
-RunIntensity
-Model
-SkipGitSync
-NoBranch
-DryRun
-ForwardedArgs
```

Il wrapper forza `-Full0To10` quando chiama il launcher.

## Gate finale

Dopo il launcher esegue:

```text
Tools/workflow/run_full0to10_manifest_contract_gate.ps1
```

Il gate produce:

```text
full0to10_run_manifest.json
full0to10_bundle_contract_validation.json
```

entrambi sotto `output/validation/...`.
