import json
import re
import sys
from pathlib import Path

ROOT = Path.home() / "blender"
PROJECT_DIR = ROOT / "blender-audio-project"

IN_JSON = PROJECT_DIR / "scene_spec_album_driven.json"
OUT_JSON = PROJECT_DIR / "scene_spec_album_driven_normalized.json"

DEFAULT_SCENE_NAME = "Living Life In Peace - Feel The Light"
DEFAULT_VISUAL_CONCEPT = "Cinematic abstract soul architecture"

PALETTE_MAP = {
    "deep_blue": "#1F3A5F",
    "muted_gold": "#B08D57",
    "deep_purple": "#5E3E8C",
    "soft_white": "#F2F0E8",
    "warm_amber": "#C27A3A",
    "dark_teal": "#1E5A63",
    "midnight_black": "#0B0D12",
}

CAMERA_PRESETS = {
    "frontal": {"location": [0.0, -8.8, 2.4], "rotation": [74.0, 0.0, 0.0]},
    "slightly_top": {"location": [0.0, -9.2, 3.4], "rotation": [72.0, 0.0, 0.0]},
    "angled_front": {"location": [1.2, -8.9, 2.9], "rotation": [73.0, 0.0, 7.0]},
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Scene brief non trovato: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def slugify(text: str) -> str:
    text = str(text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "item"


def normalize_palette(values):
    if not isinstance(values, list):
        values = []

    colors = []
    for v in values:
        if isinstance(v, str) and v in PALETTE_MAP:
            colors.append(PALETTE_MAP[v])

    if not colors:
        colors = ["#1F3A5F", "#5E3E8C", "#B08D57", "#F2F0E8"]

    dedup = []
    for c in colors:
        if c not in dedup:
            dedup.append(c)

    return dedup[:5]


def normalize_camera_style(camera_style: dict):
    if not isinstance(camera_style, dict):
        camera_style = {}

    mood = str(camera_style.get("mood", "cinematic")).strip() or "cinematic"
    movement = str(camera_style.get("movement", "floating_orbit")).strip() or "floating_orbit"
    angle_bias = str(camera_style.get("angle_bias", "slightly_top")).strip() or "slightly_top"

    try:
        lens = float(camera_style.get("lens", 50))
    except Exception:
        lens = 50.0

    if lens < 20:
        lens = 50.0
    elif lens > 85:
        lens = 65.0

    preset = CAMERA_PRESETS.get(angle_bias, CAMERA_PRESETS["slightly_top"])

    return {
        "mood": mood,
        "movement": movement,
        "lens": lens,
        "angle_bias": angle_bias,
        "location": preset["location"],
        "rotation_degrees": preset["rotation"],
    }


def build_object_specs(brief: dict):
    hero_object = brief.get("hero_object", "central_core")
    objects = [
        {
            "type": "hero_core",
            "name": "hero_core",
            "role": "central emotional centerpiece",
            "geometry": {
                "primitive": "uv_sphere",
                "location": [0.0, 0.0, 1.15],
                "rotation": [0.0, 0.0, 0.0],
                "scale": [1.15, 1.15, 1.15],
                "subdivisions": 2,
            },
            "material": "hero_core_material",
        },
        {
            "type": "light_architecture",
            "name": "light_architecture",
            "role": "surrounding luminous structure",
            "geometry": {
                "primitive": "instanced_columns_ring",
                "count": 12,
                "radius": 4.4,
                "height": 2.6,
            },
            "material": "light_arch_material",
        },
        {
            "type": "reflective_floor",
            "name": "reflective_floor",
            "role": "depth and reflections",
            "geometry": {
                "primitive": "plane",
                "location": [0.0, 0.0, 0.0],
                "rotation": [0.0, 0.0, 0.0],
                "scale": [14.0, 14.0, 1.0],
            },
            "material": "floor_material",
        },
        {
            "type": "floating_lights",
            "name": "floating_lights",
            "role": "harmonic accents",
            "geometry": {"primitive": "floating_orbs", "count": 4},
            "material": "floating_light_material",
        },
        {
            "type": "volumetric_shell",
            "name": "volumetric_shell",
            "role": "atmosphere and cinematic depth",
            "geometry": {
                "primitive": "cube_volume",
                "location": [0.0, 0.0, 3.0],
                "rotation": [0.0, 0.0, 0.0],
                "scale": [9.0, 9.0, 4.5],
            },
            "material": "volume_material",
        },
    ]

    if hero_object == "luminous_pillar":
        objects[0]["geometry"]["primitive"] = "cylinder"
        objects[0]["geometry"]["scale"] = [0.8, 0.8, 2.3]
    elif hero_object == "abstract_signal_monolith":
        objects[0]["geometry"]["primitive"] = "cube"
        objects[0]["geometry"]["scale"] = [0.9, 0.9, 2.0]
    elif hero_object == "music_totem":
        objects[0]["geometry"]["primitive"] = "stacked_orb_column"
        objects[0]["geometry"]["scale"] = [1.0, 1.0, 1.8]

    return objects


def build_materials(brief: dict):
    lighting_style = brief.get("lighting_style", "soft_volumetric_glow")

    materials = [
        {
            "name": "hero_core_material",
            "target": "hero_core",
            "shader_type": "emission_glass_mix",
            "node_features": ["noise", "color_ramp", "fresnel", "mapping_rotation", "mix_shader"],
            "purpose": "hero pulse and emotional focus",
            "defaults": {
                "emission_strength": 2.2,
                "noise_scale": 3.0,
                "fresnel": 0.65,
                "mix_factor": 0.55,
            },
        },
        {
            "name": "light_arch_material",
            "target": "light_architecture",
            "shader_type": "gradient_emission",
            "node_features": ["gradient", "color_ramp", "mapping", "emission"],
            "purpose": "rhythmic luminous architecture",
            "defaults": {"emission_strength": 1.6, "gradient_shift": 0.0, "color_mix": 0.5},
        },
        {
            "name": "floor_material",
            "target": "reflective_floor",
            "shader_type": "reflective_principled",
            "node_features": ["noise", "bump", "roughness_variation", "fresnel"],
            "purpose": "depth, reflection and grounding",
            "defaults": {"roughness": 0.24, "bump_strength": 0.08, "metallic": 0.18},
        },
        {
            "name": "floating_light_material",
            "target": "floating_lights",
            "shader_type": "soft_emission",
            "node_features": ["emission", "noise", "color_variation"],
            "purpose": "harmonic floating accents",
            "defaults": {"emission_strength": 1.5, "noise_scale": 4.0},
        },
        {
            "name": "volume_material",
            "target": "volumetric_shell",
            "shader_type": "principled_volume",
            "node_features": ["volume_density", "anisotropy"],
            "purpose": "cinematic atmosphere",
            "defaults": {"density": 0.015, "anisotropy": 0.20},
        },
    ]

    if lighting_style == "reflective_low_key_lighting":
        materials[2]["defaults"]["roughness"] = 0.18
        materials[4]["defaults"]["density"] = 0.010
    elif lighting_style == "soulful_color_bloom":
        materials[0]["defaults"]["emission_strength"] = 2.8
        materials[1]["defaults"]["emission_strength"] = 2.2

    return materials


def build_node_animation(brief: dict):
    return [
        {
            "target": "hero_core_material",
            "parameter": "emission_strength",
            "band": "beat",
            "intent": "main musical pulse",
            "strength": 1.0,
        },
        {
            "target": "hero_core_material",
            "parameter": "noise_scale",
            "band": "low",
            "intent": "body deformation illusion",
            "strength": 0.65,
        },
        {
            "target": "hero_core_material",
            "parameter": "mix_factor",
            "band": "mid",
            "intent": "surface shimmer and motion",
            "strength": 0.45,
        },
        {
            "target": "light_arch_material",
            "parameter": "emission_strength",
            "band": "high",
            "intent": "harmonic brightness",
            "strength": 0.80,
        },
        {
            "target": "light_arch_material",
            "parameter": "gradient_shift",
            "band": "mid",
            "intent": "circulating light flow",
            "strength": 0.50,
        },
        {
            "target": "floor_material",
            "parameter": "roughness",
            "band": "low",
            "intent": "subtle reflective breathing",
            "strength": 0.30,
        },
        {
            "target": "volume_material",
            "parameter": "density",
            "band": "beat",
            "intent": "volumetric pulse",
            "strength": 0.18,
        },
    ]


def build_audio_mapping(brief: dict):
    return [
        {
            "target": "hero_core",
            "property": "scale",
            "band": "low",
            "intent": "central body pulse",
            "strength": 0.55,
        },
        {
            "target": "hero_core",
            "property": "rotation",
            "band": "mid",
            "intent": "gentle musical sway",
            "strength": 0.25,
        },
        {
            "target": "light_architecture",
            "property": "rotation",
            "band": "mid",
            "intent": "architectural motion",
            "strength": 0.40,
        },
        {
            "target": "light_architecture",
            "property": "emission",
            "band": "high",
            "intent": "harmonic brightness accents",
            "strength": 0.72,
        },
        {
            "target": "floating_lights",
            "property": "intensity",
            "band": "high",
            "intent": "sparkle accents",
            "strength": 0.70,
        },
        {
            "target": "camera",
            "property": "pulse",
            "band": "beat",
            "intent": "subtle rhythmic camera bump",
            "strength": 0.28,
        },
    ]


def build_optimization():
    return {
        "use_instancing": True,
        "use_procedural_materials": True,
        "avoid_heavy_geometry": True,
        "animate_nodes_more_than_meshes": True,
        "geometry_budget": "low_geometry_high_shading",
        "notes": [
            "keep hero object simple",
            "use instanced ring architecture",
            "prefer procedural shading",
            "use one volumetric shell only",
            "avoid subdivision-heavy meshes",
        ],
    }


def build_render_strategy():
    return {
        "engine": "BLENDER_EEVEE",
        "priority": "fast iteration with rich shading",
        "notes": "use emission, procedural shaders and moderate volumetrics",
    }


def normalize_brief(brief: dict):
    scene_name = safe_scene_name(brief.get("scene_name"))
    style_mode = (
        str(brief.get("style_mode", "stylized_cinematic_abstract")).strip()
        or "stylized_cinematic_abstract"
    )
    visual_concept = safe_visual_concept(brief.get("visual_concept"))
    hero_object = str(brief.get("hero_object", "central_core")).strip() or "central_core"
    environment = str(brief.get("environment", "abstract_stage")).strip() or "abstract_stage"
    lighting_style = (
        str(brief.get("lighting_style", "soft_volumetric_glow")).strip() or "soft_volumetric_glow"
    )

    palette = normalize_palette(brief.get("palette", []))
    camera_style = normalize_camera_style(brief.get("camera_style", {}))
    objects = build_object_specs(brief)
    materials = build_materials(brief)
    node_animation = build_node_animation(brief)
    audio_mapping = build_audio_mapping(brief)
    optimization = build_optimization()
    render_strategy = build_render_strategy()

    return {
        "scene_name": scene_name,
        "style_mode": style_mode,
        "visual_concept": visual_concept,
        "hero_object": hero_object,
        "environment": environment,
        "lighting_style": lighting_style,
        "palette": palette,
        "camera_style": camera_style,
        "objects": objects,
        "materials": materials,
        "node_animation": node_animation,
        "audio_mapping": audio_mapping,
        "optimization": optimization,
        "render_strategy": render_strategy,
    }


def safe_scene_name(name: str) -> str:
    if not isinstance(name, str):
        return DEFAULT_SCENE_NAME
    name = name.strip()
    if not name or name == ".":
        return DEFAULT_SCENE_NAME
    return name


def safe_visual_concept(text: str) -> str:
    if not isinstance(text, str):
        return DEFAULT_VISUAL_CONCEPT
    text = text.strip()
    if not text or text == ".":
        return DEFAULT_VISUAL_CONCEPT
    return text


def main():
    brief = load_json(IN_JSON)
    normalized = normalize_brief(brief)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)

    print(f"[OK] Scene spec normalizzato salvato in: {OUT_JSON}")
    print(json.dumps(normalized, indent=2, ensure_ascii=False))

    tools_dir = PROJECT_DIR / "Tools" / "npu"
    if tools_dir.exists():
        if str(tools_dir) not in sys.path:
            sys.path.insert(0, str(tools_dir))
        try:
            from build_music_context import build_music_context

            manifest = build_music_context(
                scene_files=[
                    IN_JSON,
                    OUT_JSON,
                    PROJECT_DIR / "scene_spec_album_driven_raw.txt",
                    PROJECT_DIR / "scene_spec_from_npu.json",
                    PROJECT_DIR / "scene_spec_from_npu_raw.txt",
                ],
            )
        except Exception as exc:
            print(f"[WARN] Contesto musicale NPU non aggiornato: {exc}")
        else:
            print(f"[OK] Contesto musicale NPU aggiornato: {manifest['context_md']}")


if __name__ == "__main__":
    main()
