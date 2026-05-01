from __future__ import annotations

from pathlib import Path
import argparse
import json
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]

DEFAULT_MODEL_DIR = Path.home() / "blender" / "npu-models" / "Phi-3.5-mini-instruct-int4-cw-ov"
DEFAULT_CONTEXT = ROOT / "Tools" / "npu" / "npu_code_context.md"
DEFAULT_CHUNK_DIR = ROOT / "Tools" / "npu" / "npu_code_chunks"
DEFAULT_OUT = ROOT / "Tools" / "npu" / "npu_context_for_aider.md"
DEFAULT_NOTES_OUT = ROOT / "Tools" / "npu" / "npu_chunk_notes.md"
DEFAULT_MUSIC_CONTEXT = ROOT / "Tools" / "npu" / "npu_music_context.md"
DEFAULT_MUSIC_CHUNK_DIR = ROOT / "Tools" / "npu" / "npu_music_chunks"
DEFAULT_MUSIC_OUT = ROOT / "Tools" / "npu" / "npu_music_context_for_aider.md"
DEFAULT_MUSIC_NOTES_OUT = ROOT / "Tools" / "npu" / "npu_music_chunk_notes.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_text_limited(path: Path, max_chars: int) -> str:
    text = read_text(path)

    if max_chars <= 0 or len(text) <= max_chars:
        return text

    return text[:max_chars] + "\n\n[TRUNCATED BY run_npu_review.py]\n"


def split_text(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + max_chars, text_len)
        chunks.append(text[start:end])
        if end == text_len:
            break
        start = max(end - max(0, overlap_chars), start + 1)

    return chunks


def load_context_chunks(
    context_path: Path,
    chunk_dir: Path,
    chunk_chars: int,
    overlap_chars: int,
    max_chunks: int,
) -> list[tuple[str, str]]:
    chunk_files = []
    if chunk_dir.exists():
        chunk_files = sorted(chunk_dir.glob("chunk_*.md"))

    if chunk_files:
        chunks = [(path.name, read_text(path)) for path in chunk_files]
    else:
        text = read_text(context_path)
        chunks = [
            (f"context_slice_{index:03d}.md", chunk)
            for index, chunk in enumerate(split_text(text, chunk_chars, overlap_chars), 1)
        ]

    if max_chunks > 0:
        chunks = chunks[:max_chunks]

    return chunks


def fit_prompt(prefix: str, context: str, suffix: str, max_prompt_chars: int) -> str:
    if max_prompt_chars <= 0:
        return prefix + context + suffix

    budget = max_prompt_chars - len(prefix) - len(suffix)
    if budget < 1000:
        budget = 1000

    if len(context) > budget:
        context = context[:budget] + "\n\n[CHUNK TRIMMED TO FIT NPU PROMPT WINDOW]\n"

    return prefix + context + suffix


def build_onepass_prompt(context: str, max_prompt_chars: int, domain: str = "code") -> str:
    if domain == "music":
        prefix = """
Sei un agente NPU musicale per un progetto Blender audio-reactive.

Devi analizzare il contesto fornito, composto da analysis WAV, segmenti musicali e scene JSON generate.
Non devi riscrivere codice.
Non devi inventare parti del brano.
Devi produrre una memoria operativa per Aider/Ollama e per le prossime decisioni creative.

Output richiesto in Markdown:

## Track Map
Durata, BPM, segmenti, zone piu intense e zone calme.

## Audio Control Map
Come usare low, mid, high, onset e beat per deformazione mesh, materiali, luci, fog, camera e fisica.

## Scene JSON Map
Scene spec disponibili, palette, oggetti, audio mapping, nodi o materiali suggeriti.

## Suggested Aider File Sets
File e JSON da aggiungere quando si lavora su audio analysis, scene spec, materiali o animazione.

## Warnings
Rischi tecnici, dati troppo lunghi e cose da non applicare direttamente alla scena senza scelta esplicita.

CONTESTO MUSICALE:

""".lstrip()
        suffix = "\n"
        return fit_prompt(prefix, context, suffix, max_prompt_chars)

    prefix = """
Sei un revisore tecnico locale per un progetto Blender Python audio-reactive.

Devi analizzare il contesto fornito e produrre un report operativo per Aider/Ollama.
Non devi riscrivere codice.
Non devi proporre modifiche massive.
Devi indicare quali file aggiungere ad Aider per specifici interventi.

Output richiesto in Markdown:

## Project Map
Sintesi dei moduli principali.

## Musical Agent Context
Come il progetto gestisce audio, beat, envelope, materiali, fisica, fog, camera.

## Suggested Aider File Sets
Comandi /add consigliati per:
- camera
- fog
- lights
- materials
- physics
- render
- sequencer
- hotpatch
- NPU/tools

## Warnings
Rischi tecnici e cose da non toccare senza richiesta.

CONTESTO PROGETTO:

""".lstrip()
    suffix = "\n"
    return fit_prompt(prefix, context, suffix, max_prompt_chars)


