function Add-ContextFileIfPresent {
    param(
        [string[]]$Current,
        [string]$PathValue,
        [string]$Root
    )
    if ([string]::IsNullOrWhiteSpace($PathValue)) {
        return $Current
    }
    $full = Resolve-PlannedPath $PathValue
    if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
        Write-Warning "Context file not found, not adding: $PathValue"
        return $Current
    }
    $rel = Get-RepoRelativePath $Root $full
    if ($Current -notcontains $rel) {
        return @($Current + $rel)
    }
    return $Current
}

function Add-ExistingBundlePathArg {
    param(
        [string[]]$ArgsList,
        [string]$Kind,
        [string]$PathValue,
        [string]$Root,
        [bool]$WarnIfMissing = $true
    )
    if ([string]::IsNullOrWhiteSpace($PathValue)) {
        return $ArgsList
    }
    $full = Resolve-PlannedPath $PathValue
    if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
        if ($WarnIfMissing) {
            Write-Warning "Bundle $Kind not found, not adding: $PathValue"
        }
        return $ArgsList
    }
    $rel = Get-RepoRelativePath $Root $full
    return @($ArgsList + @("--$Kind", $rel))
}

function As-Array {
    param([object]$Value)
    if ($null -eq $Value) {
        return @()
    }
    return @($Value)
}

function Normalize-ContextFiles {
    param([string[]]$Values)
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    $normalized = @()
    foreach ($value in $Values) {
        $item = [string]$value
        if ([string]::IsNullOrWhiteSpace($item)) {
            continue
        }
        $item = $item.Trim().Replace("\", "/")
        if ($seen.Add($item)) {
            $normalized += $item
        }
    }
    return $normalized
}

function New-EnrichmentOutputs {
    param([string]$MemoryDb)
    return [ordered]@{
        semantic_chunks_manifest = ""
        semantic_chunks_json = ""
        selected_chunks_json = ""
        selected_chunks_markdown = ""
        selected_chunks_validation = ""
        selected_chunks_evidence_json = ""
        selected_chunks_evidence_markdown = ""
        context_pack_json = ""
        context_pack_markdown = ""
        context_pack_evidence_json = ""
        agent_state_json = ""
        agent_state_markdown = ""
        agent_state_memory_manifest = ""
        enrichment_plan_json = ""
        enrichment_plan_markdown = ""
        enrichment_plan_validation = ""
        memory_db = $MemoryDb.Replace("\", "/")
    }
}
