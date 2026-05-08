param(
    [Parameter(Mandatory = $true)][string]$ObserverDir,
    [int]$RefreshSeconds = 2,
    [int]$Limit = 20
)

$statePath = Join-Path $ObserverDir "current_state.json"
$progressPath = Join-Path $ObserverDir "progress.jsonl"

function Read-ObserverState {
    if (-not (Test-Path -LiteralPath $statePath -PathType Leaf)) { return $null }
    try { return Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json } catch { return $null }
}

while ($true) {
    Clear-Host
    Write-Host "IA-Carmine RAW debug good info" -ForegroundColor Cyan
    Write-Host "ObserverDir: $ObserverDir"
    Write-Host "Shows report-level debug, stdout/stderr tails, report pass/fail counts and process state."
    Write-Host ""

    $state = Read-ObserverState
    if ($state) {
        Write-Host ("Stamp: {0}" -f $state.stamp)
        Write-Host ("Repo:  {0}" -f $state.repo_root)
    }

    Write-Host ""
    Write-Host "Recent progress:"
    if (Test-Path -LiteralPath $progressPath -PathType Leaf) {
        Get-Content -LiteralPath $progressPath -Tail $Limit
    }

    if ($state -and $state.repo_root) {
        Write-Host ""
        Write-Host "Latest JSON reports:"
        $roots = @(
            (Join-Path $state.repo_root "output/validation"),
            (Join-Path $state.repo_root "output/ai_pipeline"),
            (Join-Path $state.repo_root "output/ai_packets"),
            (Join-Path $state.repo_root "docs/LOCAL_VALIDATION_EVIDENCE")
        )
        $reports = foreach ($root in $roots) {
            if (Test-Path -LiteralPath $root) {
                Get-ChildItem -LiteralPath $root -Recurse -File -Include *.json -ErrorAction SilentlyContinue
            }
        }
        $reports |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 16 @{Name="LastWrite";Expression={$_.LastWriteTime.ToString("HH:mm:ss")}}, Length, FullName |
            Format-Table -AutoSize -Wrap
    }

    Write-Host ""
    Write-Host "Processes:"
    Get-CimInstance Win32_Process |
        Where-Object { $_.Name -match "^(powershell|pwsh|python|python.exe|ollama|git)\.exe$" } |
        Select-Object `
            @{Name="MB";Expression={[math]::Round($_.WorkingSetSize / 1MB, 1)}},
            ProcessId,
            ParentProcessId,
            Name,
            @{Name="CommandLine";Expression={
                $cmd = $_.CommandLine
                if ($cmd -and $cmd.Length -gt 120) { $cmd.Substring(0,120) + "..." } else { $cmd }
            }} |
        Sort-Object MB -Descending |
        Format-Table -AutoSize -Wrap

    Start-Sleep -Seconds $RefreshSeconds
}
