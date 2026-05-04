# Global DataStamp and AI packets output contract

## Contract

The unified launcher resolves the run stamp once:

```powershell
if ([string]::IsNullOrWhiteSpace($Stamp)) {
  $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
}
$DataStamp = $Stamp
```

`$DataStamp` is the only per-run version key used for generated run folders introduced by this contract.

## AI packets folder

Canonical root:

```text
output/ai_packets
```

Run-scoped folder:

```text
output/ai_packets/<DataStamp>
```

Launcher variable:

```powershell
$AiPacketsRoot = "output/ai_packets"
$AiPacketsDir = Join-Path $AiPacketsRoot $DataStamp
```

Provider workload reports for the run should be written inside `$AiPacketsDir`, for example:

```text
output/ai_packets/<DataStamp>/npu_real_workload_report.md
output/ai_packets/<DataStamp>/ollama_gpu_real_workload_report.md
```

## Workload-quality gate

The quality gate reads the run folder:

```powershell
python .\Tools\validation\check_ai_workload_report_quality.py `
  --repo-root . `
  --report-dir $AiPacketsDir `
  --output .\output\validation\ai_workload_report_quality.json
```

Default behavior:

```text
existing known reports -> selected and validated
missing known reports  -> unselected_known_reports + warnings
explicit --report path -> strict, missing file is blocking
```

## Final bundle

The final bundle/evidence flow should reference the exact `$AiPacketsDir` path. This keeps push-final selection deterministic:

```text
bundle source = output/ai_packets/<DataStamp>
```

No other timestamp should be generated during the same run for this packet folder.
