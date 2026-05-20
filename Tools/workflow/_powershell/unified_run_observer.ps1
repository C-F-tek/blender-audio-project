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
        [bool]$OpenExtendedConsoles = $false,
        [int]$RefreshSeconds = 2
    )

    if ($Script:UnifiedObserverInitialized) {
        return
    }

    $Script:UnifiedObserverInitialized = $true
    $Script:UnifiedObserverDir = $ObserverDirValue
    $Script:UnifiedObserverStamp = $StampValue
    $Script:UnifiedObserverStartedAt = Get-Date
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
        extended_observer_consoles = $OpenExtendedConsoles
    }
    $state | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $Script:UnifiedObserverDir "current_state.json") -Encoding UTF8

    Write-UnifiedRunProgressEvent -Phase "observer" -Status "initialized"

    if ($OpenConsoles) {
        $exchange = Join-Path $PSScriptRoot "watch_unified_ai_public_exchange.ps1"
        Start-Process powershell.exe -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $exchange, "-ObserverDir", $Script:UnifiedObserverDir, "-RefreshSeconds", "$RefreshSeconds")
    }

    if ($OpenExtendedConsoles) {
        $conversation = Join-Path $PSScriptRoot "watch_unified_ai_conversation.ps1"
        $rawDebug = Join-Path $PSScriptRoot "watch_unified_raw_debug_good_info.ps1"
        Start-Process powershell.exe -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $conversation, "-ObserverDir", $Script:UnifiedObserverDir, "-RefreshSeconds", "$RefreshSeconds")
        Start-Process powershell.exe -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $rawDebug, "-ObserverDir", $Script:UnifiedObserverDir, "-RefreshSeconds", "$RefreshSeconds")
    }
}

function Write-UnifiedRunJsonlLine {
    param([string]$Path, [string]$Line)

    $encoding = [System.Text.UTF8Encoding]::new($false)
    $bytes = $encoding.GetBytes($Line + [Environment]::NewLine)
    $stream = [System.IO.File]::Open(
        $Path,
        [System.IO.FileMode]::Append,
        [System.IO.FileAccess]::Write,
        [System.IO.FileShare]::ReadWrite
    )
    try {
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush()
    }
    finally {
        $stream.Dispose()
    }
}

function Write-UnifiedRunObserverWarning {
    param([string]$Message)
    if ([string]::IsNullOrWhiteSpace($Script:UnifiedObserverDir)) { return }
    $warningPath = Join-Path $Script:UnifiedObserverDir "observer_write_warnings.log"
    try {
        $line = "{0} {1}" -f (Get-Date).ToString("o"), $Message
        Write-UnifiedRunJsonlLine -Path $warningPath -Line $line
    }
    catch {
        # Observer writes are diagnostic-only. Never fail the product launcher.
    }
}

function Write-UnifiedRunJsonl {
    param([string]$FileName, [hashtable]$Event)
    if ([string]::IsNullOrWhiteSpace($Script:UnifiedObserverDir)) { return }
    $path = Join-Path $Script:UnifiedObserverDir $FileName
    $Event["timestamp"] = (Get-Date).ToString("o")
    $Event["stamp"] = $Script:UnifiedObserverStamp
    $line = $Event | ConvertTo-Json -Depth 8 -Compress

    $lastError = $null
    for ($attempt = 1; $attempt -le 5; $attempt++) {
        try {
            Write-UnifiedRunJsonlLine -Path $path -Line $line
            return
        }
        catch {
            $lastError = $_.Exception.Message
            Start-Sleep -Milliseconds (50 * $attempt)
        }
    }

    Write-UnifiedRunObserverWarning -Message ("failed to append {0}: {1}" -f $FileName, $lastError)
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
