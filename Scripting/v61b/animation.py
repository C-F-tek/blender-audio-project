import math

from fog_dynamics import animate_fog_frame
from scene_utils import set_linear_interpolation_idblock

from config import (
    ALBUM_LETTER_PARTICLE_SIZE_MAX,
    ALBUM_LETTER_PARTICLE_SIZE_MIN,
    ALBUM_LETTER_ROOT_SCALE_MAX,
    ALBUM_LETTER_ROOT_SCALE_MIN,
    AURA_DEFORM_FIELD_DRIFT,
    AURA_DEFORM_FIELD_SCALE,
    AURA_DEFORM_KEYFRAME_STEP,
    BACKDROP_BREATHE_SCALE,
    BACKDROP_EMISSION_MAX,
    BACKDROP_EMISSION_MIN,
    CAMERA_BEAT_BUMP_Y,
    CAMERA_BEAT_BUMP_Z,
    CAMERA_ORBIT_AMOUNT,
    CAMERA_PUSH_AMOUNT,
    CAMERA_VERTICAL_SWAY,
    COMPOSITOR_GLARE_THRESHOLD_MAX,
    COMPOSITOR_GLARE_THRESHOLD_MIN,
    COMPOSITOR_LENS_DISPERSION_MAX,
    COMPOSITOR_LENS_DISPERSION_MIN,
    COMPOSITOR_LENS_DISTORT_MAX,
    COMPOSITOR_LENS_DISTORT_MIN,
    HERO_BEAT_TWIST_Z,
    HERO_BOUNCE_Z,
    HERO_DEFORM_CONTROLLER_RADIUS,
    HERO_DEFORM_DETAIL_STRENGTH_MAX,
    HERO_DEFORM_KEYFRAME_STEP,
    HERO_DEFORM_STRENGTH_MAX,
    HERO_DEFORM_STRENGTH_MIN,
    HERO_DEFORM_TWIST_MAX,
    HERO_DEFORM_WAVE_HEIGHT_MAX,
    HERO_DRIFT_X,
    HERO_DRIFT_Y,
    HERO_GRAVITY_STRENGTH_MAX,
    HERO_GRAVITY_STRENGTH_MIN,
    HERO_MATERIAL_BUMP_MAX,
    HERO_MATERIAL_BUMP_MIN,
    HERO_MATERIAL_EMISSION_MAX,
    HERO_MATERIAL_EMISSION_MIN,
    HERO_MATERIAL_MAPPING_DRIFT,
    HERO_MATERIAL_NOISE_SCALE_MAX,
    HERO_MATERIAL_NOISE_SCALE_MIN,
    HERO_MATERIAL_ROUGHNESS_MAX,
    HERO_MATERIAL_ROUGHNESS_MIN,
    HERO_MATERIAL_SELF_LIGHT_MAX,
    HERO_MATERIAL_SELF_LIGHT_MIN,
    HERO_ONSET_SHAKE,
    HERO_ORBIT_X,
    HERO_ORBIT_Y,
    HERO_ROT_X,
    HERO_ROT_Y,
    HERO_ROT_Z,
    HERO_SCALE_MAX,
    HERO_SCALE_MIN,
    LIGHT_ENERGY_MAX,
    LIGHT_ENERGY_MIN,
    MIST_BEAT_BOOST,
    MIST_FLOAT_AMPLITUDE,
    PHYSICS_ACCENT_EMISSION_MAX,
    PHYSICS_ACCENT_EMISSION_MIN,
    PHYSICS_ACCENT_MIX_MAX,
    PHYSICS_ACCENT_MIX_MIN,
    PHYSICS_ATOM_MICRO_WOBBLE,
    PHYSICS_ATOM_ORBIT_AUDIO_SPEED,
    PHYSICS_ATOM_ORBIT_HEIGHT_SWAY,
    PHYSICS_ATOM_ORBIT_RADIUS_PULSE,
    PHYSICS_ATOM_ORBIT_SPEED_MIN,
    RHYTHM_PARTICLE_BROWNIAN_MAX,
    RHYTHM_PARTICLE_BROWNIAN_MIN,
    RHYTHM_PARTICLE_EMIT_MAX,
    RHYTHM_PARTICLE_EMIT_MIN,
    RHYTHM_PARTICLE_KEYFRAME_STEP,
    RHYTHM_PARTICLE_NORMAL_MAX,
    RHYTHM_PARTICLE_NORMAL_MIN,
    RHYTHM_PARTICLE_SIZE_MAX,
    RHYTHM_PARTICLE_SIZE_MIN,
    RHYTHM_PARTICLE_TANGENT_MAX,
    RHYTHM_PARTICLE_TANGENT_MIN,
    SECONDARY_BOUNCE_Z,
    SECONDARY_DRIFT_X,
    SECONDARY_DRIFT_Y,
    SECONDARY_ROT_X,
    SECONDARY_ROT_Z,
    SECONDARY_SCALE_MAX,
    SECONDARY_SCALE_MIN,
    TURB_STRENGTH_MAX,
    TURB_STRENGTH_MIN,
    VORTEX_STRENGTH_MAX,
    VORTEX_STRENGTH_MIN,
)


