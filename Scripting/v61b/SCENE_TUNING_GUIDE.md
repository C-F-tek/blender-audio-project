# Spaziotempo Scene Tuning Guide

Questa guida e pensata per essere modificata mentre lavori.
Usala dopo aver generato la scena con `main_v61b.py`.

## Avvio rapido

1. Genera la scena con `main_v61b.py`.
2. Apri la sidebar della Viewport con `N`.
3. Vai nella tab `Spaziotempo`.
4. Usa `Apply Live Values` per provare i parametri sul frame corrente.
5. Usa `Apply + Keyframe` se vuoi fissare quei valori sul frame corrente.
6. Usa gli hot update selettivi per ricaricare solo la parte che hai cambiato.
7. Usa `Save Preset` e `Load Preset` per salvare/caricare i valori del pannello.

`main_v61b.py` registra automaticamente il pannello, quindi dopo il rebuild non devi aprire
`scene_tuning_panel.py` a mano. Se apri un vecchio `.blend` senza pannello registrato, puoi
ancora aprire `scene_tuning_panel.py` e premere `Alt+P`.

## Cosa controlla il pannello

### Hero / Aura

- `Hero scale`: scala globale del centro.
- `Hero deform`: moltiplica la deformazione dei modifier `HeroAudioMeshDisplace`.
- `Hero fine`: moltiplica la micro-deformazione `HeroAudioFineDisplace`.
- `Hero wave`: moltiplica l'onda `HeroAudioSurfaceWave`.
- `Hero twist`: moltiplica la torsione `HeroAudioTwistDeform`.
- `Hero material light`: moltiplica l'emissione audio dei materiali hero.
  Il materiale resta nel ramo principale; la luce extra e un layer di bordo `HeroMatSelfLight*`.
- `Hero material bump`: moltiplica il bump audio dei materiali hero.
- `Hero material rough`: regola la roughness audio dei materiali hero.
- `Hero material noise`: cambia la scala del rumore materiale.
- `Aura deform`: imposta la proprieta `aura_deform` di `AuraAudioSampler`.
- `Aura detail`: imposta il dettaglio/rumore dell'aura.
- `Aura pulse`: imposta il valore pulsante letto dai driver dell'aura.

Nota: se la scena e gia animata, `Apply Live Values` cambia il frame corrente.
Per cambiare tutta l'animazione usa la sezione `Scale Existing Animation`.

### Fog

- `Fog density`: densita del volume.
- `Fog emission`: luce interna del volume.
- `Fog noise`: scala del rumore volumetrico.
- `Fog XY`: compatta o allarga il volume sul piano.
- `Fog Z`: espande il volume in altezza.
- `Show fog cube`: mostra il contenitore volume in viewport.

Non nascondere il cubo in render se vuoi vedere il fog.
Il cubo e un contenitore volumetrico, non un oggetto decorativo.
La dinamica del fumo e gestita in `fog_dynamics.py`: i nodi density/noise/wave/mapping
vengono animati per creare un effetto tipo fumo spinto dal vento.
La rete volume usa anche `FogClumpNoise` e `FogClumpRamp`, cosi la nebbia non resta
un velo uniforme ma si compatta in grumi e poi si riapre col ritmo.

### Backdrop / Floor

- `Backdrop light`: luminosita dello sfondo.
- `Backdrop noise`: grana dello sfondo.
- `Backdrop scale`: scala del piano di sfondo.
- `Floor scale`: scala il pavimento visibile.
- `Show/Render backdrop`: visibilita viewport/render.
- `Show/Render floor`: visibilita viewport/render.

### Camera / Render

