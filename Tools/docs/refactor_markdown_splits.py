#!/usr/bin/env python3
"""Refactor IA-Carmine Markdown splits and prune approved obsolete snapshots.

Policy implemented:
- new split layout is directory-form `name.md/README.md` + `name.md/part-xxx.md`;
- old legacy split folders `name/part-xxx.md` are migrated to `name.md/part-xxx.md`;
- source file `name.md` cannot coexist with directory `name.md`, so its index/stub is moved
  to `name.md/README.md`;
- generated/evidence/runtime trees are skipped by default;
- pruning is allowlist-only and deletes only explicitly approved historical/superseded snapshots.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

MARKER_MANIFEST = "_ia_carmine_md_split_manifest.json"
DEFAULT_MAX_LINES = 400
DEFAULT_SCOPES = (".", "docs", "CHATGPT")
SKIP_DIRS = {".git", ".venv", "venv", "output", "renders", "node_modules", "__pycache__"}
SKIP_PREFIXES = (
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "indexAI/scene_scripts/",
)
PRUNE_ALLOWLIST = (
    "docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md",
    "docs/LOCAL_AI_TASKS/full-access-md-telemetry-refactor-cycle-2026-05-06.md",
    "docs/LOCAL_AI_TASKS/docs-md-obsolete-pruning-next-step.md",
)
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
MD_LINK_RE = re.compile(r"(?P<prefix>!?\[[^\]]*\]\()(?P<url><[^>]+>|[^)\s]+)(?P<title>\s+\"[^\"]*\")?(?P<suffix>\))")


def repo_root(start: Path) -> Path:
    for p in (start.resolve(), *start.resolve().parents):
        if (p / ".git").exists():
            return p
    raise SystemExit("repository root not found")


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8-sig", errors="replace").splitlines())


def skipped(path: Path, root: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    r = rel(path, root)
    return any(r.startswith(prefix) for prefix in SKIP_PREFIXES)


def git_status(root: Path) -> list[str]:
    r = subprocess.run(["git", "status", "--short"], cwd=root, text=True, capture_output=True)
    return [line for line in r.stdout.splitlines() if line.strip()]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, text: str, apply: bool) -> int:
    text = text.rstrip() + "\n"
    if apply:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    return len(text.splitlines())


def split_lines(lines: list[str], max_lines: int) -> list[list[str]]:
    budget = max(60, max_lines - 22)
    chunks: list[list[str]] = []
    current: list[str] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
        starts_heading = not in_fence and line.startswith("#") and line.lstrip("#").startswith(" ")
        if starts_heading and current and len(current) >= budget // 2:
            chunks.append(current)
            current = [line]
        elif len(current) >= budget:
            if in_fence:
                current.append("```")
                chunks.append(current)
                current = ["```", line]
            else:
                chunks.append(current)
                current = [line]
        else:
            current.append(line)
    if current:
        chunks.append(current)
    return chunks


def rewrite_links_for_part(text: str, source_name: str) -> str:
    text = text.replace(f"../{source_name}", "README.md")
    return text


def render_readme(title: str, source_note: str, part_names: list[str], max_lines: int) -> str:
    lines = [
        "<!-- IA-CARMINE-MD-SPLIT: index -->",
        f"# Indice — {title}",
        "",
        source_note,
        f"Limite massimo configurato: `{max_lines}` righe per file Markdown.",
        "",
        "## Parti",
        "",
    ]
    lines += [f"{i}. [`{name}`]({name})" for i, name in enumerate(part_names, 1)]
    lines += ["", "## Regola", "", "Split directory-form conforme alla policy: `nomefile.md/part-xxx.md`."]
    return "\n".join(lines) + "\n"


def render_part_header(title: str, index: int, total: int) -> str:
    lines = [
        "<!-- IA-CARMINE-MD-SPLIT: part -->",
        f"# {title} — parte {index:03d} di {total:03d}",
        "",
        "Sorgente indice: [`README.md`](README.md)",
        "",
        "## Navigazione",
        "",
        "- [Indice](README.md)",
    ]
    if index > 1:
        lines.append(f"- [Parte precedente](part-{index - 1:03d}.md)")
    if index < total:
        lines.append(f"- [Parte successiva](part-{index + 1:03d}.md)")
    lines.append("")
    return "\n".join(lines) + "\n"


def find_legacy_split_dirs(root: Path, scopes: list[str]) -> list[Path]:
    found: dict[str, Path] = {}
    for scope in scopes:
        base = (root / scope).resolve()
        if not base.exists():
            continue
        dirs = [base] if base.is_dir() else []
        dirs += [p for p in base.rglob("*") if p.is_dir()]
        for d in dirs:
            if skipped(d, root) or d.name.endswith(".md"):
                continue
            if any(d.glob("part-*.md")) or (d / MARKER_MANIFEST).exists():
                found[rel(d, root)] = d
    return [found[k] for k in sorted(found)]


def migrate_legacy_dir(old_dir: Path, root: Path, max_lines: int, apply: bool) -> dict[str, Any]:
    source_file = old_dir.with_name(old_dir.name + ".md")
    new_dir = source_file
    if new_dir.exists() and new_dir.is_dir():
        return {"path": rel(old_dir, root), "action": "skip_already_migrated", "target_dir": rel(new_dir, root)}
    parts = sorted(old_dir.glob("part-*.md"))
    if not parts:
        return {"path": rel(old_dir, root), "action": "skip_no_parts"}
    tmp = old_dir.with_name(old_dir.name + ".md.__tmp__")
    if apply and tmp.exists():
        shutil.rmtree(tmp)
    if apply:
        tmp.mkdir(parents=True)
    part_names = [p.name for p in parts]
    readme_source = source_file if source_file.exists() else old_dir / "README.md"
    source_note = f"Documento migrato da layout legacy `{rel(old_dir, root)}/part-xxx.md`."
    if readme_source.exists():
        source_note += f" Stub precedente: `{rel(readme_source, root)}`."
    readme_lines = write(tmp / "README.md", render_readme(source_file.name, source_note, part_names, max_lines), apply)
    migrated_parts: list[dict[str, Any]] = []
    for idx, part in enumerate(parts, 1):
        text = rewrite_links_for_part(read(part), source_file.name)
        header_re = re.compile(r"\A<!-- IA-CARMINE-MD-SPLIT: part -->.*?## Navigazione\n\n(?:- .+\n)+\n", re.S)
        text = header_re.sub("", text)
        out = render_part_header(source_file.stem, idx, len(parts)) + text
        lines = write(tmp / part.name, out, apply)
        migrated_parts.append({"path": f"{rel(new_dir, root)}/{part.name}", "lines": lines})
    manifest = {
        "kind": "ia_carmine_markdown_split_manifest",
        "layout": "directory_form_md_suffix",
        "migrated_from": rel(old_dir, root),
        "target_dir": rel(new_dir, root),
        "part_count": len(parts),
        "max_lines": max_lines,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "parts": migrated_parts,
    }
    if apply:
        (tmp / MARKER_MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        if source_file.exists() and source_file.is_file():
            source_file.unlink()
        shutil.rmtree(old_dir)
        tmp.rename(new_dir)
    return {"path": rel(old_dir, root), "action": "migrate_legacy_split", "target_dir": rel(new_dir, root), "readme_lines": readme_lines, "parts": migrated_parts}


def split_monolithic_file(path: Path, root: Path, max_lines: int, apply: bool) -> dict[str, Any]:
    if path.is_dir() or skipped(path, root) or line_count(path) <= max_lines:
        return {"path": rel(path, root), "action": "skip"}
    lines = read(path).splitlines()
    chunks = split_lines(lines, max_lines)
    new_dir = path
    tmp = path.with_name(path.name + ".__tmp__")
    if apply and tmp.exists():
        shutil.rmtree(tmp)
    if apply:
        tmp.mkdir(parents=True)
    part_names = [f"part-{i:03d}.md" for i in range(1, len(chunks) + 1)]
    part_results = []
    for idx, chunk in enumerate(chunks, 1):
        text = render_part_header(path.stem, idx, len(chunks)) + "\n".join(chunk) + "\n"
        lines_after = write(tmp / part_names[idx - 1], text, apply)
        part_results.append({"path": f"{rel(new_dir, root)}/{part_names[idx - 1]}", "lines": lines_after})
    source_note = f"Documento monolitico trasformato da file `{rel(path, root)}` a directory-form."
    readme_lines = write(tmp / "README.md", render_readme(path.name, source_note, part_names, max_lines), apply)
    if apply:
        (tmp / MARKER_MANIFEST).write_text(json.dumps({"kind": "ia_carmine_markdown_split_manifest", "layout": "directory_form_md_suffix", "source_path": rel(path, root), "part_count": len(chunks)}, indent=2) + "\n", encoding="utf-8")
        path.unlink()
        tmp.rename(new_dir)
    return {"path": rel(path, root), "action": "split_monolithic", "target_dir": rel(new_dir, root), "readme_lines": readme_lines, "parts": part_results}


def prune_obsolete(root: Path, apply: bool) -> list[dict[str, Any]]:
    out = []
    for item in PRUNE_ALLOWLIST:
        path = root / item
        if not path.exists():
            out.append({"path": item, "action": "skip_missing"})
            continue
        text = read(path).lower()
        allowed = any(token in text for token in ("historical", "superseded", "obsolete", "delete"))
        if not allowed:
            out.append({"path": item, "action": "blocked_not_marked_obsolete"})
            continue
        lines = line_count(path)
        if apply:
            path.unlink()
        out.append({"path": item, "action": "deleted_obsolete_snapshot" if apply else "would_delete_obsolete_snapshot", "lines": lines})
    return out


def write_root_tool_guide(root: Path, apply: bool) -> dict[str, Any]:
    path = root / "TOOL_UTILI_CODING.md"
    text = """# TOOL UTILI CODING

