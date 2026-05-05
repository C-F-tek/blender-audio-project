# 02 - ZIP 01 tools

```powershell
$Dest01 = ".\output\validation\patch_bundles\01_md_line_budget_tools"

Expand-Archive $Zip01 -DestinationPath $Dest01 -Force

python "$Dest01\run_patch_bundle.py"
```

## Valida

```powershell
python -m py_compile `
  .\Tools\docs\split_large_markdown.py `
  .\Tools\validation\check_markdown_line_limits.py

python .\Tools\docs\split_large_markdown.py --repo-root . --max-lines 400

python .\Tools\validation\check_markdown_line_limits.py --repo-root . --max-lines 400
```
