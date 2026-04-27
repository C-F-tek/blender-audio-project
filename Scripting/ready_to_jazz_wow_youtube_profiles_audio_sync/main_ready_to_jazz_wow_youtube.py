# -*- coding: utf-8 -*-
r"""
Ready To Jazz - Luca Vera | Dual Gravity Audio-Reactive Scene
Standalone Blender Python script.

Cosa genera:
- due oggetti centrali / fuochi gravitazionali in controfase;
- corpi satellite che orbitano attorno ai due centri e attorno al baricentro;
- keyframe sincronizzati ai dati low/mid/high/onset/beat del JSON audio;
- materiali emission, anelli orbitali, aura deformata, camera e luci audio-reactive.

Esecuzione consigliata:
1. Copia questo file in:
   C:\Users\carmi\blender\blender-audio-project\indexAI\scene_scripts\
2. Aprilo nel Text Editor di Blender e lancialo con Alt+P.

Lo script cerca automaticamente:
- Ready To Jazz-Luca Vera_Master_analysis_blender_keyframes.json
- spaziotempo_asset_inventory.json
- Ready To Jazz-Luca Vera_Master.wav
nella cartella output/audio del progetto o accanto allo script.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Iterable

import bpy
from mathutils import Vector


# =============================================================================
# CONFIGURAZIONE PRINCIPALE
# =============================================================================

TRACK_STEM = "Ready To Jazz-Luca Vera_Master"
KEYFRAME_JSON_NAME = f"{TRACK_STEM}_analysis_blender_keyframes.json"
ASSET_INVENTORY_JSON_NAME = "spaziotempo_asset_inventory.json"
AUDIO_FILE_NAME = f"{TRACK_STEM}.wav"
AUDIO_PATH_OVERRIDE: str | None = None  # es.: r"C:\Users\carmi\blender\audio\Ready To Jazz-Luca Vera_Master.wav"

# Sistema dei due core centrali: piu compatti, piu vicini e con dinamica elastica.
CORE_BASE_HALF_DISTANCE = 1.15
CORE_AUDIO_EXPAND_DISTANCE = 0.22
CORE_LOW_PULL_DISTANCE = 0.56
CORE_VERTICAL_BASE = 0.88
CORE_CONTACT_GAP = 0.028
CORE_ELASTIC_SQUASH_MAX = 0.24
CORE_ELASTIC_BULGE_FACTOR = 0.72

# Riduzione dimensioni: i core e i corpi orbitanti risultano piu eleganti e meno invadenti.
CORE_IMPORTED_TARGET_SIZE = 1.08
CORE_PROCEDURAL_RADIUS = 0.50
CORE_AURA_RADIUS = 0.72
INNER_SATELLITE_BASE_SIZE = 0.045
INNER_SATELLITE_SIZE_STEP = 0.010
INNER_SATELLITE_ANIM_SCALE_A = 0.60
INNER_SATELLITE_ANIM_SCALE_B = 0.58
OUTER_SATELLITE_BASE_SIZE = 0.028
OUTER_SATELLITE_SIZE_STEP = 0.007
OUTER_SATELLITE_ANIM_SCALE = 0.52

# 1 = keyframe su ogni frame audio disponibile; 2/3/4 = piu leggero.
# I beat e gli onset forti vengono sempre mantenuti anche se lo stride e maggiore.
MAIN_KEYFRAME_STRIDE = 2
SATELLITE_KEYFRAME_STRIDE = 4
ONSET_KEY_THRESHOLD = 0.62

# Numero dei corpi orbitanti. Aumentare richiede piu keyframe e piu tempo di build.
INNER_BODIES_PER_CORE = 7
OUTER_SHARED_BODIES = 10

# Asset ball: se true prova a importare C:\Users\carmi\blender\assets\ball\source\ball.fbx.
# Se non esiste, usa sfere procedurali.
USE_PRIMARY_BALL_ASSET = False

# Effetti avanzati "WOW".
ENABLE_WOW_ADVANCED_EFFECTS = True
ENABLE_WOW_COMPOSITOR = True
ENABLE_WOW_SHOCKWAVES = True
ENABLE_WOW_GRAVITY_LENS = True
ENABLE_WOW_PLASMA_ARCS = True
ENABLE_WOW_LIGHT_BEAMS = True
ENABLE_WOW_STAR_DUST = True
WOW_KEYFRAME_STRIDE = 4
WOW_SHOCKWAVE_COUNT = 10
WOW_PLASMA_ARC_COUNT = 7
WOW_DUST_COUNT = 110
WOW_SEED = 20260427

# Tuning look-dev: meno flash, piu atmosfera, piu materia.
FLASH_REDUCTION_FACTOR = 0.52
FOG_MAIN_DENSITY = 0.017
FOG_LAYER_DENSITY = 0.028
FOG_PULSE_AMOUNT = 0.012
ATMOS_EMISSION_SOFTNESS = 0.65

# Impostazioni render e output per YouTube/social.
RENDER_ENGINE = "BLENDER_EEVEE_NEXT"  # fallback automatico su BLENDER_EEVEE se non disponibile
FPS_FALLBACK = 30.0

# Cambia solo questa variabile per scegliere profilo render/output.
# Profili disponibili: HD_PREVIEW, HD_INTERMEDIATE, HD_FINAL, 2K_PREVIEW, 2K_INTERMEDIATE, 2K_FINAL.
FINAL_YOUTUBE = "2K_INTERMEDIATE"

OUTPUT_BASE_DIR = Path(r"C:\Users\carmi\blender\renders")
OUTPUT_PROJECT_SLUG = "ready_to_jazz_wow_elastic"
OUTPUT_FRAME_PREFIX = "ready_to_jazz_wow_"

YOUTUBE_RENDER_PROFILES = {
    "HD_PREVIEW": {
        "width": 1920, "height": 1080, "percentage": 50,
        "output_mode": "IMAGE_SEQUENCE", "motion_blur": False,
        "eevee_samples": 32, "viewport_samples": 16, "volumetric_samples": 16, "volumetric_tile_size": "8",
        "bloom_intensity": 0.012, "bloom_threshold": 1.28,
        "exposure": -0.08, "gamma": 1.0, "look": "Base Contrast",
        "image_depth": "8", "png_compression": 30,
        "video_bitrate": 12000, "video_maxrate": 16000, "audio_bitrate": 320,
    },
    "HD_INTERMEDIATE": {
        "width": 1920, "height": 1080, "percentage": 100,
        "output_mode": "IMAGE_SEQUENCE", "motion_blur": False,
        "eevee_samples": 48, "viewport_samples": 24, "volumetric_samples": 24, "volumetric_tile_size": "8",
        "bloom_intensity": 0.016, "bloom_threshold": 1.22,
        "exposure": -0.07, "gamma": 1.0, "look": "Medium High Contrast",
        "image_depth": "16", "png_compression": 20,
        "video_bitrate": 18000, "video_maxrate": 22000, "audio_bitrate": 320,
    },
    "HD_FINAL": {
        "width": 1920, "height": 1080, "percentage": 100,
        "output_mode": "IMAGE_SEQUENCE", "motion_blur": True,
        "eevee_samples": 80, "viewport_samples": 32, "volumetric_samples": 48, "volumetric_tile_size": "4",
        "bloom_intensity": 0.020, "bloom_threshold": 1.18,
        "exposure": -0.06, "gamma": 1.0, "look": "Medium High Contrast",
        "image_depth": "16", "png_compression": 15,
        "video_bitrate": 20000, "video_maxrate": 24000, "audio_bitrate": 320,
    },
    "2K_PREVIEW": {
        "width": 2560, "height": 1440, "percentage": 50,
        "output_mode": "IMAGE_SEQUENCE", "motion_blur": False,
        "eevee_samples": 36, "viewport_samples": 16, "volumetric_samples": 16, "volumetric_tile_size": "8",
        "bloom_intensity": 0.012, "bloom_threshold": 1.28,
        "exposure": -0.08, "gamma": 1.0, "look": "Base Contrast",
        "image_depth": "8", "png_compression": 30,
        "video_bitrate": 16000, "video_maxrate": 20000, "audio_bitrate": 320,
    },
    "2K_INTERMEDIATE": {
        "width": 2560, "height": 1440, "percentage": 100,
        "output_mode": "IMAGE_SEQUENCE", "motion_blur": False,
        "eevee_samples": 56, "viewport_samples": 24, "volumetric_samples": 32, "volumetric_tile_size": "8",
        "bloom_intensity": 0.017, "bloom_threshold": 1.22,
        "exposure": -0.07, "gamma": 1.0, "look": "Medium High Contrast",
        "image_depth": "16", "png_compression": 18,
        "video_bitrate": 24000, "video_maxrate": 30000, "audio_bitrate": 320,
    },
    "2K_FINAL": {
        "width": 2560, "height": 1440, "percentage": 100,
        "output_mode": "IMAGE_SEQUENCE", "motion_blur": True,
        "eevee_samples": 96, "viewport_samples": 40, "volumetric_samples": 64, "volumetric_tile_size": "4",
        "bloom_intensity": 0.022, "bloom_threshold": 1.16,
        "exposure": -0.055, "gamma": 1.0, "look": "Medium High Contrast",
        "image_depth": "16", "png_compression": 12,
        "video_bitrate": 28000, "video_maxrate": 34000, "audio_bitrate": 384,
    },
}


# =============================================================================
# UTILITY
# =============================================================================

def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, float(value)))


def smoothstep(x: float) -> float:
    x = clamp(x)
    return x * x * (3.0 - 2.0 * x)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * clamp(t)


def script_dir() -> Path:
    if "__file__" in globals():
        try:
            return Path(__file__).resolve().parent
        except Exception:
            pass
    blend_base = bpy.path.abspath("//")
    if blend_base:
        return Path(blend_base).resolve()
    return Path.cwd().resolve()


def candidate_project_dirs() -> list[Path]:
    here = script_dir()
    return [
        here,
        here.parent,
        here.parent.parent,
        here / "output",
        here.parent / "output",
        here.parent.parent / "output",
        Path(r"C:\Users\carmi\blender\blender-audio-project\output"),
        Path(r"C:\Users\carmi\blender\blender-audio-project"),
        Path(r"C:\Users\carmi\blender\blender-audio-project\audio"),
        Path(r"C:\Users\carmi\blender\audio"),
        Path(r"C:\Users\carmi\Desktop"),
        Path(r"C:\Users\carmi\Desktop\Living Life In Peace-Luca Vera"),
    ]


def find_file(filename: str) -> Path:
    for base in candidate_project_dirs():
        path = base / filename
        if path.exists():
            return path
    raise FileNotFoundError(
        f"File non trovato: {filename}. Mettilo accanto allo script oppure nella cartella output del progetto."
    )


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"JSON non valido: {path}")
    return data


def resolve_audio_path(meta: dict | None = None) -> Path | None:
    """Trova il WAV master e lo aggancia alla scena/VSE se disponibile."""
    meta = meta or {}
    candidates: list[Path] = []

    if AUDIO_PATH_OVERRIDE:
        candidates.append(Path(AUDIO_PATH_OVERRIDE))

    for key in ("audio_path", "wav_path", "source_audio", "input_audio", "track_path"):
        raw = meta.get(key)
        if raw:
            candidates.append(Path(str(raw)))

    for base in candidate_project_dirs():
        candidates.extend([
            base / AUDIO_FILE_NAME,
            base / "audio" / AUDIO_FILE_NAME,
            base / "output" / AUDIO_FILE_NAME,
        ])

    # Fallback poco costoso: cerca solo nelle directory candidate, non su tutto il disco.
    for base in candidate_project_dirs():
        try:
            if base.exists() and base.is_dir():
                candidates.extend(base.glob(f"{TRACK_STEM}*.wav"))
                candidates.extend(base.glob(f"{TRACK_STEM}*.flac"))
                candidates.extend(base.glob(f"{TRACK_STEM}*.mp3"))
        except Exception:
            pass

    seen: set[str] = set()
    for path in candidates:
        try:
            resolved = path.expanduser().resolve()
        except Exception:
            resolved = path
        key = str(resolved).lower()
        if key in seen:
            continue
        seen.add(key)
        if resolved.exists() and resolved.is_file():
            return resolved
    return None


def remove_existing_audio_strips(scene: bpy.types.Scene) -> None:
    seq = getattr(scene, "sequence_editor", None)
    if not seq:
        return
    containers = []
    for attr in ("sequences_all", "sequences", "strips"):
        obj = getattr(seq, attr, None)
        if obj is not None:
            containers.append(obj)
    for container in containers:
        try:
            for strip in list(container):
                if getattr(strip, "type", None) == "SOUND" or "audio" in strip.name.lower():
                    try:
                        container.remove(strip)
                    except Exception:
                        pass
        except Exception:
            pass


def attach_audio_to_scene(audio_path: Path | None, collection: bpy.types.Collection | None = None) -> bool:
    if audio_path is None:
        print(f"[WARN] Audio non trovato: {AUDIO_FILE_NAME}. La scena resta generata, ma senza traccia in timeline.")
        return False

    scene = bpy.context.scene
    try:
        sound = bpy.data.sounds.load(str(audio_path), check_existing=True)
    except Exception as exc:
        print(f"[WARN] Impossibile caricare audio: {audio_path} -> {exc}")
        return False

    try:
        if getattr(scene, "sequence_editor", None) is None:
            scene.sequence_editor_create()
        remove_existing_audio_strips(scene)
        seq = scene.sequence_editor
        sequences = getattr(seq, "sequences", None) or getattr(seq, "strips", None)
        if sequences is not None and hasattr(sequences, "new_sound"):
            strip = sequences.new_sound(
                name="Ready_To_Jazz_master_audio",
                filepath=str(audio_path),
                channel=1,
                frame_start=scene.frame_start,
            )
            if hasattr(strip, "show_waveform"):
                strip.show_waveform = True
            if hasattr(strip, "sound"):
                strip.sound = sound
    except Exception as exc:
        print(f"[WARN] Audio caricato, ma non inserito nel VSE: {exc}")

    try:
        bpy.ops.object.speaker_add(location=(0.0, -3.2, 1.7), rotation=(math.radians(72), 0.0, 0.0))
        speaker = bpy.context.object
        speaker.name = "Ready_To_Jazz_scene_audio_speaker"
        speaker.data.sound = sound
        speaker.data.volume = 1.0
        speaker.data.pitch = 1.0
        if collection is not None:
            link_to_collection(speaker, collection)
    except Exception as exc:
        print(f"[WARN] Speaker audio non creato: {exc}")

    # Impostazioni utili per preview sincronizzata e render con audio.
    try:
        scene.sync_mode = "AUDIO_SYNC"
    except Exception:
        pass
    for attr, value in (("use_audio_scrub", True), ("use_audio", True)):
        if hasattr(scene, attr):
            try:
                setattr(scene, attr, value)
            except Exception:
                pass
    try:
        scene.render.ffmpeg.audio_codec = "AAC"
        scene.render.ffmpeg.audio_bitrate = 320
    except Exception:
        pass

    print(f"[OK] Audio collegato alla scena: {audio_path}")
    return True


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in list(bpy.data.images):
        if block.users == 0:
            bpy.data.images.remove(block)


def set_interpolation(obj_or_data, interpolation: str = "LINEAR") -> None:
    """Imposta l'interpolazione dei keyframe senza bloccare Blender 5.1.

    In Blender 5.x alcune Action possono non esporre piu direttamente
    action.fcurves. In quel caso la funzione salta l'oggetto invece di
    interrompere la generazione della scena.
    """
    try:
        anim = getattr(obj_or_data, "animation_data", None)
        action = getattr(anim, "action", None) if anim else None
        if not action:
            return

        fcurves = getattr(action, "fcurves", None)
        if not fcurves:
            return

        for fcurve in fcurves:
            keyframe_points = getattr(fcurve, "keyframe_points", None)
            if not keyframe_points:
                continue
            for kp in keyframe_points:
                try:
                    kp.interpolation = interpolation
                except Exception:
                    pass

    except Exception as exc:
        name = getattr(obj_or_data, "name", type(obj_or_data).__name__)
        print(f"[WARN] Interpolazione keyframe saltata per {name}: {exc}")


def ensure_collection(name: str) -> bpy.types.Collection:
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def link_to_collection(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    if obj.name not in collection.objects:
        collection.objects.link(obj)
    for col in list(obj.users_collection):
        if col != collection and col.name == "Collection":
            col.objects.unlink(obj)


# =============================================================================
# MATERIALI
# =============================================================================

def _rgba(color: tuple[float, ...]) -> tuple[float, float, float, float]:
    if len(color) >= 4:
        return (float(color[0]), float(color[1]), float(color[2]), float(color[3]))
    return (float(color[0]), float(color[1]), float(color[2]), 1.0)


def _fresh_material(name: str, blend_method: str = "OPAQUE") -> tuple[bpy.types.Material, bpy.types.Nodes, bpy.types.NodeLinks]:
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.blend_method = blend_method
    try:
        mat.shadow_method = "HASHED" if blend_method != "OPAQUE" else "OPAQUE"
    except Exception:
        pass
    mat.use_screen_refraction = False
    try:
        mat.show_transparent_back = False
    except Exception:
        pass
    nt = mat.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    return mat, nt.nodes, nt.links


def _value_node(nodes: bpy.types.Nodes, name: str, value: float, location: tuple[float, float]) -> bpy.types.Node:
    node = nodes.new("ShaderNodeValue")
    node.name = name
    node.label = name
    node.location = location
    node.outputs[0].default_value = float(value)
    return node


def _set_bsdf_color_input(bsdf: bpy.types.Node, input_name: str, value) -> None:
    if bsdf and input_name in bsdf.inputs:
        bsdf.inputs[input_name].default_value = value


def make_layered_surface_mat(
    name: str,
    color_a: tuple[float, float, float, float],
    color_b: tuple[float, float, float, float],
    emission_color: tuple[float, float, float, float],
    strength: float,
    metallic: float = 0.0,
    roughness: float = 0.35,
    alpha: float = 1.0,
    transmission: float = 0.0,
    clearcoat: float = 0.0,
) -> bpy.types.Material:
    blend_method = "BLEND" if alpha < 0.999 else "OPAQUE"
    mat, nodes, links = _fresh_material(name, blend_method=blend_method)
    mat.diffuse_color = _rgba(color_a)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (760, 0)

    tex = nodes.new("ShaderNodeTexCoord")
    tex.location = (-1180, 180)
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-990, 180)
    mapping.inputs[3].default_value = (4.2, 4.2, 4.2)

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-800, 230)
    noise.inputs[2].default_value = 6.0
    noise.inputs[3].default_value = 3.2
    noise.inputs[4].default_value = 0.54

    musgrave = nodes.new("ShaderNodeTexMusgrave")
    musgrave.location = (-800, -30)
    musgrave.inputs[2].default_value = 8.0
    musgrave.inputs[3].default_value = 2.0
    musgrave.inputs[4].default_value = 0.55
    musgrave.inputs[5].default_value = 1.8

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-590, 220)
    ramp.color_ramp.elements[0].position = 0.18
    ramp.color_ramp.elements[0].color = _rgba(color_a)
    ramp.color_ramp.elements[1].position = 0.86
    ramp.color_ramp.elements[1].color = _rgba(color_b)

    mix_base = nodes.new("ShaderNodeMixRGB")
    mix_base.location = (-340, 160)
    mix_base.blend_type = "SOFT_LIGHT"
    mix_base.inputs[0].default_value = 0.38
    mix_base.inputs[2].default_value = _rgba(color_b)

    layer_weight = nodes.new("ShaderNodeLayerWeight")
    layer_weight.location = (-610, -210)
    layer_weight.inputs[0].default_value = 0.28

    bump = nodes.new("ShaderNodeBump")
    bump.location = (-140, -200)
    bump.inputs[0].default_value = 0.16
    bump.inputs[1].default_value = 0.04

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (110, -10)
    _set_bsdf_color_input(bsdf, "Metallic", metallic)
    _set_bsdf_color_input(bsdf, "Roughness", roughness)
    _set_bsdf_color_input(bsdf, "Transmission Weight", transmission)
    _set_bsdf_color_input(bsdf, "Transmission", transmission)
    _set_bsdf_color_input(bsdf, "Coat Weight", clearcoat)
    _set_bsdf_color_input(bsdf, "Clearcoat", clearcoat)
    _set_bsdf_color_input(bsdf, "IOR", 1.42)
    _set_bsdf_color_input(bsdf, "Specular IOR Level", 0.42)
    _set_bsdf_color_input(bsdf, "Specular", 0.42)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (120, 210)
    emission.inputs[0].default_value = _rgba(emission_color)

    emission_value = _value_node(nodes, "ST_EmissionStrength", strength, (-140, 370))
    alpha_value = _value_node(nodes, "ST_Alpha", alpha, (-140, 500))

    add_shader = nodes.new("ShaderNodeAddShader")
    add_shader.location = (380, 90)
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (390, -140)
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (580, 0)

    links.new(tex.outputs["Object"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(mapping.outputs["Vector"], musgrave.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], mix_base.inputs[1])
    links.new(mix_base.outputs["Color"], bsdf.inputs["Base Color"])
    if "Alpha" in bsdf.inputs:
        links.new(alpha_value.outputs[0], bsdf.inputs["Alpha"])
    links.new(musgrave.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    links.new(layer_weight.outputs["Facing"], emission.inputs["Color"])
    # preserve explicit emission palette while adding edge tint
    tint_mix = nodes.new("ShaderNodeMixRGB")
    tint_mix.location = (-40, 250)
    tint_mix.blend_type = "SCREEN"
    tint_mix.inputs[0].default_value = 0.28
    tint_mix.inputs[1].default_value = _rgba(emission_color)
    links.new(layer_weight.outputs["Fresnel"], tint_mix.inputs[2])
    links.new(tint_mix.outputs["Color"], emission.inputs["Color"])
    links.new(emission_value.outputs[0], emission.inputs["Strength"])
    links.new(bsdf.outputs[0], add_shader.inputs[0])
    links.new(emission.outputs[0], add_shader.inputs[1])
    links.new(alpha_value.outputs[0], mix_shader.inputs[0])
    links.new(transparent.outputs[0], mix_shader.inputs[1])
    links.new(add_shader.outputs[0], mix_shader.inputs[2])
    links.new(mix_shader.outputs[0], out.inputs["Surface"])
    return mat


def make_floor_mat(name: str) -> bpy.types.Material:
    mat, nodes, links = _fresh_material(name, blend_method="OPAQUE")
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (620, 0)
    tex = nodes.new("ShaderNodeTexCoord")
    tex.location = (-1120, 110)
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-930, 110)
    mapping.inputs[3].default_value = (0.7, 0.7, 0.7)
    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-730, 160)
    noise.inputs[2].default_value = 5.2
    noise.inputs[3].default_value = 2.2
    noise.inputs[4].default_value = 0.45
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-520, 160)
    ramp.color_ramp.elements[0].color = (0.02, 0.05, 0.06, 1.0)
    ramp.color_ramp.elements[1].color = (0.05, 0.14, 0.16, 1.0)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (70, 10)
    _set_bsdf_color_input(bsdf, "Metallic", 0.12)
    _set_bsdf_color_input(bsdf, "Roughness", 0.16)
    _set_bsdf_color_input(bsdf, "Specular IOR Level", 0.42)
    _set_bsdf_color_input(bsdf, "Specular", 0.42)
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (80, 220)
    emission.inputs[0].default_value = (0.00, 0.22, 0.28, 1.0)
    emission_value = _value_node(nodes, "ST_EmissionStrength", 0.045, (-140, 320))
    add_shader = nodes.new("ShaderNodeAddShader")
    add_shader.location = (330, 80)
    links.new(tex.outputs["Object"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(emission_value.outputs[0], emission.inputs["Strength"])
    links.new(bsdf.outputs[0], add_shader.inputs[0])
    links.new(emission.outputs[0], add_shader.inputs[1])
    links.new(add_shader.outputs[0], out.inputs["Surface"])
    return mat


def make_dome_mat(name: str) -> bpy.types.Material:
    mat, nodes, links = _fresh_material(name, blend_method="OPAQUE")
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (560, 0)
    tex = nodes.new("ShaderNodeTexCoord")
    tex.location = (-840, 140)
    gradient = nodes.new("ShaderNodeTexGradient")
    gradient.location = (-620, 140)
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-1020, 140)
    mapping.inputs[2].default_value[1] = 1.5708
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-420, 140)
    ramp.color_ramp.elements[0].position = 0.10
    ramp.color_ramp.elements[0].color = (0.00, 0.11, 0.15, 1.0)
    ramp.color_ramp.elements[1].position = 0.92
    ramp.color_ramp.elements[1].color = (0.01, 0.21, 0.22, 1.0)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (50, 0)
    _set_bsdf_color_input(bsdf, "Roughness", 0.92)
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (50, 200)
    emission.inputs[0].default_value = (0.02, 0.18, 0.20, 1.0)
    emission_value = _value_node(nodes, "ST_EmissionStrength", 0.06 * ATMOS_EMISSION_SOFTNESS, (-150, 300))
    add_shader = nodes.new("ShaderNodeAddShader")
    add_shader.location = (310, 80)
    links.new(tex.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], gradient.inputs["Vector"])
    links.new(gradient.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(emission_value.outputs[0], emission.inputs["Strength"])
    links.new(bsdf.outputs[0], add_shader.inputs[0])
    links.new(emission.outputs[0], add_shader.inputs[1])
    links.new(add_shader.outputs[0], out.inputs["Surface"])
    return mat


def make_volume_fog_mat(name: str, color: tuple[float, float, float, float], density: float, anisotropy: float = 0.15) -> bpy.types.Material:
    mat, nodes, links = _fresh_material(name, blend_method="BLEND")
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (470, 0)
    tex = nodes.new("ShaderNodeTexCoord")
    tex.location = (-990, 120)
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-800, 120)
    mapping.inputs[3].default_value = (1.6, 1.6, 1.1)
    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-610, 120)
    noise.inputs[2].default_value = 3.4
    noise.inputs[3].default_value = 2.0
    noise.inputs[4].default_value = 0.55
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-400, 120)
    ramp.color_ramp.elements[0].position = 0.24
    ramp.color_ramp.elements[1].position = 0.88
    density_value = _value_node(nodes, "ST_FogDensity", density, (-410, -120))
    mult = nodes.new("ShaderNodeMath")
    mult.location = (-160, 20)
    mult.operation = "MULTIPLY"
    mult.inputs[1].default_value = 1.0
    vol = nodes.new("ShaderNodeVolumePrincipled")
    vol.location = (120, 0)
    vol.inputs["Color"].default_value = _rgba(color)
    vol.inputs["Anisotropy"].default_value = anisotropy
    vol.inputs["Emission Strength"].default_value = 0.0
    links.new(tex.outputs["Object"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Alpha"], mult.inputs[0])
    links.new(density_value.outputs[0], mult.inputs[1])
    links.new(mult.outputs[0], vol.inputs["Density"])
    links.new(vol.outputs[0], out.inputs["Volume"])
    return mat


def make_principled_emission_mat(
    name: str,
    base_color: tuple[float, float, float, float],
    emission_color: tuple[float, float, float, float],
    strength: float,
    metallic: float = 0.0,
    roughness: float = 0.35,
    alpha: float = 1.0,
) -> bpy.types.Material:
    return make_layered_surface_mat(name, base_color, base_color, emission_color, strength, metallic=metallic, roughness=roughness, alpha=alpha)


def _set_named_value_node(mat: bpy.types.Material, node_name: str, value: float, frame: int) -> bool:
    if not mat or not mat.use_nodes or not mat.node_tree:
        return False
    node = mat.node_tree.nodes.get(node_name)
    if node and getattr(node, 'type', '') == 'VALUE':
        node.outputs[0].default_value = float(value)
        node.outputs[0].keyframe_insert('default_value', frame=frame)
        return True
    return False


def set_material_emission_strength(mat: bpy.types.Material, strength: float, frame: int) -> None:
    if _set_named_value_node(mat, "ST_EmissionStrength", strength, frame):
        return
    if not mat or not mat.use_nodes:
        return
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if not bsdf:
        return
    if "Emission Strength" in bsdf.inputs:
        sock = bsdf.inputs["Emission Strength"]
        sock.default_value = float(strength)
        sock.keyframe_insert("default_value", frame=frame)


def set_material_alpha(mat: bpy.types.Material, alpha: float, frame: int) -> None:
    mat.diffuse_color = (mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2], alpha)
    mat.keyframe_insert("diffuse_color", frame=frame)
    if _set_named_value_node(mat, "ST_Alpha", alpha, frame):
        return
    if not mat.use_nodes:
        return
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf and "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = alpha
        bsdf.inputs["Alpha"].keyframe_insert("default_value", frame=frame)


def set_material_volume_density(mat: bpy.types.Material, density: float, frame: int) -> None:
    if _set_named_value_node(mat, "ST_FogDensity", density, frame):
        return


# =============================================================================
# GEOMETRIA / ASSET
# =============================================================================

def add_empty(name: str, location=(0, 0, 0), empty_display_size: float = 0.5) -> bpy.types.Object:
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=location)
    obj = bpy.context.object
    obj.name = name
    obj.empty_display_size = empty_display_size
    return obj


def add_uv_sphere(
    name: str,
    radius: float,
    location: tuple[float, float, float],
    mat: bpy.types.Material | None = None,
    segments: int = 64,
    rings: int = 32,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    return obj


def add_torus(
    name: str,
    major_radius: float,
    minor_radius: float,
    location: tuple[float, float, float],
    mat: bpy.types.Material | None = None,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=192,
        minor_segments=8,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    return obj


def world_bbox(objects: Iterable[bpy.types.Object]) -> tuple[Vector, Vector]:
    coords: list[Vector] = []
    bpy.context.view_layer.update()
    for obj in objects:
        if obj.type == "MESH" and hasattr(obj, "bound_box"):
            coords.extend([obj.matrix_world @ Vector(corner) for corner in obj.bound_box])
        else:
            coords.append(obj.matrix_world.translation.copy())
    if not coords:
        return Vector((0, 0, 0)), Vector((1, 1, 1))
    min_v = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
    max_v = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
    return (min_v + max_v) * 0.5, max_v - min_v


def import_supported_asset(asset_path: Path) -> list[bpy.types.Object]:
    before = set(bpy.data.objects.keys())
    ext = asset_path.suffix.lower()
    if ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(asset_path))
    elif ext in {".glb", ".gltf"}:
        bpy.ops.import_scene.gltf(filepath=str(asset_path))
    elif ext == ".obj":
        try:
            bpy.ops.wm.obj_import(filepath=str(asset_path))
        except Exception:
            bpy.ops.import_scene.obj(filepath=str(asset_path))
    elif ext == ".blend":
        with bpy.data.libraries.load(str(asset_path), link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
    else:
        raise RuntimeError(f"Formato asset non supportato: {asset_path}")
    after = set(bpy.data.objects.keys())
    return [bpy.data.objects[name] for name in sorted(after - before)]


def find_primary_ball_asset(inventory: dict) -> Path | None:
    for asset in inventory.get("assets", []):
        if asset.get("role") == "primary_ball_asset":
            raw = asset.get("path") or ""
            path = Path(raw)
            if path.exists():
                return path
    return None


def create_central_focus(
    name: str,
    location: tuple[float, float, float],
    material: bpy.types.Material,
    aura_material: bpy.types.Material,
    asset_path: Path | None,
    collection: bpy.types.Collection,
) -> dict[str, bpy.types.Object]:
    root = add_empty(name, location=location, empty_display_size=1.2)
    link_to_collection(root, collection)

    imported: list[bpy.types.Object] = []
    if USE_PRIMARY_BALL_ASSET and asset_path and asset_path.exists():
        try:
            imported = import_supported_asset(asset_path)
        except Exception as exc:
            print(f"[WARN] Import asset fallito, uso sfera procedurale: {asset_path} -> {exc}")
            imported = []

    if imported:
        center, size = world_bbox(imported)
        max_dim = max(size.x, size.y, size.z, 0.001)
        normalize_scale = CORE_IMPORTED_TARGET_SIZE / max_dim
        for obj in imported:
            obj.name = f"{name}_{obj.name}"
            obj.location -= center
            obj.parent = root
            obj.scale *= normalize_scale
            if obj.type == "MESH":
                obj.data.materials.clear()
                obj.data.materials.append(material)
            link_to_collection(obj, collection)
        visual = imported[0]
    else:
        visual = add_uv_sphere(f"{name}_core_mesh", CORE_PROCEDURAL_RADIUS, (0, 0, 0), material, segments=96, rings=48)
        visual.parent = root
        link_to_collection(visual, collection)

    aura = add_uv_sphere(f"{name}_audio_aura", CORE_AURA_RADIUS, (0, 0, 0), aura_material, segments=96, rings=48)
    aura.parent = root
    link_to_collection(aura, collection)

    tex = bpy.data.textures.new(f"{name}_noise_texture", type="VORONOI")
    tex.noise_scale = 1.3
    disp = aura.modifiers.new(f"{name}_audio_displace", "DISPLACE")
    disp.strength = 0.08
    disp.texture = tex

    return {"root": root, "visual": visual, "aura": aura}


def add_force_field(name: str, field_type: str, location: tuple[float, float, float], collection: bpy.types.Collection) -> bpy.types.Object:
    bpy.ops.object.effector_add(type=field_type, location=location)
    obj = bpy.context.object
    obj.name = name
    link_to_collection(obj, collection)
    return obj


# =============================================================================
# YOUTUBE / SOCIAL RENDER PROFILE
# =============================================================================

def normalize_youtube_profile(profile_name: str) -> str:
    profile = str(profile_name or "2K_INTERMEDIATE").upper().replace("-", "_").replace(" ", "_")
    aliases = {
        "HD": "HD_FINAL",
        "HD_FAST": "HD_INTERMEDIATE",
        "HD_TEST": "HD_PREVIEW",
        "1080P_PREVIEW": "HD_PREVIEW",
        "1080P_INTERMEDIATE": "HD_INTERMEDIATE",
        "1080P_FINAL": "HD_FINAL",
        "2K": "2K_FINAL",
        "1440P": "2K_FINAL",
        "1440P_PREVIEW": "2K_PREVIEW",
        "1440P_INTERMEDIATE": "2K_INTERMEDIATE",
        "1440P_FINAL": "2K_FINAL",
        "PREVIEW": "HD_PREVIEW",
        "INTERMEDIATE": "2K_INTERMEDIATE",
        "FINAL": "2K_FINAL",
    }
    profile = aliases.get(profile, profile)
    if profile not in YOUTUBE_RENDER_PROFILES:
        print(f"[WARN] Profilo render sconosciuto '{profile_name}', uso 2K_INTERMEDIATE.")
        return "2K_INTERMEDIATE"
    return profile


def active_youtube_profile() -> dict:
    return YOUTUBE_RENDER_PROFILES[normalize_youtube_profile(FINAL_YOUTUBE)]


def output_paths_for_profile(profile_name: str) -> dict[str, Path]:
    profile_key = normalize_youtube_profile(profile_name)
    base = OUTPUT_BASE_DIR / f"{OUTPUT_PROJECT_SLUG}_{profile_key.lower()}"
    frames_dir = base / "frames"
    mp4_path = base / f"{OUTPUT_PROJECT_SLUG}_{profile_key.lower()}.mp4"
    return {"base": base, "frames": frames_dir, "mp4": mp4_path}


def set_first_available(obj, attr: str, values: list[str]) -> bool:
    for value in values:
        try:
            setattr(obj, attr, value)
            return True
        except Exception:
            continue
    return False


def configure_color_management(scene: bpy.types.Scene, profile: dict) -> None:
    view = getattr(scene, "view_settings", None)
    if view is None:
        return
    set_first_available(view, "view_transform", ["AgX", "Filmic", "Standard"])
    set_first_available(view, "look", [str(profile.get("look", "Medium High Contrast")), "Medium High Contrast", "Base Contrast", "None"])
    try:
        view.exposure = float(profile.get("exposure", -0.07))
    except Exception:
        pass
    try:
        view.gamma = float(profile.get("gamma", 1.0))
    except Exception:
        pass
    try:
        scene.display_settings.display_device = "sRGB"
    except Exception:
        pass
    try:
        scene.sequencer_colorspace_settings.name = "sRGB"
    except Exception:
        pass


def configure_output_settings(scene: bpy.types.Scene, profile_name: str) -> dict[str, Path]:
    profile_key = normalize_youtube_profile(profile_name)
    profile = YOUTUBE_RENDER_PROFILES[profile_key]
    paths = output_paths_for_profile(profile_key)
    paths["base"].mkdir(parents=True, exist_ok=True)
    paths["frames"].mkdir(parents=True, exist_ok=True)

    scene.render.resolution_x = int(profile["width"])
    scene.render.resolution_y = int(profile["height"])
    scene.render.resolution_percentage = int(profile["percentage"])
    scene.render.use_motion_blur = bool(profile.get("motion_blur", False))
    scene.render.use_file_extension = True

    output_mode = str(profile.get("output_mode", "IMAGE_SEQUENCE")).upper()
    if output_mode == "IMAGE_SEQUENCE":
        scene.render.filepath = str(paths["frames"] / OUTPUT_FRAME_PREFIX)
        scene.render.use_sequencer = False
        scene.render.use_overwrite = False
        try:
            scene.render.use_placeholder = True
        except Exception:
            pass
        try:
            scene.render.image_settings.media_type = "IMAGE"
        except Exception:
            pass
        try:
            scene.render.image_settings.file_format = "PNG"
            scene.render.image_settings.color_mode = "RGB"
            scene.render.image_settings.color_depth = str(profile.get("image_depth", "16"))
            scene.render.image_settings.compression = int(profile.get("png_compression", 15))
        except Exception:
            pass
    else:
        scene.render.filepath = str(paths["mp4"])
        scene.render.use_sequencer = True
        scene.render.use_overwrite = True
        try:
            scene.render.image_settings.media_type = "VIDEO"
            scene.render.image_settings.file_format = "FFMPEG"
            scene.render.image_settings.color_mode = "RGB"
        except Exception:
            pass
        try:
            scene.render.ffmpeg.format = "MPEG4"
            scene.render.ffmpeg.codec = "H264"
            scene.render.ffmpeg.audio_codec = "AAC"
            scene.render.ffmpeg.audio_bitrate = int(profile.get("audio_bitrate", 320))
            scene.render.ffmpeg.video_bitrate = int(profile.get("video_bitrate", 24000))
            scene.render.ffmpeg.maxrate = int(profile.get("video_maxrate", 30000))
            scene.render.ffmpeg.minrate = 0
            scene.render.ffmpeg.buffersize = 1792
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
        except Exception:
            pass

    return paths


def configure_engine_settings(scene: bpy.types.Scene, profile: dict) -> None:
    try:
        scene.render.engine = RENDER_ENGINE
    except Exception:
        try:
            scene.render.engine = "BLENDER_EEVEE"
        except Exception:
            pass

    eevee = getattr(scene, "eevee", None)
    if eevee is None:
        return
    if hasattr(eevee, "taa_render_samples"):
        eevee.taa_render_samples = int(profile.get("eevee_samples", 64))
    if hasattr(eevee, "taa_samples"):
        eevee.taa_samples = int(profile.get("viewport_samples", 24))
    if hasattr(eevee, "use_bloom"):
        eevee.use_bloom = True
    if hasattr(eevee, "bloom_threshold"):
        eevee.bloom_threshold = float(profile.get("bloom_threshold", 1.20))
    if hasattr(eevee, "bloom_intensity"):
        eevee.bloom_intensity = float(profile.get("bloom_intensity", 0.018))
    if hasattr(eevee, "use_gtao"):
        eevee.use_gtao = True
    if hasattr(eevee, "gtao_quality"):
        eevee.gtao_quality = 0.35
    if hasattr(eevee, "use_volumetric_lights"):
        eevee.use_volumetric_lights = True
    if hasattr(eevee, "use_volumetric_shadows"):
        eevee.use_volumetric_shadows = False
    if hasattr(eevee, "volumetric_samples"):
        eevee.volumetric_samples = int(profile.get("volumetric_samples", 32))
    if hasattr(eevee, "volumetric_tile_size"):
        try:
            eevee.volumetric_tile_size = str(profile.get("volumetric_tile_size", "8"))
        except Exception:
            pass
    if hasattr(eevee, "volumetric_start"):
        eevee.volumetric_start = 0.1
    if hasattr(eevee, "volumetric_end"):
        eevee.volumetric_end = 55.0


def apply_youtube_render_profile(scene: bpy.types.Scene, fps: float) -> dict[str, Path]:
    profile_key = normalize_youtube_profile(FINAL_YOUTUBE)
    profile = YOUTUBE_RENDER_PROFILES[profile_key]
    scene.render.fps = int(round(fps))
    configure_color_management(scene, profile)
    paths = configure_output_settings(scene, profile_key)
    configure_engine_settings(scene, profile)
    scene["st_final_youtube_profile"] = profile_key
    scene["st_output_base_dir"] = str(paths["base"])
    scene["st_output_frames_dir"] = str(paths["frames"])
    scene["st_output_mp4"] = str(paths["mp4"])
    print(f"[OK] YouTube/social profile: {profile_key}")
    print(f"[OK] Resolution: {profile['width']}x{profile['height']} @ {profile['percentage']}% | fps={int(round(fps))}")
    print(f"[OK] Output frames: {paths['frames']}")
    print(f"[OK] Output mp4:    {paths['mp4']}")
    return paths


# =============================================================================
# SCENA
# =============================================================================

def setup_scene(meta: dict) -> None:
    scene = bpy.context.scene
    fps = float(meta.get("fps") or FPS_FALLBACK)
    duration = float(meta.get("duration_sec") or 60.0)
    scene.frame_start = 1
    scene.frame_end = max(2, int(round(duration * fps)))
    apply_youtube_render_profile(scene, fps)

    world = bpy.context.scene.world or bpy.data.worlds.new("ReadyToJazzWorld")
    bpy.context.scene.world = world
    world.color = (0.018, 0.055, 0.075)


def make_environment(materials: dict[str, bpy.types.Material], collection: bpy.types.Collection) -> None:
    floor_mat = materials["floor"]
    bpy.ops.mesh.primitive_plane_add(size=32, location=(0, 0, -0.08))
    floor = bpy.context.object
    floor.name = "reflective_deep_floor"
    floor.data.materials.append(floor_mat)
    link_to_collection(floor, collection)

    # cupola morbida, non nera piatta
    dome_mat = materials["dome"]
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=18, location=(0, 0, 2.0))
    dome = bpy.context.object
    dome.name = "blue_green_soft_space_dome"
    dome.data.materials.append(dome_mat)
    dome.scale = (1.0, 1.0, 0.62)
    # Normali verso interno: visibile dall'interno in Eevee anche se non perfetto.
    dome.display_type = "TEXTURED"
    link_to_collection(dome, collection)


def make_lights(collection: bpy.types.Collection) -> dict[str, bpy.types.Object]:
    bpy.ops.object.light_add(type="AREA", location=(0, -4.5, 5.6))
    key = bpy.context.object
    key.name = "audio_key_area_light"
    key.data.energy = 480
    key.data.size = 5.5
    link_to_collection(key, collection)

    bpy.ops.object.light_add(type="POINT", location=(-3.1, 2.2, 2.0))
    a = bpy.context.object
    a.name = "gravity_A_accent_light"
    a.data.energy = 120
    a.data.shadow_soft_size = 5
    link_to_collection(a, collection)

    bpy.ops.object.light_add(type="POINT", location=(3.1, 2.2, 2.0))
    b = bpy.context.object
    b.name = "gravity_B_accent_light"
    b.data.energy = 120
    b.data.shadow_soft_size = 5
    link_to_collection(b, collection)

    return {"key": key, "A": a, "B": b}


def make_camera(collection: bpy.types.Collection) -> bpy.types.Object:
    bpy.ops.object.camera_add(location=(0.0, -8.6, 3.1), rotation=(math.radians(70), 0.0, 0.0))
    cam = bpy.context.object
    cam.name = "audio_reactive_camera"
    cam.data.lens = 58
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 8.0
    cam.data.dof.aperture_fstop = 5.6
    bpy.context.scene.camera = cam
    link_to_collection(cam, collection)
    return cam


def make_materials() -> dict[str, bpy.types.Material]:
    return {
        "core_a": make_layered_surface_mat(
            "MAT_core_A_blue_gold",
            (0.05, 0.18, 0.36, 1.0),
            (0.12, 0.56, 0.92, 1.0),
            (0.22, 0.76, 1.0, 1.0),
            0.90,
            metallic=0.05,
            roughness=0.22,
            alpha=1.0,
            transmission=0.02,
            clearcoat=0.15,
        ),
        "core_b": make_layered_surface_mat(
            "MAT_core_B_green_white",
            (0.06, 0.24, 0.16, 1.0),
            (0.26, 0.72, 0.50, 1.0),
            (0.76, 1.0, 0.88, 1.0),
            0.82,
            metallic=0.04,
            roughness=0.24,
            alpha=1.0,
            transmission=0.02,
            clearcoat=0.12,
        ),
        "aura_a": make_layered_surface_mat(
            "MAT_aura_A_translucent",
            (0.05, 0.26, 0.45, 1.0),
            (0.10, 0.48, 0.85, 1.0),
            (0.25, 0.78, 1.0, 1.0),
            0.18,
            roughness=0.12,
            alpha=0.15,
            transmission=0.06,
        ),
        "aura_b": make_layered_surface_mat(
            "MAT_aura_B_translucent",
            (0.08, 0.30, 0.18, 1.0),
            (0.18, 0.68, 0.42, 1.0),
            (0.54, 1.0, 0.76, 1.0),
            0.16,
            roughness=0.12,
            alpha=0.14,
            transmission=0.06,
        ),
        "sat_low": make_layered_surface_mat(
            "MAT_satellite_low_mass",
            (0.40, 0.16, 0.05, 1.0),
            (0.90, 0.54, 0.18, 1.0),
            (1.0, 0.68, 0.26, 1.0),
            0.16,
            metallic=0.02,
            roughness=0.28,
        ),
        "sat_mid": make_layered_surface_mat(
            "MAT_satellite_mid_mass",
            (0.28, 0.38, 0.42, 1.0),
            (0.72, 0.88, 0.92, 1.0),
            (0.62, 0.92, 1.0, 1.0),
            0.14,
            metallic=0.02,
            roughness=0.25,
        ),
        "sat_high": make_layered_surface_mat(
            "MAT_satellite_high_mass",
            (0.34, 0.14, 0.38, 1.0),
            (0.74, 0.32, 0.84, 1.0),
            (0.95, 0.48, 1.0, 1.0),
            0.18,
            metallic=0.02,
            roughness=0.24,
        ),
        "orbit": make_layered_surface_mat(
            "MAT_orbit_lines_soft",
            (0.35, 0.72, 0.82, 1.0),
            (0.74, 0.92, 1.0, 1.0),
            (0.72, 0.94, 1.0, 1.0),
            0.08,
            roughness=0.08,
            alpha=0.10,
        ),
        "floor": make_floor_mat("MAT_deep_reflective_floor"),
        "dome": make_dome_mat("MAT_soft_blue_green_dome"),
        "fog_main": make_volume_fog_mat("MAT_main_scene_fog", (0.36, 0.58, 0.62, 1.0), FOG_MAIN_DENSITY, anisotropy=0.18),
        "fog_layer": make_volume_fog_mat("MAT_low_mist_fog", (0.24, 0.40, 0.44, 1.0), FOG_LAYER_DENSITY, anisotropy=0.08),
    }


def make_satellites(
    materials: dict[str, bpy.types.Material],
    collection: bpy.types.Collection,
) -> dict[str, list[dict]]:
    orbit_a = add_empty("gravity_A_orbit_rig", (-CORE_BASE_HALF_DISTANCE, 0, 0.9), 1.0)
    orbit_b = add_empty("gravity_B_orbit_rig", (CORE_BASE_HALF_DISTANCE, 0, 0.9), 1.0)
    orbit_shared = add_empty("binary_shared_orbit_rig", (0, 0, 0.9), 1.6)
    for rig in (orbit_a, orbit_b, orbit_shared):
        link_to_collection(rig, collection)

    ring_a = add_torus("gravity_A_orbit_ring", 1.18, 0.007, orbit_a.location, materials["orbit"])
    ring_b = add_torus("gravity_B_orbit_ring", 1.18, 0.007, orbit_b.location, materials["orbit"])
    ring_shared = add_torus("binary_outer_orbit_ring", 3.10, 0.009, orbit_shared.location, materials["orbit"])
    ring_a.parent = orbit_a
    ring_b.parent = orbit_b
    ring_shared.parent = orbit_shared
    for ring in (ring_a, ring_b, ring_shared):
        link_to_collection(ring, collection)

    satellites_a: list[dict] = []
    satellites_b: list[dict] = []
    satellites_shared: list[dict] = []

    mats = [materials["sat_low"], materials["sat_mid"], materials["sat_high"]]

    for i in range(INNER_BODIES_PER_CORE):
        angle = (math.tau * i) / INNER_BODIES_PER_CORE
        radius = 0.92 + 0.12 * (i % 3)
        size = INNER_SATELLITE_BASE_SIZE + INNER_SATELLITE_SIZE_STEP * (i % 4)
        z = 0.18 * math.sin(angle * 2.0)

        obj_a = add_uv_sphere(f"A_gravity_body_{i+1:02d}", size, (radius * math.cos(angle), radius * math.sin(angle), z), mats[i % 3], 32, 16)
        obj_a.parent = orbit_a
        link_to_collection(obj_a, collection)
        satellites_a.append({"obj": obj_a, "phase": angle, "base_radius": radius, "size": size, "speed": 1.15 + 0.17 * i})

        obj_b = add_uv_sphere(f"B_gravity_body_{i+1:02d}", size, (radius * math.cos(-angle), radius * math.sin(-angle), -z), mats[(i + 1) % 3], 32, 16)
        obj_b.parent = orbit_b
        link_to_collection(obj_b, collection)
        satellites_b.append({"obj": obj_b, "phase": -angle + 0.7, "base_radius": radius, "size": size, "speed": -(1.05 + 0.14 * i)})

    for i in range(OUTER_SHARED_BODIES):
        angle = (math.tau * i) / OUTER_SHARED_BODIES
        radius = 2.64 + 0.18 * (i % 4)
        size = OUTER_SATELLITE_BASE_SIZE + OUTER_SATELLITE_SIZE_STEP * (i % 5)
        obj = add_uv_sphere(
            f"binary_gravity_outer_body_{i+1:02d}",
            size,
            (radius * math.cos(angle), radius * math.sin(angle), 0.25 * math.sin(angle * 3.0)),
            mats[(i + 2) % 3],
            24,
            12,
        )
        obj.parent = orbit_shared
        link_to_collection(obj, collection)
        satellites_shared.append({"obj": obj, "phase": angle, "base_radius": radius, "size": size, "speed": 0.42 + 0.05 * i})

    return {
        "rigs": [{"obj": orbit_a}, {"obj": orbit_b}, {"obj": orbit_shared}],
        "rings": [{"obj": ring_a}, {"obj": ring_b}, {"obj": ring_shared}],
        "A": satellites_a,
        "B": satellites_b,
        "shared": satellites_shared,
    }



# =============================================================================
# EFFETTI AVANZATI WOW
# =============================================================================

def make_transparent_emission_mat(
    name: str,
    base_color: tuple[float, float, float, float],
    emission_color: tuple[float, float, float, float],
    strength: float,
    alpha: float,
) -> bpy.types.Material:
    mat = make_principled_emission_mat(name, base_color, emission_color, strength, metallic=0.0, roughness=0.18, alpha=alpha)
    mat.blend_method = "BLEND"
    mat.show_transparent_back = True
    return mat


def set_curve_bevel(curve_obj: bpy.types.Object, value: float, frame: int) -> None:
    if not curve_obj or not getattr(curve_obj, "data", None):
        return
    curve_obj.data.bevel_depth = float(value)
    curve_obj.data.keyframe_insert("bevel_depth", frame=frame)


def add_ico_sphere(
    name: str,
    radius: float,
    location: tuple[float, float, float],
    mat: bpy.types.Material | None = None,
    subdivisions: int = 1,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    return obj


def add_poly_curve(
    name: str,
    points: list[tuple[float, float, float]],
    mat: bpy.types.Material,
    bevel_depth: float = 0.025,
    bevel_resolution: int = 4,
) -> bpy.types.Object:
    curve = bpy.data.curves.new(name, type="CURVE")
    curve.dimensions = "3D"
    curve.fill_mode = "FULL"
    curve.bevel_depth = bevel_depth
    curve.bevel_resolution = bevel_resolution
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for idx, point in enumerate(points):
        spline.points[idx].co = (point[0], point[1], point[2], 1.0)
    curve.materials.append(mat)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    return obj


def make_wow_materials() -> dict:
    mats: dict[str, object] = {}
    mats["lens_a"] = make_transparent_emission_mat(
        "MAT_wow_gravity_lens_A", (0.12, 0.65, 1.0, 0.18), (0.10, 0.82, 1.0, 1.0), 0.22, 0.18
    )
    mats["lens_b"] = make_transparent_emission_mat(
        "MAT_wow_gravity_lens_B", (0.10, 1.0, 0.62, 0.16), (0.55, 1.0, 0.70, 1.0), 0.20, 0.16
    )
    mats["arc"] = make_transparent_emission_mat(
        "MAT_wow_binary_plasma_arc", (0.24, 0.68, 0.82, 0.24), (0.58, 0.88, 0.96, 1.0), 0.48, 0.20
    )
    mats["dust"] = make_principled_emission_mat(
        "MAT_wow_depth_dust", (0.60, 0.92, 1.0, 1.0), (0.72, 0.96, 1.0, 1.0), 0.18, roughness=0.48
    )
    mats["vortex"] = make_transparent_emission_mat(
        "MAT_wow_vortex_ribbon", (0.20, 0.42, 0.56, 0.20), (0.42, 0.74, 0.82, 1.0), 0.22, 0.16
    )
    shock_mats: list[bpy.types.Material] = []
    for i in range(WOW_SHOCKWAVE_COUNT):
        shock_mats.append(
            make_transparent_emission_mat(
                f"MAT_wow_beat_shockwave_{i+1:02d}",
                (0.18, 0.50, 0.62, 0.08),
                (0.40, 0.78, 0.86, 1.0),
                0.10,
                0.08,
            )
        )
    mats["shock"] = shock_mats
    return mats


def make_wow_effects(
    collection: bpy.types.Collection,
    focus_a: dict[str, bpy.types.Object],
    focus_b: dict[str, bpy.types.Object],
) -> dict:
    wow: dict[str, object] = {"materials": make_wow_materials()}
    mats = wow["materials"]

    if not ENABLE_WOW_ADVANCED_EFFECTS:
        return wow

    if ENABLE_WOW_GRAVITY_LENS:
        lens_a = add_uv_sphere("WOW_gravity_lens_shell_A", 1.50, (0, 0, 0), mats["lens_a"], segments=96, rings=48)
        lens_b = add_uv_sphere("WOW_gravity_lens_shell_B", 1.50, (0, 0, 0), mats["lens_b"], segments=96, rings=48)
        lens_a.parent = focus_a["root"]
        lens_b.parent = focus_b["root"]
        link_to_collection(lens_a, collection)
        link_to_collection(lens_b, collection)
        for obj, label in ((lens_a, "A"), (lens_b, "B")):
            tex = bpy.data.textures.new(f"WOW_lens_noise_{label}", type="VORONOI")
            tex.noise_scale = 0.95
            disp = obj.modifiers.new(f"WOW_lens_displace_{label}", "DISPLACE")
            disp.strength = 0.025
            disp.texture = tex
        wow["lens_a"] = lens_a
        wow["lens_b"] = lens_b

    if ENABLE_WOW_SHOCKWAVES:
        shock_rig = add_empty("WOW_beat_shockwave_rig", (0, 0, 0.92), empty_display_size=1.5)
        link_to_collection(shock_rig, collection)
        rings: list[bpy.types.Object] = []
        for i in range(WOW_SHOCKWAVE_COUNT):
            ring = add_torus(
                f"WOW_beat_shockwave_ring_{i+1:02d}",
                0.90 + 0.10 * i,
                0.006 + 0.001 * (i % 3),
                (0, 0, 0),
                mats["shock"][i],
            )
            ring.parent = shock_rig
            ring.rotation_euler = (math.radians(90 if i % 2 else 0), math.radians(18 * (i % 5)), math.radians(36 * i))
            ring.scale = (0.01, 0.01, 0.01)
            link_to_collection(ring, collection)
            rings.append(ring)
        wow["shock_rig"] = shock_rig
        wow["shock_rings"] = rings

    if ENABLE_WOW_PLASMA_ARCS:
        arcs: list[bpy.types.Object] = []
        for i in range(WOW_PLASMA_ARC_COUNT):
            phase = (i / max(1, WOW_PLASMA_ARC_COUNT - 1)) * math.tau
            points = []
            for step in range(18):
                t = step / 17.0
                x = lerp(-CORE_BASE_HALF_DISTANCE, CORE_BASE_HALF_DISTANCE, t)
                bow = math.sin(t * math.pi)
                y = 0.28 * math.sin(phase + t * math.tau * 1.7) * bow
                z = 0.92 + 0.74 * bow + 0.12 * math.cos(phase + t * math.tau)
                points.append((x, y, z))
            arc = add_poly_curve(f"WOW_binary_plasma_arc_{i+1:02d}", points, mats["arc"], bevel_depth=0.012, bevel_resolution=3)
            link_to_collection(arc, collection)
            arcs.append(arc)
        wow["plasma_arcs"] = arcs

    if ENABLE_WOW_LIGHT_BEAMS:
        beams: list[bpy.types.Object] = []
        for name, loc in (
            ("WOW_volumetric_cross_beam_A", (-4.2, -4.0, 5.2)),
            ("WOW_volumetric_cross_beam_B", (4.2, -4.0, 5.2)),
            ("WOW_top_energy_beam", (0.0, -2.2, 7.2)),
        ):
            bpy.ops.object.light_add(type="SPOT", location=loc)
            beam = bpy.context.object
            beam.name = name
            beam.data.energy = 130
            beam.data.spot_size = math.radians(34)
            beam.data.spot_blend = 0.72
            beam.data.shadow_soft_size = 1.0
            link_to_collection(beam, collection)
            beams.append(beam)
        wow["beams"] = beams

    if ENABLE_WOW_STAR_DUST:
        dust_rig = add_empty("WOW_parallax_depth_dust_rig", (0, 0, 1.0), empty_display_size=1.8)
        link_to_collection(dust_rig, collection)
        rng = random.Random(WOW_SEED)
        dust: list[bpy.types.Object] = []
        for i in range(WOW_DUST_COUNT):
            theta = rng.random() * math.tau
            radius = rng.uniform(4.0, 13.5)
            z = rng.uniform(-0.7, 4.8)
            y_flatten = rng.uniform(0.55, 0.95)
            size = rng.uniform(0.010, 0.043)
            obj = add_ico_sphere(
                f"WOW_parallax_dust_{i+1:03d}",
                size,
                (radius * math.cos(theta), y_flatten * radius * math.sin(theta), z),
                mats["dust"],
                subdivisions=1,
            )
            obj.parent = dust_rig
            link_to_collection(obj, collection)
            dust.append(obj)
        wow["dust_rig"] = dust_rig
        wow["dust"] = dust

    # Ribbon a doppia spirale sul baricentro: disegna una firma visiva riconoscibile.
    ribbons: list[bpy.types.Object] = []
    for sign, name in ((1.0, "WOW_blue_vortex_ribbon"), (-1.0, "WOW_green_vortex_ribbon")):
        points = []
        for step in range(180):
            t = step / 179.0
            radius = 1.85 + 0.65 * math.sin(t * math.pi)
            ang = sign * (math.tau * 3.25 * t)
            points.append((radius * math.cos(ang), 0.68 * radius * math.sin(ang), 0.15 + 1.72 * t))
        ribbon = add_poly_curve(name, points, mats["vortex"], bevel_depth=0.014, bevel_resolution=4)
        link_to_collection(ribbon, collection)
        ribbons.append(ribbon)
    wow["ribbons"] = ribbons

    return wow


def animate_wow_effects(
    audio_frames: list[dict],
    meta: dict,
    wow: dict,
    focus_a: dict[str, bpy.types.Object],
    focus_b: dict[str, bpy.types.Object],
    camera: bpy.types.Object,
) -> None:
    if not wow or not ENABLE_WOW_ADVANCED_EFFECTS:
        return

    fps = float(meta.get("fps") or FPS_FALLBACK)
    mats: dict = wow.get("materials", {})
    lens_a = wow.get("lens_a")
    lens_b = wow.get("lens_b")
    shock_rig = wow.get("shock_rig")
    shock_rings = wow.get("shock_rings", [])
    plasma_arcs = wow.get("plasma_arcs", [])
    beams = wow.get("beams", [])
    dust_rig = wow.get("dust_rig")
    ribbons = wow.get("ribbons", [])

    for index, sample in enumerate(audio_frames):
        if WOW_KEYFRAME_STRIDE > 1 and index % WOW_KEYFRAME_STRIDE != 0:
            if float(sample.get("beat", 0.0)) < 0.5 and float(sample.get("onset", 0.0)) < ONSET_KEY_THRESHOLD:
                continue

        low = clamp(sample.get("low", 0.0))
        mid = clamp(sample.get("mid", 0.0))
        high = clamp(sample.get("high", 0.0))
        onset = clamp(sample.get("onset", 0.0))
        beat = clamp(sample.get("beat", 0.0))
        energy = clamp(0.38 * low + 0.38 * mid + 0.24 * high)
        pulse = clamp(max(beat, onset * 0.85))
        t = float(sample.get("time", 0.0))
        frame = event_frame(sample, fps)

        if lens_a:
            lens_a.scale = (1.0 + 0.16 * low + 0.13 * pulse, 1.0 + 0.12 * mid, 1.0 + 0.10 * high)
            lens_a.rotation_euler = (0.03 * t, 0.02 * math.sin(t * 0.17), 0.10 * t)
            lens_a.keyframe_insert("scale", frame=frame)
            lens_a.keyframe_insert("rotation_euler", frame=frame)
            for mod in lens_a.modifiers:
                if mod.type == "DISPLACE":
                    mod.strength = 0.018 + 0.060 * low + 0.030 * onset
                    mod.keyframe_insert("strength", frame=frame)
        if lens_b:
            lens_b.scale = (1.0 + 0.15 * high + 0.12 * pulse, 1.0 + 0.10 * mid, 1.0 + 0.13 * low)
            lens_b.rotation_euler = (-0.025 * t, 0.025 * math.cos(t * 0.13), -0.09 * t)
            lens_b.keyframe_insert("scale", frame=frame)
            lens_b.keyframe_insert("rotation_euler", frame=frame)
            for mod in lens_b.modifiers:
                if mod.type == "DISPLACE":
                    mod.strength = 0.018 + 0.055 * high + 0.030 * onset
                    mod.keyframe_insert("strength", frame=frame)

        barycenter = (focus_a["root"].location + focus_b["root"].location) * 0.5

        if shock_rig:
            shock_rig.location = barycenter + Vector((0.0, 0.0, 0.02))
            shock_rig.rotation_euler = (0.06 * math.sin(t * 0.15), 0.08 * math.cos(t * 0.11), 0.23 * t)
            shock_rig.scale = (1.0 + 0.035 * energy, 1.0 + 0.035 * energy, 1.0)
            shock_rig.keyframe_insert("location", frame=frame)
            shock_rig.keyframe_insert("rotation_euler", frame=frame)
            shock_rig.keyframe_insert("scale", frame=frame)

        if shock_rings:
            cycle = 1.65
            for i, ring in enumerate(shock_rings):
                local = ((t + i * cycle / len(shock_rings)) % cycle) / cycle
                fade = max(0.0, 1.0 - local)
                burst = smoothstep(pulse) * 0.95 + 0.15 * energy
                s = 0.35 + 4.4 * local + 1.7 * burst
                ring.scale = (s, s, 1.0)
                ring.rotation_euler.z += 0.002 * (i + 1) + 0.012 * mid
                ring.keyframe_insert("scale", frame=frame)
                ring.keyframe_insert("rotation_euler", frame=frame)
                if "shock" in mats and i < len(mats["shock"]):
                    set_material_alpha(mats["shock"][i], clamp(0.02 + 0.14 * fade * burst, 0.01, 0.22), frame)
                    set_material_emission_strength(mats["shock"][i], FLASH_REDUCTION_FACTOR * (0.05 + 0.45 * fade * burst + 0.10 * high), frame)

        if plasma_arcs:
            for i, arc in enumerate(plasma_arcs):
                phase = i / max(1, len(plasma_arcs) - 1)
                arc.rotation_euler = (0.05 * math.sin(t * 0.31 + phase), 0.10 * math.cos(t * 0.23 + phase), 0.18 * math.sin(t * 0.19 + phase))
                arc.scale = (1.0 + 0.05 * pulse, 1.0 + 0.28 * high + 0.12 * onset, 1.0 + 0.10 * mid)
                arc.keyframe_insert("rotation_euler", frame=frame)
                arc.keyframe_insert("scale", frame=frame)
                set_curve_bevel(arc, 0.003 + 0.012 * onset + 0.004 * mid, frame)
            if "arc" in mats:
                set_material_alpha(mats["arc"], clamp(0.06 + 0.14 * onset + 0.06 * beat, 0.04, 0.20), frame)
                set_material_emission_strength(mats["arc"], FLASH_REDUCTION_FACTOR * (0.10 + 0.55 * onset + 0.16 * mid), frame)

        if beams:
            targets = [focus_a["root"].location, focus_b["root"].location, barycenter + Vector((0.0, 0.0, 0.08 + 0.25 * energy))]
            for i, beam in enumerate(beams):
                target = targets[min(i, len(targets) - 1)]
                direction = target - beam.location
                beam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
                beam.data.energy = 30 + 140 * pulse + 60 * energy + (35 * low if i == 0 else 35 * high if i == 1 else 45 * mid)
                beam.data.spot_size = math.radians(16 + 10 * energy + 6 * pulse)
                beam.keyframe_insert("rotation_euler", frame=frame)
                beam.data.keyframe_insert("energy", frame=frame)
                beam.data.keyframe_insert("spot_size", frame=frame)

        if dust_rig:
            dust_rig.rotation_euler = (0.05 * math.sin(t * 0.05), 0.04 * math.cos(t * 0.04), 0.055 * t * (1.0 + 0.35 * mid))
            ds = 1.0 + 0.020 * energy + 0.026 * pulse
            dust_rig.scale = (ds, ds, ds)
            dust_rig.keyframe_insert("rotation_euler", frame=frame)
            dust_rig.keyframe_insert("scale", frame=frame)
            if "dust" in mats:
                set_material_emission_strength(mats["dust"], FLASH_REDUCTION_FACTOR * (0.03 + 0.12 * high + 0.08 * pulse), frame)

        if ribbons:
            for idx, ribbon in enumerate(ribbons):
                direction = 1.0 if idx == 0 else -1.0
                ribbon.location = barycenter
                ribbon.rotation_euler = (0.08 * math.sin(t * 0.09), 0.04 * math.cos(t * 0.12), direction * 0.36 * t * (1.0 + 0.30 * mid))
                ribbon.scale = (1.0 + 0.05 * mid, 1.0 + 0.05 * mid, 1.0 + 0.18 * pulse)
                ribbon.keyframe_insert("location", frame=frame)
                ribbon.keyframe_insert("rotation_euler", frame=frame)
                ribbon.keyframe_insert("scale", frame=frame)
                set_curve_bevel(ribbon, 0.003 + 0.008 * energy + 0.004 * pulse, frame)
            if "vortex" in mats:
                set_material_alpha(mats["vortex"], clamp(0.05 + 0.10 * energy + 0.05 * pulse, 0.04, 0.18), frame)
                set_material_emission_strength(mats["vortex"], FLASH_REDUCTION_FACTOR * (0.05 + 0.20 * mid + 0.12 * pulse), frame)

        # DOF dinamica: sui beat apre leggermente il fuoco e simula pressione cinematica senza scatti.
        if camera and camera.data and camera.data.dof:
            camera.data.dof.aperture_fstop = 6.2 - 1.35 * pulse + 0.45 * (1.0 - energy)
            camera.data.dof.focus_distance = 7.4 - 0.45 * pulse + 0.20 * math.sin(t * 0.07)
            camera.data.dof.keyframe_insert("aperture_fstop", frame=frame)
            camera.data.dof.keyframe_insert("focus_distance", frame=frame)

    animated_objects: list[bpy.types.Object] = []
    for key in ("lens_a", "lens_b", "shock_rig", "dust_rig"):
        obj = wow.get(key)
        if obj:
            animated_objects.append(obj)
    for key in ("shock_rings", "plasma_arcs", "beams", "ribbons"):
        for obj in wow.get(key, []):
            animated_objects.append(obj)

    for obj in animated_objects:
        set_interpolation(obj, "LINEAR")
        if getattr(obj, "data", None):
            set_interpolation(obj.data, "LINEAR")
    for mat in mats.values():
        if isinstance(mat, list):
            for submat in mat:
                set_interpolation(submat, "LINEAR")
                if submat.use_nodes:
                    set_interpolation(submat.node_tree, "LINEAR")
        elif hasattr(mat, "use_nodes"):
            set_interpolation(mat, "LINEAR")
            if mat.use_nodes:
                set_interpolation(mat.node_tree, "LINEAR")


def setup_wow_compositor() -> bool:
    """Configura il compositor in modo compatibile con Blender 5.1.

    In alcune build di Blender 5.x l'attributo scene.node_tree può non essere
    disponibile subito dopo scene.use_nodes = True, oppure può essere esposto
    con API differente. Questo wrapper non deve mai bloccare la generazione
    della scena: se il compositor non è disponibile, gli effetti 3D restano attivi.
    """
    if not ENABLE_WOW_COMPOSITOR:
        print("[INFO] WOW compositor disabilitato da config.")
        return False

    scene = bpy.context.scene

    try:
        scene.use_nodes = True
    except Exception as exc:
        print(f"[WARN] Impossibile abilitare il compositor: {exc}")
        return False

    tree = getattr(scene, "node_tree", None)
    if tree is None:
        tree = getattr(scene, "compositor_node_tree", None)

    if tree is None:
        print(
            "[WARN] Compositor non disponibile in questa build/API Blender 5.1. "
            "Salto i nodi compositor e continuo con gli effetti 3D."
        )
        return False

    try:
        nodes = tree.nodes
        links = tree.links
        nodes.clear()

        render_layers = nodes.new("CompositorNodeRLayers")
        render_layers.location = (0, 0)

        glare = nodes.new("CompositorNodeGlare")
        glare.location = (240, 0)
        if hasattr(glare, "glare_type"):
            glare.glare_type = "FOG_GLOW"
        if hasattr(glare, "quality"):
            glare.quality = "MEDIUM"
        if hasattr(glare, "threshold"):
            glare.threshold = 0.44
        if hasattr(glare, "size"):
            glare.size = 8

        lens = nodes.new("CompositorNodeLensdist")
        lens.location = (480, 0)
        if "Distort" in lens.inputs:
            lens.inputs["Distort"].default_value = 0.010
        if "Dispersion" in lens.inputs:
            lens.inputs["Dispersion"].default_value = 0.014

        hue = nodes.new("CompositorNodeHueSat")
        hue.location = (720, 0)
        if hasattr(hue, "color_saturation"):
            hue.color_saturation = 1.08
        if hasattr(hue, "color_value"):
            hue.color_value = 1.015

        curves = nodes.new("CompositorNodeCurveRGB")
        curves.location = (950, 0)
        try:
            curves.mapping.curves[3].points[1].location = (0.82, 0.94)
        except Exception:
            pass

        composite = nodes.new("CompositorNodeComposite")
        composite.location = (1180, 0)

        viewer = nodes.new("CompositorNodeViewer")
        viewer.location = (1180, -160)

        links.new(render_layers.outputs["Image"], glare.inputs["Image"])
        links.new(glare.outputs["Image"], lens.inputs["Image"])
        links.new(lens.outputs["Image"], hue.inputs["Image"])
        links.new(hue.outputs["Image"], curves.inputs["Image"])
        links.new(curves.outputs["Image"], composite.inputs["Image"])
        links.new(curves.outputs["Image"], viewer.inputs["Image"])

        print("[OK] WOW compositor configurato.")
        return True

    except Exception as exc:
        print(f"[WARN] Setup compositor saltato per incompatibilita API Blender 5.1: {exc}")
        return False

# =============================================================================
# ANIMAZIONE AUDIO-REACTIVE
# =============================================================================

def event_frame(audio_frame: dict, fps: float) -> int:
    # I frame audio partono da t=0; Blender da 1.
    return int(round(float(audio_frame.get("time", 0.0)) * fps)) + 1


def is_main_key(audio_frame: dict, index: int) -> bool:
    if MAIN_KEYFRAME_STRIDE <= 1 or index % MAIN_KEYFRAME_STRIDE == 0:
        return True
    return float(audio_frame.get("beat", 0.0)) >= 0.5 or float(audio_frame.get("onset", 0.0)) >= ONSET_KEY_THRESHOLD


def is_satellite_key(audio_frame: dict, index: int) -> bool:
    if SATELLITE_KEYFRAME_STRIDE <= 1 or index % SATELLITE_KEYFRAME_STRIDE == 0:
        return True
    return float(audio_frame.get("beat", 0.0)) >= 0.5 or float(audio_frame.get("onset", 0.0)) >= ONSET_KEY_THRESHOLD


def animate_scene(
    audio_frames: list[dict],
    meta: dict,
    focus_a: dict[str, bpy.types.Object],
    focus_b: dict[str, bpy.types.Object],
    satellite_data: dict[str, list[dict]],
    materials: dict[str, bpy.types.Material],
    lights: dict[str, bpy.types.Object],
    camera: bpy.types.Object,
    force_fields: dict[str, bpy.types.Object],
) -> None:
    fps = float(meta.get("fps") or FPS_FALLBACK)
    root_a = focus_a["root"]
    root_b = focus_b["root"]
    visual_a = focus_a.get("visual")
    visual_b = focus_b.get("visual")
    aura_a = focus_a["aura"]
    aura_b = focus_b["aura"]
    disp_a = aura_a.modifiers.get("GravityCore_A_audio_displace") or next((m for m in aura_a.modifiers if m.type == "DISPLACE"), None)
    disp_b = aura_b.modifiers.get("GravityCore_B_audio_displace") or next((m for m in aura_b.modifiers if m.type == "DISPLACE"), None)

    orbit_a = satellite_data["rigs"][0]["obj"]
    orbit_b = satellite_data["rigs"][1]["obj"]
    orbit_shared = satellite_data["rigs"][2]["obj"]
    ring_a = satellite_data["rings"][0]["obj"]
    ring_b = satellite_data["rings"][1]["obj"]
    ring_shared = satellite_data["rings"][2]["obj"]

    for index, sample in enumerate(audio_frames):
        low = clamp(sample.get("low", 0.0))
        mid = clamp(sample.get("mid", 0.0))
        high = clamp(sample.get("high", 0.0))
        onset = clamp(sample.get("onset", 0.0))
        beat = clamp(sample.get("beat", 0.0))
        energy = clamp(0.42 * low + 0.36 * mid + 0.22 * high)
        pulse = clamp(max(beat, onset * 0.78))
        t = float(sample.get("time", 0.0))
        frame = event_frame(sample, fps)

        if is_main_key(sample, index):
            binary_angle = 0.082 * t + 0.10 * math.sin(t * 0.07) + 0.06 * mid
            axis = Vector((math.cos(binary_angle), 0.42 * math.sin(binary_angle), 0.0))
            if axis.length < 1e-6:
                axis = Vector((1.0, 0.0, 0.0))
            axis.normalize()
            perp = Vector((-axis.y, axis.x, 0.0))

            contact_drive = clamp(0.55 * low + 0.35 * pulse + 0.24 * mid)
            elastic_cycle = 0.5 + 0.5 * math.sin(t * (1.55 + 0.65 * mid) + 0.9 * onset)
            contact_mix = clamp(0.74 * contact_drive + 0.26 * contact_drive * elastic_cycle)

            base_scale_a = max(0.78, 0.86 + 0.08 * smoothstep(low) + 0.05 * pulse)
            base_scale_b = max(0.78, 0.86 + 0.08 * smoothstep(high) + 0.04 * smoothstep(mid) + 0.05 * pulse)
            radius_a = CORE_PROCEDURAL_RADIUS * base_scale_a
            radius_b = CORE_PROCEDURAL_RADIUS * base_scale_b
            touch_distance = radius_a + radius_b + CORE_CONTACT_GAP
            extra_distance = 0.05 + 1.05 * (1.0 - contact_mix) + CORE_AUDIO_EXPAND_DISTANCE * smoothstep(high)
            center_distance = max(touch_distance, touch_distance + extra_distance)
            separation = center_distance * 0.5

            base_center = Vector((0.0, 0.0, CORE_VERTICAL_BASE + 0.03 * math.sin(t * 0.21)))
            lateral_sway = 0.14 * math.sin(t * 0.33) * (1.0 - 0.35 * contact_mix)
            vertical_a = 0.08 * smoothstep(low) + 0.025 * math.sin(t * 0.31) + 0.020 * elastic_cycle
            vertical_b = 0.08 * smoothstep(high) + 0.025 * math.cos(t * 0.27) - 0.020 * elastic_cycle

            root_a.location = base_center - axis * separation - perp * lateral_sway + Vector((0.0, 0.0, vertical_a))
            root_b.location = base_center + axis * separation + perp * lateral_sway + Vector((0.0, 0.0, vertical_b))
            barycenter = (root_a.location + root_b.location) * 0.5

            contact_amount = clamp(1.0 - (center_distance - touch_distance) / 0.42)
            squash_a = CORE_ELASTIC_SQUASH_MAX * (0.35 + 0.65 * contact_amount)
            squash_b = CORE_ELASTIC_SQUASH_MAX * (0.32 + 0.68 * contact_amount)
            squeeze_a = base_scale_a * (1.0 - squash_a * contact_mix)
            squeeze_b = base_scale_b * (1.0 - squash_b * contact_mix)
            bulge_a = base_scale_a * (1.0 + CORE_ELASTIC_BULGE_FACTOR * squash_a * contact_mix)
            bulge_b = base_scale_b * (1.0 + CORE_ELASTIC_BULGE_FACTOR * squash_b * contact_mix)
            root_a.scale = (squeeze_a, bulge_a, base_scale_a * (1.0 + 0.45 * squash_a * contact_mix + 0.04 * pulse))
            root_b.scale = (squeeze_b, bulge_b, base_scale_b * (1.0 + 0.45 * squash_b * contact_mix + 0.04 * pulse))

            root_a.rotation_euler = (0.05 * high, 0.12 * mid, binary_angle + 0.10 * onset)
            root_b.rotation_euler = (-0.05 * low, -0.12 * mid, binary_angle + math.pi - 0.10 * onset)

            aura_local_a = 1.0 + 0.12 * energy + 0.16 * contact_mix
            aura_local_b = 1.0 + 0.12 * energy + 0.16 * contact_mix
            aura_a.scale = (1.0 - 0.06 * contact_mix, aura_local_a, 1.0 + 0.10 * contact_mix)
            aura_b.scale = (1.0 - 0.06 * contact_mix, aura_local_b, 1.0 + 0.10 * contact_mix)

            if visual_a and visual_a != root_a:
                visual_a.scale = (1.0, 1.0, 1.0)
                visual_a.keyframe_insert("scale", frame=frame)
            if visual_b and visual_b != root_b:
                visual_b.scale = (1.0, 1.0, 1.0)
                visual_b.keyframe_insert("scale", frame=frame)

            for root in (root_a, root_b):
                root.keyframe_insert("location", frame=frame)
                root.keyframe_insert("scale", frame=frame)
                root.keyframe_insert("rotation_euler", frame=frame)
            aura_a.keyframe_insert("scale", frame=frame)
            aura_b.keyframe_insert("scale", frame=frame)

            if disp_a:
                disp_a.strength = 0.030 + 0.14 * low + 0.10 * onset + 0.08 * contact_amount
                disp_a.keyframe_insert("strength", frame=frame)
            if disp_b:
                disp_b.strength = 0.030 + 0.14 * high + 0.10 * onset + 0.08 * contact_amount
                disp_b.keyframe_insert("strength", frame=frame)

            # I rig orbitali simulano gravita: low = contrazione, mid = velocita angolare, high = eccitazione verticale.
            pull_a = 1.0 - 0.18 * smoothstep(low) + 0.05 * high
            pull_b = 1.0 - 0.16 * smoothstep(high) + 0.05 * low
            pull_shared = 1.0 - 0.12 * smoothstep(energy) + 0.04 * pulse

            orbit_a.location = root_a.location
            orbit_b.location = root_b.location
            orbit_shared.location = barycenter + Vector((0.0, 0.0, 0.06 + 0.08 * math.sin(t * 0.13)))
            orbit_a.scale = (pull_a, pull_a, pull_a)
            orbit_b.scale = (pull_b, pull_b, pull_b)
            orbit_shared.scale = (pull_shared, pull_shared, pull_shared)
            orbit_a.rotation_euler = (0.20 * mid, 0.15 * high, 1.45 * t * (1.0 + 0.45 * mid) + 0.4 * beat)
            orbit_b.rotation_euler = (-0.14 * low, 0.18 * mid, -1.32 * t * (1.0 + 0.38 * mid) - 0.35 * beat)
            orbit_shared.rotation_euler = (0.18 * math.sin(t * 0.11), 0.12 * math.cos(t * 0.09), 0.42 * t * (1.0 + 0.55 * mid))

            for rig in (orbit_a, orbit_b, orbit_shared):
                rig.keyframe_insert("location", frame=frame)
                rig.keyframe_insert("scale", frame=frame)
                rig.keyframe_insert("rotation_euler", frame=frame)

            ring_a.scale = (1.0 + 0.06 * high, 1.0 + 0.06 * high, 1.0)
            ring_b.scale = (1.0 + 0.06 * low, 1.0 + 0.06 * low, 1.0)
            ring_shared.scale = (1.0 + 0.04 * pulse, 1.0 + 0.04 * pulse, 1.0)
            for ring in (ring_a, ring_b, ring_shared):
                ring.keyframe_insert("scale", frame=frame)

            set_material_emission_strength(materials["core_a"], FLASH_REDUCTION_FACTOR * (0.50 + 1.40 * low + 0.60 * pulse), frame)
            set_material_emission_strength(materials["core_b"], FLASH_REDUCTION_FACTOR * (0.48 + 1.35 * high + 0.45 * mid + 0.52 * pulse), frame)
            set_material_emission_strength(materials["aura_a"], FLASH_REDUCTION_FACTOR * (0.08 + 0.42 * low + 0.24 * onset), frame)
            set_material_emission_strength(materials["aura_b"], FLASH_REDUCTION_FACTOR * (0.08 + 0.40 * high + 0.22 * onset), frame)
            set_material_alpha(materials["aura_a"], clamp(0.08 + 0.08 * energy + 0.06 * onset, 0.07, 0.22), frame)
            set_material_alpha(materials["aura_b"], clamp(0.08 + 0.08 * high + 0.06 * onset, 0.07, 0.22), frame)
            set_material_emission_strength(materials["orbit"], FLASH_REDUCTION_FACTOR * (0.05 + 0.20 * mid + 0.10 * pulse), frame)
            set_material_emission_strength(materials["sat_low"], FLASH_REDUCTION_FACTOR * (0.06 + 0.34 * low + 0.16 * beat), frame)
            set_material_emission_strength(materials["sat_mid"], FLASH_REDUCTION_FACTOR * (0.06 + 0.30 * mid + 0.14 * beat), frame)
            set_material_emission_strength(materials["sat_high"], FLASH_REDUCTION_FACTOR * (0.06 + 0.36 * high + 0.18 * onset), frame)
            set_material_volume_density(materials["fog_main"], FOG_MAIN_DENSITY + FOG_PULSE_AMOUNT * (0.35 * energy + 0.65 * pulse), frame)
            set_material_volume_density(materials["fog_layer"], FOG_LAYER_DENSITY + (FOG_PULSE_AMOUNT * 1.35) * (0.45 * low + 0.35 * energy + 0.20 * pulse), frame)

            lights["key"].data.energy = 320 + 520 * energy + 260 * pulse
            lights["A"].location = root_a.location + Vector((-0.6, -1.2, 1.4))
            lights["B"].location = root_b.location + Vector((0.6, -1.2, 1.4))
            lights["A"].data.energy = 70 + 360 * low + 160 * beat
            lights["B"].data.energy = 70 + 360 * high + 160 * onset
            for light in lights.values():
                light.keyframe_insert("location", frame=frame)
                light.data.keyframe_insert("energy", frame=frame)

            force_fields["A_force"].location = root_a.location
            force_fields["B_force"].location = root_b.location
            force_fields["A_vortex"].location = root_a.location
            force_fields["B_vortex"].location = root_b.location
            force_fields["A_force"].field.strength = -18.0 - 70.0 * low - 18.0 * beat
            force_fields["B_force"].field.strength = -18.0 - 70.0 * high - 18.0 * onset
            force_fields["A_vortex"].field.strength = 8.0 + 42.0 * mid
            force_fields["B_vortex"].field.strength = -8.0 - 42.0 * mid
            for field in force_fields.values():
                field.keyframe_insert("location", frame=frame)
                field.field.keyframe_insert("strength", frame=frame)

            cam_radius = 10.4 - 0.26 * pulse + 0.28 * math.sin(t * 0.05)
            cam_x = 0.36 * math.sin(t * 0.085) + barycenter.x * 0.24
            cam_z = 3.45 + 0.18 * energy + 0.10 * math.cos(t * 0.06) + barycenter.z * 0.05
            camera.location = (cam_x, -cam_radius + barycenter.y * 0.12, cam_z)
            target = barycenter + Vector((0.0, 0.0, 0.05 + 0.16 * energy))
            direction = target - camera.location
            camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
            camera.data.lens = 44 + 4 * smoothstep(mid) - 2 * pulse
            camera.keyframe_insert("location", frame=frame)
            camera.keyframe_insert("rotation_euler", frame=frame)
            camera.data.keyframe_insert("lens", frame=frame)

        if is_satellite_key(sample, index):
            # Inner A/B: movimento orbitale deterministico con raggio contratto dal "pozzo" gravitazionale.
            for entry in satellite_data["A"]:
                obj = entry["obj"]
                phase = entry["phase"]
                r = entry["base_radius"] * (1.0 - 0.30 * smoothstep(low) + 0.12 * smoothstep(high))
                ang = phase + entry["speed"] * t * (1.0 + 0.35 * mid) + 0.08 * onset
                z = 0.20 * math.sin(ang * 2.3 + t * 0.19) + 0.22 * high
                obj.location = (r * math.cos(ang), 0.72 * r * math.sin(ang), z)
                s = entry["size"] * (1.0 + INNER_SATELLITE_ANIM_SCALE_A * high + 0.42 * onset)
                obj.scale = (s / entry["size"], s / entry["size"], s / entry["size"])
                obj.keyframe_insert("location", frame=frame)
                obj.keyframe_insert("scale", frame=frame)

            for entry in satellite_data["B"]:
                obj = entry["obj"]
                phase = entry["phase"]
                r = entry["base_radius"] * (1.0 - 0.28 * smoothstep(high) + 0.12 * smoothstep(low))
                ang = phase + entry["speed"] * t * (1.0 + 0.35 * mid) - 0.08 * onset
                z = 0.20 * math.cos(ang * 2.1 + t * 0.17) + 0.20 * low
                obj.location = (r * math.cos(ang), 0.72 * r * math.sin(ang), z)
                s = entry["size"] * (1.0 + INNER_SATELLITE_ANIM_SCALE_B * low + 0.46 * beat)
                obj.scale = (s / entry["size"], s / entry["size"], s / entry["size"])
                obj.keyframe_insert("location", frame=frame)
                obj.keyframe_insert("scale", frame=frame)

            for entry in satellite_data["shared"]:
                obj = entry["obj"]
                phase = entry["phase"]
                r = entry["base_radius"] * (1.0 - 0.14 * smoothstep(energy) + 0.08 * onset)
                ang = phase + entry["speed"] * t * (1.0 + 0.45 * mid)
                z = 0.36 * math.sin(ang * 1.8 + t * 0.08) + 0.35 * (high - low)
                obj.location = (r * math.cos(ang), 0.58 * r * math.sin(ang), z)
                s = entry["size"] * (1.0 + OUTER_SATELLITE_ANIM_SCALE * energy + 0.38 * pulse)
                obj.scale = (s / entry["size"], s / entry["size"], s / entry["size"])
                obj.keyframe_insert("location", frame=frame)
                obj.keyframe_insert("scale", frame=frame)

    animated_objects = [
        root_a,
        root_b,
        aura_a,
        aura_b,
        orbit_a,
        orbit_b,
        orbit_shared,
        ring_a,
        ring_b,
        ring_shared,
        camera,
        *lights.values(),
        *force_fields.values(),
    ]
    for group in (satellite_data["A"], satellite_data["B"], satellite_data["shared"]):
        animated_objects.extend(entry["obj"] for entry in group)

    for obj in animated_objects:
        set_interpolation(obj, "LINEAR")
        if hasattr(obj, "data") and obj.data:
            set_interpolation(obj.data, "LINEAR")
    for mat in materials.values():
        set_interpolation(mat, "LINEAR")
        if mat.use_nodes:
            set_interpolation(mat.node_tree, "LINEAR")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    keyframe_path = find_file(KEYFRAME_JSON_NAME)
    try:
        inventory_path = find_file(ASSET_INVENTORY_JSON_NAME)
        inventory = load_json(inventory_path)
    except FileNotFoundError:
        inventory = {"assets": []}

    data = load_json(keyframe_path)
    meta = data.get("meta", {})
    audio_path = resolve_audio_path(meta)
    audio_frames = data.get("frames", [])
    if not audio_frames:
        raise ValueError(f"Nessun frame audio trovato in {keyframe_path}")

    clear_scene()
    setup_scene(meta)
    compositor_enabled = setup_wow_compositor()

    root_collection = ensure_collection("Ready_To_Jazz_Dual_Gravity_AudioScene")
    audio_loaded = attach_audio_to_scene(audio_path, root_collection)
    materials = make_materials()
    make_environment(materials, root_collection)
    lights = make_lights(root_collection)
    camera = make_camera(root_collection)

    ball_asset = find_primary_ball_asset(inventory)
    focus_a = create_central_focus(
        "GravityCore_A",
        (-CORE_BASE_HALF_DISTANCE, 0.0, 0.90),
        materials["core_a"],
        materials["aura_a"],
        ball_asset,
        root_collection,
    )
    focus_b = create_central_focus(
        "GravityCore_B",
        (CORE_BASE_HALF_DISTANCE, 0.0, 0.90),
        materials["core_b"],
        materials["aura_b"],
        ball_asset,
        root_collection,
    )

    satellites = make_satellites(materials, root_collection)
    wow_effects = make_wow_effects(root_collection, focus_a, focus_b)

    force_fields = {
        "A_force": add_force_field("GravityCore_A_negative_force_well", "FORCE", focus_a["root"].location, root_collection),
        "B_force": add_force_field("GravityCore_B_negative_force_well", "FORCE", focus_b["root"].location, root_collection),
        "A_vortex": add_force_field("GravityCore_A_vortex_field", "VORTEX", focus_a["root"].location, root_collection),
        "B_vortex": add_force_field("GravityCore_B_vortex_field", "VORTEX", focus_b["root"].location, root_collection),
    }

    animate_scene(audio_frames, meta, focus_a, focus_b, satellites, materials, lights, camera, force_fields)
    animate_wow_effects(audio_frames, meta, wow_effects, focus_a, focus_b, camera)

    # Etichetta tecnica in scena, utile quando si riapre il file.
    font_curve = bpy.data.curves.new("scene_generation_note_curve", type="FONT")
    font_curve.body = (
        "Ready To Jazz - Luca Vera | dual gravity scene | keyframes from analysis_blender_keyframes JSON"
    )
    font_curve.align_x = "CENTER"
    font_curve.size = 0.12
    font_obj = bpy.data.objects.new("scene_generation_note", font_curve)
    font_obj.location = (0.0, 3.65, 0.05)
    font_obj.rotation_euler = (math.radians(90), 0, 0)
    root_collection.objects.link(font_obj)

    bpy.context.scene.frame_set(1)
    print("=" * 80)
    print("Ready To Jazz dual gravity scene generata.")
    print(f"JSON keyframe: {keyframe_path}")
    print(f"Frame usati: {len(audio_frames)} | timeline: {bpy.context.scene.frame_start}-{bpy.context.scene.frame_end}")
    print(f"Primary ball asset: {ball_asset if ball_asset else 'fallback procedurale'}")
    print(f"Audio in scena/VSE: {'caricato' if audio_loaded else 'non trovato/non caricato'}")
    print(f"Distanza core half-base: {CORE_BASE_HALF_DISTANCE} Blender units")
    print(f"Core target size: {CORE_IMPORTED_TARGET_SIZE} | core procedural radius: {CORE_PROCEDURAL_RADIUS} | aura radius: {CORE_AURA_RADIUS}")
    print(f"Elastic touch: gap={CORE_CONTACT_GAP} | squash_max={CORE_ELASTIC_SQUASH_MAX} | bulge_factor={CORE_ELASTIC_BULGE_FACTOR}")
    print(f"Satellite size tuning: inner={INNER_SATELLITE_BASE_SIZE}+{INNER_SATELLITE_SIZE_STEP} step | outer={OUTER_SATELLITE_BASE_SIZE}+{OUTER_SATELLITE_SIZE_STEP} step")
    print(f"WOW advanced effects: {ENABLE_WOW_ADVANCED_EFFECTS}")
    print(f"Primary ball asset enabled: {USE_PRIMARY_BALL_ASSET}")
    print(f"Fog densities: main={FOG_MAIN_DENSITY} | layer={FOG_LAYER_DENSITY} | pulse={FOG_PULSE_AMOUNT}")
    print(f"WOW compositor: {'abilitato' if compositor_enabled else 'saltato/non disponibile'}")
    print(f"WOW shockwaves/arcs/lens/beams/dust: {ENABLE_WOW_SHOCKWAVES}/{ENABLE_WOW_PLASMA_ARCS}/{ENABLE_WOW_GRAVITY_LENS}/{ENABLE_WOW_LIGHT_BEAMS}/{ENABLE_WOW_STAR_DUST}")
    profile_key = normalize_youtube_profile(FINAL_YOUTUBE)
    profile_paths = output_paths_for_profile(profile_key)
    print(f"Final YouTube profile: {profile_key}")
    print(f"Output base: {profile_paths['base']}")
    print(f"Output frames: {profile_paths['frames']}")
    print(f"Output MP4 target: {profile_paths['mp4']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
