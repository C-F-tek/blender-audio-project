function Invoke-CommandChecked {
    param(
        [string]$Label,
        [scriptblock]$Block
    )
    Write-Host ""
    Write-Host "=== $Label ==="
    if ($DryRun) {
        Write-Host "[DRY-RUN] Skipped execution."
        return
    }
    & $Block 2>&1 | ForEach-Object {
        Write-Host $_
    }
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

function Invoke-LocalAiTaskPipelineValidation {
    param(
        [bool]$RunMultistepProviderWorkflow,
        [bool]$RunOllamaProbe,
        [bool]$RunNpuProbe,
        [bool]$RunNpuDecodeSmoke,
        [bool]$UsePrimaryAdvisoryProvider,
        [bool]$GeneratePatchSpecs,
        [string]$Model,
        [string]$Profile,
        [string]$PipelineRel,
        [string]$PipelineDir,
        [string]$Basename,
        [string]$ProposalBasename,
        [string]$MultistepBasename,
        [string]$MultistepProposalBasename,
        [string]$MultistepEvidenceBasename,
        [string[]]$ContextFiles,
        [string[]]$ReportFiles,
        [string]$MaxContextChars,
        [string]$RepoRootPath,
        [string]$PythonExe
    )

    if ([string]::IsNullOrWhiteSpace($PythonExe)) {
        throw "Pipeline validation requires resolved repository-owned PythonExe. Call Use-WorkflowPython in the parent workflow."
    }
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
        throw "Resolved repository-owned PythonExe does not exist: $PythonExe"
    }

    if ($RunMultistepProviderWorkflow) {
        $MultistepArgs = @(
            "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", ".\Tools\workflow\run_parallel_ai_provider_multistep.ps1",
            "-RepoRoot", ".",
            "-Profile", $Profile,
            "-OutputDir", $PipelineRel,
            "-Basename", $MultistepBasename,
            "-ProposalBasename", $MultistepProposalBasename,
            "-EvidenceBasename", $MultistepEvidenceBasename,
            "-ContextFile", ($ContextFiles -join ","),
            "-MaxContextChars", "$MaxContextChars",
            "-PythonExe", $PythonExe
        )
        if ($RunOllamaProbe) { $MultistepArgs += "-RunOllamaProbe" }
        if ($RunNpuProbe) { $MultistepArgs += "-RunNpuProbe" }
        if ($RunNpuDecodeSmoke) { $MultistepArgs += "-RunNpuDecodeSmoke" }
        if ($UsePrimaryAdvisoryProvider) { $MultistepArgs += "-UsePrimaryAdvisoryProvider" }
        if ($Model -ne "") { $MultistepArgs += @("-Model", $Model) }

        Invoke-CommandChecked -Label "Run explicit multistep provider workflow" -Block { powershell.exe @MultistepArgs }
    }

    $PacketArgs = @(
        "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", ".\Tools\workflow\run_post_validation_ai_packet.ps1",
        "-RepoRoot", ".",
        "-Profile", $Profile,
        "-OutputDir", $PipelineRel,
        "-Basename", $Basename,
        "-ProposalBasename", $ProposalBasename,
        "-ContextFile", ($ContextFiles -join ","),
        "-ReportFile", ($ReportFiles -join ","),
        "-MaxContextChars", "$MaxContextChars"
    )
    if ($UsePrimaryAdvisoryProvider) { $PacketArgs += "-UsePrimaryAdvisoryProvider" }
    if ($Model -ne "") { $PacketArgs += @("-Model", $Model) }

    Invoke-CommandChecked -Label "Build advisory packet and repository proposals" -Block { powershell.exe @PacketArgs }

    $ProposalPath = Join-Path $PipelineDir "$ProposalBasename.json"
    $ProposalRel = Get-RepoRelativePath $RepoRootPath $ProposalPath
    $ProposalValidationOutput = "output/validation/${Basename}_repository_change_proposals_contract.json"
    $PatchManifest = ""
    $PatchManifestMd = ""

    if (Test-Path -LiteralPath $ProposalPath -PathType Leaf) {
        Invoke-CommandChecked -Label "Validate repository change proposals" -Block {
            & $PythonExe .\Tools\validation\check_repository_change_proposals.py --repo-root . --proposal $ProposalRel --output $ProposalValidationOutput
        }
    }
    else {
        Write-Warning "Proposal file was not produced: $ProposalRel"
    }

    if ($GeneratePatchSpecs -and (Test-Path -LiteralPath $ProposalPath -PathType Leaf)) {
        $PatchBasename = "${Basename}_patch_specs"
        $PatchManifest = "output/patch_specs/${PatchBasename}_manifest.json"
        $PatchManifestMd = "output/patch_specs/${PatchBasename}_manifest.md"
        # IA-CARMINE-STRICT-REAL-PRODUCT-PATCH-SPECS-BEGIN
        $StrictRealProductPatchSpecs = (
            $Basename -match "official_adapter|real-product|heap-exchange" -or
            $ProposalBasename -match "official_adapter|real-product|heap-exchange" -or
            $TaskRel -match "heap-exchange-process-gate|real-product|single_dynamic_heap_exchange_run"
        )
        $PatchSpecArgs = @(
            ".\Tools\ai\build_patch_specs_from_proposals.py",
            "--repo-root", ".",
            "--proposal", $ProposalRel,
            "--output-dir", "output\patch_specs",
            "--basename", $PatchBasename
        )
        if ($StrictRealProductPatchSpecs) {
            $PatchSpecArgs += "--require-concrete"
            if ($UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow) {
                $PatchSpecArgs += "--require-provider-execution"
            }
            Write-Host "[INFO] Strict real-product patch specs enabled: no metadata-only fallback."
        }
        # IA-CARMINE-STRICT-REAL-PRODUCT-PATCH-SPECS-END
        Invoke-CommandChecked -Label "Build draft patch specs from proposals" -Block {
            & $PythonExe @PatchSpecArgs
        }
        Invoke-CommandChecked -Label "Validate draft patch specs" -Block {
            & $PythonExe .\Tools\validation\check_patch_spec_drafts.py --repo-root . --manifest $PatchManifest --output "output/validation/${Basename}_patch_spec_drafts.json"
        }
    }

    return [ordered]@{
        proposal_path = $ProposalPath
        proposal_rel = $ProposalRel
        proposal_validation_output = $ProposalValidationOutput
        patch_manifest = $PatchManifest
        patch_manifest_markdown = $PatchManifestMd
    }
}
