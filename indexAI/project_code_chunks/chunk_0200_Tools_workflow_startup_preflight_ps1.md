# Project Code Chunk 200/212

- File: `Tools/workflow/startup_preflight.ps1`
- Part: `2`
- Lines: `282-337`

## Content
```ps1
00282:                     $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "NPU/OpenVINO" -Detail "OpenVINO is UP, but NPU is not listed (devices=$deviceText)"
00283:                 } else {
00284:                     $errors = @($report.errors) -join "; "
00285:                     $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "NPU/OpenVINO" -Detail $errors
00286:                 }
00287:             } catch {
00288:                 $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "NPU/OpenVINO" -Detail $npuResult.Output
00289:             }
00290:         } else {
00291:             $checks = Add-SpaziotempoCheck -Checks $checks -Status "DOWN" -Name "NPU/OpenVINO" -Detail $npuResult.Output
00292:         }
00293:     } else {
00294:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "NPU Python" -Detail "Missing: $npuPython"
00295:     }
00296: 
00297:     if (Test-Path -LiteralPath $npuModelDir) {
00298:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "NPU model" -Detail $npuModelDir
00299:     } else {
00300:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "NPU model" -Detail "Missing: $npuModelDir"
00301:     }
00302: 
00303:     $audioPython = Join-Path $Root "venvs\blender-audio-ai\Scripts\python.exe"
00304:     if (Test-Path -LiteralPath $audioPython) {
00305:         $audioProbe = Invoke-SpaziotempoPythonProbe `
00306:             -Python $audioPython `
00307:             -Code "import librosa, numpy, matplotlib; print('audio ok')" `
00308:             -WorkingDirectory $Project `
00309:             -TimeoutSec $PythonProbeTimeoutSec
00310:         if ($audioProbe.Ok) {
00311:             $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Audio runtime" -Detail "UP: $audioPython"
00312:         } else {
00313:             $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "Audio runtime" -Detail $audioProbe.Output
00314:         }
00315:     } else {
00316:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "MISS" -Name "Audio runtime" -Detail "Missing: $audioPython"
00317:     }
00318: 
00319:     $blenderPython = Join-Path $env:ProgramFiles "Blender Foundation\Blender 5.1\5.1\python\bin\python.exe"
00320:     if (Test-Path -LiteralPath $blenderPython) {
00321:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "OK" -Name "Blender Python" -Detail $blenderPython
00322:     } else {
00323:         $checks = Add-SpaziotempoCheck -Checks $checks -Status "WARN" -Name "Blender Python" -Detail "Not found at expected path: $blenderPython"
00324:     }
00325: 
00326:     $problemCount = @($checks | Where-Object { $_.Status -in @("WARN", "DOWN", "MISS") }).Count
00327:     if (-not $Quiet) {
00328:         if ($problemCount -eq 0) {
00329:             Write-Host "=== Startup service check: all UP ===" -ForegroundColor Green
00330:         } else {
00331:             Write-Host "=== Startup service check: $problemCount warning(s) ===" -ForegroundColor Yellow
00332:         }
00333:         Write-Host ""
00334:     }
00335: 
00336:     return $checks
00337: }
```
