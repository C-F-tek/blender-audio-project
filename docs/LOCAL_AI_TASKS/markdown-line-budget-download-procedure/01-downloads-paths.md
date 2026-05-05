# 01 - Downloads paths

```powershell
cd C:\Users\carmi\blender\blender-audio-project

$Downloads = "$env:USERPROFILE\Downloads"

$Zip01 = Join-Path $Downloads "01_ia_carmine_md_line_budget_tools_patch_bundle.zip"
$Zip02 = Join-Path $Downloads "02_ia_carmine_md_line_budget_apply_bundle.zip"
$Zip03 = Join-Path $Downloads "03_ia_carmine_md_line_budget_all_in_one_bundle.zip"

Test-Path $Zip01
Test-Path $Zip02
Test-Path $Zip03
```

Se un file manca, correggere `Downloads`, non copiare ZIP nella repo.
