#!/usr/bin/env python3
"""Ensure required AI context files exist before heap/context reload.

This tool reads required files from tools.ai.build_ai_context_pack and creates
only known compact Markdown routing documents when a required path is truly
missing. Directory-form Markdown docs such as docs/PROJECT_STATUS_POINT.md/
are treated as existing when they contain README.md or part-*.md, matching
build_ai_context_pack split Markdown support.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

KNOWN_MARKDOWN_TEMPLATES: dict[str, str] = {
    "docs/README.md": """# Documentation Index

## Status

Compact repository documentation index.

Canonical root contract:

```text
../AGENTS.md
```

Current docs-side router:

```text
AI_DOCS_ENTRYPOINT.md
```

## Current first-read path

```text
../AGENTS.md
../CHATGPT.md
../CHATGPT/README.md
README.md
AI_DOCS_ENTRYPOINT.md
LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

## Active maps

| Area | Document |
|---|---|
| Runtime architecture | `MAIN_RUNTIME_ARCHITECTURE.md` |
| Local AI workflow | `LOCAL_AI_WORKFLOW.md` |
| Data flow | `DATA_FLOW.md` |
| JSON/report schemas | `JSON_SCHEMAS.md` |
| Patch-spec workflow | `PATCH_SPEC_WORKFLOW.md` |
| Project status | `PROJECT_STATUS_POINT.md` |
| AI docs entrypoint | `AI_DOCS_ENTRYPOINT.md` |
| Tooling index | `../tools/ai/README.md`, `../tools/workflow/README.md`, `../tools/validation/README.md` |

## Policy

Keep this file compact. Do not add competing first-read orders here.
""",
    "docs/PATCH_SPEC_WORKFLOW.md": """# Patch Spec Workflow

## Status

Compact required workflow bridge for patch-spec and PatchKit work.

This file is required by AI context-pack startup and is intentionally a routing
document. It does not authorize source writes by itself.

## Source-write boundary

Current controlled source-write mechanisms:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.py
patch_specs/<bundle>/fragments/*.ps1
tools/ai/patchkit/apply_patch_bundle.py
tools/ai/apply_generated_patch_specs_for_review_pr.py
```

Patch notes, proposal ledgers and generated summaries are review inputs only.
They must become deterministic patch operations or branch diffs before source
files are modified.

## Standard local sequence

```powershell
$RepoPy = (Resolve-Path .\\.venv\\Scripts\\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy .\\Tools\\ai\\patchkit\\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\\patch_specs\\<bundle>\\bundle.json `
  --dry-run

