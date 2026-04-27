param(
    [switch]$BuildOnly,
    [switch]$SkipFinal,
    [switch]$RunOllamaMusicAgent,
    [switch]$RunDualAI,
    [switch]$SkipDualNpu,
    [switch]$SkipDualOllama,
    [switch]$IncludeManual,
    [ValidateSet("plan", "implementation", "full")]
    [string]$DualPhase = "plan",
    [ValidateSet("npu", "ollama")]
    [string]$Engine = "npu",
    [ValidateSet("code", "music")]
    [string]$ReviewDomain = "code",
    [string]$OllamaModel = "qwen2.5-coder:14b",
    [string]$CreativeModel = "gpt-oss:20b",
    [string]$TechnicalModel = "qwen2.5-coder:14b"
)

$ErrorActionPreference = "Stop"

$ROOT = "$HOME\blender"
$PROJECT = "$ROOT\blender-audio-project"
$NPU_PY = "$ROOT\venvs\blender-npu-ai\Scripts\python.exe"
$BLENDER_PY = "$env:ProgramFiles\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe"
$STARTUP_PREFLIGHT = "$PROJECT\Tools\workflow\startup_preflight.ps1"

function Test-Python {
    param(
        [string]$Exe,
        [string[]]$ArgsList
    )

    try {
        & $Exe @ArgsList *> $null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

function Invoke-Step {
    param(
        [string]$Title,
        [string]$Exe,
        [string[]]$ArgsList
    )

    Write-Host ""
    Write-Host "=== $Title ==="

    & $Exe @ArgsList

    if ($LASTEXITCODE -ne 0) {
        throw "Step failed: $Title"
    }
}

if (-not (Test-Path $PROJECT)) {
    throw "Project not found: $PROJECT"
}

if (-not (Test-Path $NPU_PY)) {
    throw "NPU Python not found: $NPU_PY"
}

if (Test-Path -LiteralPath $STARTUP_PREFLIGHT) {
    . $STARTUP_PREFLIGHT
    $null = Invoke-SpaziotempoStartupCheck -Project $PROJECT -Root $ROOT -Python $NPU_PY
}

$BUILD_PY = $NPU_PY
if (-not (Test-Python -Exe $NPU_PY -ArgsList @("-c", "print('ok')"))) {
    if (Test-Path $BLENDER_PY) {
        $BUILD_PY = $BLENDER_PY
        Write-Host "NPU Python launcher is not starting; using Blender Python for context build only."
    } else {
        throw "NPU Python launcher is not starting and Blender Python fallback was not found."
    }
}

Set-Location $PROJECT

Invoke-Step `
    -Title "Build long code context" `
    -Exe $BUILD_PY `
    -ArgsList @(".\Tools\npu\build_npu_code_context.py")

Invoke-Step `
    -Title "Build long music context" `
    -Exe $BUILD_PY `
    -ArgsList @(".\Tools\npu\build_music_context.py")

Invoke-Step `
    -Title "Ensure local manual library" `
    -Exe $BUILD_PY `
    -ArgsList @(".\Tools\npu\build_blender_manual_context.py", "--ensure-only")

if ($BuildOnly) {
    Write-Host ""
    Write-Host "=== Done: build only ==="
    Write-Host "Generated:"
    Write-Host "  Tools\npu\npu_code_context.md"
    Write-Host "  Tools\npu\npu_code_index.md"
    Write-Host "  Tools\npu\npu_code_manifest.json"
    Write-Host "  Tools\npu\npu_code_chunks\chunk_*.md"
    Write-Host "  Tools\npu\npu_music_context.md"
    Write-Host "  Tools\npu\npu_music_manifest.json"
    Write-Host "  Tools\npu\npu_music_chunks\chunk_*.md"
    Write-Host "  output\Feel The Light-Luca Vera_Master_music_context.json"
    Write-Host "  output\Feel The Light-Luca Vera_Master_analysis_ai_context.json"
    Write-Host "  output\Feel The Light-Luca Vera_Master_analysis_blender_keyframes.json"
    return
}

if ($RunDualAI) {
    $DualArgs = @(
        ".\Tools\npu\run_dual_ai_pipeline.py",
        "--phase", $DualPhase,
        "--creative-model", $CreativeModel,
        "--technical-model", $TechnicalModel,
        "--npu-python", $NPU_PY
    )

    if ($SkipDualNpu) {
        $DualArgs += "--skip-npu"
    }

    if ($SkipDualOllama) {
        $DualArgs += "--skip-ollama"
    }

    if ($IncludeManual) {
        $DualArgs += "--include-manual"
    }

    Invoke-Step `
        -Title "Run dual AI pipeline" `
        -Exe $BUILD_PY `
        -ArgsList $DualArgs

    Write-Host ""
    Write-Host "=== Done: dual AI ==="
    Write-Host "Generated:"
    Write-Host "  output\Feel The Light-Luca Vera_Master_dual_ai_scene_plan.json"
    Write-Host "  Tools\npu\dual_ai_blender_agent_brief.md"
    Write-Host "  Tools\npu\npu_dual_ai_technical_notes.md"
    if (-not $SkipDualNpu) {
        Write-Host "  Tools\npu\npu_preflight_report.json"
    }
    if ($DualPhase -ne "plan" -and -not $SkipDualOllama) {
        Write-Host "  output\Feel The Light-Luca Vera_Master_ai_implementation_draft.json"
        Write-Host "  Tools\npu\generated_blender_script_candidate.py"
        Write-Host "  Tools\npu\generated_implementation_notes.md"
    }
    return
}

if ($RunOllamaMusicAgent) {
    Invoke-Step `
        -Title "Run Ollama music agent" `
        -Exe $BUILD_PY `
        -ArgsList @(
            ".\Tools\npu\run_ollama_music_agent.py",
            "--model", $OllamaModel
        )
}

if ($Engine -eq "npu" -and -not (Test-Python -Exe $NPU_PY -ArgsList @("-c", "import openvino_genai; print('ok')"))) {
    throw "NPU Python cannot start or cannot import openvino_genai. Rebuild the venv before running the NPU review, or use -BuildOnly."
}

if ($ReviewDomain -eq "music") {
    $ContextPath = ".\Tools\npu\npu_music_context.md"
    $ChunkDir = ".\Tools\npu\npu_music_chunks"
    $OutPath = ".\Tools\npu\npu_music_context_for_aider.md"
    $NotesOut = ".\Tools\npu\npu_music_chunk_notes.md"
} else {
    $ContextPath = ".\Tools\npu\npu_code_context.md"
    $ChunkDir = ".\Tools\npu\npu_code_chunks"
    $OutPath = ".\Tools\npu\npu_context_for_aider.md"
    $NotesOut = ".\Tools\npu\npu_chunk_notes.md"
}

$ReviewArgs = @(
    ".\Tools\npu\run_npu_review.py",
    "--engine", $Engine,
    "--device", "NPU",
    "--ollama-model", $OllamaModel,
    "--domain", $ReviewDomain,
    "--mode", "chunked",
    "--context", $ContextPath,
    "--chunk-dir", $ChunkDir,
    "--out", $OutPath,
    "--notes-out", $NotesOut,
    "--max-context-chars", "0",
    "--chunk-chars", "10500",
    "--chunk-overlap-chars", "700",
    "--max-prompt-chars", "15000",
    "--max-chunk-tokens", "650",
    "--max-reduce-tokens", "750",
    "--max-new-tokens", "1100",
    "--max-prompt-len", "16384",
    "--min-response-len", "512"
)

if ($SkipFinal) {
    $ReviewArgs += "--skip-final"
}

$ReviewPython = $BUILD_PY
if ($Engine -eq "npu") {
    $ReviewPython = $NPU_PY
}

Invoke-Step `
    -Title "Run long-context review ($Engine / $ReviewDomain)" `
    -Exe $ReviewPython `
    -ArgsList $ReviewArgs

Write-Host ""
Write-Host "=== Done ==="
Write-Host "Generated:"
Write-Host "  Tools\npu\npu_code_context.md"
Write-Host "  Tools\npu\npu_code_index.md"
Write-Host "  Tools\npu\npu_code_manifest.json"
Write-Host "  Tools\npu\npu_code_chunks\chunk_*.md"
Write-Host "  Tools\npu\npu_chunk_notes.md"
Write-Host "  Tools\npu\npu_context_for_aider.md"
Write-Host "  Tools\npu\npu_music_context.md"
Write-Host "  Tools\npu\npu_music_manifest.json"
Write-Host "  Tools\npu\npu_music_chunks\chunk_*.md"
Write-Host "  Tools\npu\npu_music_chunk_notes.md"
Write-Host "  Tools\npu\npu_music_context_for_aider.md"
Write-Host "  output\Feel The Light-Luca Vera_Master_analysis_ai_context.json"
Write-Host "  output\Feel The Light-Luca Vera_Master_analysis_blender_keyframes.json"
Write-Host "  output\Feel The Light-Luca Vera_Master_ollama_music_insights.json"
Write-Host "  Tools\npu\ollama_music_insights.md"