## Scopo

Indice operativo dei tool utili per coding assistito da IA, refactor Markdown, validazione e PR reviewabile.

## Refactor Markdown

| Tool | Uso |
|---|---|
| `Tools/docs/refactor_markdown_splits.py` | Migra split legacy `nomefile/part-xxx.md` in `nomefile.md/part-xxx.md`, divide Markdown monolitici e pruna snapshot obsoleti allowlist-only. |
| `Tools/validation/check_markdown_line_limits.py` | Valida il budget righe Markdown. Usare `--max-lines 400` per policy preferita e `500` come soglia hard. |
| `Tools/validation/check_docs_links.py` | Controlla link Markdown dopo split, rename o pruning. |

Comando tipico:

```powershell
python .\\Tools\\docs\\refactor_markdown_splits.py `
  --repo-root . `
  --apply `
  --migrate-legacy-splits `
  --split-monolithic `
  --prune-obsolete-snapshots `
  --write-root-tool-guide
```

## Coding/PR product lane

| Tool | Uso |
|---|---|
| `Tools/ai/build_task_patch_suggestion_report.py` | Estrae suggestion concrete da task Markdown. |
| `Tools/ai/apply_patch_suggestion_bundle.py` | Applica/dry-run deterministic operations da patch suggestion report. |
| `Tools/validation/check_patch_suggestion_product_separation.py` | Separa prodotto essenziale da telemetry/debug supplementare. |
| `Tools/ai/prepare_review_pr.py` | Prepara branch/commit/PR reviewabile con allowlist/autodiscovery include-path. |

