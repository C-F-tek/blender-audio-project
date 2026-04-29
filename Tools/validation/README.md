# Tools/validation

This folder contains lightweight repository validation helpers.

The tools are intentionally non-invasive: they inspect files and write optional
reports, but they do not rewrite source code or generated artifacts.

## Available checks

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

## Optional reports

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output output\validation\python_syntax.json
python .\Tools\validation\check_package_structure.py --repo-root . --output output\validation\package_structure.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output output\validation\json_artifacts.json
```

## Notes

- `check_python_syntax.py` compiles Python files without importing project modules.
- `check_package_structure.py` reports package-level warnings under `Scripting/`.
- `check_json_artifacts.py` checks JSON parseability and skips very large files by default.
