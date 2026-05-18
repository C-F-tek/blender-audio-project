"""Object-oriented scene-spec normalizer."""

from __future__ import annotations

from .constants import (
    CAMERA_PRESETS,
    DEFAULT_SCENE_NAME,
    DEFAULT_VISUAL_CONCEPT,
    PALETTE_MAP,
)


class SceneSpecNormalizer:
    """Build a normalized Blender scene-spec dictionary from an input brief."""

    def normalize(self, brief: dict) -> dict:
        scene_name = self.safe_scene_name(brief.get("scene_name"))
        style_mode = (
            str(brief.get("style_mode", "stylized_cinematic_abstract")).strip()
            or "stylized_cinematic_abstract"
        )
        visual_concept = self.safe_visual_concept(brief.get("visual_concept"))
        hero_object = str(brief.get("hero_object", "central_core")).strip() or "central_core"
        environment = str(brief.get("environment", "abstract_stage")).strip() or "abstract_stage"
        lighting_style = (
            str(brief.get("lighting_style", "soft_volumetric_glow")).strip()
            or "soft_volumetric_glow"
        )

        return {
            "scene_name": scene_name,
            "style_mode": style_mode,
            "visual_concept": visual_concept,
            "hero_object": hero_object,
            "environment": environment,
            "lighting_style": lighting_style,
            "palette": self.normalize_palette(brief.get("palette", [])),
            "camera_style": self.normalize_camera_style(brief.get("camera_style", {})),
            "objects": self.build_object_specs(brief),
            "materials": self.build_materials(brief),
            "node_animation": self.build_node_animation(),
            "audio_mapping": self.build_audio_mapping(),
            "optimization": self.build_optimization(),
            "render_strategy": self.build_render_strategy(),
        }

    def normalize_palette(self, values: object) -> list[str]:
        raw_values = values if isinstance(values, list) else []
        colors = [PALETTE_MAP[v] for v in raw_values if isinstance(v, str) and v in PALETTE_MAP]
        if not colors:
            colors = ["#1F3A5F", "#5E3E8C", "#B08D57", "#F2F0E8"]

        deduped: list[str] = []
        for color in colors:
            if color not in deduped:
                deduped.append(color)
        return deduped[:5]

    def normalize_camera_style(self, camera_style: object) -> dict:
        source = camera_style if isinstance(camera_style, dict) else {}
        mood = str(source.get("mood", "cinematic")).strip() or "cinematic"
        movement = str(source.get("movement", "floating_orbit")).strip() or "floating_orbit"
        angle_bias = str(source.get("angle_bias", "slightly_top")).strip() or "slightly_top"

        try:
            lens = float(source.get("lens", 50))
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

    def build_object_specs(self, brief: dict) -> list[dict]:
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
        self.apply_hero_variant(objects[0], str(hero_object))
        return objects

    def apply_hero_variant(self, hero: dict, hero_object: str) -> None:
        geometry = hero["geometry"]
        if hero_object == "luminous_pillar":
            geometry["primitive"] = "cylinder"
            geometry["scale"] = [0.8, 0.8, 2.3]
        elif hero_object == "abstract_signal_monolith":
            geometry["primitive"] = "cube"
            geometry["scale"] = [0.9, 0.9, 2.0]
        elif hero_object == "music_totem":
            geometry["primitive"] = "stacked_orb_column"
            geometry["scale"] = [1.0, 1.0, 1.8]

    def build_materials(self, brief: dict) -> list[dict]:
        lighting_style = brief.get("lighting_style", "soft_volumetric_glow")
        materials = self.default_materials()
        if lighting_style == "reflective_low_key_lighting":
            materials[2]["defaults"]["roughness"] = 0.18
            materials[4]["defaults"]["density"] = 0.010
        elif lighting_style == "soulful_color_bloom":
            materials[0]["defaults"]["emission_strength"] = 2.8
            materials[1]["defaults"]["emission_strength"] = 2.2
        return materials

    def default_materials(self) -> list[dict]:
        return [
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

    def build_node_animation(self) -> list[dict]:
        return [
            self.node_anim("hero_core_material", "emission_strength", "beat", "main musical pulse", 1.0),
            self.node_anim("hero_core_material", "noise_scale", "low", "body deformation illusion", 0.65),
            self.node_anim("hero_core_material", "mix_factor", "mid", "surface shimmer and motion", 0.45),
            self.node_anim("light_arch_material", "emission_strength", "high", "harmonic brightness", 0.80),
            self.node_anim("light_arch_material", "gradient_shift", "mid", "circulating light flow", 0.50),
            self.node_anim("floor_material", "roughness", "low", "subtle reflective breathing", 0.30),
            self.node_anim("volume_material", "density", "beat", "volumetric pulse", 0.18),
        ]

    def build_audio_mapping(self) -> list[dict]:
        return [
            self.audio_map("hero_core", "scale", "low", "central body pulse", 0.55),
            self.audio_map("hero_core", "rotation", "mid", "gentle musical sway", 0.25),
            self.audio_map("light_architecture", "rotation", "mid", "architectural motion", 0.40),
            self.audio_map("light_architecture", "emission", "high", "harmonic brightness accents", 0.72),
            self.audio_map("floating_lights", "intensity", "high", "sparkle accents", 0.70),
            self.audio_map("camera", "pulse", "beat", "subtle rhythmic camera bump", 0.28),
        ]

    @staticmethod
    def node_anim(target: str, parameter: str, band: str, intent: str, strength: float) -> dict:
        return {
            "target": target,
            "parameter": parameter,
            "band": band,
            "intent": intent,
            "strength": strength,
        }

    @staticmethod
    def audio_map(target: str, prop: str, band: str, intent: str, strength: float) -> dict:
        return {
            "target": target,
            "property": prop,
            "band": band,
            "intent": intent,
            "strength": strength,
        }

    @staticmethod
    def build_optimization() -> dict:
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

    @staticmethod
    def build_render_strategy() -> dict:
        return {
            "engine": "BLENDER_EEVEE",
            "priority": "fast iteration with rich shading",
            "notes": "use emission, procedural shaders and moderate volumetrics",
        }

    @staticmethod
    def safe_scene_name(name: object) -> str:
        if not isinstance(name, str):
            return DEFAULT_SCENE_NAME
        value = name.strip()
        return value if value and value != "." else DEFAULT_SCENE_NAME

    @staticmethod
    def safe_visual_concept(text: object) -> str:
        if not isinstance(text, str):
            return DEFAULT_VISUAL_CONCEPT
        value = text.strip()
        return value if value and value != "." else DEFAULT_VISUAL_CONCEPT
