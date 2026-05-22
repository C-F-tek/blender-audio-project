# Reusable Patchkit Controlled Bundles

## Goal

Make future IA-Carmine patch bundles small and deterministic.

Instead of creating a new one-off patcher for every intervention, future work should provide only the patch core:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*
```

and apply it through the reusable OOB runner:

```powershell
python -m ia_carmine.cli apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python -m ia_carmine.cli apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

## Why this matters

The heap/exchange center remains dynamic. GPU0, GPU1, NPU, provider lanes and context lanes can cooperate inside the runtime heap without being micromanaged.

At the boundary, however, generated proposals must become deterministic, reviewable patch operations.

Patchkit is that boundary layer.

It handles:

- backup;
- encoding and newline preservation;
- idempotency markers;
- PowerShell `Invoke-Checked` anchors;
- marker insertions;
- exact replacements;
- parser checks;
- Python compile checks;
- `git diff --check`;
- JSON/Markdown reports;
- line count reporting.

## Bundle schema v1

```json
{
  "schema_version": 1,
  "kind": "codemod_patch_bundle",
  "operations": [
    {
      "operation": "insert_after_invoke_checked",
      "target": "Tools/workflow/run_unified_local_ai_refactor.ps1",
      "label": "Build AI workload quality routing report",
      "marker": "IA-CARMINE-EXAMPLE-BEGIN",
      "content_file": "fragments/example.ps1"
    }
  ],
  "validators": [
    "powershell_parser",
    "python_compile",
    "git_diff_check"
  ]
}
```

## Supported operations

```text
insert_after_invoke_checked
insert_before_marker
insert_after_marker
replace_once
append_once
assert_marker
assert_no_naked_throw
```

## Validation

```powershell
python -m py_compile `
  .\ia_carmine\product\patchkit\filesystem.py `
  .\ia_carmine\product\patchkit\anchors.py `
  .\ia_carmine\product\patchkit\powershell.py `
  .\ia_carmine\product\patchkit\reports.py `
  .\ia_carmine\product\patchkit\apply_patch_bundle.py `
  .\Tools\validation\run_patchkit_smoke.py

python -m Tools.validation run_patchkit_smoke `
  --repo-root .

git diff --check
```

## Policy

Do not use patchkit to bypass review.

Patchkit only makes safe deterministic application repeatable. It does not change the project guardrails:

- no merge to master without operator command;
- no delete unless explicitly requested;
- no force-push;
- no rewrite history;
- no secrets, permissions, billing or visibility changes;
- no runtime Blender/FFmpeg execution;
- no generated output/index/db/renders commits.
