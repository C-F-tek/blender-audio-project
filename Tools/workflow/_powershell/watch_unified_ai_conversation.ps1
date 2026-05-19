param(
    [Parameter(Mandatory = $true)][string]$ObserverDir,
    [int]$RefreshSeconds = 2,
    [int]$Limit = 24
)

$statePath = Join-Path $ObserverDir "current_state.json"
$eventsPath = Join-Path $ObserverDir "ai_public_events.jsonl"
$progressPath = Join-Path $ObserverDir "progress.jsonl"

function Read-ObserverState {
    if (-not (Test-Path -LiteralPath $statePath -PathType Leaf)) { return $null }
    try { return Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json } catch { return $null }
}

while ($true) {
    Clear-Host
    Write-Host "IA-Carmine AI conversation / public agent dialogue" -ForegroundColor Cyan
    Write-Host "ObserverDir: $ObserverDir"
    Write-Host "Hidden chain-of-thought is not exposed. Shows public reports, rationale summaries and decision events."
    Write-Host ""

    $state = Read-ObserverState
    if ($state) {
        Write-Host ("Stamp: {0}" -f $state.stamp)
        Write-Host ("Repo:  {0}" -f $state.repo_root)
    }

    Write-Host ""
    Write-Host "Public AI exchange events:"
    if (Test-Path -LiteralPath $eventsPath -PathType Leaf) {
        Get-Content -LiteralPath $eventsPath -Tail $Limit
    } else {
        Write-Host "No explicit ai_public_events.jsonl events yet."
    }

    Write-Host ""
    Write-Host "Recent phase context:"
    if (Test-Path -LiteralPath $progressPath -PathType Leaf) {
        Get-Content -LiteralPath $progressPath -Tail 10
    }

    if ($state -and $state.repo_root) {
        Write-Host ""
        Write-Host "Latest proposal/recommendation surfaces:"
        $roots = @(
            (Join-Path $state.repo_root "output/ai_pipeline"),
            (Join-Path $state.repo_root "output/patch_specs"),
            (Join-Path $state.repo_root "output/validation"),
            (Join-Path $state.repo_root "output/ai_packets")
        )
        $files = foreach ($root in $roots) {
            if (Test-Path -LiteralPath $root) {
                Get-ChildItem -LiteralPath $root -Recurse -File -Include *.json,*.md -ErrorAction SilentlyContinue |
                    Where-Object { $_.Name -match "proposal|recommend|patch|plan|peer|broker|decision|warning|quality|runtime" }
            }
        }
        $files |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 12 @{Name="LastWrite";Expression={$_.LastWriteTime.ToString("HH:mm:ss")}}, FullName |
            Format-Table -AutoSize -Wrap
    }

    Start-Sleep -Seconds $RefreshSeconds
}