- `Preview`: applica il profilo leggero alla scena corrente senza rigenerare lo script.
- `YT Fast 1080p`: look finale leggero, risoluzione `1920x1080`.
- `YT Fast 1440p`: look finale leggero, risoluzione `2560x1440`.
- `YT Fast 4K`: look finale leggero, risoluzione `3840x2160`.
- `YT Final 1080p`: stesso look finale, risoluzione `1920x1080`.
- `YT Final 1440p`: stesso look finale, risoluzione `2560x1440`.
- `YT Final 4K`: stesso look finale, risoluzione `3840x2160`.
- `Runtime profile`: mostra l'ultimo profilo applicato.
- `YouTube final`: indica quale profilo runtime e stato applicato per ultimo.
- `Camera f-stop`: aumenta il valore se la sfera sembra troppo sfocata.
- `Motion blur`: attiva/disattiva motion blur per prove rapide o render finale.
- `Accent emission`: alza/abbassa l'emissione degli oggetti fisici `PhysicsAccent_*`.
- `Compositor glow`: aumenta/diminuisce il glow del compositor.
- `Compositor lens`: aumenta/diminuisce distorsione e dispersione lente.
- `Load Frames + Audio`: carica la sequenza immagini renderizzata e l'audio nel Video Sequencer.
  Usa `encode_image_sequence_v61b.py` e apre il Sequencer se `ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER = True`.

Profili runtime:

- Preview: `1920x1080`, render percentage `75`, motion blur off, Eevee samples `48`, volumetric samples `32`, bitrate video `12000`.
- YT Fast 1080p: `1920x1080`, render percentage `100`, motion blur off, Eevee samples `48`, volumetric samples `24`, bitrate video `18000`.
- YT Fast 1440p: `2560x1440`, render percentage `100`, motion blur off, Eevee samples `48`, volumetric samples `24`, bitrate video `24000`.
- YT Fast 4K: `3840x2160`, render percentage `100`, motion blur off, Eevee samples `48`, volumetric samples `24`, bitrate video `40000`.
- YT Final 1080p: `1920x1080`, render percentage `100`, motion blur on, Eevee samples `80`, volumetric samples `48`, bitrate video `18000`.
- YT Final 1440p: `2560x1440`, render percentage `100`, motion blur on, Eevee samples `80`, volumetric samples `48`, bitrate video `24000`.
- YT Final 4K: `3840x2160`, render percentage `100`, motion blur on, Eevee samples `80`, volumetric samples `48`, bitrate video `40000`.

Questi pulsanti cambiano le impostazioni della scena gia creata.
Non riscrivono `config.py` e non ricreano oggetti, modifier o keyframe.
`Hot Update Scene` preserva il profilo runtime selezionato.

## Hot Update Scene

`Hot Update Scene` lancia `hot_update_scene_v61b.py` dalla scena gia aperta.
Quel file e solo un wrapper: svuota la cache Python dei moduli aggiornabili e poi esegue
il package `hotpatch`.
Serve per iterare velocemente quando modifichi valori in `config.py`, `materials.py`,
`fog_dynamics.py`, `render_setup.py` o la logica di animazione leggera.

Hot update disponibili:

- `Render Only`: render/output/compositor e profilo runtime.
- `Materials`: materiali/audio nodes del centro.
- `Fog`: cubo volumetrico, nodi fog e keyframe del fumo.
- `Physics`: orbite atomiche, `HeroGravityField`, emissione e rotazione dei `PhysicsAccent_*`.
- `Hot Update All`: esegue tutto, incluse luci/world/backdrop e cleanup dei vecchi rhythm light.

`Rebuild / Restart Check` crea il text block `SPAZIOTEMPO_REBUILD_CHECK`.
Se mancano oggetti strutturali, frame count o modifier principali, consiglia `main_v61b.py`.
Se manca solo una parte patchabile, ti indica quale hot update usare.

`Optimizer Check` crea il text block `SPAZIOTEMPO_OPTIMIZER_REPORT`.
Controlla particle system, rigid body dinamici, cloth/fluid/soft body e cache/bake utili per il render.

Cosa aggiorna `Hot Update All` senza cancellare la scena:

