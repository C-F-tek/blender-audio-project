# Project Code Chunk 105/212

- File: `Scripting/v61b_backgood/SCENE_TUNING_GUIDE.md`
- Part: `1`
- Lines: `1-223`

## Content
```md
00001: # Spaziotempo Scene Tuning Guide
00002: 
00003: Questa guida e pensata per essere modificata mentre lavori.
00004: Usala dopo aver generato la scena con `main_v61b.py`.
00005: 
00006: ## Avvio rapido
00007: 
00008: 1. In Blender apri `scene_tuning_panel.py`.
00009: 2. Premi `Alt+P` nel Text Editor.
00010: 3. Apri la sidebar della Viewport con `N`.
00011: 4. Vai nella tab `Spaziotempo`.
00012: 5. Usa `Apply Live Values` per provare i parametri sul frame corrente.
00013: 6. Usa `Apply + Keyframe` se vuoi fissare quei valori sul frame corrente.
00014: 7. Usa `Hot Update Scene` per ricaricare materiali, fog, luci e keyframe audio senza ricostruire la scena.
00015: 8. Usa `Save Preset` e `Load Preset` per salvare/caricare i valori del pannello.
00016: 
00017: ## Cosa controlla il pannello
00018: 
00019: ### Hero / Aura
00020: 
00021: - `Hero scale`: scala globale del centro.
00022: - `Hero deform`: moltiplica la deformazione dei modifier `HeroAudioMeshDisplace`.
00023: - `Hero fine`: moltiplica la micro-deformazione `HeroAudioFineDisplace`.
00024: - `Hero wave`: moltiplica l'onda `HeroAudioSurfaceWave`.
00025: - `Hero twist`: moltiplica la torsione `HeroAudioTwistDeform`.
00026: - `Hero material light`: moltiplica l'emissione audio dei materiali hero.
00027:   Il materiale resta nel ramo principale; la luce extra e un layer di bordo `HeroMatSelfLight*`.
00028: - `Hero material bump`: moltiplica il bump audio dei materiali hero.
00029: - `Hero material rough`: regola la roughness audio dei materiali hero.
00030: - `Hero material noise`: cambia la scala del rumore materiale.
00031: - `Aura deform`: imposta la proprieta `aura_deform` di `AuraAudioSampler`.
00032: - `Aura detail`: imposta il dettaglio/rumore dell'aura.
00033: - `Aura pulse`: imposta il valore pulsante letto dai driver dell'aura.
00034: 
00035: Nota: se la scena e gia animata, `Apply Live Values` cambia il frame corrente.
00036: Per cambiare tutta l'animazione usa la sezione `Scale Existing Animation`.
00037: 
00038: ### Fog
00039: 
00040: - `Fog density`: densita del volume.
00041: - `Fog emission`: luce interna del volume.
00042: - `Fog noise`: scala del rumore volumetrico.
00043: - `Fog XY`: compatta o allarga il volume sul piano.
00044: - `Fog Z`: espande il volume in altezza.
00045: - `Show fog cube`: mostra il contenitore volume in viewport.
00046: 
00047: Non nascondere il cubo in render se vuoi vedere il fog.
00048: Il cubo e un contenitore volumetrico, non un oggetto decorativo.
00049: La dinamica del fumo e gestita in `fog_dynamics.py`: i nodi density/noise/wave/mapping
00050: vengono animati per creare un effetto tipo fumo spinto dal vento.
00051: La rete volume usa anche `FogClumpNoise` e `FogClumpRamp`, cosi la nebbia non resta
00052: un velo uniforme ma si compatta in grumi e poi si riapre col ritmo.
00053: 
00054: ### Backdrop / Floor
00055: 
00056: - `Backdrop light`: luminosita dello sfondo.
00057: - `Backdrop noise`: grana dello sfondo.
00058: - `Backdrop scale`: scala del piano di sfondo.
00059: - `Floor scale`: scala il pavimento visibile.
00060: - `Show/Render backdrop`: visibilita viewport/render.
00061: - `Show/Render floor`: visibilita viewport/render.
00062: 
00063: ### Camera / Render
00064: 
00065: - `Preview`: applica il profilo leggero alla scena corrente senza rigenerare lo script.
00066: - `YT Fast 1080p`: look finale leggero, risoluzione `1920x1080`.
00067: - `YT Fast 1440p`: look finale leggero, risoluzione `2560x1440`.
00068: - `YT Fast 4K`: look finale leggero, risoluzione `3840x2160`.
00069: - `YT Final 1080p`: stesso look finale, risoluzione `1920x1080`.
00070: - `YT Final 1440p`: stesso look finale, risoluzione `2560x1440`.
00071: - `YT Final 4K`: stesso look finale, risoluzione `3840x2160`.
00072: - `Runtime profile`: mostra l'ultimo profilo applicato.
00073: - `YouTube final`: indica quale profilo runtime e stato applicato per ultimo.
00074: - `Camera f-stop`: aumenta il valore se la sfera sembra troppo sfocata.
00075: - `Motion blur`: attiva/disattiva motion blur per prove rapide o render finale.
00076: - `Accent emission`: alza/abbassa l'emissione degli oggetti fisici `PhysicsAccent_*`.
00077: - `Compositor glow`: aumenta/diminuisce il glow del compositor.
00078: - `Compositor lens`: aumenta/diminuisce distorsione e dispersione lente.
00079: 
00080: Profili runtime:
00081: 
00082: - Preview: `1920x1080`, render percentage `75`, motion blur off, Eevee samples `48`, volumetric samples `32`, bitrate video `12000`.
00083: - YT Fast 1080p: `1920x1080`, render percentage `100`, motion blur off, Eevee samples `64`, volumetric samples `32`, bitrate video `18000`.
00084: - YT Fast 1440p: `2560x1440`, render percentage `100`, motion blur off, Eevee samples `64`, volumetric samples `32`, bitrate video `24000`.
00085: - YT Fast 4K: `3840x2160`, render percentage `100`, motion blur off, Eevee samples `64`, volumetric samples `32`, bitrate video `40000`.
00086: - YT Final 1080p: `1920x1080`, render percentage `100`, motion blur on, Eevee samples `96`, volumetric samples `64`, bitrate video `18000`.
00087: - YT Final 1440p: `2560x1440`, render percentage `100`, motion blur on, Eevee samples `96`, volumetric samples `64`, bitrate video `24000`.
00088: - YT Final 4K: `3840x2160`, render percentage `100`, motion blur on, Eevee samples `96`, volumetric samples `64`, bitrate video `40000`.
00089: 
00090: Questi pulsanti cambiano le impostazioni della scena gia creata.
00091: Non riscrivono `config.py` e non ricreano oggetti, modifier o keyframe.
00092: `Hot Update Scene` preserva il profilo runtime selezionato.
00093: 
00094: ## Hot Update Scene
00095: 
00096: `Hot Update Scene` lancia `hot_update_scene_v61b.py` dalla scena gia aperta.
00097: Quel file e solo un wrapper: svuota la cache Python dei moduli aggiornabili e poi esegue
00098: il package `hotpatch`.
00099: Serve per iterare velocemente quando modifichi valori in `config.py`, `materials.py`,
00100: `fog_dynamics.py`, `render_setup.py` o la logica di animazione leggera.
00101: 
00102: Cosa aggiorna senza cancellare la scena:
00103: 
00104: - render/output/compositor;
00105: - world light e area light, con variazione quasi invisibile;
00106: - sfondo `SoftRhythmBackdrop`;
00107: - emissione materiale del centro `HeroRoot`, cosi non dipende solo dal world;
00108: - materiale volumetrico e keyframe del cubo `AtmosphereCube`;
00109: - emissione/materiali/keyframe degli oggetti `PhysicsAccent_*`;
00110: - rimozione dei vecchi oggetti `RhythmPulseLight*` e `RhythmEmitterOrb*`, se presenti.
00111: 
00112: Cosa non fa:
00113: 
00114: - non importa di nuovo l'asset centrale;
00115: - non cancella la scena;
00116: - non ricrea camera, pavimento o struttura principale;
00117: - non lancia render.
00118: 
00119: Usa ancora `main_v61b.py` quando cambi struttura della scena, import asset, geometrie principali,
00120: numero di frame dell'analisi audio o sistemi particellari da ricostruire da zero.
00121: 
00122: Struttura dei patch:
00123: 
00124: - `hotpatch/common.py`: helper condivisi, config e caricamento analisi audio.
00125: - `hotpatch/render_patch.py`: render settings, output e compositor.
00126: - `hotpatch/lighting_patch.py`: world light, area light, backdrop e vecchi oggetti luce.
00127: - `hotpatch/hero_material_patch.py`: mantiene vivo il materiale hero fondendo BSDF originale e luce audio di bordo.
00128: - `hotpatch/fog_patch.py`: cubo volumetrico, nodi fog e animazione fumo/audio.
00129: - `hotpatch/accent_patch.py`: emissione e rotazione degli oggetti `PhysicsAccent_*`.
00130: - `hotpatch/runner.py`: esegue tutte le patch in ordine.
00131: 
00132: Se vuoi provare solo una parte, modifica il file patch relativo e premi di nuovo
00133: `Hot Update Scene` dal pannello.
00134: 
00135: ## Scale Existing Animation
00136: 
00137: Questa sezione modifica i keyframe gia creati.
00138: Usala con attenzione e salva una copia del blend prima di sperimentare.
00139: 
00140: - `Anim hero deform`: moltiplica i keyframe di displace, wave e twist hero.
00141: - `Anim aura`: moltiplica le FCurve del controller aura.
00142: 
00143: Poi premi `Scale Existing FCurves`.
00144: 
00145: ## Workflow consigliato
00146: 
00147: 1. Genera scena con `main_v61b.py`.
00148: 2. Se cambi solo materiali/fog/luci/config, premi `Hot Update Scene`.
00149: 3. Regola il frame 1 con `Apply Live Values`.
00150: 4. Vai su un frame forte del brano, per esempio un beat.
00151: 5. Regola fog/particelle/deformazione.
00152: 6. Premi `Apply + Keyframe`.
00153: 7. Ripeti su 3-5 punti importanti del brano.
00154: 8. Se tutta una categoria e troppo debole o troppo forte, usa `Scale Existing Animation`.
00155: 
00156: ## Render in sequenza immagini
00157: 
00158: `main_v61b.py` ora usa `RENDER_OUTPUT_MODE = "IMAGE_SEQUENCE"`.
00159: Quando premi `Render > Render Animation`, Blender scrive i frame qui:
00160: 
00161: `C:\Users\carmi\blender\renders\spaziotempo_asset_visual_v61b_frames`
00162: 
00163: Vantaggi:
00164: 
00165: - se il render si interrompe, i frame gia completati restano salvati;
00166: - puoi fare post-processing sui singoli frame;
00167: - puoi rimontare il video finale solo alla fine.
00168: 
00169: Dopo aver renderizzato i frame:
00170: 
00171: 1. Apri `encode_image_sequence_v61b.py` nel Text Editor di Blender.
00172: 2. Premi `Alt+P`.
00173: 3. Lo script prepara la sequenza immagini + audio nel Video Sequencer.
00174: 4. Premi `Render > Render Animation` per creare l'MP4 finale.
00175: 
00176: Nota: lo script di encoding non avvia automaticamente il render MP4, a meno che in `config.py`
00177: tu non imposti `ENCODE_SEQUENCE_AUTO_RENDER = True`.
00178: 
00179: ### Sample da meta brano
00180: 
00181: Se renderizzi solo un pezzo centrale, per esempio dal frame `1800`, i file avranno un nome tipo:
00182: 
00183: `spaziotempo_v61b_1800.png`
00184: 
00185: `encode_image_sequence_v61b.py` legge il numero del primo frame e sposta automaticamente l'audio,
00186: cosi il primo frame del sample corrisponde al punto corretto della canzone.
00187: 
00188: In `config.py` il comportamento e controllato da:
00189: 
00190: - `ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER = True`
00191: - `ENCODE_SEQUENCE_SKIP_PLACEHOLDERS = True`
00192: 
00193: Se trova buchi nella sequenza, usa solo il primo blocco continuo di frame.
00194: Questo evita sample fuori sync se mancano frame nel mezzo.
00195: 
00196: ## Post-processing su immagini
00197: 
00198: Il post-processing leggero conviene farlo durante il render o durante l'encoding:
00199: 
00200: - color correction;
00201: - glow moderato;
00202: - vignette leggera;
00203: - sharpen molto leggero;
00204: - piccola distorsione lente.
00205: 
00206: Questi effetti aggiungono poco tempo rispetto al render 3D.
00207: 
00208: Effetti pesanti come denoise AI, upscale AI, optical flow o blur complessi conviene farli dopo,
00209: sulla sequenza gia renderizzata, perche possono allungare molto il tempo totale.
00210: 
00211: ## Oggetti utili da selezionare
00212: 
00213: Il pannello ha pulsanti di selezione:
00214: 
00215: - `Hero`: seleziona centro e controller principali.
00216: - `Fog`: seleziona volume, sfondo e controller.
00217: ## Note di sicurezza
00218: 
00219: - `Apply Live Values` e reversibile con Undo.
00220: - `Scale Existing FCurves` modifica i keyframe: salva prima una copia.
00221: - Il preset JSON viene scritto qui:
00222: 
00223: `scene_tuning_preset.json`
```
