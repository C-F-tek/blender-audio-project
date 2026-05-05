param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/light_full0to10_evidence",
    [string]$TrackName = "current",
    [int]$MaxRepoQualityFiles = 180,
    [int]$TimeoutSeconds = 8,
    [switch]$NoExternalProbes,
    [switch]$Strict,
    [switch]$SkipMarkdownLineCheck,
    [switch]$SkipFinalProduct
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$Base, [string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return $PathValue
    }
    return (Join-Path $Base $PathValue)
}

function New-Step {
    param(
        [string]$Name,
        [string]$Command,
        [string]$Status,
        [int]$ExitCode,
        [string]$Output
    )
    [PSCustomObject]@{
        name = $Name
        command = $Command
        status = $Status
        exit_code = $ExitCode
        output = $Output
    }
}

function Invoke-LightStep {
    param(
        [string]$Name,
        [string]$ScriptPath,
        [string[]]$Arguments,
        [switch]$Optional
    )

    if (-not (Test-Path $ScriptPath)) {
        $Status = if ($Optional) { "skipped_missing_optional" } else { "missing_required" }
        Write-Host ("[WARN] {0}: {1} ({2})" -f $Name, $Status, $ScriptPath)
        return New-Step -Name $Name -Command $ScriptPath -Status $Status -ExitCode 127 -Output ""
    }

    $CommandText = "{0} {1}" -f $ScriptPath, ($Arguments -join " ")
    Write-Host ("[RUN] {0}" -f $Name)
    $OutputText = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ScriptPath @Arguments 2>&1
    $ExitCode = $LASTEXITCODE

    if ($OutputText) {
        $OutputText | ForEach-Object { Write-Host $_ }
    }

    if ($ExitCode -ne 0) {
        Write-Host ("[WARN] {0} failed with exit code {1}" -f $Name, $ExitCode)
        return New-Step -Name $Name -Command $CommandText -Status "failed" -ExitCode $ExitCode -Output (($OutputText | Out-String).Trim())
    }

    return New-Step -Name $Name -Command $CommandText -Status "passed" -ExitCode 0 -Output (($OutputText | Out-String).Trim())
}

