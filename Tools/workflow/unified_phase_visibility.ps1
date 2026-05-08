Set-StrictMode -Version Latest

function Write-UnifiedPhaseVisibilityReport {
    param(
        [string]$RepoRoot,
        [string]$PhaseName,
        [string]$Status,
        [string]$StampValue,
        [string]$OutputDir,
        [string]$CommandLine = "",
        [int]$TimeoutSeconds = 0,
        [int]$ReturnCode = 0,
        [double]$ElapsedSeconds = 0,
        [string[]]$Warnings = @(),
        [string[]]$Errors = @(),
        [string[]]$ReportFiles = @()
    )
    if ([string]::IsNullOrWhiteSpace($OutputDir)) { $OutputDir = "output" }
    if ([string]::IsNullOrWhiteSpace($StampValue)) { $StampValue = Get-Date -Format "yyyyMMdd-HHmmss" }
    $ValidationDir = Join-Path $RepoRoot (Join-Path $OutputDir "validation")
    New-Item -ItemType Directory -Force -Path $ValidationDir | Out-Null
    $JsonPath = Join-Path $ValidationDir ("{0}_phase_{1}.json" -f $StampValue, $PhaseName)
    $MdPath = Join-Path $ValidationDir ("{0}_phase_{1}.md" -f $StampValue, $PhaseName)
    $Passed = $Status -eq "passed" -or $Status -eq "skipped"
    $Report = [ordered]@{
        schema_version = 1
        kind = "unified_launcher_phase_status"
        phase = $PhaseName
        selected = $true
        status = $Status
        passed = $Passed
        timeout_seconds = $TimeoutSeconds
        return_code = $ReturnCode
        elapsed_seconds = $ElapsedSeconds
        command_line = $CommandLine
        report_json = $JsonPath.Replace('\\', '/')
        report_markdown = $MdPath.Replace('\\', '/')
        warnings = @($Warnings)
        errors = @($Errors)
        phase_reports = @($ReportFiles)
        provider_execution_performed = $false
        patch_application_performed = $false
        source_writes_performed = $false
        blender_runtime_execution_performed = $false
        ffmpeg_execution_performed = $false
    }
    $Report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $JsonPath -Encoding UTF8
    $Lines = New-Object System.Collections.Generic.List[string]
    [void]$Lines.Add("# Unified launcher phase status")
    [void]$Lines.Add("")
    [void]$Lines.Add(("- Phase: ``{0}``" -f $PhaseName))
    [void]$Lines.Add(("- Status: ``{0}``" -f $Status))
    [void]$Lines.Add(("- Passed: ``{0}``" -f $Passed))
    [void]$Lines.Add(("- Timeout seconds: ``{0}``" -f $TimeoutSeconds))
    [void]$Lines.Add(("- Return code: ``{0}``" -f $ReturnCode))
    [void]$Lines.Add(("- Elapsed seconds: ``{0}``" -f $ElapsedSeconds))
    [void]$Lines.Add("")
    [void]$Lines.Add("## Command")
    [void]$Lines.Add("")
    [void]$Lines.Add(("``{0}``" -f $CommandLine))
    [void]$Lines.Add("")
    [void]$Lines.Add("## Warnings")
    foreach ($Item in @($Warnings)) { [void]$Lines.Add(("- {0}" -f $Item)) }
    if (@($Warnings).Count -eq 0) { [void]$Lines.Add("- none") }
    [void]$Lines.Add("")
    [void]$Lines.Add("## Errors")
    foreach ($Item in @($Errors)) { [void]$Lines.Add(("- {0}" -f $Item)) }
    if (@($Errors).Count -eq 0) { [void]$Lines.Add("- none") }
    $Lines | Set-Content -LiteralPath $MdPath -Encoding UTF8
    return [ordered]@{ json = $JsonPath; markdown = $MdPath; status = $Status; passed = $Passed }
}

function ConvertTo-UnifiedCommandLineArgument {
    param([string]$Value)
    if ($null -eq $Value) { return '""' }
    if ($Value -notmatch '[\s"]') { return $Value }
    return '"' + ($Value -replace '([\\]*)"', '$1$1\"' -replace '([\\]+)$', '$1$1') + '"'
}

