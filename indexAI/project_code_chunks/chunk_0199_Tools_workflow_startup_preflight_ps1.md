# Project Code Chunk 199/212

- File: `Tools/workflow/startup_preflight.ps1`
- Part: `1`
- Lines: `1-281`

## Content
```ps1
00001: function Resolve-SpaziotempoOllamaBaseUrl {
00002:     $baseUrl = $env:OLLAMA_API_BASE
00003:     if ([string]::IsNullOrWhiteSpace($baseUrl)) {
00004:         $baseUrl = $env:OLLAMA_HOST
00005:     }
00006:     if ([string]::IsNullOrWhiteSpace($baseUrl)) {
00007:         $baseUrl = "http://127.0.0.1:11434"
00008:     }
00009:     if ($baseUrl -notmatch "^https?://") {
00010:         $baseUrl = "http://$baseUrl"
00011:     }
00012:     return $baseUrl.TrimEnd("/")
00013: }
00014: 
00015: function Find-SpaziotempoOllamaExe {
00016:     $candidates = @()
00017:     if (-not [string]::IsNullOrWhiteSpace($env:OLLAMA_EXE)) {
00018:         $candidates += $env:OLLAMA_EXE
00019:     }
00020: 
00021:     $command = Get-Command ollama -ErrorAction SilentlyContinue
00022:     if ($command) {
00023:         $candidates += $command.Source
00024:     }
00025: 
00026:     if (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
00027:         $candidates += Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
00028:         $candidates += Join-Path $env:LOCALAPPDATA "Ollama\ollama.exe"
00029:         $candidates += Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps\ollama.exe"
00030:     }
00031:     if (-not [string]::IsNullOrWhiteSpace($env:ProgramFiles)) {
00032:         $candidates += Join-Path $env:ProgramFiles "Ollama\ollama.exe"
00033:     }
00034:     if (-not [string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
00035:         $candidates += Join-Path $env:USERPROFILE "AppData\Local\Programs\Ollama\ollama.exe"
00036:     }
00037: 
00038:     foreach ($candidate in ($candidates | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)) {
00039:         if (Test-Path -LiteralPath $candidate) {
00040:             try {
00041:                 return (Resolve-Path -LiteralPath $candidate).Path
00042:             } catch {
00043:                 return $candidate
00044:             }
00045:         }
00046:     }
00047: 
00048:     return $null
00049: }
00050: 
00051: function Write-SpaziotempoCheck {
00052:     param(
00053:         [string]$Status,
00054:         [string]$Name,
00055:         [string]$Detail
00056:     )
00057: 
00058:     $color = "Gray"
00059:     if ($Status -eq "OK") {
00060:         $color = "Green"
00061:     } elseif ($Status -eq "WARN") {
00062:         $color = "Yellow"
00063:     } elseif ($Status -eq "DOWN" -or $Status -eq "MISS") {
00064:         $color = "Red"
00065:     }
00066: 
00067:     $line = "  [{0}] {1}: {2}" -f $Status, $Name, $Detail
00068:     Write-Host $line -ForegroundColor $color
00069: }
00070: 
00071: function Add-SpaziotempoCheck {
00072:     param(
00073:         [object[]]$Checks,
00074:         [string]$Status,
00075:         [string]$Name,
00076:         [string]$Detail
00077:     )
00078: 
00079:     Write-SpaziotempoCheck -Status $Status -Name $Name -Detail $Detail
00080:     return $Checks + [pscustomobject]@{
00081:         Status = $Status
00082:         Name = $Name
00083:         Detail = $Detail
00084:     }
00085: }
00086: 
00087: function Invoke-SpaziotempoPythonProbe {
00088:     param(
00089:         [string]$Python,
00090:         [string]$Code,
00091:         [string]$WorkingDirectory,
00092:         [int]$TimeoutSec = 20
00093:     )
00094: 
00095:     if ([string]::IsNullOrWhiteSpace($Python)) {
00096:         return [pscustomobject]@{
00097:             Ok = $false
00098:             TimedOut = $false
00099:             ExitCode = $null
00100:             Output = "Python executable not set."
00101:         }
00102:     }
00103: 
00104:     if ($Python -ne "python" -and -not (Test-Path -LiteralPath $Python)) {
00105:         return [pscustomobject]@{
00106:             Ok = $false
00107:             TimedOut = $false
00108:             ExitCode = $null
00109:             Output = "Python executable not found: $Python"
00110:         }
00111:     }
00112: 
00113:     $job = Start-Job -ScriptBlock {
00114:         param($PythonExe, $ProbeCode, $Cwd)
00115: 
00116:         if (-not [string]::IsNullOrWhiteSpace($Cwd) -and (Test-Path -LiteralPath $Cwd)) {
00117:             Set-Location -LiteralPath $Cwd
00118:         }
00119: 
00120:         $probeOutput = & $PythonExe -c $ProbeCode 2>&1 | Out-String
00121:         [pscustomobject]@{
00122:             ExitCode = $LASTEXITCODE
00123:             Output = ($probeOutput.Trim())
00124:         }
00125:     } -ArgumentList $Python, $Code, $WorkingDirectory
00126: 
00127:     if (-not (Wait-Job -Job $job -Timeout $TimeoutSec)) {
00128:         Stop-Job -Job $job -ErrorAction SilentlyContinue
00129:         Remove-Job -Job $job -Force -ErrorAction SilentlyContinue
00130:         return [pscustomobject]@{
00131:             Ok = $false
00132:             TimedOut = $true
00133:             ExitCode = $null
00134:             Output = "Timed out after ${TimeoutSec}s."
00135:         }
00136:     }
00137: 
00138:     $result = Receive-Job -Job $job
00139:     Remove-Job -Job $job -Force -ErrorAction SilentlyContinue
00140: 
00141:     if ($null -eq $result) {
00142:         return [pscustomobject]@{
00143:             Ok = $false
00144:             TimedOut = $false
00145:             ExitCode = $null
00146:             Output = "No probe result."
00147:         }
00148:     }
00149: 
00150:     return [pscustomobject]@{
00151:         Ok = ($result.ExitCode -eq 0)
00152:         TimedOut = $false
00153:         ExitCode = $result.ExitCode
00154:         Output = $result.Output
00155:     }
00156: }
00157: 
00158: function Invoke-SpaziotempoStartupCheck {
00159:     param(
00160:         [string]$Project,
00161:         [string]$Root,
00162:         [string]$Python,
00163:         [switch]$Quiet,
00164:         [int]$OllamaTimeoutSec = 2,
00165:         [int]$PythonProbeTimeoutSec = 25
00166:     )
00167: 
00168:     $checks = @()
00169:     if (-not $Quiet) {
00170:         Write-Host ""
00171:         Write-Host "=== Startup service check ==="
00172:     }
00173: 
00174:     $startupCheckScript = Join-Path $Project "Tools\workflow\startup_check.py"
00175:     if (Test-Path -LiteralPath $startupCheckScript) {
00176:         $candidatePythons = @()
00177:         if (-not [string]::IsNullOrWhiteSpace($Python)) {
00178:             $candidatePythons += $Python
00179:         }
00180:         $candidatePythons += "python"
00181:         $candidatePythons = $candidatePythons | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique
00182: 
00183:         foreach ($candidatePython in $candidatePythons) {
00184:             try {
00185:                 if ($candidatePython -ne "python" -and -not (Test-Path -LiteralPath $candidatePython)) {
00186:                     continue
00187:                 }
00188:                 & $candidatePython $startupCheckScript --project $Project --root $Root
00189:                 if ($LASTEXITCODE -eq 0) {
00190:                     return @()
00191:                 }
00192:             } catch {
00193:                 if (-not $Quiet) {
00194:                     Write-Host "Startup Python check failed with ${candidatePython}: $($_.Exception.Message)" -ForegroundColor Yellow
00195:                 }
00196:             }
00197:         }
00198: 
00199:         if (-not $Quiet) {
00200:             Write-Host "Python startup check unavailable; using PowerShell fallback." -ForegroundColor Yellow
00201:         }
00202:     }
00203: 
00204:     if (Test-Path -LiteralPath $Project) {
00205:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Project" -Detail $Project
00206:     } else {
00207:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "Project" -Detail "Missing: $Project"
00208:     }
00209: 
00210:     $workflowScript = Join-Path $Project "Tools\workflow\workflow_state.py"
00211:     if (Test-Path -LiteralPath $workflowScript) {
00212:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Workflow runtime" -Detail $workflowScript
00213:     } else {
00214:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "Workflow runtime" -Detail "Missing: $workflowScript"
00215:     }
00216: 
00217:     $ollamaBaseUrl = Resolve-SpaziotempoOllamaBaseUrl
00218:     $ollamaExe = Find-SpaziotempoOllamaExe
00219:     $ollamaProcesses = @(Get-Process -Name "ollama" -ErrorAction SilentlyContinue)
00220:     try {
00221:         $tags = Invoke-RestMethod -Uri "$ollamaBaseUrl/api/tags" -Method Get -TimeoutSec $OllamaTimeoutSec -ErrorAction Stop
00222:         $modelCount = @($tags.models).Count
00223:         $detail = "$ollamaBaseUrl is UP"
00224:         if ($modelCount -eq 1) {
00225:             $detail += " (1 model)"
00226:         } else {
00227:             $detail += " ($modelCount models)"
00228:         }
00229:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Ollama API" -Detail $detail
00230:     } catch {
00231:         $detail = "$ollamaBaseUrl is DOWN"
00232:         if ($ollamaProcesses.Count -gt 0) {
00233:             $detail += "; process running but API not ready"
00234:         } elseif ($ollamaExe) {
00235:             $detail += "; ollama.exe found and can be started by the AI tools"
00236:         } else {
00237:             $detail += "; ollama.exe not found"
00238:         }
00239:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "DOWN" -Name "Ollama API" -Detail $detail
00240:     }
00241: 
00242:     if ($ollamaExe) {
00243:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Ollama executable" -Detail $ollamaExe
00244:     } else {
00245:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "Ollama executable" -Detail "Set OLLAMA_EXE or install Ollama."
00246:     }
00247: 
00248:     $npuPython = Join-Path $Root "venvs\blender-npu-ai\Scripts\python.exe"
00249:     $npuModelDir = Join-Path $Root "npu-models\Phi-3.5-mini-instruct-int4-cw-ov"
00250:     if (Test-Path -LiteralPath $npuPython) {
00251:         $npuProbeCode = @'
00252: import json
00253: report = {"openvino": False, "openvino_genai": False, "devices": [], "errors": []}
00254: try:
00255:     import openvino as ov
00256:     report["openvino"] = True
00257:     report["devices"] = list(ov.Core().available_devices)
00258: except Exception as exc:
00259:     report["errors"].append("openvino: " + str(exc))
00260: try:
00261:     import openvino_genai
00262:     report["openvino_genai"] = True
00263: except Exception as exc:
00264:     report["errors"].append("openvino_genai: " + str(exc))
00265: print(json.dumps(report))
00266: '@
00267:         $npuResult = Invoke-SpaziotempoPythonProbe `
00268:             -Python $npuPython `
00269:             -Code $npuProbeCode `
00270:             -WorkingDirectory $Project `
00271:             -TimeoutSec $PythonProbeTimeoutSec
00272: 
00273:         if ($npuResult.Ok) {
00274:             $lastLine = (($npuResult.Output -split "\r?\n") | Where-Object { $_.Trim() } | Select-Object -Last 1)
00275:             try {
00276:                 $report = $lastLine | ConvertFrom-Json
00277:                 $devices = @($report.devices)
00278:                 $deviceText = if ($devices.Count -gt 0) { $devices -join "," } else { "none" }
00279:                 if ($report.openvino -and $report.openvino_genai -and ($devices -contains "NPU")) {
00280:                     $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "NPU/OpenVINO" -Detail "UP devices=$deviceText"
00281:                 } elseif ($report.openvino -and $report.openvino_genai) {
```
