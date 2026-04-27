# Ready To Jazz WOW YouTube Profiles

Cartella consigliata su Windows:

```text
C:\Users\carmi\blender\blender-audio-project\Scripting\ready_to_jazz_wow_youtube_profiles
```

File principale da aprire in Blender 5.1 e lanciare con `Alt+P`:

```text
main_ready_to_jazz_wow_youtube.py
```

## Profilo render

Nel file principale cambia la variabile:

```python
FINAL_YOUTUBE = "2K_INTERMEDIATE"
```

Profili disponibili:

- `HD_PREVIEW`: 1920x1080, 50%, veloce, motion blur off.
- `HD_INTERMEDIATE`: 1920x1080, 100%, qualità media, motion blur off.
- `HD_FINAL`: 1920x1080, 100%, qualità finale, motion blur on.
- `2K_PREVIEW`: 2560x1440, 50%, veloce, motion blur off.
- `2K_INTERMEDIATE`: 2560x1440, 100%, qualità media, motion blur off.
- `2K_FINAL`: 2560x1440, 100%, qualità finale, motion blur on.

## Output

La cartella base è:

```text
C:\Users\carmi\blender\renders
```

Lo script crea sottocartelle per profilo, per esempio:

```text
C:\Users\carmi\blender\renders\ready_to_jazz_wow_elastic_2k_intermediate\frames
```

## Color / video safe

Lo script imposta in modo esplicito:

- output PNG sequence;
- sRGB display;
- AgX con fallback Filmic/Standard;
- gamma 1.0;
- neri non assoluti nello sfondo;
- bloom controllato;
- audio nel Video Sequencer e speaker in scena se trova il WAV.

## Note

Il file è standalone: non richiede import esterni per generare la scena.
`render_profiles_reference.py` è solo una copia di riferimento dei nomi profilo.


## Encoding da frame non 1 con audio sincronizzato

`encode_final_youtube.py` ora rileva automaticamente il primo frame presente nella cartella `frames`.
Se il render parte da un frame diverso da 1, calcola l'offset audio con:

```text
offset_secondi = (first_frame - 1) / FPS
```

e passa l'audio a ffmpeg con `-ss <offset_secondi>`, così il WAV parte dal punto corretto della traccia.

Esempi:
- frame 1 a 30 fps -> audio da 0.000s
- frame 301 a 30 fps -> audio da 10.000s
- frame 901 a 30 fps -> audio da 30.000s


## Revisione look-dev atmosferica
- materiali completamente ricostruiti con node tree dedicati (non solo Principled di default);
- core, satelliti, orbite, floor e dome con materiali piu morbidi e meno "promo Blender";
- asset ball centrale disabilitato di default (`USE_PRIMARY_BALL_ASSET = False`) per usare i nuovi core shader-based;
- aggiunti due volumi di nebbia (`fog_main`, `fog_layer`) con densita animata a ritmo;
- ridotta l'intensita dei flash su core, satelliti e wow-effects;
- encode finale invariato con sync audio/frame automatico.