function Invoke-UnifiedExternalPhaseCommand {
    param(
        [string]$RepoRoot,
        [string]$PhaseName,
        [string]$StampValue,
        [string]$OutputDir,
        [string]$FilePath,
        [string[]]$Arguments,
        [int]$TimeoutSeconds,
        [switch]$Skip
    )
    if ($Skip) {
        return Write-UnifiedPhaseVisibilityReport -RepoRoot $RepoRoot -PhaseName $PhaseName -Status "skipped" -StampValue $StampValue -OutputDir $OutputDir -TimeoutSeconds $TimeoutSeconds -Warnings @("Phase selected but explicitly skipped by operator flag.")
    }
    if (-not (Test-Path -LiteralPath $FilePath -PathType Leaf)) {
        return Write-UnifiedPhaseVisibilityReport -RepoRoot $RepoRoot -PhaseName $PhaseName -Status "failed" -StampValue $StampValue -OutputDir $OutputDir -TimeoutSeconds $TimeoutSeconds -Errors @("Phase script missing: $FilePath")
    }
    if ($TimeoutSeconds -le 0) { $TimeoutSeconds = 1800 }
    $PhaseDir = Join-Path $RepoRoot (Join-Path $OutputDir ("validation/{0}_phase_{1}_process" -f $StampValue, $PhaseName))
    New-Item -ItemType Directory -Force -Path $PhaseDir | Out-Null
    $StdoutPath = Join-Path $PhaseDir "stdout.log"
    $StderrPath = Join-Path $PhaseDir "stderr.log"
    $AllArgs = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $FilePath) + @($Arguments)
    $CommandLine = "powershell.exe " + ((@($AllArgs) | ForEach-Object { ConvertTo-UnifiedCommandLineArgument ([string]$_) }) -join " ")
    $Started = Get-Date

    $ProcessInfo = New-Object System.Diagnostics.ProcessStartInfo
    $ProcessInfo.FileName = "powershell.exe"
    $ProcessInfo.Arguments = ((@($AllArgs) | ForEach-Object { ConvertTo-UnifiedCommandLineArgument ([string]$_) }) -join " ")
    $ProcessInfo.WorkingDirectory = $RepoRoot
    $ProcessInfo.UseShellExecute = $false
    $ProcessInfo.RedirectStandardOutput = $true
    $ProcessInfo.RedirectStandardError = $true
    $ProcessInfo.CreateNoWindow = $true

    $Process = New-Object System.Diagnostics.Process
    $Process.StartInfo = $ProcessInfo

    try {
        [void]$Process.Start()
        $StdoutTask = $Process.StandardOutput.ReadToEndAsync()
        $StderrTask = $Process.StandardError.ReadToEndAsync()
        $Completed = $Process.WaitForExit($TimeoutSeconds * 1000)
        $Ended = Get-Date
        $Elapsed = [Math]::Round(($Ended - $Started).TotalSeconds, 3)

        if (-not $Completed) {
            try { $Process.Kill() } catch {}
            try { $Process.WaitForExit() } catch {}
            $StdoutText = ""
            $StderrText = ""
            try { $StdoutText = $StdoutTask.Result } catch {}
            try { $StderrText = $StderrTask.Result } catch {}
            $StdoutText | Set-Content -LiteralPath $StdoutPath -Encoding UTF8
            $StderrText | Set-Content -LiteralPath $StderrPath -Encoding UTF8
            return Write-UnifiedPhaseVisibilityReport -RepoRoot $RepoRoot -PhaseName $PhaseName -Status "timeout" -StampValue $StampValue -OutputDir $OutputDir -CommandLine $CommandLine -TimeoutSeconds $TimeoutSeconds -ReturnCode -1 -ElapsedSeconds $Elapsed -Errors @("Phase timed out and process was terminated.") -ReportFiles @($StdoutPath, $StderrPath)
        }

        $Process.WaitForExit()
        $StdoutTask.Wait()
        $StderrTask.Wait()
        $StdoutTask.Result | Set-Content -LiteralPath $StdoutPath -Encoding UTF8
        $StderrTask.Result | Set-Content -LiteralPath $StderrPath -Encoding UTF8
        $ReturnCode = [int]$Process.ExitCode
    } catch {
        $Ended = Get-Date
        $Elapsed = [Math]::Round(($Ended - $Started).TotalSeconds, 3)
        try {
            if ($null -ne $Process -and -not $Process.HasExited) { $Process.Kill() }
        } catch {}
        return Write-UnifiedPhaseVisibilityReport -RepoRoot $RepoRoot -PhaseName $PhaseName -Status "failed" -StampValue $StampValue -OutputDir $OutputDir -CommandLine $CommandLine -TimeoutSeconds $TimeoutSeconds -ReturnCode -2 -ElapsedSeconds $Elapsed -Errors @(("Phase process execution failed: {0}" -f $_.Exception.Message)) -ReportFiles @($StdoutPath, $StderrPath)
    } finally {
        try { $Process.Dispose() } catch {}
    }

    if ($ReturnCode -eq 0) { $Status = "passed" } else { $Status = "failed" }
    $Errors = @()
    if ($ReturnCode -ne 0) { $Errors += ("Phase returned non-zero exit code: {0}" -f $ReturnCode) }
    return Write-UnifiedPhaseVisibilityReport -RepoRoot $RepoRoot -PhaseName $PhaseName -Status $Status -StampValue $StampValue -OutputDir $OutputDir -CommandLine $CommandLine -TimeoutSeconds $TimeoutSeconds -ReturnCode $ReturnCode -ElapsedSeconds $Elapsed -Errors $Errors -ReportFiles @($StdoutPath, $StderrPath)
}
