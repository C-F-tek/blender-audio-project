# Project Code Chunk 112/212

- File: `Scripting/v61b_backgood/world_setup.py`
- Part: `1`
- Lines: `1-174`

## Symbol Map
- Imports: `bpy`, `from pathlib import Path`, `from config import PEACE_PALETTE, WORLD_STRENGTH, USE_HDRI_WORLD, HDRI_PATH, HDRI_STRENGTH, HDRI_ROT_Z, LIGHT_ENERGY_MIN, FLOOR_SIZE, USE_SOFT_BACKDROP, BACKDROP_SIZE, BACKDROP_LOCATION, BACKDROP_ROT_X, USE_INVISIBLE_COLLISION_PLANE, INVISIBLE_COLLISION_PLANE_SIZE, INVISIBLE_COLLISION_PLANE_Z`, `from materials import build_reflective_floor_material, build_invisible_surface_material, build_soft_backdrop_material`, `from scene_utils import create_controller_empty`
- Functions: `configure_world(scene)` line 29; `create_floor_and_backdrop()` line 88; `create_area_lights()` line 151

## Content
```py
00001: import bpy
00002: from pathlib import Path
00003: 
00004: from config import (
00005:     PEACE_PALETTE,
00006:     WORLD_STRENGTH,
00007:     USE_HDRI_WORLD,
00008:     HDRI_PATH,
00009:     HDRI_STRENGTH,
00010:     HDRI_ROT_Z,
00011:     LIGHT_ENERGY_MIN,
00012:     FLOOR_SIZE,
00013:     USE_SOFT_BACKDROP,
00014:     BACKDROP_SIZE,
00015:     BACKDROP_LOCATION,
00016:     BACKDROP_ROT_X,
00017:     USE_INVISIBLE_COLLISION_PLANE,
00018:     INVISIBLE_COLLISION_PLANE_SIZE,
00019:     INVISIBLE_COLLISION_PLANE_Z,
00020: )
00021: from materials import (
00022:     build_reflective_floor_material,
00023:     build_invisible_surface_material,
00024:     build_soft_backdrop_material,
00025: )
00026: from scene_utils import create_controller_empty
00027: 
00028: 
00029: def configure_world(scene):
00030:     world = bpy.data.worlds.new("PeaceWorld") if scene.world is None else scene.world
00031:     scene.world = world
00032:     world.use_nodes = True
00033: 
00034:     nodes = world.node_tree.nodes
00035:     links = world.node_tree.links
00036: 
00037:     for n in list(nodes):
00038:         nodes.remove(n)
00039: 
00040:     out = nodes.new("ShaderNodeOutputWorld")
00041:     out.location = (900, 0)
00042: 
00043:     if USE_HDRI_WORLD and Path(HDRI_PATH).exists():
00044:         texcoord = nodes.new("ShaderNodeTexCoord")
00045:         texcoord.location = (-1200, 0)
00046: 
00047:         mapping = nodes.new("ShaderNodeMapping")
00048:         mapping.location = (-980, 0)
00049:         mapping.inputs["Rotation"].default_value[2] = HDRI_ROT_Z
00050: 
00051:         env = nodes.new("ShaderNodeTexEnvironment")
00052:         env.location = (-720, 0)
00053:         env.image = bpy.data.images.load(str(HDRI_PATH), check_existing=True)
00054: 
00055:         bg_hdri = nodes.new("ShaderNodeBackground")
00056:         bg_hdri.location = (-420, 80)
00057:         bg_hdri.inputs["Strength"].default_value = HDRI_STRENGTH
00058: 
00059:         bg_black = nodes.new("ShaderNodeBackground")
00060:         bg_black.location = (-420, -140)
00061:         bg_black.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
00062:         bg_black.inputs["Strength"].default_value = 1.0
00063: 
00064:         light_path = nodes.new("ShaderNodeLightPath")
00065:         light_path.location = (-720, -220)
00066: 
00067:         mix = nodes.new("ShaderNodeMixShader")
00068:         mix.location = (-120, 0)
00069: 
00070:         links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
00071:         links.new(mapping.outputs["Vector"], env.inputs["Vector"])
00072:         links.new(env.outputs["Color"], bg_hdri.inputs["Color"])
00073: 
00074:         links.new(light_path.outputs["Is Camera Ray"], mix.inputs[0])
00075:         links.new(bg_hdri.outputs["Background"], mix.inputs[1])
00076:         links.new(bg_black.outputs["Background"], mix.inputs[2])
00077:         links.new(mix.outputs["Shader"], out.inputs["Surface"])
00078:     else:
00079:         bg = nodes.new("ShaderNodeBackground")
00080:         bg.location = (260, 0)
00081:         bg.inputs["Strength"].default_value = WORLD_STRENGTH
00082:         bg.inputs["Color"].default_value = PEACE_PALETTE["twilight_blue"]
00083:         links.new(bg.outputs["Background"], out.inputs["Surface"])
00084: 
00085:     return world
00086: 
00087: 
00088: def create_floor_and_backdrop():
00089:     floor_mat, floor_rough_output = build_reflective_floor_material()
00090: 
00091:     bpy.ops.mesh.primitive_plane_add(size=FLOOR_SIZE, location=(0, 0, 0))
00092:     floor = bpy.context.active_object
00093:     floor.name = "PeaceFloor"
00094:     floor.data.materials.append(floor_mat)
00095: 
00096:     invisible_plane = None
00097:     if USE_INVISIBLE_COLLISION_PLANE:
00098:         invisible_mat = build_invisible_surface_material("InvisibleParticleFloorMaterial")
00099:         bpy.ops.mesh.primitive_plane_add(
00100:             size=INVISIBLE_COLLISION_PLANE_SIZE,
00101:             location=(0, 0, INVISIBLE_COLLISION_PLANE_Z),
00102:         )
00103:         invisible_plane = bpy.context.active_object
00104:         invisible_plane.name = "InvisibleParticleFloor"
00105:         invisible_plane.data.materials.append(invisible_mat)
00106:         invisible_plane.hide_render = True
00107:         invisible_plane.hide_viewport = True
00108:         invisible_plane.hide_select = True
00109: 
00110:     backdrop = None
00111:     backdrop_controls = {}
00112:     backdrop_controller = None
00113: 
00114:     if USE_SOFT_BACKDROP:
00115:         backdrop_mat, backdrop_controls = build_soft_backdrop_material()
00116:         bpy.ops.mesh.primitive_plane_add(
00117:             size=BACKDROP_SIZE,
00118:             location=BACKDROP_LOCATION,
00119:             rotation=(BACKDROP_ROT_X, 0.0, 0.0),
00120:         )
00121:         backdrop = bpy.context.active_object
00122:         backdrop.name = "SoftRhythmBackdrop"
00123:         backdrop.data.materials.append(backdrop_mat)
00124:         backdrop.hide_select = True
00125: 
00126:         try:
00127:             backdrop.visible_shadow = False
00128:         except Exception:
00129:             pass
00130: 
00131:         backdrop_controller = create_controller_empty(
00132:             "BackdropPulseController",
00133:             location=BACKDROP_LOCATION,
00134:             display_size=0.35,
00135:             hide_view=True,
00136:         )
00137: 
00138:     return {
00139:         "floor": floor,
00140:         "floor_material": floor_mat,
00141:         "floor_rough_socket": floor_rough_output,
00142:         "invisible_particle_floor": invisible_plane,
00143:         "backdrop": backdrop,
00144:         "backdrop_controller": backdrop_controller,
00145:         "backdrop_controls": backdrop_controls,
00146:         "backdrop_base_scale": backdrop.scale.copy() if backdrop else None,
00147:         "backdrop_base_location": backdrop.location.copy() if backdrop else None,
00148:     }
00149: 
00150: 
00151: def create_area_lights():
00152:     lights = []
00153: 
00154:     positions = [
00155:         (-6.0, -5.8, 5.8),
00156:         (6.0, -5.8, 5.8),
00157:         (0.0, 7.6, 4.8),
00158:     ]
00159:     colors = [
00160:         PEACE_PALETTE["soft_teal"],
00161:         PEACE_PALETTE["muted_gold"],
00162:         PEACE_PALETTE["dust_rose"],
00163:     ]
00164: 
00165:     for idx, (pos, col) in enumerate(zip(positions, colors)):
00166:         bpy.ops.object.light_add(type='AREA', location=pos)
00167:         light = bpy.context.active_object
00168:         light.name = f"AreaLight_{idx:02d}"
00169:         light.data.energy = LIGHT_ENERGY_MIN
00170:         light.data.color = (col[0], col[1], col[2])
00171:         light.scale = (4.5, 4.5, 4.5)
00172:         lights.append(light)
00173: 
00174:     return lights
```
