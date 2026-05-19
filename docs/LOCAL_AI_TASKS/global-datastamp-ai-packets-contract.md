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

## Exposed launcher parameters

The launcher exposes the AI packet location:

```powershell
-AiPacketsRoot output/ai_packets
-AiPacketsDir  output/ai_packets/<DataStamp>
```

Default resolution:

```powershell
if ([string]::IsNullOrWhiteSpace($AiPacketsRoot)) {
  $AiPacketsRoot = "output/ai_packets"
}

if ([string]::IsNullOrWhiteSpace($AiPacketsDir)) {
  $AiPacketsDir = Join-Path $AiPacketsRoot $DataStamp
}
```

`--report-dir` must be passed to `check_ai_workload_report_quality.py` only inside the `Invoke-Python @(...)` argument array. It must never be emitted as a standalone/orphan PowerShell statement.

## Workload-quality gate

The quality gate reads the run folder:

```powershell
python -m Tools.validation check_ai_workload_report_quality `
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

## Recursive AI packets root selection

`--report-dir output/ai_packets` is valid and means: inspect the root packet folder plus all immediate timestamp packet folders under it.

`--report-dir output/ai_packets/<DataStamp>` remains valid and means: inspect only that run-scoped packet folder.

The tool must select concrete workload report files only. Directories must never be treated as context files.