- render/output/compositor;
- world light e area light, con variazione quasi invisibile;
- sfondo `SoftRhythmBackdrop`;
- emissione materiale del centro `HeroRoot`, cosi non dipende solo dal world;
- materiale volumetrico e keyframe del cubo `AtmosphereCube`;
- emissione/materiali/keyframe degli oggetti `PhysicsAccent_*`;
- rimozione dei vecchi oggetti `RhythmPulseLight*` e `RhythmEmitterOrb*`, se presenti.

Cosa non fa:

- non importa di nuovo l'asset centrale;
- non cancella la scena;
- non ricrea camera, pavimento o struttura principale;
- non lancia render.

Usa ancora `main_v61b.py` quando cambi struttura della scena, import asset, geometrie principali,
numero di frame dell'analisi audio o sistemi particellari da ricostruire da zero.

Struttura dei patch:

- `hotpatch/common.py`: helper condivisi, config e caricamento analisi audio.
- `hotpatch/render_patch.py`: render settings, output e compositor.
- `hotpatch/lighting_patch.py`: world light, area light, backdrop e vecchi oggetti luce.
- `hotpatch/hero_material_patch.py`: mantiene vivo il materiale hero fondendo BSDF originale e luce audio di bordo.
- `hotpatch/fog_patch.py`: cubo volumetrico, nodi fog e animazione fumo/audio.
- `hotpatch/accent_patch.py`: emissione e rotazione degli oggetti `PhysicsAccent_*`.
- `hotpatch/diagnostics.py`: check rebuild/restart e optimizer cache/bake.
- `hotpatch/runner.py`: esegue tutte le patch in ordine.

Se vuoi provare solo una parte, modifica il file patch relativo e premi di nuovo
`Hot Update Scene` dal pannello.

## Fisica atomica

Gli oggetti `PhysicsAccent_*` sono trattati come satelliti del centro `HeroRoot`.
Il campo principale e `HeroGravityField`: segue il centro e cambia forza col ritmo.
Gli accenti orbitano su gusci diversi; basso, beat e onset modificano raggio, altezza,
velocita orbitale ed emissione materiale.

La parte visiva e keyframed per restare stabile nei render e nei sample da meta brano.
Il campo centrale resta disponibile per particelle o sistemi fisici futuri.

## Scale Existing Animation

Questa sezione modifica i keyframe gia creati.
Usala con attenzione e salva una copia del blend prima di sperimentare.

- `Anim hero deform`: moltiplica i keyframe di displace, wave e twist hero.
- `Anim aura`: moltiplica le FCurve del controller aura.

Poi premi `Scale Existing FCurves`.

## Workflow consigliato

1. Genera scena con `main_v61b.py`.
2. Se cambi solo materiali/fog/luci/config, premi `Hot Update Scene`.
3. Regola il frame 1 con `Apply Live Values`.
4. Vai su un frame forte del brano, per esempio un beat.
5. Regola fog/particelle/deformazione.
6. Premi `Apply + Keyframe`.
7. Ripeti su 3-5 punti importanti del brano.
8. Se tutta una categoria e troppo debole o troppo forte, usa `Scale Existing Animation`.

## Render in sequenza immagini

`main_v61b.py` ora usa `RENDER_OUTPUT_MODE = "IMAGE_SEQUENCE"`.
Quando premi `Render > Render Animation`, Blender scrive i frame qui:

`C:\Users\carmi\blender\renders\spaziotempo_asset_visual_v61b_frames`

Vantaggi:

- se il render si interrompe, i frame gia completati restano salvati;
- puoi fare post-processing sui singoli frame;
- puoi rimontare il video finale solo alla fine.

Dopo aver renderizzato i frame:

1. Vai nel pannello `Spaziotempo`.
2. Premi `Load Frames + Audio`.
3. Lo script prepara la sequenza immagini + audio nel Video Sequencer.
4. Premi `Render > Render Animation` per creare l'MP4 finale.

