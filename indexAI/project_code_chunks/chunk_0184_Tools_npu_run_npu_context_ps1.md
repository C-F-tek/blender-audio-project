# Project Code Chunk 184/212

- File: `Tools/npu/run_npu_context.ps1`
- Part: `1`
- Lines: `1-238`

## Content
```ps1
00001: param(
00002:     [switch]$BuildOnly,
00003:     [switch]$SkipFinal,
00004:     [switch]$RunOllamaMusicAgent,
00005:     [switch]$RunDualAI,
00006:     [switch]$SkipDualNpu,
00007:     [switch]$SkipDualOllama,
00008:     [switch]$IncludeManual,
00009:     [ValidateSet("plan", "implementation", "full")]
00010:     [string]$DualPhase = "plan",
00011:     [ValidateSet("npu", "ollama")]
00012:     [string]$Engine = "npu",
00013:     [ValidateSet("code", "music")]
00014:     [string]$ReviewDomain = "code",
00015:     [string]$OllamaModel = "qwen2.5-coder:14b",
00016:     [string]$CreativeModel = "gpt-oss:20b",
00017:     [string]$TechnicalModel = "qwen2.5-coder:14b"
00018: )
00019: 
00020: $ErrorActionPreference = "Stop"
00021: 
00022: $ROOT = "$HOME\blender"
00023: $PROJECT = "$ROOT\blender-audio-project"
00024: $NPU_PY = "$ROOT\venvs\blender-npu-ai\Scripts\python.exe"
00025: $BLENDER_PY = "$env:ProgramFiles\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe"
00026: $STARTUP_PREFLIGHT = "$PROJECT\Tools\workflow\startup_preflight.ps1"
00027: 
00028: function Test-Python {
00029:     param(
00030:         [string]$Exe,
00031:         [string[]]$ArgsList
00032:     )
00033: 
00034:     try {
00035:         & $Exe @ArgsList *> $null
00036:         return $LASTEXITCODE -eq 0
00037:     } catch {
00038:         return $false
00039:     }
00040: }
00041: 
00042: function Invoke-Step {
00043:     param(
00044:         [string]$Title,
00045:         [string]$Exe,
00046:         [string[]]$ArgsList
00047:     )
00048: 
00049:     Write-Host ""
00050:     Write-Host "=== $Title ==="
00051: 
00052:     & $Exe @ArgsList
00053: 
00054:     if ($LASTEXITCODE -ne 0) {
00055:         throw "Step failed: $Title"
00056:     }
00057: }
00058: 
00059: if (-not (Test-Path $PROJECT)) {
00060:     throw "Project not found: $PROJECT"
00061: }
00062: 
00063: if (-not (Test-Path $NPU_PY)) {
00064:     throw "NPU Python not found: $NPU_PY"
00065: }
00066: 
00067: if (Test-Path -LiteralPath $STARTUP_PREFLIGHT) {
00068:     . $STARTUP_PREFLIGHT
00069:     $null = Invoke-SpaziotempoStartupCheck -Project $PROJECT -Root $ROOT -Python $NPU_PY
00070: }
00071: 
00072: $BUILD_PY = $NPU_PY
00073: if (-not (Test-Python -Exe $NPU_PY -ArgsList @("-c", "print('ok')"))) {
00074:     if (Test-Path $BLENDER_PY) {
00075:         $BUILD_PY = $BLENDER_PY
00076:         Write-Host "NPU Python launcher is not starting; using Blender Python for context build only."
00077:     } else {
00078:         throw "NPU Python launcher is not starting and Blender Python fallback was not found."
00079:     }
00080: }
00081: 
00082: Set-Location $PROJECT
00083: 
00084: Invoke-Step `
00085:     -Title "Build long code context" `
00086:     -Exe $BUILD_PY `
00087:     -ArgsList @(".\Tools\npu\build_npu_code_context.py")
00088: 
00089: Invoke-Step `
00090:     -Title "Build long music context" `
00091:     -Exe $BUILD_PY `
00092:     -ArgsList @(".\Tools\npu\build_music_context.py")
00093: 
00094: Invoke-Step `
00095:     -Title "Ensure local manual library" `
00096:     -Exe $BUILD_PY `
00097:     -ArgsList @(".\Tools\npu\build_blender_manual_context.py", "--ensure-only")
00098: 
00099: if ($BuildOnly) {
00100:     Write-Host ""
00101:     Write-Host "=== Done: build only ==="
00102:     Write-Host "Generated:"
00103:     Write-Host "  Tools\npu\npu_code_context.md"
00104:     Write-Host "  Tools\npu\npu_code_index.md"
00105:     Write-Host "  Tools\npu\npu_code_manifest.json"
00106:     Write-Host "  Tools\npu\npu_code_chunks\chunk_*.md"
00107:     Write-Host "  Tools\npu\npu_music_context.md"
00108:     Write-Host "  Tools\npu\npu_music_manifest.json"
00109:     Write-Host "  Tools\npu\npu_music_chunks\chunk_*.md"
00110:     Write-Host "  output\Feel The Light-Luca Vera_Master_music_context.json"
00111:     Write-Host "  output\Feel The Light-Luca Vera_Master_analysis_ai_context.json"
00112:     Write-Host "  output\Feel The Light-Luca Vera_Master_analysis_blender_keyframes.json"
00113:     return
00114: }
00115: 
00116: if ($RunDualAI) {
00117:     $DualArgs = @(
00118:         ".\Tools\npu\run_dual_ai_pipeline.py",
00119:         "--phase", $DualPhase,
00120:         "--creative-model", $CreativeModel,
00121:         "--technical-model", $TechnicalModel,
00122:         "--npu-python", $NPU_PY
00123:     )
00124: 
00125:     if ($SkipDualNpu) {
00126:         $DualArgs += "--skip-npu"
00127:     }
00128: 
00129:     if ($SkipDualOllama) {
00130:         $DualArgs += "--skip-ollama"
00131:     }
00132: 
00133:     if ($IncludeManual) {
00134:         $DualArgs += "--include-manual"
00135:     }
00136: 
00137:     Invoke-Step `
00138:         -Title "Run dual AI pipeline" `
00139:         -Exe $BUILD_PY `
00140:         -ArgsList $DualArgs
00141: 
00142:     Write-Host ""
00143:     Write-Host "=== Done: dual AI ==="
00144:     Write-Host "Generated:"
00145:     Write-Host "  output\Feel The Light-Luca Vera_Master_dual_ai_scene_plan.json"
00146:     Write-Host "  Tools\npu\dual_ai_blender_agent_brief.md"
00147:     Write-Host "  Tools\npu\npu_dual_ai_technical_notes.md"
00148:     if (-not $SkipDualNpu) {
00149:         Write-Host "  Tools\npu\npu_preflight_report.json"
00150:     }
00151:     if ($DualPhase -ne "plan" -and -not $SkipDualOllama) {
00152:         Write-Host "  output\Feel The Light-Luca Vera_Master_ai_implementation_draft.json"
00153:         Write-Host "  Tools\npu\generated_blender_script_candidate.py"
00154:         Write-Host "  Tools\npu\generated_implementation_notes.md"
00155:     }
00156:     return
00157: }
00158: 
00159: if ($RunOllamaMusicAgent) {
00160:     Invoke-Step `
00161:         -Title "Run Ollama music agent" `
00162:         -Exe $BUILD_PY `
00163:         -ArgsList @(
00164:             ".\Tools\npu\run_ollama_music_agent.py",
00165:             "--model", $OllamaModel
00166:         )
00167: }
00168: 
00169: if ($Engine -eq "npu" -and -not (Test-Python -Exe $NPU_PY -ArgsList @("-c", "import openvino_genai; print('ok')"))) {
00170:     throw "NPU Python cannot start or cannot import openvino_genai. Rebuild the venv before running the NPU review, or use -BuildOnly."
00171: }
00172: 
00173: if ($ReviewDomain -eq "music") {
00174:     $ContextPath = ".\Tools\npu\npu_music_context.md"
00175:     $ChunkDir = ".\Tools\npu\npu_music_chunks"
00176:     $OutPath = ".\Tools\npu\npu_music_context_for_aider.md"
00177:     $NotesOut = ".\Tools\npu\npu_music_chunk_notes.md"
00178: } else {
00179:     $ContextPath = ".\Tools\npu\npu_code_context.md"
00180:     $ChunkDir = ".\Tools\npu\npu_code_chunks"
00181:     $OutPath = ".\Tools\npu\npu_context_for_aider.md"
00182:     $NotesOut = ".\Tools\npu\npu_chunk_notes.md"
00183: }
00184: 
00185: $ReviewArgs = @(
00186:     ".\Tools\npu\run_npu_review.py",
00187:     "--engine", $Engine,
00188:     "--device", "NPU",
00189:     "--ollama-model", $OllamaModel,
00190:     "--domain", $ReviewDomain,
00191:     "--mode", "chunked",
00192:     "--context", $ContextPath,
00193:     "--chunk-dir", $ChunkDir,
00194:     "--out", $OutPath,
00195:     "--notes-out", $NotesOut,
00196:     "--max-context-chars", "0",
00197:     "--chunk-chars", "10500",
00198:     "--chunk-overlap-chars", "700",
00199:     "--max-prompt-chars", "15000",
00200:     "--max-chunk-tokens", "650",
00201:     "--max-reduce-tokens", "750",
00202:     "--max-new-tokens", "1100",
00203:     "--max-prompt-len", "16384",
00204:     "--min-response-len", "512"
00205: )
00206: 
00207: if ($SkipFinal) {
00208:     $ReviewArgs += "--skip-final"
00209: }
00210: 
00211: $ReviewPython = $BUILD_PY
00212: if ($Engine -eq "npu") {
00213:     $ReviewPython = $NPU_PY
00214: }
00215: 
00216: Invoke-Step `
00217:     -Title "Run long-context review ($Engine / $ReviewDomain)" `
00218:     -Exe $ReviewPython `
00219:     -ArgsList $ReviewArgs
00220: 
00221: Write-Host ""
00222: Write-Host "=== Done ==="
00223: Write-Host "Generated:"
00224: Write-Host "  Tools\npu\npu_code_context.md"
00225: Write-Host "  Tools\npu\npu_code_index.md"
00226: Write-Host "  Tools\npu\npu_code_manifest.json"
00227: Write-Host "  Tools\npu\npu_code_chunks\chunk_*.md"
00228: Write-Host "  Tools\npu\npu_chunk_notes.md"
00229: Write-Host "  Tools\npu\npu_context_for_aider.md"
00230: Write-Host "  Tools\npu\npu_music_context.md"
00231: Write-Host "  Tools\npu\npu_music_manifest.json"
00232: Write-Host "  Tools\npu\npu_music_chunks\chunk_*.md"
00233: Write-Host "  Tools\npu\npu_music_chunk_notes.md"
00234: Write-Host "  Tools\npu\npu_music_context_for_aider.md"
00235: Write-Host "  output\Feel The Light-Luca Vera_Master_analysis_ai_context.json"
00236: Write-Host "  output\Feel The Light-Luca Vera_Master_analysis_blender_keyframes.json"
00237: Write-Host "  output\Feel The Light-Luca Vera_Master_ollama_music_insights.json"
00238: Write-Host "  Tools\npu\ollama_music_insights.md"
```
