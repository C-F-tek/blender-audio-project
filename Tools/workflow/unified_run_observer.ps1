$Script:UnifiedObserverDir = ""
$Script:UnifiedObserverStamp = ""
$Script:UnifiedObserverStartedAt = Get-Date
$Script:UnifiedObserverInitialized = $false

function Initialize-UnifiedRunObserver {
    param(
        [string]$StampValue,
        [string]$ObserverDirValue,
        [string]$RepoRootValue,
        [string]$RunDirValue,
        [bool]$OpenConsoles = $false,
        [int]$RefreshSeconds = 2
    )
    if ($Script:UnifiedObserverInitialized) {
        return
    }

    $Script:UnifiedObserverInitialized = $true
    $Script:UnifiedObserverDir = $ObserverDirValue
    $Script:UnifiedObserverStamp = $StampValue
    $Script:UnifiedObserverStartedAt = Get-Date
$Script:UnifiedObserverInitialized = $false
    New-Item -ItemType Directory -Force -Path $Script:UnifiedObserverDir | Out-Null

    $state = [ordered]@{
        kind = "unified_run_observer_state"
        schema_version = 1
        stamp = $StampValue
        repo_root = $RepoRootValue
        run_dir = $RunDirValue
        observer_dir = $Script:UnifiedObserverDir
        started_at = $Script:UnifiedObserverStartedAt.ToString("o")
        raw_thinking_exposed = $false
        ai_public_exchange_only = $true
    }
    $state | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $Script:UnifiedObserverDir "current_state.json") -Encoding UTF8

    Write-UnifiedRunProgressEvent -Phase "observer" -Status "initialized"

    if ($OpenConsoles) {
        $telemetry = Join-Path $PSScriptRoot "watch_unified_run_telemetry.ps1"
        $exchange = Join-Path $PSScriptRoot "watch_unified_ai_public_exchange.ps1"
        Start-Process powershell.exe -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $telemetry, "-ObserverDir", $Script:UnifiedObserverDir, "-RefreshSeconds", "$RefreshSeconds")
        Start-Process powershell.exe -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $exchange, "-ObserverDir", $Script:UnifiedObserverDir, "-RefreshSeconds", "$RefreshSeconds")
    }
}

function Write-UnifiedRunJsonl {
    param([string]$FileName, [hashtable]$Event)
    if ([string]::IsNullOrWhiteSpace($Script:UnifiedObserverDir)) { return }
    $path = Join-Path $Script:UnifiedObserverDir $FileName
    $Event["timestamp"] = (Get-Date).ToString("o")
    $Event["stamp"] = $Script:UnifiedObserverStamp
    ($Event | ConvertTo-Json -Depth 8 -Compress) | Add-Content -LiteralPath $path -Encoding UTF8
}

function Write-UnifiedRunProgressEvent {
    param([string]$Phase, [string]$Status, [string]$Message = "")
    $elapsed = [math]::Round(((Get-Date) - $Script:UnifiedObserverStartedAt).TotalSeconds, 3)
    Write-UnifiedRunJsonl -FileName "progress.jsonl" -Event @{
        kind = "unified_run_progress_event"
        schema_version = 1
        phase = $Phase
        status = $Status
        message = $Message
        elapsed_seconds = $elapsed
    }
}

function Write-UnifiedRunAiPublicEvent {
    param([string]$Lane, [string]$Speaker, [string]$EventType, [string]$Summary, [string]$SourceFile = "")
    Write-UnifiedRunJsonl -FileName "ai_public_events.jsonl" -Event @{
        kind = "ai_public_exchange_event"
        schema_version = 1
        lane = $Lane
        speaker = $Speaker
        event_type = $EventType
        summary = $Summary
        source_file = $SourceFile
        raw_thinking_exposed = $false
    }
}

