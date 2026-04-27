# Project Code Chunk 55/212

- File: `Scripting/v61b/SCENE_TUNING_GUIDE.md`
- Part: `1`
- Lines: `1-213`

## Content
```md
00001: # Spaziotempo Scene Tuning Guide
00002: 
00003: Questa guida e pensata per essere modificata mentre lavori.
00004: Usala dopo aver generato la scena con `main_v61b.py`.
00005: 
00006: ## Avvio rapido
00007: 
00008: 1. Genera la scena con `main_v61b.py`.
00009: 2. Apri la sidebar della Viewport con `N`.
00010: 3. Vai nella tab `Spaziotempo`.
00011: 4. Usa `Apply Live Values` per provare i parametri sul frame corrente.
00012: 5. Usa `Apply + Keyframe` se vuoi fissare quei valori sul frame corrente.
00013: 6. Usa gli hot update selettivi per ricaricare solo la parte che hai cambiato.
00014: 7. Usa `Save Preset` e `Load Preset` per salvare/caricare i valori del pannello.
00015: 
00016: `main_v61b.py` registra automaticamente il pannello, quindi dopo il rebuild non devi aprire
00017: `scene_tuning_panel.py` a mano. Se apri un vecchio `.blend` senza pannello registrato, puoi
00018: ancora aprire `scene_tuning_panel.py` e premere `Alt+P`.
00019: 
00020: ## Cosa controlla il pannello
00021: 
00022: ### Hero / Aura
00023: 
00024: - `Hero scale`: scala globale del centro.
00025: - `Hero deform`: moltiplica la deformazione dei modifier `HeroAudioMeshDisplace`.
00026: - `Hero fine`: moltiplica la micro-deformazione `HeroAudioFineDisplace`.
00027: - `Hero wave`: moltiplica l'onda `HeroAudioSurfaceWave`.
00028: - `Hero twist`: moltiplica la torsione `HeroAudioTwistDeform`.
00029: - `Hero material light`: moltiplica l'emissione audio dei materiali hero.
00030:   Il materiale resta nel ramo principale; la luce extra e un layer di bordo `HeroMatSelfLight*`.
00031: - `Hero material bump`: moltiplica il bump audio dei materiali hero.
00032: - `Hero material rough`: regola la roughness audio dei materiali hero.
00033: - `Hero material noise`: cambia la scala del rumore materiale.
00034: - `Aura deform`: imposta la proprieta `aura_deform` di `AuraAudioSampler`.
00035: - `Aura detail`: imposta il dettaglio/rumore dell'aura.
00036: - `Aura pulse`: imposta il valore pulsante letto dai driver dell'aura.
00037: 
00038: Nota: se la scena e gia animata, `Apply Live Values` cambia il frame corrente.
00039: Per cambiare tutta l'animazione usa la sezione `Scale Existing Animation`.
00040: 
00041: ### Fog
00042: 
00043: - `Fog density`: densita del volume.
00044: - `Fog emission`: luce interna del volume.
00045: - `Fog noise`: scala del rumore volumetrico.
00046: - `Fog XY`: compatta o allarga il volume sul piano.
00047: - `Fog Z`: espande il volume in altezza.
00048: - `Show fog cube`: mostra il contenitore volume in viewport.
00049: 
00050: Non nascondere il cubo in render se vuoi vedere il fog.
00051: Il cubo e un contenitore volumetrico, non un oggetto decorativo.
00052: La dinamica del fumo e gestita in `fog_dynamics.py`: i nodi density/noise/wave/mapping
00053: vengono animati per creare un effetto tipo fumo spinto dal vento.
00054: La rete volume usa anche `FogClumpNoise` e `FogClumpRamp`, cosi la nebbia non resta
00055: un velo uniforme ma si compatta in grumi e poi si riapre col ritmo.
00056: 
00057: ### Backdrop / Floor
00058: 
00059: - `Backdrop light`: luminosita dello sfondo.
00060: - `Backdrop noise`: grana dello sfondo.
00061: - `Backdrop scale`: scala del piano di sfondo.
00062: - `Floor scale`: scala il pavimento visibile.
00063: - `Show/Render backdrop`: visibilita viewport/render.
00064: - `Show/Render floor`: visibilita viewport/render.
00065: 
00066: ### Camera / Render
00067: 
00068: - `Preview`: applica il profilo leggero alla scena corrente senza rigenerare lo script.
00069: - `YT Fast 1080p`: look finale leggero, risoluzione `1920x1080`.
00070: - `YT Fast 1440p`: look finale leggero, risoluzione `2560x1440`.
00071: - `YT Fast 4K`: look finale leggero, risoluzione `3840x2160`.
00072: - `YT Final 1080p`: stesso look finale, risoluzione `1920x1080`.
00073: - `YT Final 1440p`: stesso look finale, risoluzione `2560x1440`.
00074: - `YT Final 4K`: stesso look finale, risoluzione `3840x2160`.
00075: - `Runtime profile`: mostra l'ultimo profilo applicato.
00076: - `YouTube final`: indica quale profilo runtime e stato applicato per ultimo.
00077: - `Camera f-stop`: aumenta il valore se la sfera sembra troppo sfocata.
00078: - `Motion blur`: attiva/disattiva motion blur per prove rapide o render finale.
00079: - `Accent emission`: alza/abbassa l'emissione degli oggetti fisici `PhysicsAccent_*`.
00080: - `Compositor glow`: aumenta/diminuisce il glow del compositor.
00081: - `Compositor lens`: aumenta/diminuisce distorsione e dispersione lente.
00082: - `Load Frames + Audio`: carica la sequenza immagini renderizzata e l'audio nel Video Sequencer.
00083:   Usa `encode_image_sequence_v61b.py` e apre il Sequencer se `ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER = True`.
00084: 
00085: Profili runtime:
00086: 
00087: - Preview: `1920x1080`, render percentage `75`, motion blur off, Eevee samples `48`, volumetric samples `32`, bitrate video `12000`.
00088: - YT Fast 1080p: `1920x1080`, render percentage `100`, motion blur off, Eevee samples `48`, volumetric samples `24`, bitrate video `18000`.
00089: - YT Fast 1440p: `2560x1440`, render percentage `100`, motion blur off, Eevee samples `48`, volumetric samples `24`, bitrate video `24000`.
00090: - YT Fast 4K: `3840x2160`, render percentage `100`, motion blur off, Eevee samples `48`, volumetric samples `24`, bitrate video `40000`.
00091: - YT Final 1080p: `1920x1080`, render percentage `100`, motion blur on, Eevee samples `80`, volumetric samples `48`, bitrate video `18000`.
00092: - YT Final 1440p: `2560x1440`, render percentage `100`, motion blur on, Eevee samples `80`, volumetric samples `48`, bitrate video `24000`.
00093: - YT Final 4K: `3840x2160`, render percentage `100`, motion blur on, Eevee samples `80`, volumetric samples `48`, bitrate video `40000`.
00094: 
00095: Questi pulsanti cambiano le impostazioni della scena gia creata.
00096: Non riscrivono `config.py` e non ricreano oggetti, modifier o keyframe.
00097: `Hot Update Scene` preserva il profilo runtime selezionato.
00098: 
00099: ## Hot Update Scene
00100: 
00101: `Hot Update Scene` lancia `hot_update_scene_v61b.py` dalla scena gia aperta.
00102: Quel file e solo un wrapper: svuota la cache Python dei moduli aggiornabili e poi esegue
00103: il package `hotpatch`.
00104: Serve per iterare velocemente quando modifichi valori in `config.py`, `materials.py`,
00105: `fog_dynamics.py`, `render_setup.py` o la logica di animazione leggera.
00106: 
00107: Hot update disponibili:
00108: 
00109: - `Render Only`: render/output/compositor e profilo runtime.
00110: - `Materials`: materiali/audio nodes del centro.
00111: - `Fog`: cubo volumetrico, nodi fog e keyframe del fumo.
00112: - `Physics`: orbite atomiche, `HeroGravityField`, emissione e rotazione dei `PhysicsAccent_*`.
00113: - `Hot Update All`: esegue tutto, incluse luci/world/backdrop e cleanup dei vecchi rhythm light.
00114: 
00115: `Rebuild / Restart Check` crea il text block `SPAZIOTEMPO_REBUILD_CHECK`.
00116: Se mancano oggetti strutturali, frame count o modifier principali, consiglia `main_v61b.py`.
00117: Se manca solo una parte patchabile, ti indica quale hot update usare.
00118: 
00119: `Optimizer Check` crea il text block `SPAZIOTEMPO_OPTIMIZER_REPORT`.
00120: Controlla particle system, rigid body dinamici, cloth/fluid/soft body e cache/bake utili per il render.
00121: 
00122: Cosa aggiorna `Hot Update All` senza cancellare la scena:
00123: 
00124: - render/output/compositor;
00125: - world light e area light, con variazione quasi invisibile;
00126: - sfondo `SoftRhythmBackdrop`;
00127: - emissione materiale del centro `HeroRoot`, cosi non dipende solo dal world;
00128: - materiale volumetrico e keyframe del cubo `AtmosphereCube`;
00129: - emissione/materiali/keyframe degli oggetti `PhysicsAccent_*`;
00130: - rimozione dei vecchi oggetti `RhythmPulseLight*` e `RhythmEmitterOrb*`, se presenti.
00131: 
00132: Cosa non fa:
00133: 
00134: - non importa di nuovo l'asset centrale;
00135: - non cancella la scena;
00136: - non ricrea camera, pavimento o struttura principale;
00137: - non lancia render.
00138: 
00139: Usa ancora `main_v61b.py` quando cambi struttura della scena, import asset, geometrie principali,
00140: numero di frame dell'analisi audio o sistemi particellari da ricostruire da zero.
00141: 
00142: Struttura dei patch:
00143: 
00144: - `hotpatch/common.py`: helper condivisi, config e caricamento analisi audio.
00145: - `hotpatch/render_patch.py`: render settings, output e compositor.
00146: - `hotpatch/lighting_patch.py`: world light, area light, backdrop e vecchi oggetti luce.
00147: - `hotpatch/hero_material_patch.py`: mantiene vivo il materiale hero fondendo BSDF originale e luce audio di bordo.
00148: - `hotpatch/fog_patch.py`: cubo volumetrico, nodi fog e animazione fumo/audio.
00149: - `hotpatch/accent_patch.py`: emissione e rotazione degli oggetti `PhysicsAccent_*`.
00150: - `hotpatch/diagnostics.py`: check rebuild/restart e optimizer cache/bake.
00151: - `hotpatch/runner.py`: esegue tutte le patch in ordine.
00152: 
00153: Se vuoi provare solo una parte, modifica il file patch relativo e premi di nuovo
00154: `Hot Update Scene` dal pannello.
00155: 
00156: ## Fisica atomica
00157: 
00158: Gli oggetti `PhysicsAccent_*` sono trattati come satelliti del centro `HeroRoot`.
00159: Il campo principale e `HeroGravityField`: segue il centro e cambia forza col ritmo.
00160: Gli accenti orbitano su gusci diversi; basso, beat e onset modificano raggio, altezza,
00161: velocita orbitale ed emissione materiale.
00162: 
00163: La parte visiva e keyframed per restare stabile nei render e nei sample da meta brano.
00164: Il campo centrale resta disponibile per particelle o sistemi fisici futuri.
00165: 
00166: ## Scale Existing Animation
00167: 
00168: Questa sezione modifica i keyframe gia creati.
00169: Usala con attenzione e salva una copia del blend prima di sperimentare.
00170: 
00171: - `Anim hero deform`: moltiplica i keyframe di displace, wave e twist hero.
00172: - `Anim aura`: moltiplica le FCurve del controller aura.
00173: 
00174: Poi premi `Scale Existing FCurves`.
00175: 
00176: ## Workflow consigliato
00177: 
00178: 1. Genera scena con `main_v61b.py`.
00179: 2. Se cambi solo materiali/fog/luci/config, premi `Hot Update Scene`.
00180: 3. Regola il frame 1 con `Apply Live Values`.
00181: 4. Vai su un frame forte del brano, per esempio un beat.
00182: 5. Regola fog/particelle/deformazione.
00183: 6. Premi `Apply + Keyframe`.
00184: 7. Ripeti su 3-5 punti importanti del brano.
00185: 8. Se tutta una categoria e troppo debole o troppo forte, usa `Scale Existing Animation`.
00186: 
00187: ## Render in sequenza immagini
00188: 
00189: `main_v61b.py` ora usa `RENDER_OUTPUT_MODE = "IMAGE_SEQUENCE"`.
00190: Quando premi `Render > Render Animation`, Blender scrive i frame qui:
00191: 
00192: `C:\Users\carmi\blender\renders\spaziotempo_asset_visual_v61b_frames`
00193: 
00194: Vantaggi:
00195: 
00196: - se il render si interrompe, i frame gia completati restano salvati;
00197: - puoi fare post-processing sui singoli frame;
00198: - puoi rimontare il video finale solo alla fine.
00199: 
00200: Dopo aver renderizzato i frame:
00201: 
00202: 1. Vai nel pannello `Spaziotempo`.
00203: 2. Premi `Load Frames + Audio`.
00204: 3. Lo script prepara la sequenza immagini + audio nel Video Sequencer.
00205: 4. Premi `Render > Render Animation` per creare l'MP4 finale.
00206: 
00207: Puoi ancora aprire `encode_image_sequence_v61b.py` e premere `Alt+P` manualmente se vuoi.
00208: 
00209: Nota: lo script di encoding non avvia automaticamente il render MP4, a meno che in `config.py`
00210: tu non imposti `ENCODE_SEQUENCE_AUTO_RENDER = True`.
00211: 
00212: ### Encoding veloce con ffmpeg
00213: 
```
