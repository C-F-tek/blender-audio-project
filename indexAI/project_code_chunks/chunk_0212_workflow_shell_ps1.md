# Project Code Chunk 212/212

- File: `workflow_shell.ps1`
- Part: `1`
- Lines: `1-35`

## Content
```ps1
00001: param(
00002:     [switch]$DebugMode,
00003:     [switch]$SkipStartupCheck
00004: )
00005: 
00006: $ErrorActionPreference = "Stop"
00007: $Project = Split-Path -Parent $MyInvocation.MyCommand.Path
00008: $Root = Split-Path -Parent $Project
00009: $NpuPython = Join-Path $Root "venvs\blender-npu-ai\Scripts\python.exe"
00010: $ShellScript = Join-Path $Project "Tools\workflow\workflow_shell.py"
00011: $StartupPreflight = Join-Path $Project "Tools\workflow\startup_preflight.ps1"
00012: 
00013: if (Test-Path -LiteralPath $NpuPython) {
00014:     $null = & $NpuPython -c "print('ok')" 2>&1
00015:     if ($LASTEXITCODE -eq 0) {
00016:         $Python = $NpuPython
00017:     } else {
00018:         Write-Host "NPU Python presente ma non avviabile; uso python di sistema per la shell workflow." -ForegroundColor Yellow
00019:         $Python = "python"
00020:     }
00021: } else {
00022:     $Python = "python"
00023: }
00024: 
00025: if ($DebugMode) {
00026:     Write-Host "Python: $Python"
00027:     Write-Host "Shell : $ShellScript"
00028: }
00029: 
00030: if (-not $SkipStartupCheck -and (Test-Path -LiteralPath $StartupPreflight)) {
00031:     . $StartupPreflight
00032:     $null = Invoke-SpaziotempoStartupCheck -Project $Project -Root $Root -Python $Python
00033: }
00034: 
00035: & $Python $ShellScript
```
