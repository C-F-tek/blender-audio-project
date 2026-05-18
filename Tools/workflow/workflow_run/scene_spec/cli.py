"""CLI for scene-spec normalization."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .constants import DEFAULT_INPUT_JSON, DEFAULT_OUTPUT_JSON
from .normalizer import SceneSpecNormalizer


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Scene brief not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"Scene brief must be a JSON object: {path}")
    return data


def maybe_update_music_context(repo_root: Path, scene_files: list[Path]) -> None:
    tools_dir = repo_root / "Tools" / "npu"
    if not tools_dir.exists():
        return
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    try:
        from build_music_context import build_music_context

        manifest = build_music_context(scene_files=scene_files)
    except Exception as exc:
        print(f"[WARN] NPU music context not updated: {exc}")
        return
    print(f"[OK] NPU music context updated: {manifest['context_md']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize IA-Carmine scene spec JSON.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--input", default=DEFAULT_INPUT_JSON)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--skip-music-context", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    input_json = resolve_path(repo_root, args.input)
    output_json = resolve_path(repo_root, args.output)

    normalized = SceneSpecNormalizer().normalize(load_json(input_json))
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(normalized, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"[OK] Normalized scene spec saved in: {output_json}")
    print(json.dumps(normalized, indent=2, ensure_ascii=False))

    if not args.skip_music_context:
        maybe_update_music_context(
            repo_root,
            [
                input_json,
                output_json,
                repo_root / "scene_spec_album_driven_raw.txt",
                repo_root / "scene_spec_from_npu.json",
                repo_root / "scene_spec_from_npu_raw.txt",
            ],
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
