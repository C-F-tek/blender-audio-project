function Test-WorkflowWindowsAppsPython {
    param([string]$PathValue)
    $normalized = $PathValue.Replace("\", "/").ToLowerInvariant()
    return ($normalized -like "*/windowsapps/*" -and [System.IO.Path]::GetFileName($PathValue).ToLowerInvariant().Contains("python"))
}

function Resolve-WorkflowPython {
    param(
        [string]$RepoRoot = ".",
        [string]$RequestedPython = ""
    )
    $rootPath = (Resolve-Path -LiteralPath $RepoRoot).Path
    $candidates = @()
    if (-not [string]::IsNullOrWhiteSpace($RequestedPython)) { $candidates += $RequestedPython }
    if (-not [string]::IsNullOrWhiteSpace($env:IA_CARMINE_PYTHON)) { $candidates += $env:IA_CARMINE_PYTHON }
    $candidates += @(
        (Join-Path $rootPath ".venv\Scripts\python.exe"),
        (Join-Path $rootPath "venv\Scripts\python.exe"),
        (Join-Path $rootPath ".venv314\Scripts\python.exe")
    )
    foreach ($candidate in $candidates) {
        if ([string]::IsNullOrWhiteSpace($candidate)) { continue }
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand -and -not (Test-WorkflowWindowsAppsPython $pythonCommand.Source)) {
        return $pythonCommand.Source
    }
    throw "No provider-capable Python found. Set IA_CARMINE_PYTHON to the repo .venv Python."
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
