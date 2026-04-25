import sys
import time
from pathlib import Path
import bpy

SCRIPT_DIR = None

try:
    text = bpy.context.space_data.text
    if text is not None and text.filepath:
        SCRIPT_DIR = Path(text.filepath).resolve().parent
except Exception:
    SCRIPT_DIR = None

if SCRIPT_DIR is None:
    SCRIPT_DIR = Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

reload_modules = {
    "config",
    "scene_utils",
    "io_utils",
    "render_setup",
    "world_setup",
    "camera_setup",
    "asset_setup",
    "atmosphere_setup",
    "physics_setup",
    "fog_dynamics",
    "fog_filaments",
    "animation",
    "scene_tuning_panel",
}
reload_prefixes = ("spaziotempo",)

for mod_name in list(sys.modules):
    if mod_name in reload_modules or any(
        mod_name == prefix or mod_name.startswith(prefix + ".") for prefix in reload_prefixes
    ):
        sys.modules.pop(mod_name, None)

from config import (
    ANALYSIS_JSON_PATH,
    AUDIO_PATH,
    OUTPUT_MP4,
    OUTPUT_IMAGE_SEQUENCE_DIR,
    OUTPUT_IMAGE_SEQUENCE_PREFIX,
    RENDER_OUTPUT_MODE,
    CLEAR_SCENE,
    CLEAR_SEQUENCER,
    FPS_OVERRIDE,
)
from scene_utils import clear_scene
from io_utils import load_json, ensure_inputs_exist, add_audio_strip
from render_setup import configure_scene_physics, configure_render
from world_setup import configure_world, create_floor_and_backdrop, create_area_lights
from camera_setup import create_camera_rig
from asset_setup import create_scene_core, create_primary_asset, create_secondary_asset
from atmosphere_setup import (
    create_hero_aura,
    create_energy_rings,
    create_energy_ribbons,
    create_variants,
    create_atmosphere_cube,
    create_mist_particles,
)
from physics_setup import create_physics_accents
from animation import animate_scene
from spaziotempo.core.collections import classify_scene_objects, compact_structure_summary


def register_tuning_panel():
    try:
        import scene_tuning_panel

        scene_tuning_panel.register()
        print("[INFO] Spaziotempo tuning panel registered. Open Viewport sidebar with N > Spaziotempo.")
    except Exception as exc:
        print(f"[WARN] Tuning panel non registrato: {exc}")


def classify_project_structure(scene):
    try:
        report = classify_scene_objects(scene, include_reserved=True)
        summary = compact_structure_summary(report)
        print(f"[INFO] Scene structure classified: {summary}")
        return report
    except Exception as exc:
        print(f"[WARN] Scene structure non classificata: {exc}")
        return None


def print_summary(scene, analysis_file, hero_asset, secondary_asset, audio_file, fps, frame_count, elapsed):
    print("=" * 68)
    print("SPAZIOTEMPOREC HERO + SECONDARY ASSET VISUAL READY")
    print(f"Engine: {scene.render.engine}")
    print(f"Resolution: {scene.render.resolution_x}x{scene.render.resolution_y} @ {scene.render.resolution_percentage}%")
    print(f"FPS: {fps}")
    print(f"Frames: {frame_count}")
    print(f"Analysis JSON: {analysis_file}")
    print(f"Hero asset:    {hero_asset['asset_file']}")
    if secondary_asset is not None:
        print(f"Secondary:     {secondary_asset['asset_file']}")
    else:
        print("Secondary:     NONE")
    print(f"Audio:         {audio_file}")
    if str(RENDER_OUTPUT_MODE).upper() == "IMAGE_SEQUENCE":
        print(f"Frames:        {OUTPUT_IMAGE_SEQUENCE_DIR}")
        print(f"Prefix:        {OUTPUT_IMAGE_SEQUENCE_PREFIX}")
        print(f"Encode MP4:    run encode_image_sequence_v61b.py after Render Animation")
    else:
        print(f"MP4:           {scene.render.filepath}")
    print(f"Elapsed:       {elapsed:.2f}s")
    print("Use Render > Render Animation to export the configured output.")
    print("=" * 68)


def main():
    t0 = time.time()

    print("[1/10] Verifica input...")
    analysis_file, audio_file = ensure_inputs_exist(
        ANALYSIS_JSON_PATH,
        AUDIO_PATH,
    )

    print("[2/10] Carico analysis JSON...")
    analysis = load_json(analysis_file)
    meta = analysis["meta"]
    frames = analysis["frames"]

    fps = FPS_OVERRIDE if FPS_OVERRIDE else meta["fps"]
    frame_count = len(frames)

    scene = bpy.context.scene
    if CLEAR_SCENE:
        print("[3/10] Pulisco scena...")
        clear_scene()

    scene.frame_start = 1
    scene.frame_end = frame_count
    scene.frame_set(1)

    print("[4/10] Configuro render e world...")
    configure_scene_physics(scene)
    configure_render(scene, OUTPUT_MP4, fps)
    configure_world(scene)

    print("[5/10] Aggiungo audio strip...")
    add_audio_strip(scene, audio_file, clear_existing=CLEAR_SEQUENCER, sync_audio=True)

    if scene.rigidbody_world is not None and scene.rigidbody_world.point_cache is not None:
        scene.rigidbody_world.point_cache.frame_start = 1
        scene.rigidbody_world.point_cache.frame_end = frame_count

    print("[6/10] Creo camera...")
    camera, target = create_camera_rig()

    print("[7/10] Creo base scena...")
    scene_base = create_floor_and_backdrop()
    lights = create_area_lights()

    print("[8/10] Importo hero + secondary asset...")
    scene_core = create_scene_core()
    hero_asset = create_primary_asset(parent=scene_core)
    secondary_asset = create_secondary_asset(parent=scene_core)

    print(f"[INFO] Hero asset file: {hero_asset['asset_file']}")
    if secondary_asset is not None:
        print(f"[INFO] Secondary asset file: {secondary_asset['asset_file']}")
    else:
        print("[INFO] Secondary asset: NONE")

    print("[9/10] Creo atmosfera e fisica...")
    aura_data = create_hero_aura(parent=scene_core)
    energy_rings = create_energy_rings(parent=scene_core)
    energy_ribbons = create_energy_ribbons(parent=scene_core)
    variants = create_variants(hero_asset["root"], parent=scene_core)

    fog_controller = create_atmosphere_cube(parent=scene_core)
    mist_particles = create_mist_particles(parent=scene_core)

    physics_data = create_physics_accents(parent=scene_core)

    print("[10/10] Animo scena...")
    animate_scene(
        scene=scene,
        frames=frames,
        camera=camera,
        target=target,
        hero_asset=hero_asset,
        secondary_asset=secondary_asset,
        aura_data=aura_data,
        fog_controller=fog_controller,
        scene_base=scene_base,
        lights=lights,
        physics_data=physics_data,
        mist_particles=mist_particles,
        variants=variants,
        energy_rings=energy_rings,
        energy_ribbons=energy_ribbons,
    )

    classify_project_structure(scene)

    elapsed = time.time() - t0
    register_tuning_panel()
    print_summary(scene, analysis_file, hero_asset, secondary_asset, audio_file, fps, frame_count, elapsed)


if __name__ == "__main__":
    main()
