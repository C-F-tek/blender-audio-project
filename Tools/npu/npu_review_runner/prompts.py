"""Prompt builders for NPU review."""

from __future__ import annotations

from .text_utils import fit_prompt

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


def build_batch_reduce_prompt(
    batch_title: str, notes: str, max_prompt_chars: int, domain: str = "code"
) -> str:
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
