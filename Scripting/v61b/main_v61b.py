import sys
import time
from pathlib import Path
import bpy
import logging

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCRIPT_DIR = None

try:
    text = bpy.context.space_data.text
    if text is not None and text.filepath:
        SCRIPT_DIR = Path(text.filepath).resolve().parent
except Exception as e:
    logging.warning(f"Impossibile determinare la directory dello script: {e}")
    SCRIPT_DIR = None

if SCRIPT_DIR is None:
    SCRIPT_DIR = Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from reload_utils import reload_known_modules

reload_known_modules()

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
        logging.info("Pannello di tuning Spaziotempo registrato. Aprire il pannello laterale con N > Spaziotempo.")
    except Exception as exc:
        logging.warning(f"Impossibile registrare il pannello di tuning: {exc}")


def classify_project_structure(scene):
    try:
        report = classify_scene_objects(scene, include_reserved=True)
        summary = compact_structure_summary(report)
        logging.info(f"Struttura della scena classificata: {summary}")
        return report
    except Exception as exc:
        logging.warning(f"Impossibile classificare la struttura della scena: {exc}")
        return None


def print_summary(scene, analysis_file, hero_asset, secondary_asset, audio_file, fps, frame_count, elapsed):
    logging.info("=" * 68)
    logging.info("SPAZIOTEMPOREC HERO + SECONDARY ASSET VISUAL READY")
    logging.info(f"Engine: {scene.render.engine}")
    logging.info(f"Resolution: {scene.render.resolution_x}x{scene.render.resolution_y} @ {scene.render.resolution_percentage}%")
    logging.info(f"FPS: {fps}")
    logging.info(f"Frames: {frame_count}")
    logging.info(f"Analysis JSON: {analysis_file}")
    logging.info(f"Hero asset:    {hero_asset['asset_file']}")
    if secondary_asset is not None:
        logging.info(f"Secondary:     {secondary_asset['asset_file']}")
    else:
        logging.info("Secondary:     NONE")
    logging.info(f"Audio:         {audio_file}")
    if str(RENDER_OUTPUT_MODE).upper() == "IMAGE_SEQUENCE":
        logging.info(f"Frames:        {OUTPUT_IMAGE_SEQUENCE_DIR}")
        logging.info(f"Prefix:        {OUTPUT_IMAGE_SEQUENCE_PREFIX}")
        logging.info(f"Encode MP4:    eseguire encode_image_sequence_v61b.py dopo il Render Animation")
    else:
        logging.info(f"MP4:           {scene.render.filepath}")
    logging.info(f"Elapsed:       {elapsed:.2f}s")
    logging.info("Utilizzare Render > Render Animation per esportare l'output configurato.")
    logging.info("=" * 68)


def main():
    t0 = time.time()

    logging.info("[1/10] Verifica input...")
    analysis_file, audio_file = ensure_inputs_exist(
        ANALYSIS_JSON_PATH,
        AUDIO_PATH,
    )

    logging.info("[2/10] Carico analysis JSON...")
    analysis = load_json(analysis_file)
    meta = analysis["meta"]
    frames = analysis["frames"]

    fps = FPS_OVERRIDE if FPS_OVERRIDE else meta["fps"]
    frame_count = len(frames)

    scene = bpy.context.scene
    if CLEAR_SCENE:
        logging.info("[3/10] Pulisco scena...")
        clear_scene()

    scene.frame_start = 1
    scene.frame_end = frame_count
    scene.frame_set(1)

    logging.info("[4/10] Configuro render e world...")
    configure_scene_physics(scene)
    configure_render(scene, OUTPUT_MP4, fps)
    configure_world(scene)

    logging.info("[5/10] Aggiungo audio strip...")
    add_audio_strip(scene, audio_file, clear_existing=CLEAR_SEQUENCER, sync_audio=True)

    if scene.rigidbody_world is not None and scene.rigidbody_world.point_cache is not None:
        scene.rigidbody_world.point_cache.frame_start = 1
        scene.rigidbody_world.point_cache.frame_end = frame_count

    logging.info("[6/10] Creo camera...")
    camera, target = create_camera_rig()

    logging.info("[7/10] Creo base scena...")
    scene_base = create_floor_and_backdrop()
    lights = create_area_lights()

    logging.info("[8/10] Importo hero + secondary asset...")
    scene_core = create_scene_core()
    hero_asset = create_primary_asset(parent=scene_core)
    secondary_asset = create_secondary_asset(parent=scene_core)

    logging.info(f"[INFO] Hero asset file: {hero_asset['asset_file']}")
    if secondary_asset is not None:
        logging.info(f"[INFO] Secondary asset file: {secondary_asset['asset_file']}")
    else:
        logging.info("[INFO] Secondary asset: NONE")

    logging.info("[9/10] Creo atmosfera e fisica...")
    aura_data = create_hero_aura(parent=scene_core)
    energy_rings = create_energy_rings(parent=scene_core)
    energy_ribbons = create_energy_ribbons(parent=scene_core)
    variants = create_variants(hero_asset["root"], parent=scene_core)

    fog_controller = create_atmosphere_cube(parent=scene_core)
    mist_particles = create_mist_particles(parent=scene_core)

    physics_data = create_physics_accents(parent=scene_core)

    logging.info("[10/10] Animo scena...")
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
