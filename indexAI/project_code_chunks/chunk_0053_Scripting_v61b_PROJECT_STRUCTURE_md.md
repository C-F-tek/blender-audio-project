# Project Code Chunk 53/212

- File: `Scripting/v61b/PROJECT_STRUCTURE.md`
- Part: `1`
- Lines: `1-43`

## Content
```md
00001: # Spaziotempo v61b Project Structure
00002: 
00003: Questa struttura non rinomina gli oggetti storici della scena: li cataloga. Gli script esistenti continuano a trovare `HeroRoot`, `AtmosphereCube`, `PhysicsAccent_*`, ecc.; sopra viene aggiunto un layer system riusabile con collection, metadati e feature catalog.
00004: 
00005: ## Package
00006: 
00007: - `spaziotempo/core/registry.py`: nomi canonici, layer, collection, feature catalog e regole di classificazione.
00008: - `spaziotempo/core/collections.py`: crea le collection `ST_*`, collega gli oggetti al layer giusto e scrive custom props `st_family`, `st_layer`, `st_feature`.
00009: - `spaziotempo/features/catalog.py`: punto di accesso per future feature modulari.
00010: 
00011: ## Layer
00012: 
00013: - `ST_00_Core`: root della scena e controlli globali.
00014: - `ST_05_World_Set`: pavimento, backdrop e set fisico.
00015: - `ST_10_Hero`: oggetto centrale, aura, materiali, deformazione mesh, anelli e ribbon.
00016: - `ST_20_Atmosphere`: cubo volumetrico, nebbia, mist e controller.
00017: - `ST_30_Atomic_Physics`: gravita centrale, satelliti fisici, campi forza e orbite.
00018: - `ST_40_Lights`: luci fisiche e supporto luminoso.
00019: - `ST_50_Render_IO`: camera, target, audio strip, sequencer e helper invisibili di output.
00020: - `ST_60_Water`: layer vuoto riservato, pronto per una futura feature acqua.
00021: - `ST_90_Technical`: ancore, sorgenti particellari, compatibilita e oggetti di supporto.
00022: 
00023: ## Regola pratica
00024: 
00025: Quando aggiungiamo una feature nuova:
00026: 
00027: 1. Si registra il layer o si usa un layer esistente in `spaziotempo/core/registry.py`.
00028: 2. Gli oggetti creati hanno prefissi chiari e una collection dedicata.
00029: 3. La logica di build resta nello script di creazione, mentre l'aggiornamento leggero va in `hotpatch/`.
00030: 4. Il pannello richiama l'hotpatch, non ricostruisce tutta la scena se cambia solo materiale/fog/render/fisica.
00031: 
00032: ## Acqua futura
00033: 
00034: L'acqua non e stata aggiunta. Il layer `ST_60_Water` serve solo come spazio pronto: in futuro potra avere un modulo dedicato, ad esempio `spaziotempo/features/water.py`, con build/update/check separati e senza toccare hero, nebbia o fisica atomica.
00035: 
00036: ## Fog veloce
00037: 
00038: La nebbia pesante vive ancora in `AtmosphereCube`, ma ora e opzionale. Di default `FOG_VOLUME_ENABLED = False` e la scena usa `FogFilament_*`: piani trasparenti procedurali, raggruppati in `FogFilamentsRoot`, animati dal modulo `fog_dynamics.py`.
00039: 
00040: Questa scelta tiene separati:
00041: 
00042: - volume vero: utile se serve profondita fisica, ma costoso e soggetto a griglia Eevee;
00043: - filamenti: piu veloci, piu puliti sullo sfondo e facili da hotpatchare.
```
