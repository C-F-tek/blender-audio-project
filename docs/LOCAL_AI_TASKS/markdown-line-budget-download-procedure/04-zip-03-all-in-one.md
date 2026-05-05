# 04 - ZIP 03 all-in-one

Usare solo se si vuole saltare ZIP 01 + ZIP 02.

```powershell
$Dest03 = ".\output\validation\patch_bundles\03_md_line_budget_all_in_one"

Expand-Archive $Zip03 -DestinationPath $Dest03 -Force

python "$Dest03\run_patch_bundle.py"

python "$Dest03\run_patch_bundle.py" --apply-doc-split
```
