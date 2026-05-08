param(
    [Parameter(Mandatory = $true)][string]$ObserverDir,
    [int]$RefreshSeconds = 2
)

$progress = Join-Path $ObserverDir "progress.jsonl"
$state = Join-Path $ObserverDir "current_state.json"

while ($true) {
    Clear-Host
    Write-Host "IA-Carmine unified run telemetry observer" -ForegroundColor Cyan
    Write-Host "ObserverDir: $ObserverDir"
    Write-Host ""

    if (Test-Path -LiteralPath $state -PathType Leaf) {
        Get-Content -LiteralPath $state -Raw | Write-Host
    }

    Write-Host ""
    Write-Host "Recent progress:"
    if (Test-Path -LiteralPath $progress -PathType Leaf) {
        Get-Content -LiteralPath $progress -Tail 20
    }

    Write-Host ""
    Write-Host "Processes:"
    Get-CimInstance Win32_Process |
        Where-Object { $_.Name -match '^(powershell|pwsh|python|python.exe|ollama|git)\.exe$' } |
        Select-Object `
            @{Name='MB';Expression={[math]::Round($_.WorkingSetSize / 1MB, 1)}},
            ProcessId,
            ParentProcessId,
            Name,
            @{Name='CommandLine';Expression={
                $cmd = $_.CommandLine
                if ($cmd -and $cmd.Length -gt 120) { $cmd.Substring(0,120) + "..." } else { $cmd }
            }} |
        Sort-Object MB -Descending |
        Format-Table -AutoSize -Wrap

    Start-Sleep -Seconds $RefreshSeconds
}

