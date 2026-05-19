import re
import sys
from pathlib import Path

import bpy


def resolve_script_dir():
    candidates = []

    try:
        text = bpy.context.space_data.text
        if text is not None and text.filepath:
            candidates.append(Path(text.filepath).resolve().parent)
    except Exception:
        pass

    if "__file__" in globals():
        try:
            candidates.append(Path(__file__).resolve().parent)
        except Exception:
            pass

    candidates.append(Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b")

    for candidate in candidates:
        if (candidate / "config.py").exists() and (
            candidate / "encode_image_sequence_v61b.py"
        ).exists():
            return candidate

    return candidates[-1]


SCRIPT_DIR = resolve_script_dir()

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

sys.modules.pop("config", None)

import config as cfg  # noqa: E402

ROOT = getattr(cfg, "ROOT", Path.home() / "blender")
RENDERS_DIR = getattr(cfg, "RENDERS_DIR", ROOT / "renders")

AUDIO_PATH = cfg.AUDIO_PATH
OUTPUT_MP4 = getattr(cfg, "OUTPUT_MP4", RENDERS_DIR / "spaziotempo_asset_visual_v61b.mp4")
OUTPUT_IMAGE_SEQUENCE_DIR = getattr(
    cfg,
    "OUTPUT_IMAGE_SEQUENCE_DIR",
    RENDERS_DIR / "spaziotempo_asset_visual_v61b_frames",
)
OUTPUT_IMAGE_SEQUENCE_PREFIX = getattr(
    cfg,
    "OUTPUT_IMAGE_SEQUENCE_PREFIX",
    "spaziotempo_v61b_",
)
IMAGE_SEQUENCE_FORMAT = getattr(cfg, "IMAGE_SEQUENCE_FORMAT", "PNG")
VIDEO_BITRATE = getattr(cfg, "VIDEO_BITRATE", 12000)
VIDEO_MAXRATE = getattr(cfg, "VIDEO_MAXRATE", 16000)
VIDEO_MINRATE = getattr(cfg, "VIDEO_MINRATE", 0)
VIDEO_BUFFERSIZE = getattr(cfg, "VIDEO_BUFFERSIZE", 1792)
AUDIO_BITRATE = getattr(cfg, "AUDIO_BITRATE", 320)
ENCODE_SEQUENCE_AUTO_RENDER = getattr(cfg, "ENCODE_SEQUENCE_AUTO_RENDER", False)
ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER = getattr(
    cfg,
    "ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER",
    True,
)
ENCODE_SEQUENCE_AUDIO_ZERO_FRAME = int(getattr(cfg, "ENCODE_SEQUENCE_AUDIO_ZERO_FRAME", 1))
ENCODE_SEQUENCE_SKIP_PLACEHOLDERS = getattr(
    cfg,
    "ENCODE_SEQUENCE_SKIP_PLACEHOLDERS",
    True,
)
ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER = getattr(
    cfg,
    "ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER",
    True,
)


def extract_frame_number(path):
    stem = path.stem
    tail = (
        stem[len(OUTPUT_IMAGE_SEQUENCE_PREFIX) :]
        if stem.startswith(OUTPUT_IMAGE_SEQUENCE_PREFIX)
        else stem
    )
    match = re.search(r"(\d+)$", tail)
    return int(match.group(1)) if match else None


def sorted_frame_files():
    ext = ".png" if IMAGE_SEQUENCE_FORMAT.upper() == "PNG" else ""
    pattern = f"{OUTPUT_IMAGE_SEQUENCE_PREFIX}*{ext}" if ext else f"{OUTPUT_IMAGE_SEQUENCE_PREFIX}*"
    files = []

    for path in Path(OUTPUT_IMAGE_SEQUENCE_DIR).glob(pattern):
        if not path.is_file():
            continue
        if ENCODE_SEQUENCE_SKIP_PLACEHOLDERS:
            try:
                if path.stat().st_size <= 0:
                    continue
            except Exception:
                continue
        files.append(path)

    return sorted(
        files,
        key=lambda path: (
            extract_frame_number(path) is None,
            extract_frame_number(path) or 0,
            path.name,
        ),
    )


def contiguous_frame_files(frame_files):
    if not frame_files:
        return [], None

    first_frame = extract_frame_number(frame_files[0])
    if first_frame is None:
        return frame_files, None

    kept = [frame_files[0]]
    expected = first_frame + 1

    for path in frame_files[1:]:
        frame_number = extract_frame_number(path)
        if frame_number != expected:
            print(
                "[WARN] Gap nella sequenza: "
                f"atteso frame {expected}, trovato {frame_number or path.name}. "
                "Uso solo il blocco continuo iniziale per mantenere sync audio."
            )
            break

        kept.append(path)
        expected += 1

    return kept, first_frame


def get_sequence_collection(editor):
    for attr in ("sequences", "strips"):
        collection = getattr(editor, attr, None)
        if collection is not None:
            return collection
    raise AttributeError("SequenceEditor non espone ne 'sequences' ne 'strips'.")


def all_editor_strips(editor):
    for attr in ("sequences_all", "strips_all", "sequences", "strips"):
        collection = getattr(editor, attr, None)
        if collection is None:
            continue
        try:
            return list(collection)
        except Exception:
            pass
    return []


def remove_editor_strip(editor, strip):
    for attr in ("sequences", "strips"):
        collection = getattr(editor, attr, None)
        if collection is None or not hasattr(collection, "remove"):
            continue
        try:
            collection.remove(strip)
            return True
        except Exception:
            pass
    return False


def force_visible_sequencer(scene, editor):
    try:
        bpy.context.window.scene = scene
    except Exception:
        pass

    try:
        bpy.context.workspace.sequencer_scene = scene
    except Exception:
        pass

    if not ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER:
        return

    try:
        area = bpy.context.area
        if area is not None:
            area.type = "SEQUENCE_EDITOR"
            space = area.spaces.active
            for attr, value in [
                ("view_type", "SEQUENCER_PREVIEW"),
                ("display_mode", "SEQUENCER_PREVIEW"),
            ]:
                try:
                    if hasattr(space, attr):
                        setattr(space, attr, value)
                except Exception:
                    pass
    except Exception:
        pass

    try:
        screen = bpy.context.screen
        for area in screen.areas:
            if area.type != "SEQUENCE_EDITOR":
                continue
            region = next((r for r in area.regions if r.type == "WINDOW"), None)
            if region is None:
                continue
            with bpy.context.temp_override(area=area, region=region, scene=scene):
                try:
                    bpy.ops.sequencer.view_all()
                except Exception:
                    pass
    except Exception:
        pass


def clear_sequence_editor(scene):
    editor = scene.sequence_editor
    if editor is None:
        editor = scene.sequence_editor_create()
        return editor

    for strip in all_editor_strips(editor):
        remove_editor_strip(editor, strip)
    return editor


def add_image_sequence(editor, frame_files):
    collection = get_sequence_collection(editor)
    strip = collection.new_image(
        name="SpaziotempoRenderedFrames",
        filepath=str(frame_files[0]),
        channel=1,
        frame_start=1,
    )

    for frame_path in frame_files[1:]:
        try:
            strip.elements.append(frame_path.name)
        except Exception:
            break

    try:
        strip.frame_final_duration = len(frame_files)
    except Exception:
        pass

    return strip


def add_synced_audio(editor, first_frame):
    audio_offset_frames = 0
    audio_start_frame = 1
    if ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER and first_frame is not None:
        audio_offset_frames = max(0, int(first_frame) - ENCODE_SEQUENCE_AUDIO_ZERO_FRAME)
        audio_start_frame = 1 - audio_offset_frames

    collection = get_sequence_collection(editor)
    sound = collection.new_sound(
        name="Feel The Light Audio",
        filepath=str(AUDIO_PATH),
        channel=2,
        frame_start=audio_start_frame,
    )

    if audio_offset_frames > 0:
        print(
            "[INFO] Audio sincronizzato: "
            f"frame originale {first_frame}, frame zero audio {ENCODE_SEQUENCE_AUDIO_ZERO_FRAME}, "
            f"audio strip start {audio_start_frame}."
        )
    else:
        print("[INFO] Audio sample avviato dal frame 1 della canzone.")

    return sound


def configure_video_output(scene, frame_count):
    scene.frame_start = 1
    scene.frame_end = frame_count
    scene.render.filepath = str(OUTPUT_MP4)
    scene.render.use_file_extension = True
    scene.render.use_overwrite = True
    scene.render.use_sequencer = True

    try:
        scene.render.image_settings.media_type = "VIDEO"
    except Exception:
        pass
    try:
        scene.render.image_settings.file_format = "FFMPEG"
        scene.render.image_settings.color_mode = "RGB"
    except Exception:
        pass

    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.audio_codec = "AAC"
    scene.render.ffmpeg.audio_bitrate = AUDIO_BITRATE

    for crf in ("PERC_LOSSLESS", "HIGH"):
        try:
            scene.render.ffmpeg.constant_rate_factor = crf
            break
        except Exception:
            pass
    try:
        scene.render.ffmpeg.ffmpeg_preset = "GOOD"
    except Exception:
        pass
    try:
        scene.render.ffmpeg.video_bitrate = VIDEO_BITRATE
        scene.render.ffmpeg.maxrate = VIDEO_MAXRATE
        scene.render.ffmpeg.minrate = VIDEO_MINRATE
        scene.render.ffmpeg.buffersize = VIDEO_BUFFERSIZE
    except Exception:
        pass


def print_strip_report(scene, editor):
    strips = all_editor_strips(editor)
    print(f"[INFO] Scene corrente: {scene.name}")
    print(f"[INFO] Strip nel Video Sequencer: {len(strips)}")
    for strip in strips:
        try:
            print(
                "[INFO] Strip: "
                f"{strip.name} | type={strip.type} | channel={strip.channel} | "
                f"start={strip.frame_start} | duration={strip.frame_final_duration}"
            )
        except Exception:
            print(f"[INFO] Strip: {getattr(strip, 'name', '<senza nome>')}")


def main():
    print("[INFO] Encode config:")
    print(f"[INFO] Frames dir: {OUTPUT_IMAGE_SEQUENCE_DIR}")
    print(f"[INFO] Prefix:     {OUTPUT_IMAGE_SEQUENCE_PREFIX}")
    print(f"[INFO] Format:     {IMAGE_SEQUENCE_FORMAT}")
    print(f"[INFO] Sync audio: {ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER}")
    print(f"[INFO] Skip empty: {ENCODE_SEQUENCE_SKIP_PLACEHOLDERS}")
    print(f"[INFO] Switch VSE: {ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER}")

    frame_files = sorted_frame_files()
    if not frame_files:
        raise FileNotFoundError(f"Nessun frame trovato in: {OUTPUT_IMAGE_SEQUENCE_DIR}")

    frame_files, first_frame = contiguous_frame_files(frame_files)
    if not frame_files:
        raise FileNotFoundError(f"Nessun frame valido trovato in: {OUTPUT_IMAGE_SEQUENCE_DIR}")

    if not Path(AUDIO_PATH).exists():
        raise FileNotFoundError(f"Audio non trovato: {AUDIO_PATH}")

    scene = bpy.context.scene
    editor = clear_sequence_editor(scene)
    image_strip = add_image_sequence(editor, frame_files)

    try:
        audio_strip = add_synced_audio(editor, first_frame)
    except Exception as exc:
        audio_strip = None
        print(f"[WARN] Audio strip non aggiunta: {exc}")

    configure_video_output(scene, len(frame_files))
    force_visible_sequencer(scene, editor)
    print_strip_report(scene, editor)

    print("=" * 68)
    print("SPAZIOTEMPO IMAGE SEQUENCE ENCODE READY")
    print(f"Frames: {len(frame_files)}")
    print(f"Image strip: {getattr(image_strip, 'name', '<non creata>')}")
    print(f"Audio strip: {getattr(audio_strip, 'name', '<non creata>')}")
    if first_frame is not None:
        print(f"First frame: {first_frame}")
    print(f"Input:  {OUTPUT_IMAGE_SEQUENCE_DIR}")
    print(f"Audio:  {AUDIO_PATH}")
    print(f"MP4:    {OUTPUT_MP4}")
    if ENCODE_SEQUENCE_AUTO_RENDER:
        print("AUTO_RENDER attivo: avvio encoding MP4.")
        bpy.ops.render.render(animation=True)
    else:
        print("Premi Render > Render Animation per creare l'MP4 dalla sequenza.")
    print("=" * 68)


if __name__ == "__main__":
    main()
