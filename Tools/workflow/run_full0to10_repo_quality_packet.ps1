param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_repo_quality_packet",
    [string[]]$InputPath = @(),
    [string]$OutputFile = "output/validation/full0to10_repo_quality_packet/quality.md",
    [string]$Tool = "repo_quality_reader",
    [string]$Request = "Leggi MD e Python del progetto Full0To10 e produci quality packet operativo",
    [switch]$WriteOutput,
    [switch]$AllowOutputOutsideOutput,
    [switch]$DiagnosticsOnly,
    [int]$MaxFiles = 240
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$Base, [string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) { return $PathValue }
    return (Join-Path $Base $PathValue)
}

function Normalize-InputPaths {
    param([string[]]$RawItems)
    $Items = New-Object System.Collections.Generic.List[string]
    foreach ($Raw in $RawItems) {
        if ([string]::IsNullOrWhiteSpace($Raw)) { continue }
        $Parts = $Raw -split "[,;`r`n]+"
        foreach ($Part in $Parts) {
            $Value = $Part.Trim().Trim('"').Trim("'")
            if (-not [string]::IsNullOrWhiteSpace($Value)) {
                $Items.Add($Value)
            }
        }
    }
    return @($Items.ToArray())
}

function Show-PacketSummary {
    param([string]$SummaryPath)
    if (-not (Test-Path $SummaryPath)) {
        Write-Host "[WARN] Repo quality packet summary was not written: $SummaryPath"
        return
    }
    $Packet = Get-Content $SummaryPath -Raw | ConvertFrom-Json
    Write-Host "[INFO] Repo quality packet summary: $SummaryPath"
    Write-Host "[INFO] passed: $($Packet.passed)"
    Write-Host "[INFO] errors: $($Packet.errors | ConvertTo-Json -Compress)"
    Write-Host "[INFO] warnings: $($Packet.warnings | ConvertTo-Json -Compress)"
    if ($Packet.inventory -and $Packet.inventory.items) {
        $Missing = @($Packet.inventory.items | Where-Object { $_.exists -ne $true })
        if ($Missing.Count -gt 0) {
            Write-Host "[WARN] Missing explicit/scanned inputs:"
            $Missing | ForEach-Object { Write-Host "  - $($_.path) kind=$($_.kind)" }
        }
    }
    if ($Packet.user_output) {
        Write-Host "[INFO] user_output: path=$($Packet.user_output.path) written=$($Packet.user_output.written) allowed=$($Packet.user_output.allowed)"
    }
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$NormalizedInputPath = Normalize-InputPaths -RawItems $InputPath
Write-Host "[INFO] Normalized input count: $($NormalizedInputPath.Count)"
foreach ($Item in $NormalizedInputPath) { Write-Host "[INFO] input: $Item" }

$Summary = Join-Path $OutputPath "full0to10_repo_quality_packet.from_cli.json"
$Args = @(
    "--repo-root", $RepoRoot,
    "--output-dir", $OutputPath,
    "--output-file", $OutputFile,
    "--tool", $Tool,
    "--request", $Request,
    "--max-files", $MaxFiles,
    "--output", $Summary
)

foreach ($InputItem in $NormalizedInputPath) {
    $Args += @("--input", $InputItem)
}
if ($WriteOutput) { $Args += "--write-output" }
if ($AllowOutputOutsideOutput) { $Args += "--allow-output-outside-output" }

$ScriptPath = Join-Path $RepoRoot "Tools/ai/build_full0to10_repo_quality_packet.py"
Write-Host "[INFO] Repo quality packet JSON target: $Summary"
Write-Host "[INFO] Repo quality output file: $OutputFile"

$PythonOutput = & python $ScriptPath @Args 2>&1
$ExitCode = $LASTEXITCODE
if ($PythonOutput) { $PythonOutput | ForEach-Object { Write-Host $_ } }

Show-PacketSummary -SummaryPath $Summary

if ($ExitCode -ne 0 -and -not $DiagnosticsOnly) {
    throw "Full0To10 repo quality packet failed with exit code $ExitCode. See: $Summary"
}

Write-Host "[OK] Repo quality packet JSON: $Summary"
Write-Host "[OK] Repo quality packet MD: $(Join-Path $OutputPath 'full0to10_repo_quality_packet.md')"
