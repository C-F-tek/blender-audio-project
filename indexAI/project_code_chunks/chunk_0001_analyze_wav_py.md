# Project Code Chunk 1/212

- File: `analyze_wav.py`
- Part: `1`
- Lines: `1-245`

## Symbol Map
- Imports: `argparse`, `json`, `sys`, `from pathlib import Path`, `librosa`, `numpy`, `matplotlib.pyplot`
- Functions: `moving_average(x, window)` line 11; `robust_normalize(x, floor_percentile, ceil_percentile)` line 18; `compress_curve(x, gamma)` line 27; `band_envelope_from_stft(S_mag, freqs, fmin, fmax)` line 32; `resample_to_fps(times, values, fps, duration)` line 48; `build_music_context_if_available(json_path, output_dir, run_ollama, ollama_model)` line 54; `build_ai_memory_context_if_available(track_stem, output_dir)` line 92; `main()` line 106

## Content
```py
00001: import argparse
00002: import json
00003: import sys
00004: from pathlib import Path
00005: 
00006: import librosa
00007: import numpy as np
00008: import matplotlib.pyplot as plt
00009: 
00010: 
00011: def moving_average(x: np.ndarray, window: int) -> np.ndarray:
00012:     if window <= 1:
00013:         return x
00014:     kernel = np.ones(window, dtype=np.float64) / window
00015:     return np.convolve(x, kernel, mode="same")
00016: 
00017: 
00018: def robust_normalize(x: np.ndarray, floor_percentile: float = 5.0, ceil_percentile: float = 99.0) -> np.ndarray:
00019:     lo = np.percentile(x, floor_percentile)
00020:     hi = np.percentile(x, ceil_percentile)
00021:     if hi - lo < 1e-12:
00022:         return np.zeros_like(x)
00023:     y = (x - lo) / (hi - lo)
00024:     return np.clip(y, 0.0, 1.0)
00025: 
00026: 
00027: def compress_curve(x: np.ndarray, gamma: float = 0.8) -> np.ndarray:
00028:     x = np.clip(x, 0.0, 1.0)
00029:     return np.power(x, gamma)
00030: 
00031: 
00032: def band_envelope_from_stft(
00033:     S_mag: np.ndarray,
00034:     freqs: np.ndarray,
00035:     fmin: float,
00036:     fmax: float,
00037: ) -> np.ndarray:
00038:     mask = (freqs >= fmin) & (freqs < fmax)
00039:     if not np.any(mask):
00040:         return np.zeros(S_mag.shape[1], dtype=np.float64)
00041: 
00042:     band = S_mag[mask, :]
00043:     # Energia media della banda per frame
00044:     env = np.mean(band, axis=0)
00045:     return env
00046: 
00047: 
00048: def resample_to_fps(times: np.ndarray, values: np.ndarray, fps: float, duration: float):
00049:     target_times = np.arange(0, duration, 1.0 / fps)
00050:     target_values = np.interp(target_times, times, values)
00051:     return target_times, target_values
00052: 
00053: 
00054: def build_music_context_if_available(
00055:     json_path: Path,
00056:     output_dir: Path,
00057:     run_ollama: bool = False,
00058:     ollama_model: str = "qwen2.5-coder:14b",
00059: ) -> None:
00060:     tools_dir = Path(__file__).resolve().parent / "Tools" / "npu"
00061:     if not tools_dir.exists():
00062:         return
00063: 
00064:     track_stem = json_path.stem.replace("_analysis", "")
00065:     track_summary_path = output_dir / f"{track_stem}_track_summary.json"
00066:     compact_json_path = output_dir / f"{track_stem}_music_context.json"
00067:     ai_context_path = output_dir / f"{track_stem}_analysis_ai_context.json"
00068:     blender_keyframes_path = output_dir / f"{track_stem}_analysis_blender_keyframes.json"
00069: 
00070:     if str(tools_dir) not in sys.path:
00071:         sys.path.insert(0, str(tools_dir))
00072: 
00073:     try:
00074:         from build_music_context import build_music_context
00075: 
00076:         manifest = build_music_context(
00077:             analysis_path=json_path,
00078:             track_summary_path=track_summary_path,
00079:             compact_json_path=compact_json_path,
00080:             analysis_ai_context_path=ai_context_path,
00081:             blender_keyframes_path=blender_keyframes_path,
00082:             run_ollama=run_ollama,
00083:             ollama_model=ollama_model,
00084:         )
00085:     except Exception as exc:
00086:         print(f"[WARN] Contesto musicale NPU non aggiornato: {exc}")
00087:         return
00088: 
00089:     print(f"[OK] Contesto musicale NPU aggiornato: {manifest['context_md']}")
00090: 
00091: 
00092: def build_ai_memory_context_if_available(track_stem: str, output_dir: Path) -> dict:
00093:     tools_dir = Path(__file__).resolve().parent / "Tools" / "npu"
00094:     if not tools_dir.exists():
00095:         return {}
00096:     if str(tools_dir) not in sys.path:
00097:         sys.path.insert(0, str(tools_dir))
00098:     try:
00099:         from ai_memory_context import build_ai_memory_context
00100: 
00101:         return build_ai_memory_context(track_stem=track_stem, output_dir=output_dir)
00102:     except Exception:
00103:         return {}
00104: 
00105: 
00106: def main():
00107:     parser = argparse.ArgumentParser(description="Analizza un WAV e genera curve low/mid/high + onsets + beats per Blender.")
00108:     parser.add_argument("input_wav", type=str, help="Percorso del file WAV")
00109:     parser.add_argument("--output-dir", type=str, default="output", help="Cartella output")
00110:     parser.add_argument("--fps", type=float, default=30.0, help="FPS target per Blender")
00111:     parser.add_argument("--n-fft", type=int, default=2048, help="Dimensione finestra FFT")
00112:     parser.add_argument("--hop-length", type=int, default=512, help="Hop length STFT")
00113:     parser.add_argument("--low-max", type=float, default=180.0, help="Fine banda low in Hz")
00114:     parser.add_argument("--mid-max", type=float, default=2000.0, help="Fine banda mid in Hz")
00115:     parser.add_argument("--high-max", type=float, default=8000.0, help="Fine banda high in Hz")
00116:     parser.add_argument("--smooth-low", type=int, default=9, help="Smoothing low")
00117:     parser.add_argument("--smooth-mid", type=int, default=7, help="Smoothing mid")
00118:     parser.add_argument("--smooth-high", type=int, default=5, help="Smoothing high")
00119:     parser.add_argument("--smooth-onset", type=int, default=3, help="Smoothing onset")
00120:     parser.add_argument("--gamma-low", type=float, default=0.8, help="Compressione gamma low")
00121:     parser.add_argument("--gamma-mid", type=float, default=0.85, help="Compressione gamma mid")
00122:     parser.add_argument("--gamma-high", type=float, default=0.9, help="Compressione gamma high")
00123:     parser.add_argument("--skip-music-context", action="store_true", help="Non rigenerare i chunk NPU musicali")
00124:     parser.add_argument("--run-ollama-agent", action="store_true", help="Esegue Ollama sul contesto compatto dopo l'analisi")
00125:     parser.add_argument("--ollama-model", default="qwen2.5-coder:14b", help="Modello Ollama per insight JSON")
00126:     args = parser.parse_args()
00127: 
00128:     input_path = Path(args.input_wav).expanduser().resolve()
00129:     output_dir = Path(args.output_dir).expanduser().resolve()
00130:     output_dir.mkdir(parents=True, exist_ok=True)
00131: 
00132:     if not input_path.exists():
00133:         raise FileNotFoundError(f"File non trovato: {input_path}")
00134: 
00135:     print(f"[INFO] Carico: {input_path}")
00136:     y, sr = librosa.load(str(input_path), sr=None, mono=True)
00137:     duration = len(y) / sr
00138:     print(f"[INFO] Sample rate: {sr} Hz")
00139:     print(f"[INFO] Durata: {duration:.2f} s")
00140: 
00141:     # STFT
00142:     S = librosa.stft(y, n_fft=args.n_fft, hop_length=args.hop_length)
00143:     S_mag = np.abs(S)
00144:     freqs = librosa.fft_frequencies(sr=sr, n_fft=args.n_fft)
00145:     frame_times = librosa.frames_to_time(
00146:         np.arange(S_mag.shape[1]),
00147:         sr=sr,
00148:         hop_length=args.hop_length,
00149:         n_fft=args.n_fft,
00150:     )
00151: 
00152:     # Bande
00153:     low_env = band_envelope_from_stft(S_mag, freqs, 20.0, args.low_max)
00154:     mid_env = band_envelope_from_stft(S_mag, freqs, args.low_max, args.mid_max)
00155:     high_env = band_envelope_from_stft(S_mag, freqs, args.mid_max, args.high_max)
00156: 
00157:     # Normalizzazione + smoothing + compressione
00158:     low_env = compress_curve(robust_normalize(moving_average(low_env, args.smooth_low)), args.gamma_low)
00159:     mid_env = compress_curve(robust_normalize(moving_average(mid_env, args.smooth_mid)), args.gamma_mid)
00160:     high_env = compress_curve(robust_normalize(moving_average(high_env, args.smooth_high)), args.gamma_high)
00161: 
00162:     # Onset envelope
00163:     onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=args.hop_length)
00164:     onset_times = librosa.times_like(onset_env, sr=sr, hop_length=args.hop_length)
00165:     onset_env = robust_normalize(moving_average(onset_env, args.smooth_onset))
00166: 
00167:     # Beat tracking
00168:     tempo_raw, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=args.hop_length)
00169:     tempo = float(np.ravel(tempo_raw)[0]) if np.size(tempo_raw) > 0 else 0.0
00170:     beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=args.hop_length)
00171: 
00172:     # Resampling alle FPS di Blender
00173:     rt_low_t, rt_low = resample_to_fps(frame_times, low_env, args.fps, duration)
00174:     rt_mid_t, rt_mid = resample_to_fps(frame_times, mid_env, args.fps, duration)
00175:     rt_high_t, rt_high = resample_to_fps(frame_times, high_env, args.fps, duration)
00176:     rt_onset_t, rt_onset = resample_to_fps(onset_times, onset_env, args.fps, duration)
00177: 
00178:     # Beat impulse train a FPS
00179:     beat_signal = np.zeros_like(rt_low_t)
00180:     if len(beat_times) > 0:
00181:         beat_indices = np.searchsorted(rt_low_t, beat_times)
00182:         beat_indices = beat_indices[(beat_indices >= 0) & (beat_indices < len(beat_signal))]
00183:         beat_signal[beat_indices] = 1.0
00184: 
00185:     # Output JSON
00186:     track_stem = input_path.stem
00187:     payload = {
00188:         "meta": {
00189:             "input_wav": str(input_path),
00190:             "sample_rate": sr,
00191:             "duration_sec": duration,
00192:             "fps": args.fps,
00193:             "n_fft": args.n_fft,
00194:             "hop_length": args.hop_length,
00195:             "bands_hz": {
00196:                 "low": [20.0, args.low_max],
00197:                 "mid": [args.low_max, args.mid_max],
00198:                 "high": [args.mid_max, args.high_max],
00199:             },
00200:             "estimated_tempo_bpm": float(tempo),
00201:             "ai_memory_context": build_ai_memory_context_if_available(track_stem, output_dir),
00202:         },
00203:         "frames": [
00204:             {
00205:                 "time": float(t),
00206:                 "low": float(rt_low[i]),
00207:                 "mid": float(rt_mid[i]),
00208:                 "high": float(rt_high[i]),
00209:                 "onset": float(rt_onset[i]),
00210:                 "beat": float(beat_signal[i]),
00211:             }
00212:             for i, t in enumerate(rt_low_t)
00213:         ],
00214:         "beats": [float(x) for x in beat_times],
00215:     }
00216: 
00217:     json_path = output_dir / f"{input_path.stem}_analysis.json"
00218:     blender_keyframes_path = output_dir / f"{input_path.stem}_analysis_blender_keyframes.json"
00219:     with open(json_path, "w", encoding="utf-8") as f:
00220:         json.dump(payload, f, indent=2)
00221:     with open(blender_keyframes_path, "w", encoding="utf-8") as f:
00222:         json.dump(payload, f, indent=2)
00223: 
00224:     # Plot diagnostico
00225:     plt.figure(figsize=(14, 8))
00226:     plt.plot(rt_low_t, rt_low, label="low")
00227:     plt.plot(rt_mid_t, rt_mid, label="mid")
00228:     plt.plot(rt_high_t, rt_high, label="high")
00229:     plt.plot(rt_onset_t, rt_onset, label="onset", alpha=0.8)
00230:     for bt in beat_times:
00231:         plt.axvline(bt, linestyle="--", alpha=0.15)
00232:     plt.title(f"Audio analysis: {input_path.name}")
00233:     plt.xlabel("Time (s)")
00234:     plt.ylabel("Normalized value")
00235:     plt.legend()
00236:     plt.tight_layout()
00237: 
00238:     png_path = output_dir / f"{input_path.stem}_analysis.png"
00239:     plt.savefig(png_path, dpi=150)
00240:     plt.close()
00241: 
00242:     print(f"[OK] JSON completo Blender salvato in: {json_path}")
00243:     print(f"[OK] Alias completo keyframe salvato in: {blender_keyframes_path}")
00244:     print(f"[OK] Grafico salvato in: {png_path}")
00245:     print(f"[INFO] BPM stimato: {float(tempo):.2f}")
```
