# Project Code Chunk 186/212

- File: `Tools/npu/run_npu_review.py`
- Part: `2`
- Lines: `327-565`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `from datetime import datetime`
- Functions: `read_text(path)` line 21; `read_text_limited(path, max_chars)` line 25; `split_text(text, max_chars, overlap_chars)` line 34; `load_context_chunks(context_path, chunk_dir, chunk_chars, overlap_chars, max_chunks)` line 52; `fit_prompt(prefix, context, suffix, max_prompt_chars)` line 78; `build_onepass_prompt(context, max_prompt_chars, domain)` line 92; `build_chunk_prompt(title, index, total, context, max_prompt_chars, domain)` line 163; `build_batch_reduce_prompt(batch_title, notes, max_prompt_chars, domain)` line 235; `build_final_prompt(notes, max_prompt_chars, domain)` line 274; `create_pipeline(model_dir, device, max_prompt_len, min_response_len)` line 346; `create_ollama_pipeline(args)` line 358; `generate_text(pipe, prompt, max_new_tokens)` line 373; `write_notes(notes_out, notes)` line 378; `pack_batches(items, max_chars)` line 393; `reduce_notes(pipe, notes, args)` line 413; `run_onepass(pipe, context_path, args)` line 435; `run_chunked(pipe, context_path, chunk_dir, notes_out, args)` line 441; `main()` line 477
- Assignments: `ROOT`, `DEFAULT_MODEL_DIR`, `DEFAULT_CONTEXT`, `DEFAULT_CHUNK_DIR`, `DEFAULT_OUT`, `DEFAULT_NOTES_OUT`, `DEFAULT_MUSIC_CONTEXT`, `DEFAULT_MUSIC_CHUNK_DIR`, `DEFAULT_MUSIC_OUT`, `DEFAULT_MUSIC_NOTES_OUT`

