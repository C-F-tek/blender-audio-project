[CmdletBinding()]
param(
    [string]$RepoRoot = ".",
    [string]$Stamp = "",
    [string]$OutputRoot = "output",
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [string]$TaskMarkdown = "docs/LOCAL_AI_TASKS/patch-notes-quality-product-2026-05-07.md",
    [string]$IssueNumber = "",
    [switch]$RunGpuNpuProvider,
    [switch]$RequireProviderArtifacts,
    [switch]$RunLegacyNpuAuditorProvider,
    [switch]$SkipMemoryReload,
    [switch]$SkipPostValidationPacket,
    [switch]$SkipSharedToolboxBundle,
    [switch]$UseLegacyPowerShellImplementation,
    [switch]$BuildEvidence,
    [switch]$GeneratePatchSpecs,
    [switch]$ContinueOnValidationError,
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
    [ValidateSet("startup", "deferred", "live-seed-only", "disabled", "final-provider")]
    [string]$NpuMicroStartMode = "deferred",
    [switch]$SkipNpuMicroProvider,
    [switch]$SkipNpuLiveToolSeed,
    [int]$NpuMicroMaxLiveProviderRounds = 0,
    [int]$MinRecommendations = 1,
    [int]$MinPatchPlans = 1,
    [int]$RepositoryConsistencyMapWorkers = 8,
    [ValidateSet("process", "thread", "auto")]
    [string]$RepositoryConsistencyMapWorkerBackend = "process",
    [double]$RepositoryConsistencyMapWorkerCpuTarget = 0.40,
    [int]$RepositoryConsistencyMapMaxAutoWorkers = 8
)

$ErrorActionPreference = "Stop"
$PythonRunner = Join-Path $PSScriptRoot "run_agent_review_full_toolbox_decision_loop.py"
if (-not (Test-Path -LiteralPath $PythonRunner -PathType Leaf)) {
    throw "Full toolbox decision-loop Python runner not found: $PythonRunner"
}

$PythonEnvScript = Join-Path $PSScriptRoot "python_env.ps1"
. $PythonEnvScript
$RepoRootPath = (Resolve-Path -LiteralPath $RepoRoot).Path
$PythonExe = Use-WorkflowPython -RepoRoot $RepoRootPath

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
