"""Generated file sources for agent-review patch bundles."""

from __future__ import annotations

def bundle_runner_source() -> str:
    return r'''#!/usr/bin/env python3
"""Apply or inspect an IA-Carmine agent-review patch bundle.

Default mode is dry-run. Use --apply explicitly to write managed Markdown blocks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

MANAGED_BEGIN_PREFIX = "<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN"
MANAGED_END_PREFIX = "<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def run_git_status(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001
        return f"GIT_STATUS_ERROR: {type(exc).__name__}: {exc}"
    return completed.stdout.strip()


def replace_or_append_managed_block(text: str, operation: dict[str, Any]) -> tuple[str, str]:
    block = str(operation["block"])
    begin_prefix = str(operation.get("managed_begin_prefix") or MANAGED_BEGIN_PREFIX)
    end_prefix = str(operation.get("managed_end_prefix") or MANAGED_END_PREFIX)
    block_id = ""
    for line in block.splitlines():
        if line.startswith(begin_prefix):
            marker = "id="
            if marker in line:
                block_id = line.split(marker, 1)[1].split("-->", 1)[0].strip()
            break
    if not block_id:
        return text.rstrip() + "\n" + block, "append"
    begin_marker = f"{begin_prefix} id={block_id} -->"
    end_marker = f"{end_prefix} id={block_id} -->"
    start = text.find(begin_marker)
    if start == -1:
        return text.rstrip() + "\n" + block, "append"
    end = text.find(end_marker, start)
    if end == -1:
        raise ValueError(f"managed begin marker exists without matching end marker: {block_id}")
    end += len(end_marker)
    replacement = text[:start].rstrip() + "\n" + block.strip() + "\n" + text[end:].lstrip()
    return replacement.rstrip() + "\n", "replace"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--manifest", default="patches/manifest.json")
    parser.add_argument("--report", default="patch_bundle_result.json")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    bundle_root = Path(__file__).resolve().parent
    manifest_path = bundle_root / args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    status = run_git_status(repo_root)
    errors: list[str] = []
    warnings: list[str] = []
    results: list[dict[str, Any]] = []

    if status and not args.allow_dirty:
        errors.append("working tree is not clean; rerun with --allow-dirty only after manual review")

    for operation in manifest.get("operations", []):
        target = str(operation.get("target") or "")
        target_path = (repo_root / target).resolve(strict=False)
        try:
            target_path.relative_to(repo_root)
        except ValueError:
            errors.append(f"target escapes repo root: {target}")
            continue
        if operation.get("kind") != "markdown_managed_block":
            warnings.append(f"skipped unsupported operation kind for {target}: {operation.get('kind')}")
            continue
        if not target_path.exists() or not target_path.is_file():
            errors.append(f"target missing: {target}")
            continue
        text = target_path.read_text(encoding="utf-8")
        before_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        try:
            new_text, action = replace_or_append_managed_block(text, operation)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{target}: {type(exc).__name__}: {exc}")
            continue
        after_hash = hashlib.sha256(new_text.encode("utf-8")).hexdigest()
        changed = before_hash != after_hash
        if args.apply and not errors and changed:
            target_path.write_text(new_text, encoding="utf-8", newline="\n")
        results.append(
            {
                "id": operation.get("id"),
                "target": target,
                "action": action,
                "changed": changed,
                "applied": bool(args.apply and changed and not errors),
                "before_sha256": before_hash,
                "after_sha256": after_hash,
            }
        )

    report = {
        "schema_version": 1,
        "kind": "agent_review_patch_bundle_result",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": bool(args.apply and not errors),
        "source_writes_performed": bool(args.apply and not errors),
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "apply_requested": bool(args.apply),
        "allow_dirty": bool(args.allow_dirty),
        "operation_count": len(manifest.get("operations", [])),
        "changed_count": sum(1 for item in results if item.get("changed")),
        "applied_count": sum(1 for item in results if item.get("applied")),
        "results": results,
        "git_status_before": status,
    }
    report_path = bundle_root / args.report
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "passed": report["passed"],
        "errors": report["errors"],
        "warnings": report["warnings"],
        "apply_requested": report["apply_requested"],
        "operation_count": report["operation_count"],
        "changed_count": report["changed_count"],
        "applied_count": report["applied_count"],
        "report": str(report_path),
        "patch_application_performed": report["patch_application_performed"],
    }, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
'''

def validation_script_source() -> str:
    return r"""param(
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
Set-Location $RepoRoot
python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax_after_patch_bundle.json
python -m Tools.validation check_validation_report_contract --repo-root . --report-file .\output\validation\python_syntax_after_patch_bundle.json --output .\output\validation\validation_report_contract_after_patch_bundle.json
git diff --check
git status --short
"""

def readme_source(bundle_name: str, operation_count: int, skipped_count: int) -> str:
    return f"""# IA-Carmine Agent Review Patch Bundle

Bundle: `{bundle_name}`

This bundle is generated from an `agent_review_patch_plan` report.

- Operations: `{operation_count}`
- Skipped candidates: `{skipped_count}`
- Default mode: dry-run
- Apply mode: explicit `--apply`
- Supported automatic operation: managed Markdown block append/replace only

## Dry-run

```powershell
python .\\run_patch_bundle.py --repo-root C:\\Users\\carmi\\blender\\blender-audio-project
```

## Apply

```powershell
python .\\run_patch_bundle.py --repo-root C:\\Users\\carmi\\blender\\blender-audio-project --apply
```

If your working tree is intentionally dirty, add `--allow-dirty` only after manual review.

## Validate after apply

```powershell
.\\scripts\\validate_after_patch.ps1 -RepoRoot C:\\Users\\carmi\\blender\\blender-audio-project
```

## Guardrails

This bundle never executes providers, never runs Blender, never writes SQLite and never performs Git operations.
"""
