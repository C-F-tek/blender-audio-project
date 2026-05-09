Set-StrictMode -Version Latest

function Publish-UnifiedHeapExchangeEvents {
    param(
        [Parameter(Mandatory=$true)][string]$StampValue,
        [Parameter(Mandatory=$true)][string]$OutputDirValue,
        [Parameter(Mandatory=$true)][string]$Root
    )

    if (-not (Get-Command Write-UnifiedRunAiPublicEvent -ErrorAction SilentlyContinue)) {
        Write-Warning "Write-UnifiedRunAiPublicEvent is not available; heap/exchange public events cannot be emitted."
        return 0
    }

    $emitted = 0

    $officialJson = Join-Path $OutputDirValue ("validation/{0}_phase_official.json" -f $StampValue)
    if (Test-Path -LiteralPath $officialJson -PathType Leaf) {
        $source = Convert-ToRepoRelativePath -Root $Root -PathValue $officialJson
        Write-UnifiedRunAiPublicEvent `
            -Lane "official" `
            -Speaker "official_adapter" `
            -EventType "decision" `
            -Summary "Official adapter phase report is available for the current heap/exchange run." `
            -SourceFile $source
        $emitted++
    }

    $aiPipelineDir = Join-Path $OutputDirValue "ai_pipeline"
    if (Test-Path -LiteralPath $aiPipelineDir -PathType Container) {
        $proposalReports = Get-ChildItem -LiteralPath $aiPipelineDir -File -Filter ("*_ollama_proposals_{0}.json" -f $StampValue) -ErrorAction SilentlyContinue
        foreach ($file in @($proposalReports)) {
            $source = Convert-ToRepoRelativePath -Root $Root -PathValue $file.FullName
            Write-UnifiedRunAiPublicEvent `
                -Lane "provider" `
                -Speaker "ollama" `
                -EventType "proposal" `
                -Summary "Ollama provider proposal surface was produced for the current heap/exchange run." `
                -SourceFile $source
            $emitted++
        }

        $advisoryReports = Get-ChildItem -LiteralPath $aiPipelineDir -File -Filter ("*_ollama_{0}.json" -f $StampValue) -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -notmatch "_manifest\.json$" -and $_.Name -notmatch "_proposals_" }

        foreach ($file in @($advisoryReports)) {
            $source = Convert-ToRepoRelativePath -Root $Root -PathValue $file.FullName
            Write-UnifiedRunAiPublicEvent `
                -Lane "provider" `
                -Speaker "ollama" `
                -EventType "recommendation" `
                -Summary "Ollama advisory report was produced for the current heap/exchange run." `
                -SourceFile $source
            $emitted++
        }
    }

    $patchSpecManifest = Join-Path $OutputDirValue ("patch_specs/{0}_official_adapter_patch_specs_manifest.json" -f $StampValue)
    if (Test-Path -LiteralPath $patchSpecManifest -PathType Leaf) {
        $source = Convert-ToRepoRelativePath -Root $Root -PathValue $patchSpecManifest
        Write-UnifiedRunAiPublicEvent `
            -Lane "patch_specs" `
            -Speaker "official_adapter" `
            -EventType "patch_spec_manifest" `
            -Summary "Generated patch-spec manifest was produced for the current heap/exchange run." `
            -SourceFile $source
        $emitted++
    }

    if ($emitted -eq 0) {
        Write-Warning "No heap/exchange public events were emitted for stamp $StampValue; chain contract may fail."
    }

    return $emitted
}

function Reset-UnifiedNonProductArtifactsBeforeReviewBridge {
    param(
        [Parameter(Mandatory=$true)][string]$StampValue,
        [Parameter(Mandatory=$true)][string]$Root,
        [Parameter(Mandatory=$true)][string]$RunDirValue,
        [Parameter(Mandatory=$true)][string]$EvidenceDirValue
    )

    $archiveRoot = Join-Path $RunDirValue "nonproduct_artifacts_before_review_bridge"
    New-Item -ItemType Directory -Force -Path $archiveRoot | Out-Null

    $generatedChunkFiles = @(
        "indexAI/code_chunks/semantic_code_chunks.json",
        "indexAI/code_chunks/semantic_code_chunks_manifest.json"
    )

    foreach ($relativePath in $generatedChunkFiles) {
        $fullPath = Join-Path $Root $relativePath
        if (Test-Path -LiteralPath $fullPath -PathType Leaf) {
            & git restore --worktree -- $relativePath
            if ($LASTEXITCODE -ne 0) {
                throw "failed to restore non-product generated chunk artifact: $relativePath"
            }
        }
    }

    $evidenceRoot = Join-Path $Root $EvidenceDirValue
    if (Test-Path -LiteralPath $evidenceRoot -PathType Container) {
        $evidenceFiles = Get-ChildItem -LiteralPath $evidenceRoot -File -Filter ("{0}*" -f $StampValue) -ErrorAction SilentlyContinue
        foreach ($file in @($evidenceFiles)) {
            $relative = Convert-ToRepoRelativePath -Root $Root -PathValue $file.FullName
            $target = Join-Path $archiveRoot $relative
            $targetDir = Split-Path $target -Parent
            New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
            Move-Item -LiteralPath $file.FullName -Destination $target -Force
        }
    }
}

function Assert-UnifiedReviewBridgeCleanTree {
    $status = @(& git status --short)
    if ($LASTEXITCODE -ne 0) {
        throw "git status failed while checking review bridge cleanliness"
    }

    if (@($status).Count -gt 0) {
        $joined = ($status -join [Environment]::NewLine)
        throw "review bridge requires a clean working tree after non-product artifact cleanup. Remaining status:$([Environment]::NewLine)$joined"
    }
}

function Invoke-UnifiedHeapExchangePreReviewBridge {
    param(
        [Parameter(Mandatory=$true)][string]$StampValue,
        [Parameter(Mandatory=$true)][string]$OutputDirValue,
        [Parameter(Mandatory=$true)][string]$Root,
        [Parameter(Mandatory=$true)][string]$RunDirValue,
        [Parameter(Mandatory=$true)][string]$EvidenceDirValue
    )

    $emitted = Publish-UnifiedHeapExchangeEvents `
        -StampValue $StampValue `
        -OutputDirValue $OutputDirValue `
        -Root $Root

    Reset-UnifiedNonProductArtifactsBeforeReviewBridge `
        -StampValue $StampValue `
        -Root $Root `
        -RunDirValue $RunDirValue `
        -EvidenceDirValue $EvidenceDirValue

    Assert-UnifiedReviewBridgeCleanTree

    Write-Host ("[HEAP-EXCHANGE] Pre-review bridge ready. emitted_events={0}" -f $emitted)
}
