param(
    [Parameter(Mandatory = $true)][string]$ObserverDir,
    [int]$RefreshSeconds = 2
)

$events = Join-Path $ObserverDir "ai_public_events.jsonl"
$progress = Join-Path $ObserverDir "progress.jsonl"

while ($true) {
    Clear-Host
    Write-Host "IA-Carmine AI public exchange / agent dialogue / decision log" -ForegroundColor Cyan
    Write-Host "ObserverDir: $ObserverDir"
    Write-Host "Raw hidden chain-of-thought is not exposed here."
    Write-Host ""

    if (Test-Path -LiteralPath $events -PathType Leaf) {
        Get-Content -LiteralPath $events -Tail 30
    } else {
        Write-Host "No AI public exchange events yet."
    }

    Write-Host ""
    Write-Host "Recent phase events:"
    if (Test-Path -LiteralPath $progress -PathType Leaf) {
        Get-Content -LiteralPath $progress -Tail 10
    }

    Start-Sleep -Seconds $RefreshSeconds
}
