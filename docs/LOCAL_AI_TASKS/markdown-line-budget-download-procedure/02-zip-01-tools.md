# 02 - ZIP 01 tools

```powershell
$Dest01 = ".\output\validation\patch_bundles\01_md_line_budget_tools"

Expand-Archive $Zip01 -DestinationPath $Dest01 -Force

python "$Dest01\run_patch_bundle.py"
```

## Valida

```powershell
python -m py_compile `
  .\Tools\docs\_shared\large_markdown_splitter_core.py `
  .\Tools\docs\_shared\split_large_markdown_cli.py `
  .\Tools\validation\check_markdown_line_limits.py

python -m Tools.docs split_large_markdown --repo-root . --max-lines 400

python -m Tools.validation check_markdown_line_limits --repo-root . --max-lines 400
```
