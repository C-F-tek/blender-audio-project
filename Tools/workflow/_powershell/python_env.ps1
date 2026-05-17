function Test-WorkflowWindowsAppsPython {
    param([string]$PathValue)
    if ([string]::IsNullOrWhiteSpace($PathValue)) { return $false }
    $normalized = $PathValue.Replace("\", "/").ToLowerInvariant()
    return ($normalized -like "*/windowsapps/*" -and [System.IO.Path]::GetFileName($PathValue).ToLowerInvariant().Contains("python"))
}

function Test-WorkflowRepoPython {
    param(
        [string]$PathValue,
        [string]$RepoRoot
    )
    if ([string]::IsNullOrWhiteSpace($PathValue)) { return $false }
    if (-not (Test-Path -LiteralPath $PathValue -PathType Leaf)) { return $false }
    if (Test-WorkflowWindowsAppsPython $PathValue) { return $false }
    $rootPath = (Resolve-Path -LiteralPath $RepoRoot).Path.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
    $resolvedPath = (Resolve-Path -LiteralPath $PathValue).Path
    $normalizedRoot = $rootPath.Replace("\", "/").ToLowerInvariant()
    $normalizedPath = $resolvedPath.Replace("\", "/").ToLowerInvariant()
    return ($normalizedPath -eq $normalizedRoot -or $normalizedPath.StartsWith($normalizedRoot + "/"))
}

function Resolve-WorkflowPython {
    param(
        [string]$RepoRoot = ".",
        [string]$RequestedPython = ""
    )
    $rootPath = (Resolve-Path -LiteralPath $RepoRoot).Path
    $explicitCandidates = @()
    if (-not [string]::IsNullOrWhiteSpace($RequestedPython)) { $explicitCandidates += $RequestedPython }
    if (-not [string]::IsNullOrWhiteSpace($env:IA_CARMINE_PYTHON)) { $explicitCandidates += $env:IA_CARMINE_PYTHON }

    foreach ($candidate in $explicitCandidates) {
        if ([string]::IsNullOrWhiteSpace($candidate)) { continue }
        if (-not (Test-WorkflowRepoPython -PathValue $candidate -RepoRoot $rootPath)) {
            throw "Rejected non-repository IA-CARMINE Python '$candidate'. Use the repository .venv Python, not system PATH Python."
        }
        return (Resolve-Path -LiteralPath $candidate).Path
    }

    $repoCandidates = @(
        (Join-Path $rootPath ".venv\Scripts\python.exe"),
        (Join-Path $rootPath "venv\Scripts\python.exe"),
        (Join-Path $rootPath ".venv314\Scripts\python.exe")
    )
    foreach ($candidate in $repoCandidates) {
        if (Test-WorkflowRepoPython -PathValue $candidate -RepoRoot $rootPath) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }
    throw "No repository-owned provider-capable Python found. Create .venv or set IA_CARMINE_PYTHON to a Python executable inside the repository."
}

function Use-WorkflowPython {
    param(
        [string]$RepoRoot = ".",
        [string]$RequestedPython = ""
    )
    $rootPath = (Resolve-Path -LiteralPath $RepoRoot).Path
    $resolved = Resolve-WorkflowPython -RepoRoot $rootPath -RequestedPython $RequestedPython
    $script:WorkflowPythonExe = $resolved
    $env:IA_CARMINE_PYTHON = $resolved
    $env:PYTHONPATH = $rootPath
    if (Test-Path -LiteralPath $resolved -PathType Leaf) {
        $pythonDir = Split-Path -Parent $resolved
        if ($env:PATH -notlike "*$pythonDir*") {
            $env:PATH = $pythonDir + [System.IO.Path]::PathSeparator + $env:PATH
        }
    }
    Set-Alias -Name python -Value $resolved -Scope Script -Force
    return $resolved
}

function Invoke-WorkflowPython {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    if ([string]::IsNullOrWhiteSpace($script:WorkflowPythonExe)) {
        throw "Workflow Python is not initialized. Call Use-WorkflowPython first."
    }
    & $script:WorkflowPythonExe @Arguments
}
