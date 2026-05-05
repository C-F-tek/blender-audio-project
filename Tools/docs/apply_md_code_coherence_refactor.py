#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def repo_root_from(start: Path) -> Path:
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"Repository root not found from {start}")


def limited_lines(lines: list[str], limit: int = 390) -> str:
    if len(lines) <= limit:
        return "\
".join(lines).rstrip() + "\
"
    head = lines[: limit - 8]
    head.extend([
        "",
        "## Troncato",
        "",
        f"Questo documento è stato limitato a {limit} righe.",
        "Rigenerare il report completo in `output/validation/` per il dettaglio integrale.",
    ])
    return "\
".join(head).rstrip() + "\
"


def read_report(repo: Path, report_arg: str) -> dict[str, Any]:
    path = repo / report_arg
    if not path.exists():
        builder = repo / "Tools" / "docs" / "build_code_aware_md_coherence.py"
        if not builder.exists():
            raise SystemExit(f"[FAIL] Missing report and builder: {path}")
        subprocess.run([
            sys.executable, str(builder),
            "--repo-root", str(repo),
            "--output", report_arg,
            "--markdown-output", "output/validation/md_code_coherence_report.md",
        ], cwd=repo, check=True)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def render_tool_index(report: dict[str, Any], stamp: str) -> str:
    scripts = report.get("scripts", [])
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in scripts:
        path = s.get("path", "")
        if not path.startswith("Tools/"):
            continue
        parts = path.split("/")
        group = "/".join(parts[:2]) if len(parts) >= 2 else "Tools"
        groups[group].append(s)

    lines = [
        "# Code-aware tool index",
        "",
        f"Generated: `{stamp}`",
        "",
        "Questo indice è derivato dal codice locale tramite `Tools/docs/build_code_aware_md_coherence.py`.",
        "Non sostituisce i runbook canonici; serve come mappa compatta per review e PR.",
        "",
        "## Regole",
        "",
        "- Non eseguire provider o runtime Blender/FFmpeg da questo indice.",
        "- Non committare `output/**`, `*.db`, `*.sqlite`, `renders/**`.",
        "- Ogni comando reale va validato contro il parser/param block dello script target.",
        "",
    ]
    for group in sorted(groups):
        lines.append(f"## {group}")
        lines.append("")
        for s in sorted(groups[group], key=lambda x: x.get("path", ""))[:80]:
            flags = s.get("argparse_flags") or s.get("ps_params") or []
            flag_preview = ", ".join(flags[:10]) if flags else "no explicit CLI contract detected"
            lines.append(f"- `{s.get('path')}` — lines=`{s.get('lines')}`; flags: {flag_preview}")
        lines.append("")
    return limited_lines(lines)


def render_current_state(report: dict[str, Any], stamp: str) -> str:
    summary = report.get("summary", {})
    by_kind = summary.get("by_kind", {})
    by_sev = summary.get("by_severity", {})
    lines = [
        "# Markdown/code coherence current state",
        "",
        f"Generated: `{stamp}`",
        "",
        "## Summary",
        "",
        f"- Markdown scanned: `{summary.get('markdown_count')}`",
        f"- Scripts scanned: `{summary.get('script_count')}`",
        f"- Findings: `{summary.get('finding_count')}`",
        f"- Patch plan candidates: `{summary.get('patch_plan_count')}`",
        "",
        "## Findings by severity",
        "",
    ]
    for k, v in sorted(by_sev.items()):
        lines.append(f"- `{k}`: `{v}`")
    lines += ["", "## Findings by kind", ""]
    for k, v in sorted(by_kind.items()):
        lines.append(f"- `{k}`: `{v}`")
    lines += ["", "## Next actions", ""]
    for plan in report.get("patch_plan", []):
        lines.append(f"### {plan.get('id')} — {plan.get('area')}")
        lines.append(f"- Risk: `{plan.get('risk')}`")
        lines.append(f"- Status: `{plan.get('status')}`")
        lines.append(f"- Rationale: {plan.get('rationale')}")
        lines.append(f"- Strategy: {plan.get('strategy')}")
        lines.append("")
    lines += ["## Top 80 findings", ""]
    for f in report.get("findings", [])[:80]:
        lines.append(f"- `{f.get('severity')}` `{f.get('kind')}` `{f.get('path')}` -> {f.get('detail')}")
    return limited_lines(lines)


def render_command_contract(report: dict[str, Any], stamp: str) -> str:
    scripts = report.get("scripts", [])
    command_scripts = [s for s in scripts if s.get("command_like") and s.get("path", "").startswith("Tools/")]
    lines = [
        "# Code-aware command contract",
        "",
        f"Generated: `{stamp}`",
        "",
        "Questo file sintetizza i contratti CLI visibili dal codice: `argparse.add_argument()` per Python e `param(...)` per PowerShell.",
        "Se un comando documentato usa flag non presenti qui, va verificato se la documentazione è stale o se lo script usa parsing dinamico.",
        "",
    ]
    for s in sorted(command_scripts, key=lambda x: x.get("path", ""))[:160]:
        flags = s.get("argparse_flags") or s.get("ps_params") or []
        lines.append(f"## `{s.get('path')}`")
        lines.append("")
        lines.append(f"- Lines: `{s.get('lines')}`")
        lines.append(f"- Has main: `{s.get('has_main')}`")
        if flags:
            lines.append("- Flags:")
            for flag in flags[:60]:
                lines.append(f"  - `{flag}`")
        else:
            lines.append("- Flags: `none detected`")
        lines.append("")
    return limited_lines(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply safe code-aware Markdown coherence docs generated from report.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report", default="output/validation/md_code_coherence_report.json")
    parser.add_argument("--apply", action="store_true", help="Write generated docs. Default is dry-run.")
    parser.add_argument("--stamp", default="")
    args = parser.parse_args()

    repo = repo_root_from(Path(args.repo_root))
    stamp = args.stamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    report = read_report(repo, args.report)
    targets = {
        "docs/LOCAL_AI_TASKS/code-aware-tool-index.md": render_tool_index(report, stamp),
        "docs/LOCAL_AI_TASKS/md-code-coherence-current-state.md": render_current_state(report, stamp),
        "docs/LOCAL_AI_TASKS/code-aware-command-contract.md": render_command_contract(report, stamp),
    }
    print("[PLAN] Generated docs:")
    for rel, content in targets.items():
        print(f"- {rel}: {len(content.splitlines())} lines")
    if not args.apply:
        print("[DRY-RUN] Re-run with --apply to write generated docs.")
        return 0
    for rel, content in targets.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        old = path.read_text(encoding="utf-8-sig") if path.exists() else None
        if old == content:
            print(f"[SKIP] unchanged {rel}")
        else:
            path.write_text(content, encoding="utf-8", newline="\
")
            print(f"[WRITE] {rel}: {len(content.splitlines())} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
