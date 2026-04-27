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
USE_PRIMARY_BALL_ASSET = True

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

# Impostazioni render leggere ma cinematografiche.
RENDER_ENGINE = "BLENDER_EEVEE_NEXT"  # fallback automatico su BLENDER_EEVEE se non disponibile
RESOLUTION_X = 3840
RESOLUTION_Y = 2160
FPS_FALLBACK = 30.0


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

def make_principled_emission_mat(
    name: str,
    base_color: tuple[float, float, float, float],
    emission_color: tuple[float, float, float, float],
    strength: float,
    metallic: float = 0.0,
    roughness: float = 0.35,
    alpha: float = 1.0,
) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (base_color[0], base_color[1], base_color[2], alpha)
    mat.use_nodes = True
    mat.blend_method = "BLEND" if alpha < 1.0 else "OPAQUE"
    mat.use_screen_refraction = False

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = base_color
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = emission_color
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = strength
    return mat


def set_material_emission_strength(mat: bpy.types.Material, strength: float, frame: int) -> None:
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
    if not mat.use_nodes:
        return
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf and "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = alpha
        bsdf.inputs["Alpha"].keyframe_insert("default_value", frame=frame)


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
# SCENA
# =============================================================================

def setup_scene(meta: dict) -> None:
    scene = bpy.context.scene
    fps = float(meta.get("fps") or FPS_FALLBACK)
    duration = float(meta.get("duration_sec") or 60.0)
    scene.frame_start = 1
    scene.frame_end = max(2, int(round(duration * fps)))
    scene.render.fps = int(round(fps))
    scene.render.resolution_x = RESOLUTION_X
    scene.render.resolution_y = RESOLUTION_Y
    scene.render.resolution_percentage = 50

    try:
        scene.render.engine = RENDER_ENGINE
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"

    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "use_bloom"):
            scene.eevee.use_bloom = True
        if hasattr(scene.eevee, "bloom_intensity"):
            scene.eevee.bloom_intensity = 0.18
        if hasattr(scene.eevee, "use_gtao"):
            scene.eevee.use_gtao = True

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
        "core_a": make_principled_emission_mat(
            "MAT_core_A_blue_gold", (0.08, 0.42, 0.72, 1.0), (0.10, 0.72, 1.0, 1.0), 1.6, metallic=0.25
        ),
        "core_b": make_principled_emission_mat(
            "MAT_core_B_green_white", (0.05, 0.62, 0.45, 1.0), (0.55, 1.0, 0.72, 1.0), 1.25, metallic=0.2
        ),
        "aura_a": make_principled_emission_mat(
            "MAT_aura_A_translucent", (0.05, 0.50, 0.95, 0.30), (0.1, 0.8, 1.0, 1.0), 0.55, alpha=0.32
        ),
        "aura_b": make_principled_emission_mat(
            "MAT_aura_B_translucent", (0.05, 0.95, 0.55, 0.28), (0.42, 1.0, 0.72, 1.0), 0.50, alpha=0.30
        ),
        "sat_low": make_principled_emission_mat(
            "MAT_satellite_low_mass", (0.92, 0.55, 0.18, 1.0), (1.0, 0.62, 0.20, 1.0), 0.65, metallic=0.15
        ),
        "sat_mid": make_principled_emission_mat(
            "MAT_satellite_mid_mass", (0.78, 0.92, 0.95, 1.0), (0.55, 0.95, 1.0, 1.0), 0.75, metallic=0.1
        ),
        "sat_high": make_principled_emission_mat(
            "MAT_satellite_high_mass", (0.78, 0.33, 0.92, 1.0), (0.95, 0.40, 1.0, 1.0), 1.0, metallic=0.1
        ),
        "orbit": make_principled_emission_mat(
            "MAT_orbit_lines_soft", (0.34, 0.86, 1.0, 0.22), (0.32, 0.88, 1.0, 1.0), 0.32, alpha=0.24
        ),
        "floor": make_principled_emission_mat(
            "MAT_deep_reflective_floor", (0.015, 0.052, 0.065, 1.0), (0.0, 0.18, 0.22, 1.0), 0.05, metallic=0.35, roughness=0.18
        ),
        "dome": make_principled_emission_mat(
            "MAT_soft_blue_green_dome", (0.02, 0.14, 0.18, 1.0), (0.0, 0.20, 0.24, 1.0), 0.18, roughness=0.7
        ),
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
        "MAT_wow_binary_plasma_arc", (0.55, 0.92, 1.0, 0.68), (0.55, 0.96, 1.0, 1.0), 1.8, 0.68
    )
    mats["dust"] = make_principled_emission_mat(
        "MAT_wow_depth_dust", (0.60, 0.92, 1.0, 1.0), (0.72, 0.96, 1.0, 1.0), 0.18, roughness=0.48
    )
    mats["vortex"] = make_transparent_emission_mat(
        "MAT_wow_vortex_ribbon", (0.25, 0.78, 1.0, 0.44), (0.20, 0.92, 1.0, 1.0), 0.75, 0.44
    )
    shock_mats: list[bpy.types.Material] = []
    for i in range(WOW_SHOCKWAVE_COUNT):
        shock_mats.append(
            make_transparent_emission_mat(
                f"MAT_wow_beat_shockwave_{i+1:02d}",
                (0.25, 0.85, 1.0, 0.24),
                (0.35, 0.95, 1.0, 1.0),
                0.35,
                0.20,
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
                    set_material_alpha(mats["shock"][i], clamp(0.05 + 0.55 * fade * burst, 0.02, 0.72), frame)
                    set_material_emission_strength(mats["shock"][i], 0.18 + 2.8 * fade * burst + 0.6 * high, frame)

        if plasma_arcs:
            for i, arc in enumerate(plasma_arcs):
                phase = i / max(1, len(plasma_arcs) - 1)
                arc.rotation_euler = (0.05 * math.sin(t * 0.31 + phase), 0.10 * math.cos(t * 0.23 + phase), 0.18 * math.sin(t * 0.19 + phase))
                arc.scale = (1.0 + 0.05 * pulse, 1.0 + 0.28 * high + 0.12 * onset, 1.0 + 0.10 * mid)
                arc.keyframe_insert("rotation_euler", frame=frame)
                arc.keyframe_insert("scale", frame=frame)
                set_curve_bevel(arc, 0.006 + 0.026 * onset + 0.010 * mid, frame)
            if "arc" in mats:
                set_material_alpha(mats["arc"], clamp(0.18 + 0.44 * onset + 0.20 * beat, 0.12, 0.78), frame)
                set_material_emission_strength(mats["arc"], 0.45 + 3.4 * onset + 1.0 * mid, frame)

        if beams:
            targets = [focus_a["root"].location, focus_b["root"].location, barycenter + Vector((0.0, 0.0, 0.08 + 0.25 * energy))]
            for i, beam in enumerate(beams):
                target = targets[min(i, len(targets) - 1)]
                direction = target - beam.location
                beam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
                beam.data.energy = 80 + 470 * pulse + 140 * energy + (90 * low if i == 0 else 90 * high if i == 1 else 120 * mid)
                beam.data.spot_size = math.radians(24 + 24 * energy + 14 * pulse)
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
                set_material_emission_strength(mats["dust"], 0.06 + 0.32 * high + 0.18 * pulse, frame)

        if ribbons:
            for idx, ribbon in enumerate(ribbons):
                direction = 1.0 if idx == 0 else -1.0
                ribbon.location = barycenter
                ribbon.rotation_euler = (0.08 * math.sin(t * 0.09), 0.04 * math.cos(t * 0.12), direction * 0.36 * t * (1.0 + 0.30 * mid))
                ribbon.scale = (1.0 + 0.05 * mid, 1.0 + 0.05 * mid, 1.0 + 0.18 * pulse)
                ribbon.keyframe_insert("location", frame=frame)
                ribbon.keyframe_insert("rotation_euler", frame=frame)
                ribbon.keyframe_insert("scale", frame=frame)
                set_curve_bevel(ribbon, 0.007 + 0.018 * energy + 0.010 * pulse, frame)
            if "vortex" in mats:
                set_material_alpha(mats["vortex"], clamp(0.16 + 0.32 * energy + 0.20 * pulse, 0.12, 0.65), frame)
                set_material_emission_strength(mats["vortex"], 0.25 + 1.4 * mid + 0.9 * pulse, frame)

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

            set_material_emission_strength(materials["core_a"], 0.75 + 3.6 * low + 1.8 * pulse, frame)
            set_material_emission_strength(materials["core_b"], 0.75 + 3.2 * high + 1.4 * mid + 1.4 * pulse, frame)
            set_material_emission_strength(materials["aura_a"], 0.30 + 1.85 * low + 0.95 * onset, frame)
            set_material_emission_strength(materials["aura_b"], 0.30 + 1.75 * high + 0.85 * onset, frame)
            set_material_alpha(materials["aura_a"], 0.18 + 0.22 * energy + 0.16 * onset, frame)
            set_material_alpha(materials["aura_b"], 0.17 + 0.20 * high + 0.16 * onset, frame)
            set_material_emission_strength(materials["orbit"], 0.18 + 0.70 * mid + 0.35 * pulse, frame)
            set_material_emission_strength(materials["sat_low"], 0.30 + 1.70 * low + 0.60 * beat, frame)
            set_material_emission_strength(materials["sat_mid"], 0.30 + 1.60 * mid + 0.55 * beat, frame)
            set_material_emission_strength(materials["sat_high"], 0.30 + 1.80 * high + 0.65 * onset, frame)

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
    print(f"WOW compositor: {'abilitato' if compositor_enabled else 'saltato/non disponibile'}")
    print(f"WOW shockwaves/arcs/lens/beams/dust: {ENABLE_WOW_SHOCKWAVES}/{ENABLE_WOW_PLASMA_ARCS}/{ENABLE_WOW_GRAVITY_LENS}/{ENABLE_WOW_LIGHT_BEAMS}/{ENABLE_WOW_STAR_DUST}")
    print("=" * 80)


if __name__ == "__main__":
    main()
