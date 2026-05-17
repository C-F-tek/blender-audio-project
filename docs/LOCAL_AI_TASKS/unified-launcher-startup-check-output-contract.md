# Unified launcher startup check output contract

## Scope

This document records the stable CLI contract for:

```text
python -m Tools.workflow startup_check
```

The tool is used directly by operators and indirectly by:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

## Public CLI

Supported options:

```text
--project <path>
--root <path>
--repo-root <path>
--output <path>
--text-output <path>
--json
```

`--repo-root` is a compatibility alias for `--root`.

`--output` is the selected JSON report path. It is intended for launcher-controlled and operator-controlled runs.

`--text-output` is optional. If omitted, the text report is written next to the JSON output using the same basename and `.txt` suffix.

`--json` prints the JSON report to stdout while still writing the selected report files.

## Launcher contract

The unified launcher may call:

```powershell
python -m Tools.workflow startup_check `
  --repo-root . `
  --output .\output\validation\startup_check_smoke_<STAMP>.json `
  --json
```

This call must remain report-only:

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
blender_runtime_execution_performed = false
ffmpeg_execution_performed = false
```

## Validation

Use:

```powershell
python -m Tools.validation run_startup_check_cli_contract_smoke `
  --repo-root . `
  --output .\output\validation\startup_check_cli_contract_smoke.json `
  --markdown-output .\output\validation\startup_check_cli_contract_smoke.md
```

## Validation report contract

The selected JSON report written by `--output` must itself be a validation report candidate.

Required common fields:

```text
schema_version
repo_root
passed
```

Recommended/common fields:

```text
kind
errors
warnings
```

The startup report uses:

```text
kind = startup_check
schema_version = 1
```

It also keeps the legacy fields `project`, `root`, `ok`, `warning_count` and `checks` for existing consumers.

## Production/debug note

`python -m Tools.workflow startup_check --output` is independent from the unified launcher's `-Prod` switch.

`-Prod` controls extra launcher debug-tail evidence only. It does not remove the startup smoke report selected through `--output`.
