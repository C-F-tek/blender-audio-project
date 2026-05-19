# Tools/validation/docs_hygiene context

## Role

`Tools/validation/docs_hygiene` contains checks and builders for documentation hygiene, Markdown inventories, line counts, package structure, links, JSON artifacts and refactor consistency.

## Responsibilities

- Build Markdown and script inventories.
- Check Markdown/code coherence.
- Check docs links and contract drift.
- Check file and Markdown line limits.
- Check Python syntax and package structure.
- Build Python line-count reports.
- Check generated JSON artifacts.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation build_markdown_inventory ...
python -m Tools.validation build_script_inventory ...
python -m Tools.validation check_docs_links ...
python -m Tools.validation check_docs_contract_drift ...
python -m Tools.validation check_code_contract_drift ...
python -m Tools.validation check_file_line_limits ...
python -m Tools.validation check_markdown_line_limits ...
python -m Tools.validation check_python_syntax ...
python -m Tools.validation check_package_structure ...
python -m Tools.validation build_python_line_count_csv ...
```

## Output role

Outputs are validation or inventory reports. Raw output normally stays under `output/**` unless a compact evidence artifact is selected.

## Notes

- Use these checks before large documentation passes.
- Keep generated inventories out of Git by default.
- Add checks here when documentation contract rules change.
