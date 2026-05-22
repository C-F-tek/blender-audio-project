"""CLI entrypoint for external heap revision context generation."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from ia_carmine._shared.report_io import print_json_report
from .common import read_json, write_json, write_text
from .output import attach_to_composer_documents, render_markdown
from .report import build_report

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pointer-manifest", required=True)
    parser.add_argument("--composer-json", default="")
    parser.add_argument("--causality-json", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--documents-dir", default="")
    parser.add_argument("--no-documents-copy", action="store_true")
    args = parser.parse_args()

    pointer_path = Path(args.pointer_manifest).resolve()
    pointer = read_json(str(pointer_path))
    if not pointer:
        raise SystemExit(f"pointer manifest unreadable: {pointer_path}")
    composer = read_json(args.composer_json)
    causality = read_json(args.causality_json)
    output = (
        Path(args.output).resolve()
        if args.output
        else pointer_path.with_name("external_heap_revision_context.json")
    )
    markdown = (
        Path(args.markdown_output).resolve() if args.markdown_output else output.with_suffix(".md")
    )
    report = build_report(pointer, composer, causality)
    report["documents_copy_performed"] = False
    report["documents_outputs"] = {}
    write_json(output, report)
    write_text(markdown, render_markdown(report))
    if not args.no_documents_copy:
        documents_outputs = attach_to_composer_documents(
            composer, output, markdown, args.documents_dir
        )
        if documents_outputs:
            report["documents_copy_performed"] = True
            report["documents_outputs"] = documents_outputs
            write_json(output, report)
            documents_json = documents_outputs.get("documents_json")
            if documents_json:
                shutil.copyfile(output, Path(documents_json).expanduser().resolve())
        else:
            report["warnings"].append(
                "composer documents_dir not found; revision context kept in run dir only"
            )
            write_json(output, report)
    print_json_report(report)
    return 0
