class RealProductLauncherError {
    [string]$Code
    [string]$Message
    [int]$ExitCode

    RealProductLauncherError([string]$Code, [string]$Message, [int]$ExitCode) {
        $this.Code = $Code
        $this.Message = $Message
        $this.ExitCode = $ExitCode
    }
}

function Stop-RealProductLauncher {
    param(
        [string]$Code,
        [string]$Message,
        [int]$ExitCode = 2,
        [string]$Root = "",
        [string]$StampValue = "",
        [string]$DetailPath = ""
    )

    $ErrorObject = [RealProductLauncherError]::new($Code, $Message, $ExitCode)

    $EffectiveRoot = $Root
    if ([string]::IsNullOrWhiteSpace($EffectiveRoot)) {
        try {
            $MaybeRoot = (& git rev-parse --show-toplevel 2>$null)
            if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($MaybeRoot)) {
                $EffectiveRoot = $MaybeRoot.Trim()
            }
        }
        catch {
            $EffectiveRoot = ""
        }
    }
    if ([string]::IsNullOrWhiteSpace($EffectiveRoot)) {
        $EffectiveRoot = (Get-Location).Path
    }

    $EffectiveStamp = $StampValue
    if ([string]::IsNullOrWhiteSpace($EffectiveStamp)) {
        $EffectiveStamp = Get-Date -Format "yyyyMMdd-HHmmss"
    }

    $OutputDir = Join-Path $EffectiveRoot "output/validation"
    $JsonPath = Join-Path $OutputDir ("real_product_wrapper_error_{0}.json" -f $EffectiveStamp)
    $MarkdownPath = Join-Path $OutputDir ("real_product_wrapper_error_{0}.md" -f $EffectiveStamp)

    $Report = [ordered]@{
        schema_version = 1
        kind = "real_product_wrapper_error"
        generated_at = (Get-Date).ToString("s")
        repo_root = $EffectiveRoot.Replace("\", "/")
        stamp = $EffectiveStamp
        passed = $false
        error_code = $ErrorObject.Code
        message = $ErrorObject.Message
        detail_path = $DetailPath
        provider_execution_performed = $false
        patch_application_performed = $false
        source_writes_performed = $false
        exit_code = $ErrorObject.ExitCode
        errors = @($ErrorObject.Message)
        warnings = @()
    }

    try {
        New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
        ($Report | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $JsonPath -Encoding UTF8

        $Markdown = @(
            "# Real Product Wrapper Error",
            "",
            "- Passed: ``False``",
            "- Error code: ``$($ErrorObject.Code)``",
            "- Message: $($ErrorObject.Message)",
            "- Detail path: ``$DetailPath``",
            "- JSON report: ``$JsonPath``",
            "- Exit code: ``$($ErrorObject.ExitCode)``",
            ""
        ) -join "`n"
        Set-Content -LiteralPath $MarkdownPath -Value ($Markdown + "`n") -Encoding UTF8

        Write-Host "[ERROR] $($ErrorObject.Code): $($ErrorObject.Message)" -ForegroundColor Red
        Write-Host "[ERROR] Structured wrapper report: $JsonPath" -ForegroundColor Red
    }
    catch {
        Write-Host "[ERROR] $($ErrorObject.Code): $($ErrorObject.Message)" -ForegroundColor Red
        Write-Host "[ERROR] Failed to write structured wrapper report: $($_.Exception.Message)" -ForegroundColor Red
    }

    exit $ErrorObject.ExitCode
}

function Resolve-RepoRoot {
    param([string]$Root)
    Push-Location $Root
    try {
        $resolved = (& git rev-parse --show-toplevel 2>$null)
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($resolved)) {
            Stop-RealProductLauncher -Code "not_git_repository" -Message "This command must be run inside a Git repository checkout." -Root $Root -StampValue $Stamp
        }
        return (Resolve-Path $resolved.Trim()).Path
    }
    finally {
        Pop-Location
    }
}

function Get-RepoRelativePath {
    param(
        [string]$Root,
        [string]$PathValue
    )
    $full = [System.IO.Path]::GetFullPath($PathValue)
    $rootFull = [System.IO.Path]::GetFullPath($Root)
    if (-not $rootFull.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $rootFull += [System.IO.Path]::DirectorySeparatorChar
    }
    if ($full.StartsWith($rootFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $full.Substring($rootFull.Length).Replace("\", "/")
    }
    return $full.Replace("\", "/")
}

function New-SafeSlug {
    param([string]$Value)
    $slug = [regex]::Replace($Value.ToLowerInvariant(), "[^a-z0-9._-]+", "-").Trim("-", ".", "_")
    if ([string]::IsNullOrWhiteSpace($slug)) { return "task" }
    return $slug
}