## Validazioni minime

```powershell
python -m py_compile .\\Tools\\docs\\refactor_markdown_splits.py
python .\\Tools\\validation\\check_docs_links.py --repo-root .
python .\\Tools\\validation\\check_markdown_line_limits.py --repo-root . --max-lines 500
python .\Tools\validation\check_file_line_limits.py --repo-root . --output .\output\validation\file_line_limits.json
git diff --check
git status --short
```

## Guardrail

Non committare `output/**`, `renders/**`, DB SQLite, chunk generati o patch bundle locali. Le modifiche distruttive devono restare su branch reviewabile e passare da PR.
"""
    lines = write(path, text, apply)
    return {"path": rel(path, root), "action": "write_root_tool_guide", "lines": lines}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    ap.add_argument("--scope", action="append", default=[])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--migrate-legacy-splits", action="store_true")
    ap.add_argument("--split-monolithic", action="store_true")
    ap.add_argument("--prune-obsolete-snapshots", action="store_true")
    ap.add_argument("--write-root-tool-guide", action="store_true")
    ap.add_argument("--output", default="output/validation/markdown_refactor_report.json")
    ap.add_argument("--markdown-output", default="output/validation/markdown_refactor_report.md")
    args = ap.parse_args()
    root = repo_root(Path(args.repo_root))
    scopes = args.scope or list(DEFAULT_SCOPES)
    results: list[dict[str, Any]] = []
    if args.migrate_legacy_splits:
        for old in find_legacy_split_dirs(root, scopes):
            results.append(migrate_legacy_dir(old, root, args.max_lines, args.apply))
    if args.split_monolithic:
        for scope in scopes:
            base = (root / scope).resolve()
            files = [base] if base.is_file() else [p for p in base.rglob("*.md") if p.is_file()] if base.exists() else []
            for path in sorted(files):
                if not skipped(path, root) and path.suffix == ".md" and path.exists():
                    item = split_monolithic_file(path, root, args.max_lines, args.apply)
                    if item.get("action") != "skip":
                        results.append(item)
    if args.prune_obsolete_snapshots:
        results.extend(prune_obsolete(root, args.apply))
    if args.write_root_tool_guide:
        results.append(write_root_tool_guide(root, args.apply))
    report = {
        "kind": "ia_carmine_markdown_refactor",
        "apply": bool(args.apply),
        "max_lines": args.max_lines,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "results": results,
        "git_status_after": git_status(root) if args.apply else [],
    }
    out = root / args.output
    md = root / args.markdown_output
    out.parent.mkdir(parents=True, exist_ok=True)
    md.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md.write_text(render_md(report), encoding="utf-8")
    print(f"[OK] report={rel(out, root)} results={len(results)} apply={args.apply}")
    for item in results:
        print(f"[{item.get('action')}] {item.get('path')} -> {item.get('target_dir', '')}")
    return 0


def render_md(report: dict[str, Any]) -> str:
    lines = ["# Markdown refactor report", "", f"- Apply: `{report['apply']}`", f"- Max lines: `{report['max_lines']}`", f"- Results: `{len(report['results'])}`", "", "## Results", ""]
    for item in report["results"]:
        lines.append(f"- `{item.get('path')}` action=`{item.get('action')}` target=`{item.get('target_dir', '')}`")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
