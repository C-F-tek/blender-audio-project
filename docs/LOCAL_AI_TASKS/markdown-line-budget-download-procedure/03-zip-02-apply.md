# 03 - ZIP 02 apply

```powershell
$Dest02 = ".\output\validation\patch_bundles\02_md_line_budget_apply"

Expand-Archive $Zip02 -DestinationPath $Dest02 -Force
```

## Dry-run

```powershell
python "$Dest02\run_patch_bundle.py"
```

## Apply reale

```powershell
python "$Dest02\run_patch_bundle.py" --apply-doc-split
```

## Validazione

```powershell
python -m Tools.validation check_markdown_line_limits --repo-root . --max-lines 400
git diff --check
git status --short
```
