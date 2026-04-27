import argparse
import json
import sys
from pathlib import Path

import librosa
import numpy as np
import matplotlib.pyplot as plt


def moving_average(x: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return x
    kernel = np.ones(window, dtype=np.float64) / window
    return np.convolve(x, kernel, mode="same")


def robust_normalize(x: np.ndarray, floor_percentile: float = 5.0, ceil_percentile: float = 99.0) -> np.ndarray:
    lo = np.percentile(x, floor_percentile)
    hi = np.percentile(x, ceil_percentile)
    if hi - lo < 1e-12:
        return np.zeros_like(x)
    y = (x - lo) / (hi - lo)
    return np.clip(y, 0.0, 1.0)


def compress_curve(x: np.ndarray, gamma: float = 0.8) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return np.power(x, gamma)


def band_envelope_from_stft(
    S_mag: np.ndarray,
    freqs: np.ndarray,
    fmin: float,
    fmax: float,
) -> np.ndarray:
    mask = (freqs >= fmin) & (freqs < fmax)
    if not np.any(mask):
        return np.zeros(S_mag.shape[1], dtype=np.float64)

    band = S_mag[mask, :]
    # Energia media della banda per frame
    env = np.mean(band, axis=0)
    return env


def resample_to_fps(times: np.ndarray, values: np.ndarray, fps: float, duration: float):
    target_times = np.arange(0, duration, 1.0 / fps)
    target_values = np.interp(target_times, times, values)
    return target_times, target_values


def build_music_context_if_available(
    json_path: Path,
    output_dir: Path,
    run_ollama: bool = False,
    ollama_model: str = "qwen2.5-coder:14b",
) -> None:
    tools_dir = Path(__file__).resolve().parent / "Tools" / "npu"
    if not tools_dir.exists():
        return

    track_stem = json_path.stem.replace("_analysis", "")
    track_summary_path = output_dir / f"{track_stem}_track_summary.json"
    compact_json_path = output_dir / f"{track_stem}_music_context.json"
    ai_context_path = output_dir / f"{track_stem}_analysis_ai_context.json"
    blender_keyframes_path = output_dir / f"{track_stem}_analysis_blender_keyframes.json"

    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))

    try:
        from build_music_context import build_music_context

        manifest = build_music_context(
            analysis_path=json_path,
            track_summary_path=track_summary_path,
            compact_json_path=compact_json_path,
            analysis_ai_context_path=ai_context_path,
            blender_keyframes_path=blender_keyframes_path,
            run_ollama=run_ollama,
            ollama_model=ollama_model,
        )
    except Exception as exc:
        print(f"[WARN] Contesto musicale NPU non aggiornato: {exc}")
        return

    print(f"[OK] Contesto musicale NPU aggiornato: {manifest['context_md']}")


def build_ai_memory_context_if_available(track_stem: str, output_dir: Path) -> dict:
    tools_dir = Path(__file__).resolve().parent / "Tools" / "npu"
    if not tools_dir.exists():
        return {}
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    try:
        from ai_memory_context import build_ai_memory_context

        return build_ai_memory_context(track_stem=track_stem, output_dir=output_dir)
    except Exception:
        return {}


