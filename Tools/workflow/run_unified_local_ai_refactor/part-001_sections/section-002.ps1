
function Test-ResetCandidateIsActiveRunArtifact {
    param([string]$RelativePath)

    if ([string]::IsNullOrWhiteSpace($RelativePath)) { return $false }
    $normalized = $RelativePath.Replace("\", "/")

    $activeStamps = @()
    foreach ($name in @("DataStamp", "Stamp")) {
        $variable = Get-Variable -Name $name -Scope Script -ErrorAction SilentlyContinue
        if ($null -ne $variable -and -not [string]::IsNullOrWhiteSpace([string]$variable.Value)) {
            $activeStamps += [string]$variable.Value
        }
    }

    foreach ($activeStamp in @($activeStamps | Select-Object -Unique)) {
        if ($normalized -like ("output/local_ai_runs/{0}_*" -f $activeStamp)) { return $true }
        if ($normalized -like ("output/ai_packets/{0}/*" -f $activeStamp)) { return $true }
    }

    return $false
}


function Get-ResetCandidates {
    param([string]$Root, [datetime]$BeforeDate, [switch]$IncludeMemory, [switch]$IncludeGeneratedIndex)
    $patterns = @(
        @{ category = "local_ai_runs"; path = "output/local_ai_runs" },
        @{ category = "ai_pipeline"; path = "output/ai_pipeline" },
        @{ category = "validation_reports"; path = "output/validation" },
        @{ category = "ai_context_packs"; path = "output/ai_context_packs" },
        @{ category = "patch_specs"; path = "output/patch_specs" }
    )
    if ($IncludeMemory) {
        $patterns += @{ category = "agent_memory"; path = "indexAI/agent_memory" }
    }
    if ($IncludeGeneratedIndex) {
        $patterns += @{ category = "generated_index_context"; path = "indexAI/code_chunks" }
        $patterns += @{ category = "generated_project_chunks"; path = "indexAI/project_code_chunks" }
    }

    $items = @()
    foreach ($entry in $patterns) {
        $rootPath = Join-Path $Root $entry.path
        if (-not (Test-Path -LiteralPath $rootPath)) { continue }
        $files = Get-ChildItem -LiteralPath $rootPath -Recurse -File -Force -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            if ($BeforeDate -ne [datetime]::MinValue -and $file.LastWriteTime -ge $BeforeDate) { continue }
            $relativePath = Convert-ToRepoRelativePath $Root $file.FullName
            if (Test-ResetCandidateIsActiveRunArtifact -RelativePath $relativePath) { continue }
            $items += [ordered]@{
                path = $relativePath
                category = $entry.category
                last_write_time = $file.LastWriteTime.ToString("o")
                size_bytes = $file.Length
            }
        }
    }
    return @($items | Sort-Object category, path)
}

function Write-ResetPlan {
    param(
        [object[]]$Candidates,
        [string]$OutputJson,
        [string]$OutputMd,
        [datetime]$BeforeDate,
        [bool]$Apply,
        [string]$Root
    )

    $totalBytes = 0
    foreach ($item in @($Candidates)) {
        $totalBytes += [int64]$item.size_bytes
    }

    $resetBefore = $null
    $resetBeforeText = "not set"
    if ($BeforeDate -ne [datetime]::MinValue) {
        $resetBefore = $BeforeDate.ToString("o")
        $resetBeforeText = $resetBefore
    }

    $report = [ordered]@{
        schema_version = 1
        kind = "local_ai_reset_plan"
        repo_root = $Root
        passed = $true
        apply_reset = $Apply
        reset_before_date = $resetBefore
        candidate_count = @($Candidates).Count
        total_size_bytes = $totalBytes
        candidates = $Candidates
        warnings = @("Reset mode is report-only unless -ApplyReset and exact -ConfirmResetText are supplied.")
        errors = @()
    }

    ($report | ConvertTo-Json -Depth 8) |
        Set-Content -LiteralPath $OutputJson -Encoding UTF8

    $lines = New-Object System.Collections.Generic.List[string]
    [void]$lines.Add("# Local AI Reset Plan")
    [void]$lines.Add("")
    [void]$lines.Add(("- Apply reset: ``{0}``" -f $Apply))
    [void]$lines.Add(("- Candidate count: ``{0}``" -f @($Candidates).Count))
    [void]$lines.Add(("- Total bytes: ``{0}``" -f $totalBytes))
    [void]$lines.Add(("- Reset before date: ``{0}``" -f $resetBeforeText))
    [void]$lines.Add("")
    [void]$lines.Add("| Path | Category | Last write time | Size bytes |")
    [void]$lines.Add("|---|---|---|---:|")

    foreach ($item in @($Candidates)) {
        [void]$lines.Add((
            "| ``{0}`` | ``{1}`` | ``{2}`` | {3} |" -f
            $item.path,
            $item.category,
            $item.last_write_time,
            $item.size_bytes
        ))
    }

    $lines | Set-Content -LiteralPath $OutputMd -Encoding UTF8
}



function Resolve-PythonExe {
    param(
        [string]$Requested,
        [string]$Root
    )

    $candidates = @()

    if (-not [string]::IsNullOrWhiteSpace($Requested)) {
        $candidates += $Requested
    }

    if (-not [string]::IsNullOrWhiteSpace($env:IA_CARMINE_PYTHON)) {
        $candidates += $env:IA_CARMINE_PYTHON
    }

    $localVenv = Join-Path $Root ".venv"
    $localVenvPython = Join-Path $localVenv "Scripts/python.exe"

    $candidates += @(
        $localVenvPython,
        (Join-Path $Root "venv/Scripts/python.exe"),
        (Join-Path $Root ".venv314/Scripts/python.exe")
    )

    foreach ($candidate in $candidates) {
        if ([string]::IsNullOrWhiteSpace($candidate)) { continue }

        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    if (-not (Test-Path -LiteralPath $localVenvPython -PathType Leaf)) {
        $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
        if ($pyLauncher) {
            Write-Host "[INFO] Local .venv not found; attempting bootstrap with py -3.12."
            & py -3.12 -m venv $localVenv

            if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $localVenvPython -PathType Leaf)) {
                Write-Host "[INFO] py -3.12 bootstrap failed or unavailable; attempting py -3.13."
                & py -3.13 -m venv $localVenv
            }

            if (Test-Path -LiteralPath $localVenvPython -PathType Leaf) {
                return (Resolve-Path -LiteralPath $localVenvPython).Path
            }
        }
    }
    throw "No repository-owned Python interpreter found. Set -PythonExe or IA_CARMINE_PYTHON to a Python executable under the repository, or create .venv/Scripts/python.exe."
}

function Invoke-Python {
    param([string[]]$PythonArgs)
    & $ResolvedPythonExe @PythonArgs
}


function Get-OptionalPropertyValue {
    param(
        [object]$Object,
        [string]$Name,
        [object]$Default = ""
    )

    if ($null -eq $Object) {
        return $Default
    }

    $Property = $Object.PSObject.Properties[$Name]
    if ($null -eq $Property) {
        return $Default
    }

    if ($null -eq $Property.Value) {
        return $Default
    }

    return $Property.Value
}
