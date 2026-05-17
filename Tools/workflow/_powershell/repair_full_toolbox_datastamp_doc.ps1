<#
.SYNOPSIS
  Repair the Global DataStamp / AI packets section in the canonical full-toolbox procedure.

.DESCRIPTION
  Replaces the malformed section between:
    ### Global DataStamp and AI packets contract
  and:
    ### Runtime tool capability manifest

  This is documentation-only. It does not run providers, Blender, FFmpeg, git commit, git push, or patch apply.
#>
[CmdletBinding()]
param(
    [string]$DocPath = ".\docs\LOCAL_AI_TASKS\full-toolbox-0-to-10-semi-automatic-procedure.md"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $DocPath -PathType Leaf)) {
    throw "Missing procedure document: $DocPath"
}

$ResolvedDocPath = (Resolve-Path -LiteralPath $DocPath).Path
$Doc = Get-Content -LiteralPath $ResolvedDocPath -Raw

$StartHeading = "### Global DataStamp and AI packets contract"
$EndHeading = "### Runtime tool capability manifest"

$Start = $Doc.IndexOf($StartHeading, [System.StringComparison]::Ordinal)
$End = $Doc.IndexOf($EndHeading, [System.StringComparison]::Ordinal)

if ($Start -lt 0) {
    throw "Start heading not found: $StartHeading"
}
if ($End -lt 0) {
    throw "End heading not found: $EndHeading"
}
if ($End -le $Start) {
    throw "Invalid heading order: Runtime tool capability manifest appears before DataStamp section."
}

$Section = @'
### Global DataStamp and AI packets contract

Every unified launcher run must resolve one timestamp only. The run stamp is the single global version key for all run-scoped folders introduced by this contract.

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$DataStamp = $Stamp
```

The run-scoped AI packets directory is:

```powershell
$AiPacketsRoot = ".\output\ai_packets"
$AiPacketsDir = Join-Path $AiPacketsRoot $DataStamp
```

Contract:

```text
output/ai_packets/<DataStamp> is the run packet directory.
It is a directory, not a context file.
Never pass output/ai_packets/<DataStamp> as -ExtraContextFile.
Only concrete files inside the directory may be used as context/report inputs.
```

Allowed packet files include:

```text
output/ai_packets/<DataStamp>/npu_real_workload_report.md
output/ai_packets/<DataStamp>/ollama_gpu_real_workload_report.md
```

The workload-quality gate must receive the directory through:

```powershell
--report-dir $AiPacketsDir
```

The official/local advisory context must receive only concrete files. Before passing `-ExtraContextFile`, sanitize context inputs:

```powershell
$ContextFiles = @($ContextFiles | Where-Object {
    $ContextPath = [string]$_
    -not (Test-Path -LiteralPath $ContextPath -PathType Container)
})
```

Git policy remains unchanged:

```text
Do not commit output/**.
Commit only source, docs, tests, and compact evidence explicitly listed by evidence_to_commit.
```

'@

$Before = $Doc.Substring(0, $Start)
$After = $Doc.Substring($End)
$Fixed = ($Before + $Section + $After).TrimEnd() + "`r`n"

[System.IO.File]::WriteAllText($ResolvedDocPath, $Fixed, [System.Text.UTF8Encoding]::new($false))

$LineCount = (Get-Content -LiteralPath $ResolvedDocPath | Measure-Object -Line).Lines
Write-Host "[OK] Repaired DataStamp section: $ResolvedDocPath"
Write-Host "[OK] Resulting lines: $LineCount"
Write-Host "[OK] No commit or push performed."
