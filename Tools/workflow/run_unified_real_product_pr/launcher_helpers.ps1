function Add-LauncherArg {
    param(
        [string]$Name,
        [string]$Value
    )
    $script:LauncherArgs += @($Name, $Value)
}

function Add-OptionalLauncherArg {
    param(
        [string]$Name,
        [string]$Value
    )
    if (-not [string]::IsNullOrWhiteSpace($Value)) {
        Add-LauncherArg -Name $Name -Value $Value
    }
}

function Add-LauncherSwitch {
    param(
        [string]$Name,
        [bool]$Enabled
    )
    if ($Enabled) {
        $script:LauncherArgs += $Name
    }
}

function Invoke-LocalAiArtifactReset {
    param(
        [string]$Root,
        [string]$LauncherPath,
        [int]$RetentionDays,
        [bool]$IncludeMemory,
        [bool]$IncludeGeneratedIndex,
        [string]$PythonPath
    )

    if ($RetentionDays -lt 0) {
        Stop-RealProductLauncher -Code "invalid_reset_retention_days" -Message "-ResetLocalAiArtifactsRetentionDays must be zero or greater." -Root $Root -StampValue $Stamp
    }

    $ResetBefore = if ($RetentionDays -gt 0) {
        (Get-Date).AddDays(-$RetentionDays).Date
    }
    else {
        (Get-Date).AddSeconds(1)
    }

    $ResetTool = Join-Path $Root "Tools/workflow/run_local_ai_artifact_reset/cli.py"
    if (-not (Test-Path -LiteralPath $ResetTool -PathType Leaf)) {
        Stop-RealProductLauncher -Code "bounded_reset_tool_missing" -Message "Bounded pre-run reset helper missing: $ResetTool" -Root $Root -StampValue $Stamp -DetailPath $ResetTool
    }

    $ResetJson = Join-Path $Root ("output/validation/prerun_local_ai_reset_{0}.json" -f $Stamp)
    $ResetMd = Join-Path $Root ("output/validation/prerun_local_ai_reset_{0}.md" -f $Stamp)

    $ResetArgs = @(
        $ResetTool,
        "--repo-root", $Root,
        "--before-date", $ResetBefore.ToString("s"),
        "--active-stamp", $Stamp,
        "--output", $ResetJson,
        "--markdown-output", $ResetMd
    )

    if (-not $DryRun) {
        $ResetArgs += @("--apply", "--confirm-reset-text", "DELETE LOCAL AI ARTIFACTS")
    }
    if ($IncludeMemory) {
        $ResetArgs += "--include-memory-reset"
    }
    if ($IncludeGeneratedIndex) {
        $ResetArgs += "--include-generated-index-reset"
    }

    Write-Host "=== IA-Carmine bounded pre-run local AI reset ==="
    Write-Host "Reset before: $($ResetBefore.ToString("s"))"
    Write-Host "Retention days: $RetentionDays"
    Write-Host "Include memory reset: $IncludeMemory"
    Write-Host "Include generated index reset: $IncludeGeneratedIndex"
    Write-Host "Active stamp: $Stamp"
    Write-Host "Report: $ResetJson"
    Write-Host "[RUN] $PythonPath $($ResetArgs -join ' ')"

    & $PythonPath @ResetArgs
    if ($LASTEXITCODE -ne 0) {
        Stop-RealProductLauncher -Code "local_ai_prerun_reset_failed" -Message "Pre-run local AI reset failed with exit code $LASTEXITCODE. See $ResetJson" -Root $Root -StampValue $Stamp -DetailPath $ResetJson
    }

    Write-Host "[OK] Bounded pre-run local AI reset completed: $ResetJson"
    Write-Host ""
}
