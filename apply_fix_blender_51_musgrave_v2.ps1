# Fix Blender 5.1 compatibility: ShaderNodeTexMusgrave -> ShaderNodeTexNoise
# Esegui dalla root del repository:
#   powershell -ExecutionPolicy Bypass -File .\apply_fix_blender_51_musgrave_v2.ps1

$ErrorActionPreference = "Stop"

$File = ".\Scripting\ready_to_jazz_wow_youtube_profiles_audio_sync\main_ready_to_jazz_wow_youtube.py"

if (-not (Test-Path $File)) {
    throw "File non trovato: $File. Esegui lo script dalla root del repository."
}

$Text = Get-Content $File -Raw -Encoding UTF8
$BeforeLines = (($Text -split "`r?`n").Count)

if ($Text -notlike '*ShaderNodeTexMusgrave*') {
    Write-Host "[INFO] ShaderNodeTexMusgrave non trovato: patch gia applicata o file gia corretto."
} else {
    $Pattern = '(?ms)    musgrave = nodes\.new\("ShaderNodeTexMusgrave"\)\r?\n    musgrave\.location = \(-800, -30\)\r?\n    musgrave\.inputs\[2\]\.default_value = 8\.0\r?\n    musgrave\.inputs\[3\]\.default_value = 2\.0\r?\n    musgrave\.inputs\[4\]\.default_value = 0\.55\r?\n    musgrave\.inputs\[5\]\.default_value = 1\.8'
    $Replacement = @'
    detail_noise = nodes.new("ShaderNodeTexNoise")
    detail_noise.location = (-800, -30)
    detail_noise.inputs["Scale"].default_value = 18.0
    detail_noise.inputs["Detail"].default_value = 10.0
    detail_noise.inputs["Roughness"].default_value = 0.58
    if "Distortion" in detail_noise.inputs:
        detail_noise.inputs["Distortion"].default_value = 0.18
'@

    $NewText = [regex]::Replace($Text, $Pattern, $Replacement, 1)

    if ($NewText -eq $Text) {
        throw "Blocco ShaderNodeTexMusgrave non trovato nel formato previsto. Patch non applicata."
    }

    $NewText = $NewText.Replace('links.new(mapping.outputs["Vector"], musgrave.inputs["Vector"])', 'links.new(mapping.outputs["Vector"], detail_noise.inputs["Vector"])')
    $NewText = $NewText.Replace('links.new(musgrave.outputs["Fac"], bump.inputs["Height"])', 'links.new(detail_noise.outputs["Fac"], bump.inputs["Height"])')

    Set-Content $File -Value $NewText -Encoding UTF8 -NoNewline
}

$AfterText = Get-Content $File -Raw -Encoding UTF8
$AfterLines = (($AfterText -split "`r?`n").Count)

if ($AfterText -like '*ShaderNodeTexMusgrave*') {
    throw "Patch incompleta: ShaderNodeTexMusgrave e ancora presente."
}
if ($AfterText -notlike '*detail_noise = nodes.new("ShaderNodeTexNoise")*') {
    throw "Patch incompleta: detail_noise non presente."
}

Write-Host "[OK] Patch applicata."
Write-Host "[INFO] Righe prima: $BeforeLines"
Write-Host "[INFO] Righe dopo : $AfterLines"
Write-Host ""
git diff -- Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py
