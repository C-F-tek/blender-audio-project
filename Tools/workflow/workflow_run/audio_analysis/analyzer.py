"""Object-oriented WAV analysis for Blender keyframe artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import librosa
import matplotlib.pyplot as plt
import numpy as np

from .context_bridge import MusicContextBridge
from .defaults import DEFAULT_OLLAMA_MODEL
from .signals import (
    band_envelope_from_stft,
    compress_curve,
    moving_average,
    resample_to_fps,
    robust_normalize,
)


@dataclass(frozen=True)
class AudioAnalysisOptions:
    input_wav: Path
    output_dir: Path
    repo_root: Path
    fps: float = 30.0
    n_fft: int = 2048
    hop_length: int = 512
    low_max: float = 180.0
    mid_max: float = 2000.0
    high_max: float = 8000.0
    smooth_low: int = 9
    smooth_mid: int = 7
    smooth_high: int = 5
    smooth_onset: int = 3
    gamma_low: float = 0.8
    gamma_mid: float = 0.85
    gamma_high: float = 0.9
    skip_music_context: bool = False
    run_ollama_agent: bool = False
    ollama_model: str = DEFAULT_OLLAMA_MODEL


@dataclass(frozen=True)
class AudioAnalysisResult:
    analysis_json: Path
    blender_keyframes_json: Path
    plot_png: Path
    tempo_bpm: float
    duration_sec: float
    frame_count: int


class AudioAnalyzer:
    """Build low/mid/high/onset/beat curves from a WAV file."""

    def __init__(self, context_bridge: MusicContextBridge | None = None) -> None:
        self.context_bridge = context_bridge

    def analyze(self, options: AudioAnalysisOptions) -> AudioAnalysisResult:
        input_path = options.input_wav.expanduser().resolve()
        output_dir = options.output_dir.expanduser().resolve()
        repo_root = options.repo_root.expanduser().resolve()
        bridge = self.context_bridge or MusicContextBridge(repo_root)

        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {input_path}")

        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"[INFO] Loading: {input_path}")
        y, sr = librosa.load(str(input_path), sr=None, mono=True)
        duration = len(y) / sr
        print(f"[INFO] Sample rate: {sr} Hz")
        print(f"[INFO] Duration: {duration:.2f} s")

        magnitude = np.abs(librosa.stft(y, n_fft=options.n_fft, hop_length=options.hop_length))
        freqs = librosa.fft_frequencies(sr=sr, n_fft=options.n_fft)
        frame_times = librosa.frames_to_time(
            np.arange(magnitude.shape[1]),
            sr=sr,
            hop_length=options.hop_length,
            n_fft=options.n_fft,
        )

        low_env = self._band_curve(
            magnitude,
            freqs,
            20.0,
            options.low_max,
            options.smooth_low,
            options.gamma_low,
        )
        mid_env = self._band_curve(
            magnitude,
            freqs,
            options.low_max,
            options.mid_max,
            options.smooth_mid,
            options.gamma_mid,
        )
        high_env = self._band_curve(
            magnitude,
            freqs,
            options.mid_max,
            options.high_max,
            options.smooth_high,
            options.gamma_high,
        )

        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=options.hop_length)
        onset_times = librosa.times_like(onset_env, sr=sr, hop_length=options.hop_length)
        onset_env = robust_normalize(moving_average(onset_env, options.smooth_onset))

        tempo_raw, beat_frames = librosa.beat.beat_track(
            y=y,
            sr=sr,
            hop_length=options.hop_length,
        )
        tempo = float(np.ravel(tempo_raw)[0]) if np.size(tempo_raw) > 0 else 0.0
        beat_times = librosa.frames_to_time(
            beat_frames,
            sr=sr,
            hop_length=options.hop_length,
        )

        rt_low_t, rt_low = resample_to_fps(frame_times, low_env, options.fps, duration)
        _, rt_mid = resample_to_fps(frame_times, mid_env, options.fps, duration)
        _, rt_high = resample_to_fps(frame_times, high_env, options.fps, duration)
        rt_onset_t, rt_onset = resample_to_fps(
            onset_times,
            onset_env,
            options.fps,
            duration,
        )
        beat_signal = self._beat_signal(rt_low_t, beat_times)

        track_stem = input_path.stem
        payload = self._payload(
            options=options,
            input_path=input_path,
            sample_rate=sr,
            duration=duration,
            tempo=tempo,
            track_stem=track_stem,
            output_dir=output_dir,
            bridge=bridge,
            times=rt_low_t,
            low=rt_low,
            mid=rt_mid,
            high=rt_high,
            onset=rt_onset,
            beat=beat_signal,
            beat_times=beat_times,
        )

        analysis_json = output_dir / f"{track_stem}_analysis.json"
        blender_keyframes_json = output_dir / f"{track_stem}_analysis_blender_keyframes.json"
        analysis_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        blender_keyframes_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        plot_png = output_dir / f"{track_stem}_analysis.png"
        self._write_plot(
            plot_png,
            input_path.name,
            rt_low_t,
            rt_low,
            rt_mid,
            rt_high,
            rt_onset_t,
            rt_onset,
            beat_times,
        )

        print(f"[OK] Blender JSON saved in: {analysis_json}")
        print(f"[OK] Keyframe alias saved in: {blender_keyframes_json}")
        print(f"[OK] Plot saved in: {plot_png}")
        print(f"[INFO] Estimated BPM: {tempo:.2f}")

        if not options.skip_music_context:
            bridge.build_music_context(
                analysis_path=analysis_json,
                track_summary_path=output_dir / f"{track_stem}_track_summary.json",
                compact_json_path=output_dir / f"{track_stem}_music_context.json",
                analysis_ai_context_path=output_dir / f"{track_stem}_analysis_ai_context.json",
                blender_keyframes_path=blender_keyframes_json,
                run_ollama=options.run_ollama_agent,
                ollama_model=options.ollama_model,
            )

        return AudioAnalysisResult(
            analysis_json=analysis_json,
            blender_keyframes_json=blender_keyframes_json,
            plot_png=plot_png,
            tempo_bpm=tempo,
            duration_sec=duration,
            frame_count=len(rt_low_t),
        )

    @staticmethod
    def _band_curve(
        magnitude: np.ndarray,
        freqs: np.ndarray,
        fmin: float,
        fmax: float,
        smooth_window: int,
        gamma: float,
    ) -> np.ndarray:
        env = band_envelope_from_stft(magnitude, freqs, fmin, fmax)
        return compress_curve(robust_normalize(moving_average(env, smooth_window)), gamma)

    @staticmethod
    def _beat_signal(times: np.ndarray, beat_times: np.ndarray) -> np.ndarray:
        signal = np.zeros_like(times)
        if len(beat_times) == 0:
            return signal
        beat_indices = np.searchsorted(times, beat_times)
        beat_indices = beat_indices[(beat_indices >= 0) & (beat_indices < len(signal))]
        signal[beat_indices] = 1.0
        return signal

    @staticmethod
    def _payload(
        *,
        options: AudioAnalysisOptions,
        input_path: Path,
        sample_rate: int,
        duration: float,
        tempo: float,
        track_stem: str,
        output_dir: Path,
        bridge: MusicContextBridge,
        times: np.ndarray,
        low: np.ndarray,
        mid: np.ndarray,
        high: np.ndarray,
        onset: np.ndarray,
        beat: np.ndarray,
        beat_times: np.ndarray,
    ) -> dict:
        return {
            "meta": {
                "input_wav": str(input_path),
                "sample_rate": sample_rate,
                "duration_sec": duration,
                "fps": options.fps,
                "n_fft": options.n_fft,
                "hop_length": options.hop_length,
                "bands_hz": {
                    "low": [20.0, options.low_max],
                    "mid": [options.low_max, options.mid_max],
                    "high": [options.mid_max, options.high_max],
                },
                "estimated_tempo_bpm": float(tempo),
                "ai_memory_context": bridge.build_ai_memory_context(track_stem, output_dir),
            },
            "frames": [
                {
                    "time": float(t),
                    "low": float(low[i]),
                    "mid": float(mid[i]),
                    "high": float(high[i]),
                    "onset": float(onset[i]),
                    "beat": float(beat[i]),
                }
                for i, t in enumerate(times)
            ],
            "beats": [float(item) for item in beat_times],
        }

    @staticmethod
    def _write_plot(
        path: Path,
        input_name: str,
        low_times: np.ndarray,
        low: np.ndarray,
        mid: np.ndarray,
        high: np.ndarray,
        onset_times: np.ndarray,
        onset: np.ndarray,
        beat_times: np.ndarray,
    ) -> None:
        plt.figure(figsize=(14, 8))
        plt.plot(low_times, low, label="low")
        plt.plot(low_times, mid, label="mid")
        plt.plot(low_times, high, label="high")
        plt.plot(onset_times, onset, label="onset", alpha=0.8)
        for beat_time in beat_times:
            plt.axvline(beat_time, linestyle="--", alpha=0.15)
        plt.title(f"Audio analysis: {input_name}")
        plt.xlabel("Time (s)")
        plt.ylabel("Normalized value")
        plt.legend()
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()
