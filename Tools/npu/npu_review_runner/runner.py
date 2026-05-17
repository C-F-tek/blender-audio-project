"""Execution and report helpers for NPU review."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from .config import ROOT
from .prompts import build_batch_reduce_prompt, build_chunk_prompt, build_final_prompt, build_onepass_prompt
from .providers import generate_text
from .text_utils import load_context_chunks, read_text, read_text_limited

def write_notes(notes_out: Path, notes: list[tuple[str, str]]) -> None:
    lines = [
        "# NPU Chunk Notes\n\n",
        f"Generated: `{datetime.now().isoformat(timespec='seconds')}`\n\n",
    ]

    for index, (title, text) in enumerate(notes, 1):
        lines.append(f"\n---\n\n## Note {index}: `{title}`\n\n")
        lines.append(text.strip())
        lines.append("\n")

    notes_out.parent.mkdir(parents=True, exist_ok=True)
    notes_out.write_text("".join(lines), encoding="utf-8")


def pack_batches(items: list[str], max_chars: int) -> list[str]:
    batches: list[str] = []
    current: list[str] = []
    current_len = 0

    for item in items:
        item_len = len(item) + 2
        if current and current_len + item_len > max_chars:
            batches.append("\n\n".join(current))
            current = []
            current_len = 0
        current.append(item)
        current_len += item_len

    if current:
        batches.append("\n\n".join(current))

    return batches


def reduce_notes(pipe, notes: list[tuple[str, str]], args: argparse.Namespace) -> str:
    current = [f"## {title}\n\n{text}" for title, text in notes]
    round_index = 1

    while len("\n\n".join(current)) > args.reduce_batch_chars and len(current) > 1:
        batches = pack_batches(current, args.reduce_batch_chars)
        reduced: list[str] = []

        for batch_index, batch in enumerate(batches, 1):
            title = f"round {round_index}, batch {batch_index}/{len(batches)}"
            print(f"[NPU] Reducing {title}...")
            prompt = build_batch_reduce_prompt(title, batch, args.max_prompt_chars, args.domain)
            reduced.append(generate_text(pipe, prompt, args.max_reduce_tokens))

        current = reduced
        round_index += 1

    final_notes = "\n\n".join(current)
    final_prompt = build_final_prompt(final_notes, args.max_prompt_chars, args.domain)
    return generate_text(pipe, final_prompt, args.max_new_tokens)


def run_onepass(pipe, context_path: Path, args: argparse.Namespace) -> str:
    context = read_text_limited(context_path, args.max_context_chars)
    prompt = build_onepass_prompt(context, args.max_prompt_chars, args.domain)
    return generate_text(pipe, prompt, args.max_new_tokens)


def run_chunked(
    pipe, context_path: Path, chunk_dir: Path, notes_out: Path, args: argparse.Namespace
) -> str:
    if args.reuse_notes and notes_out.exists():
        print(f"[NPU] Reusing existing notes: {notes_out}")
        notes = [(notes_out.name, read_text(notes_out))]
        return reduce_notes(pipe, notes, args)

    chunks = load_context_chunks(
        context_path=context_path,
        chunk_dir=chunk_dir,
        chunk_chars=args.chunk_chars,
        overlap_chars=args.chunk_overlap_chars,
        max_chunks=args.max_chunks,
    )

    if not chunks:
        raise RuntimeError("No context chunks found.")

    notes: list[tuple[str, str]] = []
    total = len(chunks)

    for index, (title, context) in enumerate(chunks, 1):
        print(f"[NPU] Reading chunk {index}/{total}: {title}")
        prompt = build_chunk_prompt(
            title, index, total, context, args.max_prompt_chars, args.domain
        )
        note = generate_text(pipe, prompt, args.max_chunk_tokens)
        notes.append((title, note))
        write_notes(notes_out, notes)

    print(f"[OK] Wrote chunk notes: {notes_out}")

    if args.skip_final:
        return "# NPU chunk notes generated\n\nFinal reduce skipped by --skip-final.\n"

    print("[NPU] Building final long-context report...")
    return reduce_notes(pipe, notes, args)


def write_metadata_report(
    args: argparse.Namespace,
    out_path: Path,
    notes_out: Path,
    *,
    provider_execution_performed: bool,
    generated_output_written: bool,
    provider_empty_response: bool = False,
) -> None:
    if not args.metadata_out:
        return
    metadata_path = Path(args.metadata_out)
    metadata = {
        "schema_version": 1,
        "kind": "npu_review_metadata",
        "repo_root": str(ROOT),
        "passed": True,
        "errors": [],
        "warnings": [],
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "engine": args.engine,
        "provider": "ollama" if args.engine == "ollama" else "openvino_npu",
        "device": args.device if args.engine == "npu" else None,
        "domain": args.domain,
        "mode": args.mode,
        "metadata_only": bool(args.metadata_only),
        "context": str(Path(args.context)),
        "chunk_dir": str(Path(args.chunk_dir)),
        "output": str(out_path),
        "notes_output": str(notes_out),
        "provider_execution_performed": bool(provider_execution_performed),
        "generated_output_written": bool(generated_output_written),
        "provider_empty_response": bool(provider_empty_response),
        "source_writes_performed": False,
        "patch_application_performed": False,
        "advisory_role": "probe_or_knowledge_broker"
        if args.engine == "npu"
        else "primary_advisory_when_quality_approved",
        "quality_gate_required_before_advisory_use": True,
    }
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"[OK] Wrote metadata: {metadata_path}")
