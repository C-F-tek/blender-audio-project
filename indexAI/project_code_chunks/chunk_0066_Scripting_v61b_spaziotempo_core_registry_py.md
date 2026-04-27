# Project Code Chunk 66/212

- File: `Scripting/v61b/spaziotempo/core/registry.py`
- Part: `1`
- Lines: `1-221`

## Symbol Map
- Imports: `from dataclasses import dataclass`
- Classes: `LayerSpec` line 16
- Assignments: `PROJECT_ROOT_COLLECTION`, `STRUCTURE_VERSION`, `LAYER_SPECS`, `LAYER_ORDER`, `EXACT_OBJECT_LAYERS`, `PREFIX_OBJECT_LAYERS`, `PARENT_LAYER_HINTS`, `TYPE_FALLBACK_LAYERS`, `FEATURE_CATALOG`

## Content
```py
00001: """Central naming, layer, and feature registry for the Blender scene.
00002: 
00003: This module is intentionally data-first. Existing scripts can keep their
00004: current object names while newer modules use this registry to classify objects
00005: and decide where future features should live.
00006: """
00007: 
00008: from dataclasses import dataclass
00009: 
00010: 
00011: PROJECT_ROOT_COLLECTION = "ST_Project_Spaziotempo"
00012: STRUCTURE_VERSION = "2026-04-layered-v1"
00013: 
00014: 
00015: @dataclass(frozen=True)
00016: class LayerSpec:
00017:     key: str
00018:     collection: str
00019:     family: str
00020:     layer: int
00021:     feature: str
00022:     description: str
00023:     reserved: bool = False
00024: 
00025: 
00026: LAYER_SPECS = {
00027:     "core": LayerSpec(
00028:         key="core",
00029:         collection="ST_00_Core",
00030:         family="core",
00031:         layer=0,
00032:         feature="scene",
00033:         description="Scene anchors, project root objects, and global controls.",
00034:     ),
00035:     "world_set": LayerSpec(
00036:         key="world_set",
00037:         collection="ST_05_World_Set",
00038:         family="environment",
00039:         layer=5,
00040:         feature="stage",
00041:         description="Floor, backdrop, and visible physical set pieces.",
00042:     ),
00043:     "hero": LayerSpec(
00044:         key="hero",
00045:         collection="ST_10_Hero",
00046:         family="hero",
00047:         layer=10,
00048:         feature="central_asset",
00049:         description="Central sphere/object, aura, mesh deformation, rings, ribbons, and variants.",
00050:     ),
00051:     "atmosphere": LayerSpec(
00052:         key="atmosphere",
00053:         collection="ST_20_Atmosphere",
00054:         family="atmosphere",
00055:         layer=20,
00056:         feature="fog",
00057:         description="Volumetric fog, mist controls, soft backdrop pulse, and atmosphere controllers.",
00058:     ),
00059:     "atomic_physics": LayerSpec(
00060:         key="atomic_physics",
00061:         collection="ST_30_Atomic_Physics",
00062:         family="physics",
00063:         layer=30,
00064:         feature="orbit_accents",
00065:         description="Main gravity, orbiting physical accents, force fields, and audio-driven motion.",
00066:     ),
00067:     "lighting": LayerSpec(
00068:         key="lighting",
00069:         collection="ST_40_Lights",
00070:         family="lighting",
00071:         layer=40,
00072:         feature="rhythm_light",
00073:         description="Scene lights and emission-driven lighting controls.",
00074:     ),
00075:     "render_io": LayerSpec(
00076:         key="render_io",
00077:         collection="ST_50_Render_IO",
00078:         family="render_io",
00079:         layer=50,
00080:         feature="camera_audio_output",
00081:         description="Camera, targets, image sequence/audio IO helpers, and invisible render helpers.",
00082:     ),
00083:     "water": LayerSpec(
00084:         key="water",
00085:         collection="ST_60_Water",
00086:         family="water",
00087:         layer=60,
00088:         feature="future_water",
00089:         description="Reserved empty layer for future water/fluid/refraction feature modules.",
00090:         reserved=True,
00091:     ),
00092:     "technical": LayerSpec(
00093:         key="technical",
00094:         collection="ST_90_Technical",
00095:         family="technical",
00096:         layer=90,
00097:         feature="support",
00098:         description="Hidden anchors, disabled experiments, compatibility objects, and utility sources.",
00099:     ),
00100: }
00101: 
00102: 
00103: LAYER_ORDER = (
00104:     "core",
00105:     "world_set",
00106:     "hero",
00107:     "atmosphere",
00108:     "atomic_physics",
00109:     "lighting",
00110:     "render_io",
00111:     "water",
00112:     "technical",
00113: )
00114: 
00115: 
00116: EXACT_OBJECT_LAYERS = {
00117:     "SceneCore": "core",
00118:     "HeroRoot": "hero",
00119:     "HeroAura": "hero",
00120:     "AuraAudioDeformField": "hero",
00121:     "MainCamera": "render_io",
00122:     "CameraTarget": "render_io",
00123:     "PeaceFloor": "world_set",
00124:     "InvisibleParticleFloor": "render_io",
00125:     "SoftRhythmBackdrop": "atmosphere",
00126:     "BackdropPulseController": "atmosphere",
00127:     "AtmosphereCube": "atmosphere",
00128:     "FogPulseController": "atmosphere",
00129:     "FogFilamentsRoot": "atmosphere",
00130:     "MistParticlesRoot": "atmosphere",
00131:     "HeroGravityField": "atomic_physics",
00132:     "PulseForceField": "atomic_physics",
00133:     "AtmosphereTurbulence": "atomic_physics",
00134:     "OrbitVortex": "atomic_physics",
00135:     "WindLeft": "atomic_physics",
00136:     "WindRight": "atomic_physics",
00137:     "RhythmParticlePhysicsRoot": "technical",
00138:     "AlbumLetterParticleSources": "technical",
00139: }
00140: 
00141: 
00142: PREFIX_OBJECT_LAYERS = (
00143:     ("HeroAudio", "hero"),
00144:     ("HeroMesh", "hero"),
00145:     ("HeroVariant", "hero"),
00146:     ("EnergyRing", "hero"),
00147:     ("EnergyRibbon", "hero"),
00148:     ("Aura", "hero"),
00149:     ("MistParticle", "atmosphere"),
00150:     ("Fog", "atmosphere"),
00151:     ("FogFilament_", "atmosphere"),
00152:     ("PhysicsAccent_", "atomic_physics"),
00153:     ("PhysicsAnchor_", "technical"),
00154:     ("PhysicsSpring_", "technical"),
00155:     ("AreaLight_", "lighting"),
00156:     ("AlbumLetterParticle", "technical"),
00157:     ("Water", "water"),
00158:     ("Fluid", "water"),
00159: )
00160: 
00161: 
00162: PARENT_LAYER_HINTS = {
00163:     "HeroRoot": "hero",
00164:     "HeroAura": "hero",
00165:     "MistParticlesRoot": "atmosphere",
00166:     "RhythmParticlePhysicsRoot": "technical",
00167:     "SceneCore": "core",
00168: }
00169: 
00170: 
00171: TYPE_FALLBACK_LAYERS = {
00172:     "CAMERA": "render_io",
00173:     "LIGHT": "lighting",
00174:     "VOLUME": "atmosphere",
00175: }
00176: 
00177: 
00178: FEATURE_CATALOG = {
00179:     "scene": {
00180:         "layer": "core",
00181:         "module": "main_v61b.py",
00182:         "hotpatch": False,
00183:         "notes": "Owns structural bootstrap and must be rebuilt for primary object graph changes.",
00184:     },
00185:     "central_asset": {
00186:         "layer": "hero",
00187:         "module": "asset_setup.py + atmosphere_setup.py + materials.py",
00188:         "hotpatch": "MATERIALS",
00189:         "notes": "Owns hero mesh, material nodes, aura, audio deform, and nearby decorative forms.",
00190:     },
00191:     "fog": {
00192:         "layer": "atmosphere",
00193:         "module": "atmosphere_setup.py + fog_dynamics.py + hotpatch/fog_patch.py",
00194:         "hotpatch": "FOG",
00195:         "notes": "Owns volumetric cube, noise/clump material nodes, and fog pulse controllers.",
00196:     },
00197:     "orbit_accents": {
00198:         "layer": "atomic_physics",
00199:         "module": "physics_setup.py + animation.py + hotpatch/accent_patch.py",
00200:         "hotpatch": "PHYSICS",
00201:         "notes": "Owns audio-driven orbiting accents and force-field style controls.",
00202:     },
00203:     "rhythm_light": {
00204:         "layer": "lighting",
00205:         "module": "world_setup.py + hotpatch/lighting_patch.py",
00206:         "hotpatch": "ALL",
00207:         "notes": "Owns physical lights and low-amplitude support lighting.",
00208:     },
00209:     "camera_audio_output": {
00210:         "layer": "render_io",
00211:         "module": "camera_setup.py + io_utils.py + encode_image_sequence_v61b.py",
00212:         "hotpatch": "RENDER",
00213:         "notes": "Owns camera, audio strip, image sequence loading, and render/output settings.",
00214:     },
00215:     "future_water": {
00216:         "layer": "water",
00217:         "module": "spaziotempo/features/water.py (future)",
00218:         "hotpatch": "future WATER",
00219:         "notes": "Reserved only. Do not create water objects until the feature is requested.",
00220:     },
00221: }
```