Puoi ancora aprire `encode_image_sequence_v61b.py` e premere `Alt+P` manualmente se vuoi.

Nota: lo script di encoding non avvia automaticamente il render MP4, a meno che in `config.py`
tu non imposti `ENCODE_SEQUENCE_AUTO_RENDER = True`.

### Encoding veloce con ffmpeg

Per evitare banding e artefatti nei gradienti della nebbia, usa il pulsante:

`Encode MP4 FFmpeg`

Questo legge direttamente i PNG renderizzati, sincronizza l'audio anche se il sample parte da un frame centrale, e scrive l'MP4 con H.264 ad alta qualita. Le impostazioni sono in `config.py`:

- `ENCODE_USE_EXTERNAL_FFMPEG = True`
- `FFMPEG_CRF = 16` final / `17` preview
- `FFMPEG_PRESET = "slow"`
- `FFMPEG_TUNE = "film"`

Se Blender non vede ancora ffmpeg nel PATH, lo script prova anche a cercarlo in Desktop/Downloads.

### Sample da meta brano

Se renderizzi solo un pezzo centrale, per esempio dal frame `1800`, i file avranno un nome tipo:

`spaziotempo_v61b_1800.png`

`encode_image_sequence_v61b.py` legge il numero del primo frame e sposta automaticamente l'audio,
cosi il primo frame del sample corrisponde al punto corretto della canzone.

In `config.py` il comportamento e controllato da:

- `ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER = True`
- `ENCODE_SEQUENCE_SKIP_PLACEHOLDERS = True`

Se trova buchi nella sequenza, usa solo il primo blocco continuo di frame.
Questo evita sample fuori sync se mancano frame nel mezzo.

## Post-processing su immagini

Il post-processing leggero conviene farlo durante il render o durante l'encoding:

- color correction;
- glow moderato;
- vignette leggera;
- sharpen molto leggero;
- piccola distorsione lente.

Questi effetti aggiungono poco tempo rispetto al render 3D.

Effetti pesanti come denoise AI, upscale AI, optical flow o blur complessi conviene farli dopo,
sulla sequenza gia renderizzata, perche possono allungare molto il tempo totale.

## Nebbia leggera

La nebbia volumetrica piena e disattivata di default con:

`FOG_VOLUME_ENABLED = False`

Al suo posto vengono creati `FogFilament_*`: banchi sottili e trasparenti animati a ritmo.
Sono piu leggeri del volume Eevee e riducono gli artefatti quadrati sullo sfondo.
Se vuoi riattivare il volume vero, porta `FOG_VOLUME_ENABLED = True`, ma aspettati render piu pesanti.

## Oggetti utili da selezionare

Il pannello ha pulsanti di selezione:

- `Hero`: seleziona centro e controller principali.
- `Fog`: seleziona volume, sfondo e controller.

## Struttura progetto

Il progetto ora ha un layer system in `spaziotempo/`:

- `spaziotempo/core/registry.py`: nomi canonici, layer e feature catalog.
- `spaziotempo/core/collections.py`: crea le collection `ST_*` e classifica gli oggetti.
- `PROJECT_STRUCTURE.md`: briefing tecnico della struttura.

Le collection principali sono:

- `ST_00_Core`
- `ST_05_World_Set`
- `ST_10_Hero`
- `ST_20_Atmosphere`
- `ST_30_Atomic_Physics`
- `ST_40_Lights`
- `ST_50_Render_IO`
- `ST_60_Water` vuota e riservata per il futuro
- `ST_90_Technical`

`main_v61b.py` e `Hot Update All` aggiornano automaticamente questa classificazione.
Gli oggetti storici non vengono rinominati, quindi gli script continuano a funzionare.
## Note di sicurezza

- `Apply Live Values` e reversibile con Undo.
- `Scale Existing FCurves` modifica i keyframe: salva prima una copia.
- Il preset JSON viene scritto qui:

`scene_tuning_preset.json`