& $RepoPy .\\Tools\\ai\\patchkit\\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\\patch_specs\\<bundle>\\bundle.json
```

## Required validation posture

```text
inspect current source
verify target files exist
avoid output/**, renders/**, *.db, *.sqlite, indexAI/code_chunks/**
run py_compile or focused validator when Python changes
run git diff --check
report resulting line counts for scripts/code
record unavailable/degraded provider lanes as evidence, not success
```

## Read next

```text
../AGENTS.md
AI_DOCS_ENTRYPOINT.md
LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
../patch_specs/README.md
../tools/ai/patchkit/apply_patch_bundle.py
```
""",
    "docs/PROJECT_STATUS_POINT.md": """# Project Status Point

## Status

Compact current status checkpoint for IA-Carmine repository self-improvement.

## Current project identity

```text
IA-Carmine Local AI Orchestration Workbench
```

The active architecture is the local AI orchestration workbench: heap/exchange
runtime, provider lanes, broker/tool execution, memory/context preload,
validators, evidence bundles and patch/review product lanes.

## Current runtime target

```text
IN -> preload/context/memory/tool state -> heap/exchange loop -> deterministic OUT
```

## Product expectation

A successful product run must produce concrete reviewable output, not only
telemetry. Proposal chunks must reference real repository paths and must not be
placeholder/TODO/stub content.
""",
    "docs/DATA_FLOW.md": """# Data Flow

## Status

Compact active data-flow contract.

## Runtime flow

```text
operator task / task Markdown
  -> required docs/context initializer
  -> real product preflight
  -> tool catalog + repo docs + semantic chunks + memory inventory
  -> startup task-file / heap input
  -> heap blackboard / exchange state
  -> provider lanes and deterministic tools
  -> proposal chunks / patch specs / evidence
  -> composer / review product / final package
```

## Failure rule

A degraded context preload may continue only when artifact usefulness is
recorded explicitly. A final product must fail honestly when no concrete
proposal/patch output exists.
""",
    "docs/LOCAL_AI_WORKFLOW.md": """# Local AI Workflow

## Status

Compact workflow contract for local AI runs.

## Canonical product path

```text
tools/workflow/run_unified_real_product_pr.ps1
```

## Heap/context closure path

```text
tools/ai/run_heap_runtime_context_closure.py
```

The heap closure path must perform:

```text
required context file initialization
real product preflight
startup docs/memory/tool/context reload
heap runtime execution
composer/export closure
```

## Python environment

```powershell
$RepoPy = (Resolve-Path .\\.venv\\Scripts\\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path
```
""",
    "docs/JSON_SCHEMAS.md": """# JSON Schemas

## Status

Compact schema orientation for IA-Carmine reports.

## Common report fields

```text
schema_version
kind
generated_at
repo_root
passed
errors
warnings
provider_execution_performed
patch_application_performed
source_writes_performed
```

## Context preload fields

```text
tool_executions
effective_passed
artifact_useful
input_ready_before_heap
startup_task_file
required_context_files_json
tool_catalog
memory_inventory
operational_memory
transient_request_context
ai_context_pack
semantic_chunks
repo_docs
```

## Contract rule

When a tool continues after partial failure, it must record the degraded
requirement and the artifact usefulness explicitly.
""",
}


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return (
            path.resolve(strict=False)
            .relative_to(repo_root.resolve(strict=False))
            .as_posix()
        )
    except ValueError:
        return path.as_posix()


def split_markdown_parts(path: Path) -> list[Path]:
    if not path.is_dir() or not path.name.endswith(".md"):
        return []
    parts: list[Path] = []
    readme = path / "README.md"
    if readme.is_file():
        parts.append(readme)
    parts.extend(sorted(item for item in path.glob("part-*.md") if item.is_file()))
    return parts


def required_path_exists(path: Path) -> bool:
    if path.is_file():
        return True
    return bool(split_markdown_parts(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Required AI Context Files",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Profile: `{report['profile']}`",
        f"- Apply: `{report['apply']}`",
        f"- Created count: `{len(report['created_files'])}`",
        f"- Existing split-doc count: `{len(report['existing_split_docs'])}`",
        f"- Missing unhandled count: `{len(report['missing_unhandled'])}`",
        "",
        "## Required files",
        "",
    ]
    for item in report["required_files"]:
        lines.append(
            f"- `{item['path']}` exists_before=`{item['exists_before']}` "
            f"exists_after=`{item['exists_after']}` split_doc=`{item['split_doc']}` "
            f"created=`{item['created']}` allowed=`{item['initializable']}`"
        )
    if report["missing_unhandled"]:
        lines.extend(["", "## Missing unhandled", ""])
        for item in report["missing_unhandled"]:
            lines.append(f"- `{item}`")
    return "\n".join(lines) + "\n"


def load_profiles(repo_root: Path) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    module = importlib.import_module("tools.ai.build_ai_context_pack")
    profiles = getattr(module, "PROFILES", {})
    return profiles if isinstance(profiles, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--profile", default="project_self_improvement")
    parser.add_argument(
        "--output", default="output/validation/required_ai_context_files.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/required_ai_context_files.md"
    )
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    profiles = load_profiles(repo_root)
    profile = profiles.get(args.profile)
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(profile, dict):
        errors.append(f"unknown context pack profile: {args.profile}")
        profile = {}

    required_items = [
        item
        for item in profile.get("required_files", [])
        if isinstance(item, dict) and str(item.get("path") or "").strip()
    ]
    required_reports: list[dict[str, Any]] = []
    created_files: list[str] = []
    existing_split_docs: list[str] = []
    missing_unhandled: list[str] = []

    for item in required_items:
        rel_path = str(item.get("path") or "").strip().replace("\\", "/")
        target = repo_root / rel_path
        exists_before = required_path_exists(target)
        split_doc = bool(split_markdown_parts(target))
        initializable = rel_path in KNOWN_MARKDOWN_TEMPLATES
        created = False

        if split_doc:
            existing_split_docs.append(rel_path)

        if not exists_before:
            if initializable and not target.exists():
                if args.apply:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(
                        KNOWN_MARKDOWN_TEMPLATES[rel_path].rstrip() + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
                    created = True
                    created_files.append(rel_path)
                else:
                    warnings.append(
                        f"would initialize missing required context file: {rel_path}"
                    )
            elif initializable and target.exists() and target.is_dir():
                # A directory exists but is not a valid split Markdown doc. Do not overwrite it.
                missing_unhandled.append(rel_path)
            else:
                missing_unhandled.append(rel_path)

        exists_after = required_path_exists(target)
        required_reports.append(
            {
                "path": rel_path,
                "role": item.get("role", ""),
                "exists_before": exists_before,
                "exists_after": exists_after,
                "split_doc": split_doc,
                "initializable": initializable,
                "created": created,
            }
        )

    if missing_unhandled:
        errors.append(
            "missing required context files without safe initializer: "
            + ", ".join(missing_unhandled)
        )

    report = {
        "schema_version": 1,
        "kind": "required_ai_context_files",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "profile": args.profile,
        "apply": bool(args.apply),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": bool(created_files),
        "created_files": created_files,
        "existing_split_docs": existing_split_docs,
        "missing_unhandled": missing_unhandled,
        "required_files": required_reports,
        "errors": errors,
        "warnings": warnings,
    }

    output = (repo_root / args.output).resolve()
    markdown_output = (repo_root / args.markdown_output).resolve()
    write_json(output, report)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                **report,
                "output": repo_rel(repo_root, output),
                "markdown_output": repo_rel(repo_root, markdown_output),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
