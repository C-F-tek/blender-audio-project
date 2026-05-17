# Standalone Blender scene builder generated from Spaziotempo JSON context.
# Review-only draft: run inside Blender Text Editor with Alt+P.
from __future__ import annotations

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

TRACK_STEM = "LLL-Luca Vera_Master"
ANALYSIS_JSON = Path(
    "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\LLL-Luca Vera_Master_analysis.json"
)
MUSIC_CONTEXT_JSON = Path(
    "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\LLL-Luca Vera_Master_music_context.json"
)
AI_CONTEXT_JSON = Path(
    "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\LLL-Luca Vera_Master_analysis_ai_context.json"
)
BLENDER_KEYFRAMES_JSON = Path(
    "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\LLL-Luca Vera_Master_analysis_blender_keyframes.json"
)
ASSET_INVENTORY_JSON = (
    Path(
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\spaziotempo_asset_inventory.json"
    )
    if True
    else None
)
USE_DUAL_FOCUS = True


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def preferred_ball_asset_path(inventory: dict) -> Path | None:
    for asset in inventory.get("assets", []):
        if asset.get("role") == "primary_ball_asset":
            path = Path(asset.get("path") or "")
            if path.exists():
                return path
    return None


def import_asset_file(asset_file: Path) -> list[bpy.types.Object]:
    before = set(bpy.data.objects.keys())
    ext = asset_file.suffix.lower()
    if ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(asset_file))
    elif ext in {".glb", ".gltf"}:
        bpy.ops.import_scene.gltf(filepath=str(asset_file))
    elif ext == ".obj":
        try:
            bpy.ops.wm.obj_import(filepath=str(asset_file))
        except Exception:
            bpy.ops.import_scene.obj(filepath=str(asset_file))
    elif ext == ".blend":
        with bpy.data.libraries.load(str(asset_file), link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
        for obj in data_to.objects:
            if obj:
                bpy.context.collection.objects.link(obj)
    else:
        raise RuntimeError(f"Unsupported asset format: {asset_file}")
    new_names = set(bpy.data.objects.keys()) - before
    return [bpy.data.objects[name] for name in new_names if name in bpy.data.objects]


def get_world_bbox(objects: list[bpy.types.Object]):
    coords = []
    bpy.context.view_layer.update()
    for obj in objects:
        if obj.type == "EMPTY":
            coords.append(obj.matrix_world.translation.copy())
            continue
        if not hasattr(obj, "bound_box"):
            continue
        try:
            coords.extend([obj.matrix_world @ Vector(corner) for corner in obj.bound_box])
        except Exception:
            coords.append(obj.matrix_world.translation.copy())
    if not coords:
        return Vector((0, 0, 0)), Vector((1, 1, 1)), Vector((0, 0, 0))
    min_v = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
    max_v = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
    return (min_v + max_v) * 0.5, max_v - min_v, min_v


def make_asset_focus(
    name: str,
    asset_path: Path,
    location,
    material: bpy.types.Material,
    fallback_radius: float = 1.0,
) -> bpy.types.Object:
    try:
        objects = import_asset_file(asset_path)
    except Exception as exc:
        print(f"Asset import failed, using procedural sphere: {asset_path} / {exc}")
        return add_uv_sphere(name, fallback_radius, location, material, segments=96)
    meshes = [obj for obj in objects if obj.type == "MESH"]
    focus = meshes[0] if meshes else objects[0]
    focus.name = name
    for obj in objects:
        if obj != focus:
            matrix = obj.matrix_world.copy()
            obj.parent = focus
            obj.matrix_world = matrix
        if hasattr(obj.data, "materials"):
            obj.data.materials.clear()
            obj.data.materials.append(material)

    center, size, min_v = get_world_bbox(objects)
    max_dim = max(size.x, size.y, size.z, 0.0001)
    target_dim = fallback_radius * 2.0
    focus.scale = (target_dim / max_dim, target_dim / max_dim, target_dim / max_dim)
    bpy.context.view_layer.update()
    center, _size, min_v = get_world_bbox(objects)
    focus.location += Vector(location) - center
    focus.location.z += float(location[2]) - min_v.z
    focus["imported_asset_children"] = len(objects)
    return focus


def make_collection(name: str) -> bpy.types.Collection:
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection


def link_to(collection: bpy.types.Collection, obj: bpy.types.Object) -> None:
    for parent in list(obj.users_collection):
        parent.objects.unlink(obj)
    collection.objects.link(obj)


def create_material(name: str, color, emission_strength: float = 0.0) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = color
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = color
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.42
    return mat


def add_uv_sphere(
    name: str, radius: float, location, material: bpy.types.Material, segments: int = 64
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=max(16, segments // 2), radius=radius, location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.name = name + "Mesh"
    obj.data.materials.append(material)
    return obj


def add_text_label(
    text: str, location, size: float, material: bpy.types.Material
) -> bpy.types.Object:
    bpy.ops.object.text_add(location=location, rotation=(math.radians(72), 0.0, 0.0))
    obj = bpy.context.object
    obj.name = "AlbumTitle_Text"
    obj.data.body = text
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.025
    obj.data.materials.append(material)
    return obj


def animate_value(
    obj: bpy.types.Object, data_path: str, frames: list[tuple[int, float]], index: int | None = None
) -> None:
    for frame, value in frames:
        if index is None:
            setattr(obj, data_path, value)
            obj.keyframe_insert(data_path=data_path, frame=frame)
        else:
            current = getattr(obj, data_path)
            current[index] = value
            obj.keyframe_insert(data_path=data_path, frame=frame, index=index)


def keyframe_material_emission(mat: bpy.types.Material, frame: int, strength: float) -> None:
    if not mat.use_nodes or not mat.node_tree:
        return
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if not bsdf or "Emission Strength" not in bsdf.inputs:
        return
    socket = bsdf.inputs["Emission Strength"]
    socket.default_value = strength
    socket.keyframe_insert(data_path="default_value", frame=frame)


def apply_full_audio_keyframes(
    hero: bpy.types.Object,
    disp: bpy.types.Modifier,
    hero_mat: bpy.types.Material,
    keyframes: dict,
    fps: float,
) -> int:
    audio_frames = keyframes.get("frames") or []
    inserted = 0
    for audio in audio_frames:
        time_sec = float(audio.get("time") or 0.0)
        frame = int(round(time_sec * fps)) + 1
        low = float(audio.get("low") or 0.0)
        mid = float(audio.get("mid") or 0.0)
        high = float(audio.get("high") or 0.0)
        onset = float(audio.get("onset") or 0.0)
        beat = float(audio.get("beat") or 0.0)

        # Full-frame audio deformation: not only uniform scale, but an asymmetric pulse plus displacement.
        hero.scale = (
            1.0 + low * 0.12 + beat * 0.025,
            1.0 + mid * 0.075 + onset * 0.018,
            1.0 + high * 0.055 + low * 0.035,
        )
        hero.keyframe_insert(data_path="scale", frame=frame)

        disp.strength = 0.035 + low * 0.11 + mid * 0.045 + onset * 0.025 + beat * 0.018
        disp.keyframe_insert(data_path="strength", frame=frame)

        keyframe_material_emission(hero_mat, frame, 0.28 + high * 0.55 + onset * 0.22 + beat * 0.18)
        inserted += 1
    return inserted


def apply_full_audio_keyframes_inverted(
    hero: bpy.types.Object,
    disp: bpy.types.Modifier,
    hero_mat: bpy.types.Material,
    keyframes: dict,
    fps: float,
) -> int:
    audio_frames = keyframes.get("frames") or []
    inserted = 0
    for audio in audio_frames:
        time_sec = float(audio.get("time") or 0.0)
        frame = int(round(time_sec * fps)) + 1
        low = float(audio.get("low") or 0.0)
        mid = float(audio.get("mid") or 0.0)
        high = float(audio.get("high") or 0.0)
        onset = float(audio.get("onset") or 0.0)
        beat = float(audio.get("beat") or 0.0)
        hero.scale = (
            1.0 + high * 0.12 + onset * 0.018,
            1.0 + low * 0.075 + beat * 0.025,
            1.0 + mid * 0.055 + high * 0.035,
        )
        hero.keyframe_insert(data_path="scale", frame=frame)
        disp.strength = 0.035 + high * 0.11 + low * 0.045 + onset * 0.02
        disp.keyframe_insert(data_path="strength", frame=frame)
        keyframe_material_emission(hero_mat, frame, 0.25 + low * 0.45 + mid * 0.20 + beat * 0.22)
        inserted += 1
    return inserted


def build_scene() -> None:
    analysis = load_json(ANALYSIS_JSON)
    music = load_json(MUSIC_CONTEXT_JSON)
    ai_context = load_json(AI_CONTEXT_JSON)
    keyframes = load_json(BLENDER_KEYFRAMES_JSON)
    asset_inventory = load_json(ASSET_INVENTORY_JSON) if ASSET_INVENTORY_JSON else {}

    meta = (
        keyframes.get("meta")
        or analysis.get("meta")
        or (ai_context.get("analysis_summary") or {}).get("meta")
        or {}
    )
    fps = float(meta.get("fps") or 30.0)
    duration = float(meta.get("duration_sec") or 180.0)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = max(1, int(duration * fps))
    scene.render.fps = int(round(fps))

    clear_scene()
    col_core = make_collection("AI Scene Core")
    col_orbits = make_collection("AI Audio Orbits")
    col_fog = make_collection("AI Volumetric Forms")
    col_refs = make_collection("AI JSON References")

    hero_mat = create_material("AI_Hero_Material_MatterEmission", (0.70, 0.86, 0.88, 1.0), 0.45)
    counter_mat = create_material("AI_Hero_CounterMaterial_Ball", (0.95, 0.72, 0.45, 1.0), 0.55)
    accent_mat = create_material("AI_Accent_Emission_Material", (0.95, 0.72, 0.45, 1.0), 1.2)
    cool_mat = create_material("AI_Cool_Background_Material", (0.13, 0.38, 0.44, 1.0), 0.08)
    fog_mat = create_material("AI_Fog_Filament_Material", (0.48, 0.78, 0.84, 0.35), 0.12)
    text_mat = create_material("AI_Title_Material", (0.82, 0.91, 0.88, 1.0), 0.35)

    ball_asset = preferred_ball_asset_path(asset_inventory)
    hero_location = (-0.95, 0, 1.75) if USE_DUAL_FOCUS else (0, 0, 1.75)
    hero = add_uv_sphere(
        "AI_HeroAura_DeformableCore",
        1.20 if USE_DUAL_FOCUS else 1.35,
        hero_location,
        hero_mat,
        segments=96,
    )
    link_to(col_core, hero)
    disp = hero.modifiers.new("AI_Audio_Displace_LowMid", "DISPLACE")
    tex = bpy.data.textures.new("AI_Audio_Deformation_Texture", "VORONOI")
    tex.noise_scale = 1.15
    tex.intensity = 0.42
    disp.texture = tex
    disp.strength = 0.08

    counter_hero = None
    counter_disp = None
    if USE_DUAL_FOCUS:
        if ball_asset:
            counter_hero = make_asset_focus(
                "AI_BallAsset_CounterCore",
                ball_asset,
                (0.95, 0, 1.75),
                counter_mat,
                fallback_radius=1.12,
            )
        else:
            counter_hero = add_uv_sphere(
                "AI_CounterSphere_DeformableCore", 1.12, (0.95, 0, 1.75), counter_mat, segments=96
            )
        link_to(col_core, counter_hero)
        counter_disp = counter_hero.modifiers.new("AI_Audio_Displace_InvertedBall", "DISPLACE")
        counter_tex = bpy.data.textures.new("AI_Audio_Deformation_Texture_InvertedBall", "VORONOI")
        counter_tex.noise_scale = 1.35
        counter_tex.intensity = 0.38
        counter_disp.texture = counter_tex
        counter_disp.strength = 0.07

    segments = music.get("segments") or []
    sample_segments = segments[:: max(1, len(segments) // 16)] or segments[:16]
    for idx, segment in enumerate(sample_segments[:18]):
        controls = segment.get("controls") or {}
        angle = idx * (math.tau / max(1, len(sample_segments[:18])))
        band = segment.get("dominant_band") or controls.get("primary_band") or "mid"
        score = float(segment.get("intensity_score") or 0.2)
        radius = 3.4 + score * 1.8
        z = 1.45 + math.sin(angle * 2.0) * 0.55
        mat = accent_mat if band == "high" else cool_mat if band == "mid" else hero_mat
        sat = add_uv_sphere(
            f"AI_AudioSatellite_{idx + 1:02d}_{band}",
            0.12 + score * 0.18,
            (math.cos(angle) * radius, math.sin(angle) * radius, z),
            mat,
            segments=32,
        )
        link_to(col_orbits, sat)
        sat["segment_index"] = int(segment.get("index") or idx + 1)
        sat["audio_band"] = str(band)
        sat["json_start_sec"] = float(segment.get("start_sec") or 0.0)
        start_frame = int(float(segment.get("start_sec") or 0.0) * fps) + 1
        end_frame = int(float(segment.get("end_sec") or 0.0) * fps) + 1
        for frame, rot in [(start_frame, angle), (end_frame, angle + math.tau * (1.0 + score))]:
            sat.rotation_euler[2] = rot
            sat.keyframe_insert(data_path="rotation_euler", frame=frame, index=2)
        scale = 1.0 + float(controls.get("accent_emission") or score) * 0.85
        sat.scale = (scale, scale, scale)
        sat.keyframe_insert(data_path="scale", frame=start_frame)

    # Procedural fog represented as visible soft filaments instead of heavy volume simulation.
    for idx in range(24):
        angle = idx * math.tau / 24
        length = 0.9 + (idx % 5) * 0.24
        bpy.ops.mesh.primitive_cube_add(
            size=1, location=(math.cos(angle) * 2.6, math.sin(angle) * 2.6, 1.0 + (idx % 6) * 0.22)
        )
        fog = bpy.context.object
        fog.name = f"AI_FogFilament_{idx + 1:02d}"
        fog.scale = (0.035, length, 0.035)
        fog.rotation_euler[2] = angle
        fog.data.materials.append(fog_mat)
        link_to(col_fog, fog)
        for frame, mul in [(1, 0.65), (scene.frame_end // 2, 1.35), (scene.frame_end, 0.75)]:
            fog.scale = (0.035 * mul, length * mul, 0.035 * mul)
            fog.keyframe_insert(data_path="scale", frame=frame)

    title = add_text_label(TRACK_STEM.replace("_Master", ""), (0, -3.25, 0.72), 0.34, text_mat)
    link_to(col_refs, title)

    inserted_full_keyframes = apply_full_audio_keyframes(hero, disp, hero_mat, keyframes, fps)
    hero["full_audio_keyframes_inserted"] = inserted_full_keyframes
    if counter_hero and counter_disp:
        counter_inserted = apply_full_audio_keyframes_inverted(
            counter_hero, counter_disp, counter_mat, keyframes, fps
        )
        counter_hero["full_audio_keyframes_inserted"] = counter_inserted
        counter_hero["source_asset"] = str(ball_asset) if ball_asset else "procedural_fallback"

    bpy.ops.object.light_add(
        type="AREA", location=(0, -4.8, 4.8), rotation=(math.radians(60), 0, 0)
    )
    key = bpy.context.object
    key.name = "AI_Soft_Key_Light"
    key.data.energy = 450
    key.data.size = 5.5
    link_to(col_core, key)

    bpy.ops.object.camera_add(location=(0, -7.4, 3.2), rotation=(math.radians(65), 0, 0))
    camera = bpy.context.object
    camera.name = "AI_Album_Camera"
    scene.camera = camera
    camera.data.lens = 42

    world = scene.world or bpy.data.worlds.new("AI_World")
    scene.world = world
    world.color = (0.025, 0.095, 0.105)

    scene["ai_generated_from"] = str(MUSIC_CONTEXT_JSON)
    scene["full_keyframes_reference"] = str(BLENDER_KEYFRAMES_JSON)
    scene["note"] = (
        "Standalone AI scene draft. Existing project files were used only as style reference."
    )


if __name__ == "__main__":
    build_scene()