def build_chunk_prompt(
    title: str,
    index: int,
    total: int,
    context: str,
    max_prompt_chars: int,
    domain: str = "code",
) -> str:
    if domain == "music":
        prefix = f"""
Sei un agente NPU musicale per un progetto Blender audio-reactive.

Leggi questo chunk musicale {index}/{total}: {title}

Obiettivo: estrai memoria operativa da analysis WAV, segmenti audio o scene JSON.
Non inventare. Non riscrivere codice. Non trasformare il chunk in istruzioni definitive di scena.

Output Markdown compatto:

## Chunk Role
Che cosa descrive: overview, segmento audio, scene spec, raw prompt o mapping.

## Musical Cues
Zone intense/calde, low/mid/high/onset/beat importanti, transizioni.

## Visual Control Ideas
Deformazione hero, emissione materiali, fog, luci, camera, fisica, sequencer.

## Scene JSON Links
Oggetti, palette, materiali, audio mappings e limiti del JSON.

## Keep / Avoid
Cose da conservare e rischi da evitare nei prossimi hotpatch.

CHUNK:

""".lstrip()
        suffix = "\n"
        return fit_prompt(prefix, context, suffix, max_prompt_chars)

    prefix = f"""
Sei un agente NPU musicale/tecnico per un progetto Blender Python audio-reactive.

Leggi questo chunk {index}/{total}: {title}

Obiettivo: estrai solo informazioni operative da riusare nella sintesi finale.
Non inventare. Non riscrivere codice. Non fare una review generica.

Output Markdown massimo e compatto:

## Chunk Role
Ruolo del file o dei file nel progetto.

## Important Symbols
Funzioni, classi, costanti o pannelli da ricordare.

## Audio/Visual Controls
Parametri che influenzano musica, beat, luci, materiali, fog, fisica, render o sequencer.

## Dependencies
Relazioni con altri moduli.

## Risks
Rischi di modifica e punti dove serve contesto aggiuntivo.

CHUNK:

""".lstrip()
    suffix = "\n"
    return fit_prompt(prefix, context, suffix, max_prompt_chars)


def build_batch_reduce_prompt(batch_title: str, notes: str, max_prompt_chars: int, domain: str = "code") -> str:
    if domain == "music":
        prefix = f"""
Sei un agente NPU musicale. Devi comprimere note parziali da analysis WAV e scene JSON.

Batch: {batch_title}

Mantieni solo:
- mappa musicale del brano
- segmenti e cue audio rilevanti
- relazioni con scene JSON, palette, oggetti e audio mapping
- controlli visuali consigliati
- rischi tecnici o creativi

NOTE:

""".lstrip()
        suffix = "\n\nProduci una sintesi Markdown compatta per il reduce finale musicale.\n"
        return fit_prompt(prefix, notes, suffix, max_prompt_chars)

    prefix = f"""
Sei un agente NPU musicale/tecnico. Devi comprimere note parziali del progetto Blender.

Batch: {batch_title}

Mantieni solo informazioni operative:
- mappa moduli
- controlli audio-reactive
- file da aggiungere ad Aider
- rischi tecnici
- dipendenze tra moduli

NOTE:

""".lstrip()
    suffix = "\n\nProduci una sintesi Markdown compatta per il reduce finale.\n"
    return fit_prompt(prefix, notes, suffix, max_prompt_chars)


