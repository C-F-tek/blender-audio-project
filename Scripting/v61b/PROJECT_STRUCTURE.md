# Spaziotempo v61b Project Structure

Questa struttura non rinomina gli oggetti storici della scena: li cataloga. Gli script esistenti continuano a trovare `HeroRoot`, `AtmosphereCube`, `PhysicsAccent_*`, ecc.; sopra viene aggiunto un layer system riusabile con collection, metadati e feature catalog.

## Package

- `spaziotempo/core/registry.py`: nomi canonici, layer, collection, feature catalog e regole di classificazione.
- `spaziotempo/core/collections.py`: crea le collection `ST_*`, collega gli oggetti al layer giusto e scrive custom props `st_family`, `st_layer`, `st_feature`.
- `spaziotempo/features/catalog.py`: punto di accesso per future feature modulari.

## Layer

- `ST_00_Core`: root della scena e controlli globali.
- `ST_05_World_Set`: pavimento, backdrop e set fisico.
- `ST_10_Hero`: oggetto centrale, aura, materiali, deformazione mesh, anelli e ribbon.
- `ST_20_Atmosphere`: cubo volumetrico, nebbia, mist e controller.
- `ST_30_Atomic_Physics`: gravita centrale, satelliti fisici, campi forza e orbite.
- `ST_40_Lights`: luci fisiche e supporto luminoso.
- `ST_50_Render_IO`: camera, target, audio strip, sequencer e helper invisibili di output.
- `ST_60_Water`: layer vuoto riservato, pronto per una futura feature acqua.
- `ST_90_Technical`: ancore, sorgenti particellari, compatibilita e oggetti di supporto.

## Regola pratica

Quando aggiungiamo una feature nuova:

1. Si registra il layer o si usa un layer esistente in `spaziotempo/core/registry.py`.
2. Gli oggetti creati hanno prefissi chiari e una collection dedicata.
3. La logica di build resta nello script di creazione, mentre l'aggiornamento leggero va in `hotpatch/`.
4. Il pannello richiama l'hotpatch, non ricostruisce tutta la scena se cambia solo materiale/fog/render/fisica.

## Acqua futura

L'acqua non e stata aggiunta. Il layer `ST_60_Water` serve solo come spazio pronto: in futuro potra avere un modulo dedicato, ad esempio `spaziotempo/features/water.py`, con build/update/check separati e senza toccare hero, nebbia o fisica atomica.

## Fog veloce

La nebbia pesante vive ancora in `AtmosphereCube`, ma ora e opzionale. Di default `FOG_VOLUME_ENABLED = False` e la scena usa `FogFilament_*`: piani trasparenti procedurali, raggruppati in `FogFilamentsRoot`, animati dal modulo `fog_dynamics.py`.

Questa scelta tiene separati:

- volume vero: utile se serve profondita fisica, ma costoso e soggetto a griglia Eevee;
- filamenti: piu veloci, piu puliti sullo sfondo e facili da hotpatchare.