## Content
```py
00327: ## Musical/Visual Control Map
00328: Audio, beat, envelope, materiali, luci, fog, fisica, render, sequencer, hotpatch.
00329: 
00330: ## Suggested Aider File Sets
00331: Blocchi /add consigliati per interventi mirati.
00332: 
00333: ## Safe Workflow
00334: Ordine consigliato per modifiche e verifiche.
00335: 
00336: ## Warnings
00337: Rischi tecnici, file delicati, dipendenze da non rompere.
00338: 
00339: NOTE DEI CHUNK:
00340: 
00341: """.lstrip()
00342:     suffix = "\n"
00343:     return fit_prompt(prefix, notes, suffix, max_prompt_chars)
00344: 
00345: 
00346: def create_pipeline(model_dir: Path, device: str, max_prompt_len: int, min_response_len: int):
00347:     import openvino_genai as ov_genai
00348: 
00349:     pipeline_config = {
00350:         "MAX_PROMPT_LEN": max_prompt_len,
00351:         "MIN_RESPONSE_LEN": min_response_len,
00352:         "CACHE_DIR": str(ROOT / "Tools" / "npu" / ".npucache"),
00353:     }
00354: 
00355:     return ov_genai.LLMPipeline(str(model_dir), device, **pipeline_config)
00356: 
00357: 
00358: def create_ollama_pipeline(args: argparse.Namespace):
00359:     from ollama_runtime import OllamaSession
00360: 
00361:     session_kwargs = {
00362:         "model": args.ollama_model,
00363:         "keep_alive": args.ollama_keep_alive,
00364:         "shutdown_server": not args.keep_ollama_server,
00365:         "unload_model": not args.keep_ollama_model,
00366:     }
00367:     if args.ollama_base_url:
00368:         session_kwargs["base_url"] = args.ollama_base_url
00369: 
00370:     return OllamaSession(**session_kwargs).start()
00371: 
00372: 
00373: def generate_text(pipe, prompt: str, max_new_tokens: int) -> str:
00374:     result = pipe.generate(prompt, max_new_tokens=max_new_tokens)
00375:     return str(result).strip()
00376: 
00377: 
00378: def write_notes(notes_out: Path, notes: list[tuple[str, str]]) -> None:
00379:     lines = [
00380:         "# NPU Chunk Notes\n\n",
00381:         f"Generated: `{datetime.now().isoformat(timespec='seconds')}`\n\n",
00382:     ]
00383: 
00384:     for index, (title, text) in enumerate(notes, 1):
00385:         lines.append(f"\n---\n\n## Note {index}: `{title}`\n\n")
00386:         lines.append(text.strip())
00387:         lines.append("\n")
00388: 
00389:     notes_out.parent.mkdir(parents=True, exist_ok=True)
00390:     notes_out.write_text("".join(lines), encoding="utf-8")
00391: 
00392: 
00393: def pack_batches(items: list[str], max_chars: int) -> list[str]:
00394:     batches: list[str] = []
00395:     current: list[str] = []
00396:     current_len = 0
00397: 
00398:     for item in items:
00399:         item_len = len(item) + 2
00400:         if current and current_len + item_len > max_chars:
00401:             batches.append("\n\n".join(current))
00402:             current = []
00403:             current_len = 0
00404:         current.append(item)
00405:         current_len += item_len
00406: 
00407:     if current:
00408:         batches.append("\n\n".join(current))
00409: 
00410:     return batches
00411: 
00412: 
00413: def reduce_notes(pipe, notes: list[tuple[str, str]], args: argparse.Namespace) -> str:
00414:     current = [f"## {title}\n\n{text}" for title, text in notes]
00415:     round_index = 1
00416: 
00417:     while len("\n\n".join(current)) > args.reduce_batch_chars and len(current) > 1:
00418:         batches = pack_batches(current, args.reduce_batch_chars)
00419:         reduced: list[str] = []
00420: 
00421:         for batch_index, batch in enumerate(batches, 1):
00422:             title = f"round {round_index}, batch {batch_index}/{len(batches)}"
00423:             print(f"[NPU] Reducing {title}...")
00424:             prompt = build_batch_reduce_prompt(title, batch, args.max_prompt_chars, args.domain)
00425:             reduced.append(generate_text(pipe, prompt, args.max_reduce_tokens))
00426: 
00427:         current = reduced
00428:         round_index += 1
00429: 
00430:     final_notes = "\n\n".join(current)
00431:     final_prompt = build_final_prompt(final_notes, args.max_prompt_chars, args.domain)
00432:     return generate_text(pipe, final_prompt, args.max_new_tokens)
00433: 
00434: 
00435: def run_onepass(pipe, context_path: Path, args: argparse.Namespace) -> str:
00436:     context = read_text_limited(context_path, args.max_context_chars)
00437:     prompt = build_onepass_prompt(context, args.max_prompt_chars, args.domain)
00438:     return generate_text(pipe, prompt, args.max_new_tokens)
00439: 
00440: 
00441: def run_chunked(pipe, context_path: Path, chunk_dir: Path, notes_out: Path, args: argparse.Namespace) -> str:
00442:     if args.reuse_notes and notes_out.exists():
00443:         print(f"[NPU] Reusing existing notes: {notes_out}")
00444:         notes = [(notes_out.name, read_text(notes_out))]
00445:         return reduce_notes(pipe, notes, args)
00446: 
00447:     chunks = load_context_chunks(
00448:         context_path=context_path,
00449:         chunk_dir=chunk_dir,
00450:         chunk_chars=args.chunk_chars,
00451:         overlap_chars=args.chunk_overlap_chars,
00452:         max_chunks=args.max_chunks,
00453:     )
00454: 
00455:     if not chunks:
00456:         raise RuntimeError("No context chunks found.")
00457: 
00458:     notes: list[tuple[str, str]] = []
00459:     total = len(chunks)
00460: 
00461:     for index, (title, context) in enumerate(chunks, 1):
00462:         print(f"[NPU] Reading chunk {index}/{total}: {title}")
00463:         prompt = build_chunk_prompt(title, index, total, context, args.max_prompt_chars, args.domain)
00464:         note = generate_text(pipe, prompt, args.max_chunk_tokens)
00465:         notes.append((title, note))
00466:         write_notes(notes_out, notes)
00467: 
00468:     print(f"[OK] Wrote chunk notes: {notes_out}")
00469: 
00470:     if args.skip_final:
00471:         return "# NPU chunk notes generated\n\nFinal reduce skipped by --skip-final.\n"
00472: 
00473:     print("[NPU] Building final long-context report...")
00474:     return reduce_notes(pipe, notes, args)
00475: 
00476: 
00477: def main() -> None:
00478:     parser = argparse.ArgumentParser()
00479:     parser.add_argument("--model-dir", default=str(DEFAULT_MODEL_DIR))
00480:     parser.add_argument("--context")
00481:     parser.add_argument("--chunk-dir")
00482:     parser.add_argument("--out")
00483:     parser.add_argument("--notes-out")
00484:     parser.add_argument("--device", default="NPU")
00485:     parser.add_argument("--engine", choices=["npu", "ollama"], default="npu")
00486:     parser.add_argument("--ollama-model", default="qwen2.5-coder:14b")
00487:     parser.add_argument("--ollama-base-url", default=None)
00488:     parser.add_argument("--ollama-keep-alive", default="5m")
00489:     parser.add_argument("--keep-ollama-server", action="store_true")
00490:     parser.add_argument("--keep-ollama-model", action="store_true")
00491:     parser.add_argument("--domain", choices=["code", "music"], default="code")
00492:     parser.add_argument("--mode", choices=["chunked", "onepass"], default="chunked")
00493:     parser.add_argument("--max-context-chars", type=int, default=0)
00494:     parser.add_argument("--chunk-chars", type=int, default=11000)
00495:     parser.add_argument("--chunk-overlap-chars", type=int, default=700)
00496:     parser.add_argument("--max-chunks", type=int, default=0)
00497:     parser.add_argument("--max-prompt-chars", type=int, default=15000)
00498:     parser.add_argument("--max-prompt-len", type=int, default=16384)
00499:     parser.add_argument("--min-response-len", type=int, default=512)
00500:     parser.add_argument("--max-chunk-tokens", type=int, default=650)
00501:     parser.add_argument("--max-reduce-tokens", type=int, default=750)
00502:     parser.add_argument("--max-new-tokens", type=int, default=1100)
00503:     parser.add_argument("--reduce-batch-chars", type=int, default=12000)
00504:     parser.add_argument("--reuse-notes", action="store_true")
00505:     parser.add_argument("--skip-final", action="store_true")
00506: 
00507:     args = parser.parse_args()
00508: 
00509:     if args.domain == "music":
00510:         args.context = args.context or str(DEFAULT_MUSIC_CONTEXT)
00511:         args.chunk_dir = args.chunk_dir or str(DEFAULT_MUSIC_CHUNK_DIR)
00512:         args.out = args.out or str(DEFAULT_MUSIC_OUT)
00513:         args.notes_out = args.notes_out or str(DEFAULT_MUSIC_NOTES_OUT)
00514:     else:
00515:         args.context = args.context or str(DEFAULT_CONTEXT)
00516:         args.chunk_dir = args.chunk_dir or str(DEFAULT_CHUNK_DIR)
00517:         args.out = args.out or str(DEFAULT_OUT)
00518:         args.notes_out = args.notes_out or str(DEFAULT_NOTES_OUT)
00519: 
00520:     model_dir = Path(args.model_dir)
00521:     context_path = Path(args.context)
00522:     chunk_dir = Path(args.chunk_dir)
00523:     out_path = Path(args.out)
00524:     notes_out = Path(args.notes_out)
00525: 
00526:     if args.engine == "npu" and not model_dir.exists():
00527:         raise FileNotFoundError(f"Model dir not found: {model_dir}")
00528: 
00529:     if not context_path.exists():
00530:         raise FileNotFoundError(f"Context file not found: {context_path}")
00531: 
00532:     print(f"[AI] Engine: {args.engine}")
00533:     print(f"[AI] Mode: {args.mode}")
00534:     print(f"[AI] Domain: {args.domain}")
00535: 
00536:     if args.engine == "ollama":
00537:         print(f"[Ollama] Model preference: {args.ollama_model}")
00538:         pipe = create_ollama_pipeline(args)
00539:     else:
00540:         print(f"[NPU] Loading model: {model_dir}")
00541:         print(f"[NPU] Device: {args.device}")
00542:         pipe = create_pipeline(
00543:             model_dir=model_dir,
00544:             device=args.device,
00545:             max_prompt_len=args.max_prompt_len,
00546:             min_response_len=args.min_response_len,
00547:         )
00548: 
00549:     try:
00550:         if args.mode == "onepass":
00551:             text = run_onepass(pipe, context_path, args)
00552:         else:
00553:             text = run_chunked(pipe, context_path, chunk_dir, notes_out, args)
00554:     finally:
00555:         if hasattr(pipe, "close"):
00556:             pipe.close()
00557: 
00558:     out_path.parent.mkdir(parents=True, exist_ok=True)
00559:     out_path.write_text(text.strip() + "\n", encoding="utf-8")
00560: 
00561:     print(f"[OK] Wrote: {out_path}")
00562: 
00563: 
00564: if __name__ == "__main__":
00565:     main()
```