def build_final_prompt(notes: str, max_prompt_chars: int, domain: str = "code") -> str:
    if domain == "music":
        prefix = """
Sei il coordinatore dell'agente NPU musicale per un progetto Blender audio-reactive.

Combina le note dei chunk in una memoria operativa unica.
Non inventare dettagli non presenti nelle note.
Priorita: rendere utili analysis WAV e scene JSON senza passare tutto il JSON lungo nel prompt.

Output richiesto in Markdown:

## Track Map
Struttura del brano, durata, BPM, segmenti forti/calmati.

## Long Music Context Strategy
Come usare overview, segmenti e scene chunk quando il contesto cresce.

## Audio-To-Visual Map
Low, mid, high, onset, beat verso hero mesh, materiali, emissioni, fog, camera, fisica.

## Scene JSON Map
Scene spec, palette, oggetti e mapping da tenere presenti.

## Suggested Aider File Sets
Blocchi /add consigliati per analisi WAV, scene JSON, animazione e materiali.

## Safe Workflow
Ordine consigliato per generare dati, leggere chunk, decidere hotpatch e verificare.

## Warnings
Rischi tecnici, dati da non usare alla cieca, limiti dei JSON generati.

NOTE DEI CHUNK:

""".lstrip()
        suffix = "\n"
        return fit_prompt(prefix, notes, suffix, max_prompt_chars)

    prefix = """
Sei il coordinatore dell'agente NPU musicale/tecnico per un progetto Blender Python audio-reactive.

Combina le note dei chunk in un report operativo unico.
Non inventare dettagli non presenti nelle note.
Priorita: aiutare Aider/Ollama e l'utente a sapere quali file caricare e dove intervenire.

Output richiesto in Markdown:

## Project Map
Mappa dei moduli e responsabilita.

## Long Context Strategy
Come usare indice, chunk e note per continuare il lavoro senza perdere contesto.

## Musical/Visual Control Map
Audio, beat, envelope, materiali, luci, fog, fisica, render, sequencer, hotpatch.

## Suggested Aider File Sets
Blocchi /add consigliati per interventi mirati.

## Safe Workflow
Ordine consigliato per modifiche e verifiche.

## Warnings
Rischi tecnici, file delicati, dipendenze da non rompere.

NOTE DEI CHUNK:

""".lstrip()
    suffix = "\n"
    return fit_prompt(prefix, notes, suffix, max_prompt_chars)


def create_pipeline(model_dir: Path, device: str, max_prompt_len: int, min_response_len: int):
    import openvino_genai as ov_genai

    pipeline_config = {
        "MAX_PROMPT_LEN": max_prompt_len,
        "MIN_RESPONSE_LEN": min_response_len,
        "CACHE_DIR": str(ROOT / "Tools" / "npu" / ".npucache"),
    }

    return ov_genai.LLMPipeline(str(model_dir), device, **pipeline_config)


def create_ollama_pipeline(args: argparse.Namespace):
    from ollama_runtime import OllamaSession

    session_kwargs = {
        "model": args.ollama_model,
        "keep_alive": args.ollama_keep_alive,
        "shutdown_server": not args.keep_ollama_server,
        "unload_model": not args.keep_ollama_model,
    }
    if args.ollama_base_url:
        session_kwargs["base_url"] = args.ollama_base_url

    return OllamaSession(**session_kwargs).start()


def generate_text(pipe, prompt: str, max_new_tokens: int) -> str:
    result = pipe.generate(prompt, max_new_tokens=max_new_tokens)
    return str(result).strip()


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


def run_chunked(pipe, context_path: Path, chunk_dir: Path, notes_out: Path, args: argparse.Namespace) -> str:
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
        prompt = build_chunk_prompt(title, index, total, context, args.max_prompt_chars, args.domain)
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
        "source_writes_performed": False,
        "patch_application_performed": False,
        "advisory_role": "probe_or_knowledge_broker" if args.engine == "npu" else "primary_advisory_when_quality_approved",
        "quality_gate_required_before_advisory_use": True,
    }
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[OK] Wrote metadata: {metadata_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", default=str(DEFAULT_MODEL_DIR))
    parser.add_argument("--context")
    parser.add_argument("--chunk-dir")
    parser.add_argument("--out")
    parser.add_argument("--notes-out")
    parser.add_argument("--metadata-out", help="Optional JSON sidecar describing provider execution and advisory role.")
    parser.add_argument("--metadata-only", action="store_true", help="Write metadata sidecar without loading providers or generating review text.")
    parser.add_argument("--device", default="NPU")
    parser.add_argument("--engine", choices=["npu", "ollama"], default="npu")
    parser.add_argument("--ollama-model", default="qwen2.5-coder:14b")
    parser.add_argument("--ollama-base-url", default=None)
    parser.add_argument("--ollama-keep-alive", default="5m")
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