def keyframe_if_possible(idblock, data_path, frame):
    try:
        idblock.keyframe_insert(data_path=data_path, frame=frame)
    except Exception:
        pass


def get_scene_compositor_tree(scene):
    for attr in ("node_tree", "compositor_node_tree"):
        tree = getattr(scene, attr, None)
        if tree is not None:
            return tree
    return None


def rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse):
    band = str(band)
    response = float(response)

    if band == "low":
        drive = low * 0.74 + beat * 0.18 + local_pulse * 0.16
    elif band == "mid":
        drive = mid * 0.68 + low * 0.14 + local_pulse * 0.18
    elif band == "beat":
        drive = beat * 0.70 + low * 0.22 + local_pulse * 0.14
    elif band == "onset":
        drive = onset * 0.72 + high * 0.18 + local_pulse * 0.12
    else:
        drive = high * 0.68 + onset * 0.24 + pulse * 0.08 + local_pulse * 0.12

    return min(1.0, max(0.0, drive * response))



_ANIMATION_PARTS_DIR = __import__("pathlib").Path(__file__).with_name("animation_parts")
_ANIMATE_SETUP_PARTS = (
    'setup_001.pyfrag',
)
_ANIMATE_FRAME_PARTS = (
    'frame_001.pyfrag',
    'frame_002.pyfrag',
    'frame_003.pyfrag',
)
_ANIMATE_FINALIZE_PARTS = (
    'finalize_001.pyfrag',
)


def _compile_animation_parts(names):
    compiled = []
    for name in names:
        path = _ANIMATION_PARTS_DIR / name
        compiled.append(compile(path.read_text(encoding="utf-8"), str(path), "exec"))
    return tuple(compiled)


_ANIMATE_SETUP = _compile_animation_parts(_ANIMATE_SETUP_PARTS)
_ANIMATE_FRAME = _compile_animation_parts(_ANIMATE_FRAME_PARTS)
_ANIMATE_FINALIZE = _compile_animation_parts(_ANIMATE_FINALIZE_PARTS)

def animate_scene(
    scene,
    frames,
    camera,
    target,
    hero_asset,
    secondary_asset,
    aura_data,
    fog_controller,
    scene_base,
    lights,
    physics_data,
    mist_particles,
    variants,
    energy_rings,
    energy_ribbons,
):
    _locals = dict(locals())
    for _code in _ANIMATE_SETUP:
        exec(_code, globals(), _locals)
    for i, sample in enumerate(frames, start=1):
        _locals["i"] = i
        _locals["sample"] = sample
        for _code in _ANIMATE_FRAME:
            exec(_code, globals(), _locals)
    for _code in _ANIMATE_FINALIZE:
        exec(_code, globals(), _locals)
