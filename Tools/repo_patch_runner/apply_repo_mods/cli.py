from __future__ import annotations

import argparse
import sys
from pathlib import Path

from Tools.repo_patch_runner._shared.apply_repo_mods import (
    PatchError,
    _resolve_repo_root,
    _run_git_diff,
    apply_spec,
    load_spec,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe repository patch runner")
    parser.add_argument("--spec", required=True, help="Percorso del file JSON con le modifiche")
    parser.add_argument("--repo-root", default=None, help="Root del repository; default: directory corrente")
    parser.add_argument("--write", action="store_true", help="Scrive davvero le modifiche")
    parser.add_argument("--dry-run", action="store_true", help="Simula senza scrivere")
    parser.add_argument("--no-backup", action="store_true", help="Non crea backup prima della scrittura")
    parser.add_argument("--show-diff", action="store_true", help="Mostra git diff dopo l'applicazione")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if args.write and args.dry_run:
        print("[ERRORE] Usa --write oppure --dry-run, non entrambi", file=sys.stderr)
        return 2

    try:
        root = _resolve_repo_root(args.repo_root)
        spec_path = Path(args.spec).expanduser()
        if not spec_path.is_absolute():
            spec_path = (root / spec_path).resolve()
        if not spec_path.exists():
            raise PatchError(f"Spec non trovato: {spec_path}")

        spec = load_spec(spec_path)
        write = bool(args.write)
        print(f"[INFO] Mode: {'WRITE' if write else 'DRY-RUN'}")
        print(f"[INFO] Repo: {root}")
        print(f"[INFO] Spec: {spec_path}")
        if spec.get("description"):
            print(f"[INFO] Description: {spec['description']}")

        reports = apply_spec(root, spec, write=write, no_backup=bool(args.no_backup))
        print("\n[SUMMARY]")
        changed_paths: list[Path] = []
        for report in reports:
            rel = report.path.relative_to(root)
            if report.changed:
                changed_paths.append(report.path)
            status = "changed" if report.changed else "unchanged"
            print(
                f"- {rel}: {status}, replacements={report.replacements_applied}, "
                f"lines={report.before_lines}->{report.after_lines}, "
                f"bom_removed={report.bom_removed}"
            )

        if args.show_diff and write:
            print("\n[GIT DIFF]")
            _run_git_diff(root, changed_paths)
        print("\n[OK] Modifiche applicate." if write else "\n[OK] Dry-run completato. Riesegui con --write per scrivere.")
        return 0
    except PatchError as exc:
        print(f"[ERRORE] {exc}", file=sys.stderr)
        return 1
