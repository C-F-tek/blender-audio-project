# Project Code Chunk 56/212

- File: `Scripting/v61b/SCENE_TUNING_GUIDE.md`
- Part: `2`
- Lines: `214-304`

## Content
```md
00214: Per evitare banding e artefatti nei gradienti della nebbia, usa il pulsante:
00215: 
00216: `Encode MP4 FFmpeg`
00217: 
00218: Questo legge direttamente i PNG renderizzati, sincronizza l'audio anche se il sample parte da un frame centrale, e scrive l'MP4 con H.264 ad alta qualita. Le impostazioni sono in `config.py`:
00219: 
00220: - `ENCODE_USE_EXTERNAL_FFMPEG = True`
00221: - `FFMPEG_CRF = 16` final / `17` preview
00222: - `FFMPEG_PRESET = "slow"`
00223: - `FFMPEG_TUNE = "film"`
00224: 
00225: Se Blender non vede ancora ffmpeg nel PATH, lo script prova anche a cercarlo in Desktop/Downloads.
00226: 
00227: ### Sample da meta brano
00228: 
00229: Se renderizzi solo un pezzo centrale, per esempio dal frame `1800`, i file avranno un nome tipo:
00230: 
00231: `spaziotempo_v61b_1800.png`
00232: 
00233: `encode_image_sequence_v61b.py` legge il numero del primo frame e sposta automaticamente l'audio,
00234: cosi il primo frame del sample corrisponde al punto corretto della canzone.
00235: 
00236: In `config.py` il comportamento e controllato da:
00237: 
00238: - `ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER = True`
00239: - `ENCODE_SEQUENCE_SKIP_PLACEHOLDERS = True`
00240: 
00241: Se trova buchi nella sequenza, usa solo il primo blocco continuo di frame.
00242: Questo evita sample fuori sync se mancano frame nel mezzo.
00243: 
00244: ## Post-processing su immagini
00245: 
00246: Il post-processing leggero conviene farlo durante il render o durante l'encoding:
00247: 
00248: - color correction;
00249: - glow moderato;
00250: - vignette leggera;
00251: - sharpen molto leggero;
00252: - piccola distorsione lente.
00253: 
00254: Questi effetti aggiungono poco tempo rispetto al render 3D.
00255: 
00256: Effetti pesanti come denoise AI, upscale AI, optical flow o blur complessi conviene farli dopo,
00257: sulla sequenza gia renderizzata, perche possono allungare molto il tempo totale.
00258: 
00259: ## Nebbia leggera
00260: 
00261: La nebbia volumetrica piena e disattivata di default con:
00262: 
00263: `FOG_VOLUME_ENABLED = False`
00264: 
00265: Al suo posto vengono creati `FogFilament_*`: banchi sottili e trasparenti animati a ritmo.
00266: Sono piu leggeri del volume Eevee e riducono gli artefatti quadrati sullo sfondo.
00267: Se vuoi riattivare il volume vero, porta `FOG_VOLUME_ENABLED = True`, ma aspettati render piu pesanti.
00268: 
00269: ## Oggetti utili da selezionare
00270: 
00271: Il pannello ha pulsanti di selezione:
00272: 
00273: - `Hero`: seleziona centro e controller principali.
00274: - `Fog`: seleziona volume, sfondo e controller.
00275: 
00276: ## Struttura progetto
00277: 
00278: Il progetto ora ha un layer system in `spaziotempo/`:
00279: 
00280: - `spaziotempo/core/registry.py`: nomi canonici, layer e feature catalog.
00281: - `spaziotempo/core/collections.py`: crea le collection `ST_*` e classifica gli oggetti.
00282: - `PROJECT_STRUCTURE.md`: briefing tecnico della struttura.
00283: 
00284: Le collection principali sono:
00285: 
00286: - `ST_00_Core`
00287: - `ST_05_World_Set`
00288: - `ST_10_Hero`
00289: - `ST_20_Atmosphere`
00290: - `ST_30_Atomic_Physics`
00291: - `ST_40_Lights`
00292: - `ST_50_Render_IO`
00293: - `ST_60_Water` vuota e riservata per il futuro
00294: - `ST_90_Technical`
00295: 
00296: `main_v61b.py` e `Hot Update All` aggiornano automaticamente questa classificazione.
00297: Gli oggetti storici non vengono rinominati, quindi gli script continuano a funzionare.
00298: ## Note di sicurezza
00299: 
00300: - `Apply Live Values` e reversibile con Undo.
00301: - `Scale Existing FCurves` modifica i keyframe: salva prima una copia.
00302: - Il preset JSON viene scritto qui:
00303: 
00304: `scene_tuning_preset.json`
```
