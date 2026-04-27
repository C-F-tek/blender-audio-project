# Project Code Chunk 185/212

- File: `Tools/npu/run_npu_review.py`
- Part: `1`
- Lines: `1-326`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `from datetime import datetime`
- Functions: `read_text(path)` line 21; `read_text_limited(path, max_chars)` line 25; `split_text(text, max_chars, overlap_chars)` line 34; `load_context_chunks(context_path, chunk_dir, chunk_chars, overlap_chars, max_chunks)` line 52; `fit_prompt(prefix, context, suffix, max_prompt_chars)` line 78; `build_onepass_prompt(context, max_prompt_chars, domain)` line 92; `build_chunk_prompt(title, index, total, context, max_prompt_chars, domain)` line 163; `build_batch_reduce_prompt(batch_title, notes, max_prompt_chars, domain)` line 235; `build_final_prompt(notes, max_prompt_chars, domain)` line 274; `create_pipeline(model_dir, device, max_prompt_len, min_response_len)` line 346; `create_ollama_pipeline(args)` line 358; `generate_text(pipe, prompt, max_new_tokens)` line 373; `write_notes(notes_out, notes)` line 378; `pack_batches(items, max_chars)` line 393; `reduce_notes(pipe, notes, args)` line 413; `run_onepass(pipe, context_path, args)` line 435; `run_chunked(pipe, context_path, chunk_dir, notes_out, args)` line 441; `main()` line 477
- Assignments: `ROOT`, `DEFAULT_MODEL_DIR`, `DEFAULT_CONTEXT`, `DEFAULT_CHUNK_DIR`, `DEFAULT_OUT`, `DEFAULT_NOTES_OUT`, `DEFAULT_MUSIC_CONTEXT`, `DEFAULT_MUSIC_CHUNK_DIR`, `DEFAULT_MUSIC_OUT`, `DEFAULT_MUSIC_NOTES_OUT`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import argparse
00005: from datetime import datetime
00006: 
00007: 
00008: ROOT = Path(__file__).resolve().parents[2]
00009: 
00010: DEFAULT_MODEL_DIR = Path.home() / "blender" / "npu-models" / "Phi-3.5-mini-instruct-int4-cw-ov"
00011: DEFAULT_CONTEXT = ROOT / "Tools" / "npu" / "npu_code_context.md"
00012: DEFAULT_CHUNK_DIR = ROOT / "Tools" / "npu" / "npu_code_chunks"
00013: DEFAULT_OUT = ROOT / "Tools" / "npu" / "npu_context_for_aider.md"
00014: DEFAULT_NOTES_OUT = ROOT / "Tools" / "npu" / "npu_chunk_notes.md"
00015: DEFAULT_MUSIC_CONTEXT = ROOT / "Tools" / "npu" / "npu_music_context.md"
00016: DEFAULT_MUSIC_CHUNK_DIR = ROOT / "Tools" / "npu" / "npu_music_chunks"
00017: DEFAULT_MUSIC_OUT = ROOT / "Tools" / "npu" / "npu_music_context_for_aider.md"
00018: DEFAULT_MUSIC_NOTES_OUT = ROOT / "Tools" / "npu" / "npu_music_chunk_notes.md"
00019: 
00020: 
00021: def read_text(path: Path) -> str:
00022:     return path.read_text(encoding="utf-8", errors="replace")
00023: 
00024: 
00025: def read_text_limited(path: Path, max_chars: int) -> str:
00026:     text = read_text(path)
00027: 
00028:     if max_chars <= 0 or len(text) <= max_chars:
00029:         return text
00030: 
00031:     return text[:max_chars] + "\n\n[TRUNCATED BY run_npu_review.py]\n"
00032: 
00033: 
00034: def split_text(text: str, max_chars: int, overlap_chars: int) -> list[str]:
00035:     if len(text) <= max_chars:
00036:         return [text]
00037: 
00038:     chunks: list[str] = []
00039:     start = 0
00040:     text_len = len(text)
00041: 
00042:     while start < text_len:
00043:         end = min(start + max_chars, text_len)
00044:         chunks.append(text[start:end])
00045:         if end == text_len:
00046:             break
00047:         start = max(end - max(0, overlap_chars), start + 1)
00048: 
00049:     return chunks
00050: 
00051: 
00052: def load_context_chunks(
00053:     context_path: Path,
00054:     chunk_dir: Path,
00055:     chunk_chars: int,
00056:     overlap_chars: int,
00057:     max_chunks: int,
00058: ) -> list[tuple[str, str]]:
00059:     chunk_files = []
00060:     if chunk_dir.exists():
00061:         chunk_files = sorted(chunk_dir.glob("chunk_*.md"))
00062: 
00063:     if chunk_files:
00064:         chunks = [(path.name, read_text(path)) for path in chunk_files]
00065:     else:
00066:         text = read_text(context_path)
00067:         chunks = [
00068:             (f"context_slice_{index:03d}.md", chunk)
00069:             for index, chunk in enumerate(split_text(text, chunk_chars, overlap_chars), 1)
00070:         ]
00071: 
00072:     if max_chunks > 0:
00073:         chunks = chunks[:max_chunks]
00074: 
00075:     return chunks
00076: 
00077: 
00078: def fit_prompt(prefix: str, context: str, suffix: str, max_prompt_chars: int) -> str:
00079:     if max_prompt_chars <= 0:
00080:         return prefix + context + suffix
00081: 
00082:     budget = max_prompt_chars - len(prefix) - len(suffix)
00083:     if budget < 1000:
00084:         budget = 1000
00085: 
00086:     if len(context) > budget:
00087:         context = context[:budget] + "\n\n[CHUNK TRIMMED TO FIT NPU PROMPT WINDOW]\n"
00088: 
00089:     return prefix + context + suffix
00090: 
00091: 
00092: def build_onepass_prompt(context: str, max_prompt_chars: int, domain: str = "code") -> str:
00093:     if domain == "music":
00094:         prefix = """
00095: Sei un agente NPU musicale per un progetto Blender audio-reactive.
00096: 
00097: Devi analizzare il contesto fornito, composto da analysis WAV, segmenti musicali e scene JSON generate.
00098: Non devi riscrivere codice.
00099: Non devi inventare parti del brano.
00100: Devi produrre una memoria operativa per Aider/Ollama e per le prossime decisioni creative.
00101: 
00102: Output richiesto in Markdown:
00103: 
00104: ## Track Map
00105: Durata, BPM, segmenti, zone piu intense e zone calme.
00106: 
00107: ## Audio Control Map
00108: Come usare low, mid, high, onset e beat per deformazione mesh, materiali, luci, fog, camera e fisica.
00109: 
00110: ## Scene JSON Map
00111: Scene spec disponibili, palette, oggetti, audio mapping, nodi o materiali suggeriti.
00112: 
00113: ## Suggested Aider File Sets
00114: File e JSON da aggiungere quando si lavora su audio analysis, scene spec, materiali o animazione.
00115: 
00116: ## Warnings
00117: Rischi tecnici, dati troppo lunghi e cose da non applicare direttamente alla scena senza scelta esplicita.
00118: 
00119: CONTESTO MUSICALE:
00120: 
00121: """.lstrip()
00122:         suffix = "\n"
00123:         return fit_prompt(prefix, context, suffix, max_prompt_chars)
00124: 
00125:     prefix = """
00126: Sei un revisore tecnico locale per un progetto Blender Python audio-reactive.
00127: 
00128: Devi analizzare il contesto fornito e produrre un report operativo per Aider/Ollama.
00129: Non devi riscrivere codice.
00130: Non devi proporre modifiche massive.
00131: Devi indicare quali file aggiungere ad Aider per specifici interventi.
00132: 
00133: Output richiesto in Markdown:
00134: 
00135: ## Project Map
00136: Sintesi dei moduli principali.
00137: 
00138: ## Musical Agent Context
00139: Come il progetto gestisce audio, beat, envelope, materiali, fisica, fog, camera.
00140: 
00141: ## Suggested Aider File Sets
00142: Comandi /add consigliati per:
00143: - camera
00144: - fog
00145: - lights
00146: - materials
00147: - physics
00148: - render
00149: - sequencer
00150: - hotpatch
00151: - NPU/tools
00152: 
00153: ## Warnings
00154: Rischi tecnici e cose da non toccare senza richiesta.
00155: 
00156: CONTESTO PROGETTO:
00157: 
00158: """.lstrip()
00159:     suffix = "\n"
00160:     return fit_prompt(prefix, context, suffix, max_prompt_chars)
00161: 
00162: 
00163: def build_chunk_prompt(
00164:     title: str,
00165:     index: int,
00166:     total: int,
00167:     context: str,
00168:     max_prompt_chars: int,
00169:     domain: str = "code",
00170: ) -> str:
00171:     if domain == "music":
00172:         prefix = f"""
00173: Sei un agente NPU musicale per un progetto Blender audio-reactive.
00174: 
00175: Leggi questo chunk musicale {index}/{total}: {title}
00176: 
00177: Obiettivo: estrai memoria operativa da analysis WAV, segmenti audio o scene JSON.
00178: Non inventare. Non riscrivere codice. Non trasformare il chunk in istruzioni definitive di scena.
00179: 
00180: Output Markdown compatto:
00181: 
00182: ## Chunk Role
00183: Che cosa descrive: overview, segmento audio, scene spec, raw prompt o mapping.
00184: 
00185: ## Musical Cues
00186: Zone intense/calde, low/mid/high/onset/beat importanti, transizioni.
00187: 
00188: ## Visual Control Ideas
00189: Deformazione hero, emissione materiali, fog, luci, camera, fisica, sequencer.
00190: 
00191: ## Scene JSON Links
00192: Oggetti, palette, materiali, audio mappings e limiti del JSON.
00193: 
00194: ## Keep / Avoid
00195: Cose da conservare e rischi da evitare nei prossimi hotpatch.
00196: 
00197: CHUNK:
00198: 
00199: """.lstrip()
00200:         suffix = "\n"
00201:         return fit_prompt(prefix, context, suffix, max_prompt_chars)
00202: 
00203:     prefix = f"""
00204: Sei un agente NPU musicale/tecnico per un progetto Blender Python audio-reactive.
00205: 
00206: Leggi questo chunk {index}/{total}: {title}
00207: 
00208: Obiettivo: estrai solo informazioni operative da riusare nella sintesi finale.
00209: Non inventare. Non riscrivere codice. Non fare una review generica.
00210: 
00211: Output Markdown massimo e compatto:
00212: 
00213: ## Chunk Role
00214: Ruolo del file o dei file nel progetto.
00215: 
00216: ## Important Symbols
00217: Funzioni, classi, costanti o pannelli da ricordare.
00218: 
00219: ## Audio/Visual Controls
00220: Parametri che influenzano musica, beat, luci, materiali, fog, fisica, render o sequencer.
00221: 
00222: ## Dependencies
00223: Relazioni con altri moduli.
00224: 
00225: ## Risks
00226: Rischi di modifica e punti dove serve contesto aggiuntivo.
00227: 
00228: CHUNK:
00229: 
00230: """.lstrip()
00231:     suffix = "\n"
00232:     return fit_prompt(prefix, context, suffix, max_prompt_chars)
00233: 
00234: 
00235: def build_batch_reduce_prompt(batch_title: str, notes: str, max_prompt_chars: int, domain: str = "code") -> str:
00236:     if domain == "music":
00237:         prefix = f"""
00238: Sei un agente NPU musicale. Devi comprimere note parziali da analysis WAV e scene JSON.
00239: 
00240: Batch: {batch_title}
00241: 
00242: Mantieni solo:
00243: - mappa musicale del brano
00244: - segmenti e cue audio rilevanti
00245: - relazioni con scene JSON, palette, oggetti e audio mapping
00246: - controlli visuali consigliati
00247: - rischi tecnici o creativi
00248: 
00249: NOTE:
00250: 
00251: """.lstrip()
00252:         suffix = "\n\nProduci una sintesi Markdown compatta per il reduce finale musicale.\n"
00253:         return fit_prompt(prefix, notes, suffix, max_prompt_chars)
00254: 
00255:     prefix = f"""
00256: Sei un agente NPU musicale/tecnico. Devi comprimere note parziali del progetto Blender.
00257: 
00258: Batch: {batch_title}
00259: 
00260: Mantieni solo informazioni operative:
00261: - mappa moduli
00262: - controlli audio-reactive
00263: - file da aggiungere ad Aider
00264: - rischi tecnici
00265: - dipendenze tra moduli
00266: 
00267: NOTE:
00268: 
00269: """.lstrip()
00270:     suffix = "\n\nProduci una sintesi Markdown compatta per il reduce finale.\n"
00271:     return fit_prompt(prefix, notes, suffix, max_prompt_chars)
00272: 
00273: 
00274: def build_final_prompt(notes: str, max_prompt_chars: int, domain: str = "code") -> str:
00275:     if domain == "music":
00276:         prefix = """
00277: Sei il coordinatore dell'agente NPU musicale per un progetto Blender audio-reactive.
00278: 
00279: Combina le note dei chunk in una memoria operativa unica.
00280: Non inventare dettagli non presenti nelle note.
00281: Priorita: rendere utili analysis WAV e scene JSON senza passare tutto il JSON lungo nel prompt.
00282: 
00283: Output richiesto in Markdown:
00284: 
00285: ## Track Map
00286: Struttura del brano, durata, BPM, segmenti forti/calmati.
00287: 
00288: ## Long Music Context Strategy
00289: Come usare overview, segmenti e scene chunk quando il contesto cresce.
00290: 
00291: ## Audio-To-Visual Map
00292: Low, mid, high, onset, beat verso hero mesh, materiali, emissioni, fog, camera, fisica.
00293: 
00294: ## Scene JSON Map
00295: Scene spec, palette, oggetti e mapping da tenere presenti.
00296: 
00297: ## Suggested Aider File Sets
00298: Blocchi /add consigliati per analisi WAV, scene JSON, animazione e materiali.
00299: 
00300: ## Safe Workflow
00301: Ordine consigliato per generare dati, leggere chunk, decidere hotpatch e verificare.
00302: 
00303: ## Warnings
00304: Rischi tecnici, dati da non usare alla cieca, limiti dei JSON generati.
00305: 
00306: NOTE DEI CHUNK:
00307: 
00308: """.lstrip()
00309:         suffix = "\n"
00310:         return fit_prompt(prefix, notes, suffix, max_prompt_chars)
00311: 
00312:     prefix = """
00313: Sei il coordinatore dell'agente NPU musicale/tecnico per un progetto Blender Python audio-reactive.
00314: 
00315: Combina le note dei chunk in un report operativo unico.
00316: Non inventare dettagli non presenti nelle note.
00317: Priorita: aiutare Aider/Ollama e l'utente a sapere quali file caricare e dove intervenire.
00318: 
00319: Output richiesto in Markdown:
00320: 
00321: ## Project Map
00322: Mappa dei moduli e responsabilita.
00323: 
00324: ## Long Context Strategy
00325: Come usare indice, chunk e note per continuare il lavoro senza perdere contesto.
00326: 
```