def main():
    parser = argparse.ArgumentParser(description="Analizza un WAV e genera curve low/mid/high + onsets + beats per Blender.")
    parser.add_argument("input_wav", type=str, help="Percorso del file WAV")
    parser.add_argument("--output-dir", type=str, default="output", help="Cartella output")
    parser.add_argument("--fps", type=float, default=30.0, help="FPS target per Blender")
    parser.add_argument("--n-fft", type=int, default=2048, help="Dimensione finestra FFT")
    parser.add_argument("--hop-length", type=int, default=512, help="Hop length STFT")
    parser.add_argument("--low-max", type=float, default=180.0, help="Fine banda low in Hz")
    parser.add_argument("--mid-max", type=float, default=2000.0, help="Fine banda mid in Hz")
    parser.add_argument("--high-max", type=float, default=8000.0, help="Fine banda high in Hz")
    parser.add_argument("--smooth-low", type=int, default=9, help="Smoothing low")
    parser.add_argument("--smooth-mid", type=int, default=7, help="Smoothing mid")
    parser.add_argument("--smooth-high", type=int, default=5, help="Smoothing high")
    parser.add_argument("--smooth-onset", type=int, default=3, help="Smoothing onset")
    parser.add_argument("--gamma-low", type=float, default=0.8, help="Compressione gamma low")
    parser.add_argument("--gamma-mid", type=float, default=0.85, help="Compressione gamma mid")
    parser.add_argument("--gamma-high", type=float, default=0.9, help="Compressione gamma high")
    parser.add_argument("--skip-music-context", action="store_true", help="Non rigenerare i chunk NPU musicali")
    parser.add_argument("--run-ollama-agent", action="store_true", help="Esegue Ollama sul contesto compatto dopo l'analisi")
    parser.add_argument("--ollama-model", default="qwen2.5-coder:14b", help="Modello Ollama per insight JSON")
    args = parser.parse_args()

    input_path = Path(args.input_wav).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"File non trovato: {input_path}")

    print(f"[INFO] Carico: {input_path}")
    y, sr = librosa.load(str(input_path), sr=None, mono=True)
    duration = len(y) / sr
    print(f"[INFO] Sample rate: {sr} Hz")
    print(f"[INFO] Durata: {duration:.2f} s")

    # STFT
    S = librosa.stft(y, n_fft=args.n_fft, hop_length=args.hop_length)
    S_mag = np.abs(S)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=args.n_fft)
    frame_times = librosa.frames_to_time(
        np.arange(S_mag.shape[1]),
        sr=sr,
        hop_length=args.hop_length,
        n_fft=args.n_fft,
    )

    # Bande
    low_env = band_envelope_from_stft(S_mag, freqs, 20.0, args.low_max)
    mid_env = band_envelope_from_stft(S_mag, freqs, args.low_max, args.mid_max)
    high_env = band_envelope_from_stft(S_mag, freqs, args.mid_max, args.high_max)

    # Normalizzazione + smoothing + compressione
    low_env = compress_curve(robust_normalize(moving_average(low_env, args.smooth_low)), args.gamma_low)
    mid_env = compress_curve(robust_normalize(moving_average(mid_env, args.smooth_mid)), args.gamma_mid)
    high_env = compress_curve(robust_normalize(moving_average(high_env, args.smooth_high)), args.gamma_high)

    # Onset envelope
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=args.hop_length)
    onset_times = librosa.times_like(onset_env, sr=sr, hop_length=args.hop_length)
    onset_env = robust_normalize(moving_average(onset_env, args.smooth_onset))

    # Beat tracking
    tempo_raw, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=args.hop_length)
    tempo = float(np.ravel(tempo_raw)[0]) if np.size(tempo_raw) > 0 else 0.0
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=args.hop_length)

    # Resampling alle FPS di Blender
    rt_low_t, rt_low = resample_to_fps(frame_times, low_env, args.fps, duration)
    rt_mid_t, rt_mid = resample_to_fps(frame_times, mid_env, args.fps, duration)
    rt_high_t, rt_high = resample_to_fps(frame_times, high_env, args.fps, duration)
    rt_onset_t, rt_onset = resample_to_fps(onset_times, onset_env, args.fps, duration)

    # Beat impulse train a FPS
    beat_signal = np.zeros_like(rt_low_t)
    if len(beat_times) > 0:
        beat_indices = np.searchsorted(rt_low_t, beat_times)
        beat_indices = beat_indices[(beat_indices >= 0) & (beat_indices < len(beat_signal))]
        beat_signal[beat_indices] = 1.0

    # Output JSON
    track_stem = input_path.stem
    payload = {
        "meta": {
            "input_wav": str(input_path),
            "sample_rate": sr,
            "duration_sec": duration,
            "fps": args.fps,
            "n_fft": args.n_fft,
            "hop_length": args.hop_length,
            "bands_hz": {
                "low": [20.0, args.low_max],
                "mid": [args.low_max, args.mid_max],
                "high": [args.mid_max, args.high_max],
            },
            "estimated_tempo_bpm": float(tempo),
            "ai_memory_context": build_ai_memory_context_if_available(track_stem, output_dir),
        },
        "frames": [
            {
                "time": float(t),
                "low": float(rt_low[i]),
                "mid": float(rt_mid[i]),
                "high": float(rt_high[i]),
                "onset": float(rt_onset[i]),
                "beat": float(beat_signal[i]),
            }
            for i, t in enumerate(rt_low_t)
        ],
        "beats": [float(x) for x in beat_times],
    }

    json_path = output_dir / f"{input_path.stem}_analysis.json"
    blender_keyframes_path = output_dir / f"{input_path.stem}_analysis_blender_keyframes.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    with open(blender_keyframes_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # Plot diagnostico
    plt.figure(figsize=(14, 8))
    plt.plot(rt_low_t, rt_low, label="low")
    plt.plot(rt_mid_t, rt_mid, label="mid")
    plt.plot(rt_high_t, rt_high, label="high")
    plt.plot(rt_onset_t, rt_onset, label="onset", alpha=0.8)
    for bt in beat_times:
        plt.axvline(bt, linestyle="--", alpha=0.15)
    plt.title(f"Audio analysis: {input_path.name}")
    plt.xlabel("Time (s)")
    plt.ylabel("Normalized value")
    plt.legend()
    plt.tight_layout()

    png_path = output_dir / f"{input_path.stem}_analysis.png"
    plt.savefig(png_path, dpi=150)
    plt.close()

    print(f"[OK] JSON completo Blender salvato in: {json_path}")
    print(f"[OK] Alias completo keyframe salvato in: {blender_keyframes_path}")
    print(f"[OK] Grafico salvato in: {png_path}")
    print(f"[INFO] BPM stimato: {float(tempo):.2f}")

    if not args.skip_music_context:
        build_music_context_if_available(
            json_path,
            output_dir,
            run_ollama=args.run_ollama_agent,
            ollama_model=args.ollama_model,
        )


if __name__ == "__main__":
    main()
