function Resolve-SpaziotempoOllamaBaseUrl {
    $baseUrl = $env:OLLAMA_API_BASE
    if ([string]::IsNullOrWhiteSpace($baseUrl)) {
        $baseUrl = $env:OLLAMA_HOST
    }
    if ([string]::IsNullOrWhiteSpace($baseUrl)) {
        $baseUrl = "http://127.0.0.1:11434"
    }
    if ($baseUrl -notmatch "^https?://") {
        $baseUrl = "http://$baseUrl"
    }
    return $baseUrl.TrimEnd("/")
}

function Find-SpaziotempoOllamaExe {
    $candidates = @()
    if (-not [string]::IsNullOrWhiteSpace($env:OLLAMA_EXE)) {
        $candidates += $env:OLLAMA_EXE
    }

    $command = Get-Command ollama -ErrorAction SilentlyContinue
    if ($command) {
        $candidates += $command.Source
    }

    if (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
        $candidates += Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
        $candidates += Join-Path $env:LOCALAPPDATA "Ollama\ollama.exe"
        $candidates += Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps\ollama.exe"
    }
    if (-not [string]::IsNullOrWhiteSpace($env:ProgramFiles)) {
        $candidates += Join-Path $env:ProgramFiles "Ollama\ollama.exe"
    }
    if (-not [string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
        $candidates += Join-Path $env:USERPROFILE "AppData\Local\Programs\Ollama\ollama.exe"
    }

    foreach ($candidate in ($candidates | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)) {
        if (Test-Path -LiteralPath $candidate) {
            try {
                return (Resolve-Path -LiteralPath $candidate).Path
            } catch {
                return $candidate
            }
        }
    }

    return $null
}

function Write-SpaziotempoCheck {
    param(
        [string]$Status,
        [string]$Name,
        [string]$Detail
    )

    $color = "Gray"
    if ($Status -eq "OK") {
        $color = "Green"
    } elseif ($Status -eq "WARN") {
        $color = "Yellow"
    } elseif ($Status -eq "DOWN" -or $Status -eq "MISS") {
        $color = "Red"
    }

    $line = "  [{0}] {1}: {2}" -f $Status, $Name, $Detail
    Write-Host $line -ForegroundColor $color
}

function Add-SpaziotempoCheck {
    param(
        [object[]]$Checks,
        [string]$Status,
        [string]$Name,
        [string]$Detail
    )

    Write-SpaziotempoCheck -Status $Status -Name $Name -Detail $Detail
    return $Checks + [pscustomobject]@{
        Status = $Status
        Name = $Name
        Detail = $Detail
    }
}

function Invoke-SpaziotempoPythonProbe {
    param(
        [string]$Python,
        [string]$Code,
        [string]$WorkingDirectory,
        [int]$TimeoutSec = 20
    )

    if ([string]::IsNullOrWhiteSpace($Python)) {
        return [pscustomobject]@{
            Ok = $false
            TimedOut = $false
            ExitCode = $null
            Output = "Python executable not set."
        }
    }

    if ($Python -ne "python" -and -not (Test-Path -LiteralPath $Python)) {
        return [pscustomobject]@{
            Ok = $false
            TimedOut = $false
            ExitCode = $null
            Output = "Python executable not found: $Python"
        }
    }

    $job = Start-Job -ScriptBlock {
        param($PythonExe, $ProbeCode, $Cwd)

        if (-not [string]::IsNullOrWhiteSpace($Cwd) -and (Test-Path -LiteralPath $Cwd)) {
            Set-Location -LiteralPath $Cwd
        }

        $probeOutput = & $PythonExe -c $ProbeCode 2>&1 | Out-String
        [pscustomobject]@{
            ExitCode = $LASTEXITCODE
            Output = ($probeOutput.Trim())
        }
    } -ArgumentList $Python, $Code, $WorkingDirectory

    if (-not (Wait-Job -Job $job -Timeout $TimeoutSec)) {
        Stop-Job -Job $job -ErrorAction SilentlyContinue
        Remove-Job -Job $job -Force -ErrorAction SilentlyContinue
        return [pscustomobject]@{
            Ok = $false
            TimedOut = $true
            ExitCode = $null
            Output = "Timed out after ${TimeoutSec}s."
        }
    }

    $result = Receive-Job -Job $job
    Remove-Job -Job $job -Force -ErrorAction SilentlyContinue

    if ($null -eq $result) {
        return [pscustomobject]@{
            Ok = $false
            TimedOut = $false
            ExitCode = $null
            Output = "No probe result."
        }
    }

    return [pscustomobject]@{
        Ok = ($result.ExitCode -eq 0)
        TimedOut = $false
        ExitCode = $result.ExitCode
        Output = $result.Output
    }
}

function Invoke-SpaziotempoStartupCheck {
    param(
        [string]$Project,
        [string]$Root,
        [string]$Python,
        [switch]$Quiet,
        [int]$OllamaTimeoutSec = 2,
        [int]$PythonProbeTimeoutSec = 25
    )

    $checks = @()
    if (-not $Quiet) {
        Write-Host ""
        Write-Host "=== Startup service check ==="
    }

    $startupCheckScript = Join-Path $Project "Tools\workflow\startup_check.py"
    if (Test-Path -LiteralPath $startupCheckScript) {
        $candidatePythons = @()
        if (-not [string]::IsNullOrWhiteSpace($Python)) {
            $candidatePythons += $Python
        }
        $candidatePythons += "python"
        $candidatePythons = $candidatePythons | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique

        foreach ($candidatePython in $candidatePythons) {
            try {
                if ($candidatePython -ne "python" -and -not (Test-Path -LiteralPath $candidatePython)) {
                    continue
                }
                & $candidatePython $startupCheckScript --project $Project --root $Root
                if ($LASTEXITCODE -eq 0) {
                    return @()
                }
            } catch {
                if (-not $Quiet) {
                    Write-Host "Startup Python check failed with ${candidatePython}: $($_.Exception.Message)" -ForegroundColor Yellow
                }
            }
        }

        if (-not $Quiet) {
            Write-Host "Python startup check unavailable; using PowerShell fallback." -ForegroundColor Yellow
        }
    }

    if (Test-Path -LiteralPath $Project) {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Project" -Detail $Project
    } else {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "Project" -Detail "Missing: $Project"
    }

    $workflowScript = Join-Path $Project "Tools\workflow\workflow_state.py"
    if (Test-Path -LiteralPath $workflowScript) {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Workflow runtime" -Detail $workflowScript
    } else {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "Workflow runtime" -Detail "Missing: $workflowScript"
    }

    $ollamaBaseUrl = Resolve-SpaziotempoOllamaBaseUrl
    $ollamaExe = Find-SpaziotempoOllamaExe
    $ollamaProcesses = @(Get-Process -Name "ollama" -ErrorAction SilentlyContinue)
    try {
        $tags = Invoke-RestMethod -Uri "$ollamaBaseUrl/api/tags" -Method Get -TimeoutSec $OllamaTimeoutSec -ErrorAction Stop
        $modelCount = @($tags.models).Count
        $detail = "$ollamaBaseUrl is UP"
        if ($modelCount -eq 1) {
            $detail += " (1 model)"
        } else {
            $detail += " ($modelCount models)"
        }
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Ollama API" -Detail $detail
    } catch {
        $detail = "$ollamaBaseUrl is DOWN"
        if ($ollamaProcesses.Count -gt 0) {
            $detail += "; process running but API not ready"
        } elseif ($ollamaExe) {
            $detail += "; ollama.exe found and can be started by the AI tools"
        } else {
            $detail += "; ollama.exe not found"
        }
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "DOWN" -Name "Ollama API" -Detail $detail
    }

    if ($ollamaExe) {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Ollama executable" -Detail $ollamaExe
    } else {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "Ollama executable" -Detail "Set OLLAMA_EXE or install Ollama."
    }

    $npuPython = Join-Path $Root "venvs\blender-npu-ai\Scripts\python.exe"
    $npuModelDir = Join-Path $Root "npu-models\Phi-3.5-mini-instruct-int4-cw-ov"
    if (Test-Path -LiteralPath $npuPython) {
        $npuProbeCode = @'
import json
report = {"openvino": False, "openvino_genai": False, "devices": [], "errors": []}
try:
    import openvino as ov
    report["openvino"] = True
    report["devices"] = list(ov.Core().available_devices)
except Exception as exc:
    report["errors"].append("openvino: " + str(exc))
try:
    import openvino_genai
    report["openvino_genai"] = True
except Exception as exc:
    report["errors"].append("openvino_genai: " + str(exc))
print(json.dumps(report))
'@
        $npuResult = Invoke-SpaziotempoPythonProbe `
            -Python $npuPython `
            -Code $npuProbeCode `
            -WorkingDirectory $Project `
            -TimeoutSec $PythonProbeTimeoutSec

        if ($npuResult.Ok) {
            $lastLine = (($npuResult.Output -split "\r?\n") | Where-Object { $_.Trim() } | Select-Object -Last 1)
            try {
                $report = $lastLine | ConvertFrom-Json
                $devices = @($report.devices)
                $deviceText = if ($devices.Count -gt 0) { $devices -join "," } else { "none" }
                if ($report.openvino -and $report.openvino_genai -and ($devices -contains "NPU")) {
                    $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "NPU/OpenVINO" -Detail "UP devices=$deviceText"
                } elseif ($report.openvino -and $report.openvino_genai) {
                    $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "NPU/OpenVINO" -Detail "OpenVINO is UP, but NPU is not listed (devices=$deviceText)"
                } else {
                    $errors = @($report.errors) -join "; "
                    $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "NPU/OpenVINO" -Detail $errors
                }
            } catch {
                $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "NPU/OpenVINO" -Detail $npuResult.Output
            }
        } else {
            $checks = Add-SpaziotempoCheck -Checks $checks -Status "DOWN" -Name "NPU/OpenVINO" -Detail $npuResult.Output
        }
    } else {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "NPU Python" -Detail "Missing: $npuPython"
    }

    if (Test-Path -LiteralPath $npuModelDir) {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "NPU model" -Detail $npuModelDir
    } else {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "NPU model" -Detail "Missing: $npuModelDir"
    }

    $audioPython = Join-Path $Root "venvs\blender-audio-ai\Scripts\python.exe"
    if (Test-Path -LiteralPath $audioPython) {
        $audioProbe = Invoke-SpaziotempoPythonProbe `
            -Python $audioPython `
            -Code "import librosa, numpy, matplotlib; print('audio ok')" `
            -WorkingDirectory $Project `
            -TimeoutSec $PythonProbeTimeoutSec
        if ($audioProbe.Ok) {
            $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Audio runtime" -Detail "UP: $audioPython"
        } else {
            $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "Audio runtime" -Detail $audioProbe.Output
        }
    } else {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "Audio runtime" -Detail "Missing: $audioPython"
    }

    $blenderPython = Join-Path $env:ProgramFiles "Blender Foundation\Blender 5.1\5.1\python\bin\python.exe"
    if (Test-Path -LiteralPath $blenderPython) {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Blender Python" -Detail $blenderPython
    } else {
        $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "Blender Python" -Detail "Not found at expected path: $blenderPython"
    }

    $problemCount = @($checks | Where-Object { $_.Status -in @("WARN", "DOWN", "MISS") }).Count
    if (-not $Quiet) {
        if ($problemCount -eq 0) {
            Write-Host "=== Startup service check: all UP ===" -ForegroundColor Green
        } else {
            Write-Host "=== Startup service check: $problemCount warning(s) ===" -ForegroundColor Yellow
        }
        Write-Host ""
    }

    return $checks
}
