"""CLI entrypoint for audio analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

from .defaults import DEFAULT_OLLAMA_MODEL


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a WAV file and generate Blender audio-curve artifacts."
    )
    parser.add_argument("input_wav", type=str, help="Input WAV path")
    parser.add_argument("--repo-root", type=str, default=".", help="Repository root")
    parser.add_argument("--output-dir", type=str, default="output", help="Output directory")
    parser.add_argument("--fps", type=float, default=30.0, help="Target Blender FPS")
    parser.add_argument("--n-fft", type=int, default=2048, help="FFT window size")
    parser.add_argument("--hop-length", type=int, default=512, help="STFT hop length")
    parser.add_argument("--low-max", type=float, default=180.0, help="Low band end in Hz")
    parser.add_argument("--mid-max", type=float, default=2000.0, help="Mid band end in Hz")
    parser.add_argument("--high-max", type=float, default=8000.0, help="High band end in Hz")
    parser.add_argument("--smooth-low", type=int, default=9, help="Low-band smoothing")
    parser.add_argument("--smooth-mid", type=int, default=7, help="Mid-band smoothing")
    parser.add_argument("--smooth-high", type=int, default=5, help="High-band smoothing")
    parser.add_argument("--smooth-onset", type=int, default=3, help="Onset smoothing")
    parser.add_argument("--gamma-low", type=float, default=0.8, help="Low-band gamma")
    parser.add_argument("--gamma-mid", type=float, default=0.85, help="Mid-band gamma")
    parser.add_argument("--gamma-high", type=float, default=0.9, help="High-band gamma")
    parser.add_argument("--skip-music-context", action="store_true")
    parser.add_argument("--run-ollama-agent", action="store_true")
    parser.add_argument("--ollama-model", default=DEFAULT_OLLAMA_MODEL)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    from .analyzer import AudioAnalysisOptions, AudioAnalyzer

    repo_root = Path(args.repo_root).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser()
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    options = AudioAnalysisOptions(
        input_wav=Path(args.input_wav),
        output_dir=output_dir,
        repo_root=repo_root,
        fps=args.fps,
        n_fft=args.n_fft,
        hop_length=args.hop_length,
        low_max=args.low_max,
        mid_max=args.mid_max,
        high_max=args.high_max,
        smooth_low=args.smooth_low,
        smooth_mid=args.smooth_mid,
        smooth_high=args.smooth_high,
        smooth_onset=args.smooth_onset,
        gamma_low=args.gamma_low,
        gamma_mid=args.gamma_mid,
        gamma_high=args.gamma_high,
        skip_music_context=args.skip_music_context,
        run_ollama_agent=args.run_ollama_agent,
        ollama_model=args.ollama_model,
    )
    AudioAnalyzer().analyze(options)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
