[CmdletBinding()]
param(
    [string]$RepoRoot = ".",
    [string]$Stamp = "",
    [string]$OutputRoot = "output",
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [switch]$RunGpuNpuProvider,
    [switch]$RequireProviderArtifacts,
    [switch]$RunLegacyNpuAuditorProvider,
    [switch]$SkipMemoryReload,
    [switch]$SkipPostValidationPacket,
    [switch]$SkipSharedToolboxBundle,
    [switch]$UseLegacyPowerShellImplementation,
    [int]$BudgetMinutes = 30,
    [int]$MaxRounds = 20,
    [int]$FilesPerRound = 8,
    [int]$MaxContextFiles = 220,
    [int]$MaxCharsPerFile = 6000,
    [int]$MaxNewTokens = 3600,
    [int]$MaxRecommendations = 20,
    [int]$MaxPatchPlans = 20,
    [string]$KeepAlive = "35m",
    [int]$NpuAuditorEveryRounds = 3,
    [int]$NpuAuditorTimeoutSeconds = 420,
    [int]$NpuMaxContextChars = 8000,
    [int]$NpuMaxPromptChars = 1200,
    [int]$NpuMaxNewTokens = 384,
    [int]$NpuMicroTimeoutSeconds = 60,
    [int]$NpuMicroBrokerTimeoutSeconds = 90,
    [int]$NpuFinalWaitSeconds = 180,
    [ValidateSet("startup", "deferred", "live-seed-only", "disabled")]
    [string]$NpuMicroStartMode = "deferred",
    [switch]$SkipNpuMicroProvider,
    [switch]$SkipNpuLiveToolSeed,
    [int]$NpuMicroMaxLiveProviderRounds = 0,
    [int]$MinRecommendations = 1,
    [int]$MinPatchPlans = 1,
    [int]$RepositoryConsistencyMapWorkers = 0
)

$ErrorActionPreference = "Stop"
$PythonRunner = Join-Path $PSScriptRoot "run_agent_review_full_toolbox_decision_loop.py"
if (-not (Test-Path -LiteralPath $PythonRunner -PathType Leaf)) {
    throw "Full toolbox decision-loop Python runner not found: $PythonRunner"
}

$PythonExe = "python"
if (-not [string]::IsNullOrWhiteSpace($env:IA_CARMINE_PYTHON) -and (Test-Path -LiteralPath $env:IA_CARMINE_PYTHON -PathType Leaf)) {
    $PythonExe = $env:IA_CARMINE_PYTHON
} elseif (Test-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\.venv\Scripts\python.exe") -PathType Leaf) {
    $PythonExe = (Resolve-Path (Join-Path $PSScriptRoot "..\..\.venv\Scripts\python.exe")).Path
}

$ForwardArgs = @($PythonRunner)
foreach ($Key in $PSBoundParameters.Keys) {
    $Value = $PSBoundParameters[$Key]
    if ($Value -is [System.Management.Automation.SwitchParameter]) {
        if ($Value.IsPresent) {
            $ForwardArgs += "--$Key"
        }
    } else {
        $ForwardArgs += "--$Key"
        $ForwardArgs += "$Value"
    }
}

& $PythonExe @ForwardArgs
if ($null -ne $LASTEXITCODE) {
    exit $LASTEXITCODE
}
