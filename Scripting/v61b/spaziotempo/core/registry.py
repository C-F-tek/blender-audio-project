"""Central naming, layer, and feature registry for the Blender scene.

This module is intentionally data-first. Existing scripts can keep their
current object names while newer modules use this registry to classify objects
and decide where future features should live.
"""

from dataclasses import dataclass

PROJECT_ROOT_COLLECTION = "ST_Project_Spaziotempo"
STRUCTURE_VERSION = "2026-04-layered-v1"


@dataclass(frozen=True)
class LayerSpec:
    key: str
    collection: str
    family: str
    layer: int
    feature: str
    description: str
    reserved: bool = False


LAYER_SPECS = {
    "core": LayerSpec(
        key="core",
        collection="ST_00_Core",
        family="core",
        layer=0,
        feature="scene",
        description="Scene anchors, project root objects, and global controls.",
    ),
    "world_set": LayerSpec(
        key="world_set",
        collection="ST_05_World_Set",
        family="environment",
        layer=5,
        feature="stage",
        description="Floor, backdrop, and visible physical set pieces.",
    ),
    "hero": LayerSpec(
        key="hero",
        collection="ST_10_Hero",
        family="hero",
        layer=10,
        feature="central_asset",
        description="Central sphere/object, aura, mesh deformation, rings, ribbons, and variants.",
    ),
    "atmosphere": LayerSpec(
        key="atmosphere",
        collection="ST_20_Atmosphere",
        family="atmosphere",
        layer=20,
        feature="fog",
        description="Volumetric fog, mist controls, soft backdrop pulse, and atmosphere controllers.",
    ),
    "atomic_physics": LayerSpec(
        key="atomic_physics",
        collection="ST_30_Atomic_Physics",
        family="physics",
        layer=30,
        feature="orbit_accents",
        description="Main gravity, orbiting physical accents, force fields, and audio-driven motion.",
    ),
    "lighting": LayerSpec(
        key="lighting",
        collection="ST_40_Lights",
        family="lighting",
        layer=40,
        feature="rhythm_light",
        description="Scene lights and emission-driven lighting controls.",
    ),
    "render_io": LayerSpec(
        key="render_io",
        collection="ST_50_Render_IO",
        family="render_io",
        layer=50,
        feature="camera_audio_output",
        description="Camera, targets, image sequence/audio IO helpers, and invisible render helpers.",
    ),
    "water": LayerSpec(
        key="water",
        collection="ST_60_Water",
        family="water",
        layer=60,
        feature="future_water",
        description="Reserved empty layer for future water/fluid/refraction feature modules.",
        reserved=True,
    ),
    "technical": LayerSpec(
        key="technical",
        collection="ST_90_Technical",
        family="technical",
        layer=90,
        feature="support",
        description="Hidden anchors, disabled experiments, compatibility objects, and utility sources.",
    ),
}


LAYER_ORDER = (
    "core",
    "world_set",
    "hero",
    "atmosphere",
    "atomic_physics",
    "lighting",
    "render_io",
    "water",
    "technical",
)


EXACT_OBJECT_LAYERS = {
    "SceneCore": "core",
    "HeroRoot": "hero",
    "HeroAura": "hero",
    "AuraAudioDeformField": "hero",
    "MainCamera": "render_io",
    "CameraTarget": "render_io",
    "PeaceFloor": "world_set",
    "InvisibleParticleFloor": "render_io",
    "SoftRhythmBackdrop": "atmosphere",
    "BackdropPulseController": "atmosphere",
    "AtmosphereCube": "atmosphere",
    "FogPulseController": "atmosphere",
    "FogFilamentsRoot": "atmosphere",
    "MistParticlesRoot": "atmosphere",
    "HeroGravityField": "atomic_physics",
    "PulseForceField": "atomic_physics",
    "AtmosphereTurbulence": "atomic_physics",
    "OrbitVortex": "atomic_physics",
    "WindLeft": "atomic_physics",
    "WindRight": "atomic_physics",
    "RhythmParticlePhysicsRoot": "technical",
    "AlbumLetterParticleSources": "technical",
}


PREFIX_OBJECT_LAYERS = (
    ("HeroAudio", "hero"),
    ("HeroMesh", "hero"),
    ("HeroVariant", "hero"),
    ("EnergyRing", "hero"),
    ("EnergyRibbon", "hero"),
    ("Aura", "hero"),
    ("MistParticle", "atmosphere"),
    ("Fog", "atmosphere"),
    ("FogFilament_", "atmosphere"),
    ("PhysicsAccent_", "atomic_physics"),
    ("PhysicsAnchor_", "technical"),
    ("PhysicsSpring_", "technical"),
    ("AreaLight_", "lighting"),
    ("AlbumLetterParticle", "technical"),
    ("Water", "water"),
    ("Fluid", "water"),
)


PARENT_LAYER_HINTS = {
    "HeroRoot": "hero",
    "HeroAura": "hero",
    "MistParticlesRoot": "atmosphere",
    "RhythmParticlePhysicsRoot": "technical",
    "SceneCore": "core",
}


TYPE_FALLBACK_LAYERS = {
    "CAMERA": "render_io",
    "LIGHT": "lighting",
    "VOLUME": "atmosphere",
}


FEATURE_CATALOG = {
    "scene": {
        "layer": "core",
        "module": "main_v61b.py",
        "hotpatch": False,
        "notes": "Owns structural bootstrap and must be rebuilt for primary object graph changes.",
    },
    "central_asset": {
        "layer": "hero",
        "module": "asset_setup.py + atmosphere_setup.py + materials.py",
        "hotpatch": "MATERIALS",
        "notes": "Owns hero mesh, material nodes, aura, audio deform, and nearby decorative forms.",
    },
    "fog": {
        "layer": "atmosphere",
        "module": "atmosphere_setup.py + fog_dynamics.py + hotpatch/fog_patch.py",
        "hotpatch": "FOG",
        "notes": "Owns volumetric cube, noise/clump material nodes, and fog pulse controllers.",
    },
    "orbit_accents": {
        "layer": "atomic_physics",
        "module": "physics_setup.py + animation.py + hotpatch/accent_patch.py",
        "hotpatch": "PHYSICS",
        "notes": "Owns audio-driven orbiting accents and force-field style controls.",
    },
    "rhythm_light": {
        "layer": "lighting",
        "module": "world_setup.py + hotpatch/lighting_patch.py",
        "hotpatch": "ALL",
        "notes": "Owns physical lights and low-amplitude support lighting.",
    },
    "camera_audio_output": {
        "layer": "render_io",
        "module": "camera_setup.py + io_utils.py + encode_image_sequence_v61b.py",
        "hotpatch": "RENDER",
        "notes": "Owns camera, audio strip, image sequence loading, and render/output settings.",
    },
    "future_water": {
        "layer": "water",
        "module": "spaziotempo/features/water.py (future)",
        "hotpatch": "future WATER",
        "notes": "Reserved only. Do not create water objects until the feature is requested.",
    },
}
