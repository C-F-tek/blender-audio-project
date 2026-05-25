"""CLI for NPU review."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import (
    DEFAULT_CHUNK_DIR,
    DEFAULT_CONTEXT,
    DEFAULT_MODEL_DIR,
    DEFAULT_MUSIC_CHUNK_DIR,
    DEFAULT_MUSIC_CONTEXT,
    DEFAULT_MUSIC_NOTES_OUT,
    DEFAULT_MUSIC_OUT,
    DEFAULT_NOTES_OUT,
    DEFAULT_OUT,
)
from .providers import create_ollama_pipeline, create_pipeline
from .runner import run_chunked, run_onepass, write_metadata_report

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", default="")
    parser.add_argument("--context")
    parser.add_argument("--chunk-dir")
    parser.add_argument("--out")
    parser.add_argument("--notes-out")
    parser.add_argument(
        "--metadata-out",
        help="Optional JSON sidecar describing provider execution and advisory role.",
    )
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Write metadata sidecar without loading providers or generating review text.",
    )
    parser.add_argument("--device", default="NPU")
    parser.add_argument("--engine", choices=["npu", "ollama"], default="npu")
    parser.add_argument("--ollama-model", default="")
    parser.add_argument("--ollama-base-url", default="")
    parser.add_argument("--ollama-keep-alive", default="")
    parser.add_argument("--keep-ollama-server", action="store_true")
    parser.add_argument("--keep-ollama-model", action="store_true")
    parser.add_argument("--domain", choices=["code", "music"], default="code")
    parser.add_argument("--mode", choices=["chunked", "onepass"], default="chunked")
    parser.add_argument("--max-context-chars", type=int, default=0)
    parser.add_argument("--chunk-chars", type=int, default=11000)
    parser.add_argument("--chunk-overlap-chars", type=int, default=700)
    parser.add_argument("--max-chunks", type=int, default=0)
    parser.add_argument("--max-prompt-chars", type=int, default=15000)
    parser.add_argument("--max-prompt-len", type=int, default=16384)
    parser.add_argument("--min-response-len", type=int, default=512)
    parser.add_argument("--max-chunk-tokens", type=int, default=650)
    parser.add_argument("--max-reduce-tokens", type=int, default=750)
    parser.add_argument("--max-new-tokens", type=int, default=1100)
    parser.add_argument("--reduce-batch-chars", type=int, default=12000)
    parser.add_argument("--reuse-notes", action="store_true")
    parser.add_argument("--skip-final", action="store_true")

    args = parser.parse_args()
    if args.engine == "ollama":
        missing = []
        if not str(args.ollama_model or "").strip():
            missing.append("--ollama-model")
        if not str(args.ollama_base_url or "").strip():
            missing.append("--ollama-base-url")
        if not str(args.ollama_keep_alive or "").strip():
            missing.append("--ollama-keep-alive")
        if missing:
            parser.error("missing explicit Ollama review runner parameter(s): " + ", ".join(missing))
    if args.engine == "npu" and not str(args.model_dir or "").strip():
        parser.error("missing explicit NPU review runner parameter: --model-dir")

    if args.domain == "music":
        args.context = args.context or str(DEFAULT_MUSIC_CONTEXT)
        args.chunk_dir = args.chunk_dir or str(DEFAULT_MUSIC_CHUNK_DIR)
        args.out = args.out or str(DEFAULT_MUSIC_OUT)
        args.notes_out = args.notes_out or str(DEFAULT_MUSIC_NOTES_OUT)
    else:
        args.context = args.context or str(DEFAULT_CONTEXT)
        args.chunk_dir = args.chunk_dir or str(DEFAULT_CHUNK_DIR)
        args.out = args.out or str(DEFAULT_OUT)
        args.notes_out = args.notes_out or str(DEFAULT_NOTES_OUT)

    model_dir = Path(args.model_dir)
    context_path = Path(args.context)
    out_path = Path(args.out)
    notes_out = Path(args.notes_out)

    if args.metadata_only:
        if not args.metadata_out:
            parser.error("--metadata-only requires --metadata-out")
        write_metadata_report(
            args,
            out_path,
            notes_out,
            provider_execution_performed=False,
            generated_output_written=False,
            provider_empty_response=False,
        )
        print("[OK] Metadata-only mode: provider not loaded and no review text generated")
        return

    if args.engine == "npu" and not model_dir.exists():
        raise FileNotFoundError(f"Model dir not found: {model_dir}")

    if not context_path.exists():
        raise FileNotFoundError(f"Context file not found: {context_path}")

    print(f"[AI] Engine: {args.engine}")
    print(f"[AI] Mode: {args.mode}")
    print(f"[AI] Domain: {args.domain}")

    if args.engine == "ollama":
        print(f"[Ollama] Model preference: {args.ollama_model}")
        pipe = create_ollama_pipeline(args)
    else:
        print(f"[NPU] Loading model: {model_dir}")
        print(f"[NPU] Device: {args.device}")
        pipe = create_pipeline(
            model_dir=model_dir,
            device=args.device,
            max_prompt_len=args.max_prompt_len,
            min_response_len=args.min_response_len,
        )

    try:
        if args.mode == "onepass":
            text = run_onepass(pipe, context_path, args)
        else:
            text = run_chunked(pipe, context_path, Path(args.chunk_dir), notes_out, args)
    finally:
        if hasattr(pipe, "close"):
            pipe.close()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text.strip() + "\n", encoding="utf-8")
    write_metadata_report(
        args,
        out_path,
        notes_out,
        provider_execution_performed=True,
        generated_output_written=True,
    )

    print(f"[OK] Wrote: {out_path}")


if __name__ == "__main__":
    main()
