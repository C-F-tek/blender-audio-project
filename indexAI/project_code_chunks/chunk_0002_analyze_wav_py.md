# Project Code Chunk 2/212

- File: `analyze_wav.py`
- Part: `2`
- Lines: `246-257`

## Symbol Map
- Imports: `argparse`, `json`, `sys`, `from pathlib import Path`, `librosa`, `numpy`, `matplotlib.pyplot`
- Functions: `moving_average(x, window)` line 11; `robust_normalize(x, floor_percentile, ceil_percentile)` line 18; `compress_curve(x, gamma)` line 27; `band_envelope_from_stft(S_mag, freqs, fmin, fmax)` line 32; `resample_to_fps(times, values, fps, duration)` line 48; `build_music_context_if_available(json_path, output_dir, run_ollama, ollama_model)` line 54; `build_ai_memory_context_if_available(track_stem, output_dir)` line 92; `main()` line 106

## Content
```py
00246: 
00247:     if not args.skip_music_context:
00248:         build_music_context_if_available(
00249:             json_path,
00250:             output_dir,
00251:             run_ollama=args.run_ollama_agent,
00252:             ollama_model=args.ollama_model,
00253:         )
00254: 
00255: 
00256: if __name__ == "__main__":
00257:     main()
```
