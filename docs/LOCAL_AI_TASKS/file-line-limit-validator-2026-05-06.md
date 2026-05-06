# File line-limit validator — 2026-05-06

## Status

Active report-only validator for the IA-Carmine 400-line policy.

```text
Tool: Tools/validation/check_file_line_limits.py
Mode: report-only
Source writes: false
Patch application: false
Provider execution: false
Runtime/media execution: false
```

## Purpose

The validator measures maintained Markdown and source/script files against the current maintainability policy:

```text
Markdown: <= 400 lines per active .md file
Python/PowerShell/scripts/source code: <= 400 lines per maintained source file
```

It reports violations. It does not rewrite, split, delete or move files.

## Why this exists

The policy is now operational for both documentation and code.

Oversized files remain useful as evidence of technical debt, but they must not become reasons to avoid tool usage. They should be measured, tracked and refactored progressively.

## Default scope

Included suffixes by default:

```text
.md
.py
.ps1
.psm1
.psd1
.sh
.bat
.cmd
.js
.ts
.tsx
.jsx
```

Excluded directories by default:

```text
.git
.venv
venv
__pycache__
node_modules
output
renders
indexAI/code_chunks
indexAI/project_code_chunks
```

## Example command

```powershell
python .\Tools\validation\check_file_line_limits.py `
  --repo-root . `
  --output .\output\validation\file_line_limit_report.json `
  --markdown-output .\output\validation\file_line_limit_report.md
```

Strict mode for CI/local gate:

```powershell
python .\Tools\validation\check_file_line_limits.py `
  --repo-root . `
  --output .\output\validation\file_line_limit_report.json `
  --markdown-output .\output\validation\file_line_limit_report.md `
  --fail-on-violations
```

## Report contract

Expected JSON root fields:

```text
schema_version
kind=file_line_limit_report
generated_at
repo_root
max_lines
include_suffixes
excluded_dirs
checked_file_count
violation_count
violations
errors
passed
provider_execution_performed=false
patch_application_performed=false
source_writes_performed=false
persistent_memory_write_performed=false
```

## Interpretation

```text
passed=true
  No checked file exceeds the configured line limit and no read errors occurred.

passed=false
  One or more files exceed the limit or a file could not be read.
```

A violation is not an automatic refactor instruction. It is a measurable backlog item.

## Remediation policy

For Markdown over 400 lines:

```text
Keep the original file as a compact index.
Create a sibling folder named exactly like the file, including .md: <file>.md/.
Move detailed content into <file>.md/part-001.md, part-002.md, ...
Keep each part under 400 lines.
```

For code over 400 lines:

```text
Keep public entrypoints/wrappers compact.
Move implementation into a same-purpose package or module folder.
Split by responsibility.
Preserve CLI/API compatibility unless explicitly allowed to break it.
Report line counts for every created or modified code/script file.
```

Existing oversized files are technical debt. Do not split them blindly during unrelated work.

## Full0To10 relation

The validator is a Full0To10 evidence lane candidate. It should be included when checking repository maintainability, documentation drift or refactor readiness.

It does not disable other tools. It only makes size debt visible.
