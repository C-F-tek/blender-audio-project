import json
from pathlib import Path


def load_json(path):
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def ensure_file_exists(path, label="File"):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{label} non trovato: {path}")
    return path


def ensure_inputs_exist(analysis_path, audio_path):
    analysis_file = ensure_file_exists(analysis_path, "Analysis JSON")
    audio_file = ensure_file_exists(audio_path, "Audio")
    return analysis_file, audio_file


def clear_sequencer(scene):
    seq = scene.sequence_editor
    if not seq:
        return

    strips = getattr(seq, "strips", None)
    if strips is not None:
        for strip in list(strips):
            try:
                strips.remove(strip)
            except Exception:
                pass
        return

    sequences_all = getattr(seq, "sequences_all", None)
    sequences = getattr(seq, "sequences", None)
    if sequences_all is not None and sequences is not None:
        for strip in list(sequences_all):
            try:
                sequences.remove(strip)
            except Exception:
                pass


def add_audio_strip(scene, audio_path, clear_existing=True, sync_audio=True):
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio non trovato: {audio_path}")

    seq = scene.sequence_editor
    if seq is None:
        seq = scene.sequence_editor_create()

    if clear_existing:
        clear_sequencer(scene)

    strip_name = audio_path.stem

    if hasattr(seq, "strips") and hasattr(seq.strips, "new_sound"):
        sound_strip = seq.strips.new_sound(
            name=strip_name,
            filepath=str(audio_path),
            channel=1,
            frame_start=1,
        )
    elif hasattr(seq, "sequences") and hasattr(seq.sequences, "new_sound"):
        sound_strip = seq.sequences.new_sound(strip_name, str(audio_path), 1, 1)
    else:
        raise RuntimeError("API Sequencer non compatibile per creare una sound strip.")

    if sync_audio:
        try:
            scene.sync_mode = "AUDIO_SYNC"
        except Exception:
            pass

    return sound_strip