function Invoke-PythonStep {
    param(
        [string]$Name,
        [string]$PythonScript,
        [string[]]$Arguments,
        [switch]$Optional
    )

    if (-not (Test-Path $PythonScript)) {
        $Status = if ($Optional) { "skipped_missing_optional" } else { "missing_required" }
        Write-Host ("[WARN] {0}: {1} ({2})" -f $Name, $Status, $PythonScript)
        return New-Step -Name $Name -Command $PythonScript -Status $Status -ExitCode 127 -Output ""
    }

    $CommandText = "python {0} {1}" -f $PythonScript, ($Arguments -join " ")
    Write-Host ("[RUN] {0}" -f $Name)
    $OutputText = & python $PythonScript @Arguments 2>&1
    $ExitCode = $LASTEXITCODE

    if ($OutputText) {
        $OutputText | ForEach-Object { Write-Host $_ }
    }

    if ($ExitCode -ne 0) {
        Write-Host ("[WARN] {0} failed with exit code {1}" -f $Name, $ExitCode)
        return New-Step -Name $Name -Command $CommandText -Status "failed" -ExitCode $ExitCode -Output (($OutputText | Out-String).Trim())
    }

    return New-Step -Name $Name -Command $CommandText -Status "passed" -ExitCode 0 -Output (($OutputText | Out-String).Trim())
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$Steps = New-Object System.Collections.Generic.List[object]
$NoProbeArgs = @()
if ($NoExternalProbes) {
    $NoProbeArgs += "-NoExternalProbes"
}

$Steps.Add((Invoke-LightStep -Name "startup_guard" -ScriptPath (Join-Path $RepoRoot "Tools/workflow/run_full0to10_startup_check_guard.ps1") -Arguments @("-RepoRoot", $RepoRoot, "-OutputDir", (Join-Path $OutputPath "startup"), "-TrackName", $TrackName) -Optional))
$Steps.Add((Invoke-LightStep -Name "track_inputs" -ScriptPath (Join-Path $RepoRoot "Tools/workflow/run_full0to10_track_input_contract.ps1") -Arguments @("-RepoRoot", $RepoRoot, "-OutputDir", (Join-Path $OutputPath "track_inputs"), "-TrackName", $TrackName) -Optional))

$RepoQualityInputs = @(".\README.md", ".\docs", ".\Tools\ai", ".\Tools\workflow", ".\Tools\validation")
$RepoQualityArgs = @(
    "-RepoRoot", $RepoRoot,
    "-OutputDir", (Join-Path $OutputPath "repo_quality"),
    "-InputPath", ($RepoQualityInputs -join ","),
    "-OutputFile", (Join-Path $OutputPath "repo_quality/quality.md"),
    "-Tool", "light_full0to10_repo_quality_reader",
    "-Request", "Light Full0To10 evidence-only repo quality packet",
    "-MaxFiles", "$MaxRepoQualityFiles",
    "-WriteOutput"
)
$Steps.Add((Invoke-LightStep -Name "repo_quality" -ScriptPath (Join-Path $RepoRoot "Tools/workflow/run_full0to10_repo_quality_packet.ps1") -Arguments $RepoQualityArgs -Optional))

if (-not $SkipMarkdownLineCheck) {
    $Steps.Add((Invoke-PythonStep -Name "markdown_line_limit" -PythonScript (Join-Path $RepoRoot "Tools/validation/check_markdown_line_limits.py") -Arguments @("--repo-root", $RepoRoot, "--max-lines", "400", "--output", (Join-Path $OutputPath "markdown_line_limit.json")) -Optional))
}

$ProviderArgs = @("-RepoRoot", $RepoRoot, "-TimeoutSeconds", "$TimeoutSeconds") + $NoProbeArgs
$Steps.Add((Invoke-LightStep -Name "accelerator_control" -ScriptPath (Join-Path $RepoRoot "Tools/workflow/run_full0to10_accelerator_control.ps1") -Arguments ($ProviderArgs + @("-OutputDir", (Join-Path $OutputPath "accelerator_control"), "-Request", "Light Full0To10 accelerator evidence")) -Optional))
$Steps.Add((Invoke-LightStep -Name "provider_governor" -ScriptPath (Join-Path $RepoRoot "Tools/workflow/run_full0to10_provider_governor.ps1") -Arguments ($ProviderArgs + @("-OutputDir", (Join-Path $OutputPath "provider_governor"), "-Request", "Light Full0To10 provider governor evidence")) -Optional))
$Steps.Add((Invoke-LightStep -Name "provider_invocation_plan" -ScriptPath (Join-Path $RepoRoot "Tools/workflow/run_full0to10_provider_invocation_plan.ps1") -Arguments ($ProviderArgs + @("-OutputDir", (Join-Path $OutputPath "provider_invocation_plan"), "-Request", "Light Full0To10 provider dry-run invocation plan")) -Optional))
$Steps.Add((Invoke-LightStep -Name "provider_execution_bridge" -ScriptPath (Join-Path $RepoRoot "Tools/workflow/run_full0to10_provider_execution_bridge.ps1") -Arguments ($ProviderArgs + @("-OutputDir", (Join-Path $OutputPath "provider_execution_bridge"), "-Request", "Light Full0To10 provider execution bridge")) -Optional))

if (-not $SkipFinalProduct) {
    $FinalArgs = @("--repo-root", $RepoRoot, "--output-dir", (Join-Path $OutputPath "final_product"), "--request", "Light Full0To10 final product evidence", "--no-external-probes", "--timeout-seconds", "$TimeoutSeconds", "--output", (Join-Path $OutputPath "final_product.from_cli.json"))
    $Steps.Add((Invoke-PythonStep -Name "final_tool_product" -PythonScript (Join-Path $RepoRoot "Tools/ai/build_full0to10_final_tool_product.py") -Arguments $FinalArgs -Optional))
}

$Failed = @($Steps | Where-Object { $_.status -eq "failed" -or $_.status -eq "missing_required" })
$Report = [PSCustomObject]@{
    kind = "full0to10_light_evidence_only_run"
    passed = ($Failed.Count -eq 0)
    strict = [bool]$Strict
    output_dir = $OutputPath
    step_count = $Steps.Count
    failed_count = $Failed.Count
    steps = $Steps
    provider_execution_performed = $false
    patch_application_performed = $false
    blender_runtime_execution_performed = $false
    ffmpeg_execution_performed = $false
}

$JsonPath = Join-Path $OutputPath "full0to10_light_evidence_only_run.json"
$MdPath = Join-Path $OutputPath "full0to10_light_evidence_only_run.md"
$Report | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $JsonPath

$Lines = New-Object System.Collections.Generic.List[string]
$Lines.Add("# Full0To10 light evidence-only run")
$Lines.Add("")
$Lines.Add(('- Passed: `{0}`' -f $Report.passed))
$Lines.Add(('- Steps: `{0}`' -f $Report.step_count))
$Lines.Add(('- Failed: `{0}`' -f $Report.failed_count))
$Lines.Add("")
$Lines.Add("## Steps")
$Lines.Add("")
foreach ($Step in $Steps) {
    $Lines.Add(('- `{0}` status=`{1}` exit=`{2}`' -f $Step.name, $Step.status, $Step.exit_code))
}
$Lines.Add("")
$Lines | Set-Content -Encoding UTF8 $MdPath

Write-Host ("[OK] Light evidence JSON: {0}" -f $JsonPath)
Write-Host ("[OK] Light evidence MD: {0}" -f $MdPath)

if ($Strict -and $Failed.Count -gt 0) {
    throw ("Light evidence-only run failed in strict mode. See: {0}" -f $JsonPath)
}
