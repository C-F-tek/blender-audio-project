# Project Code Chunk 69/212

- File: `Scripting/v61b/world_setup.py`
- Part: `1`
- Lines: `1-198`

## Symbol Map
- Imports: `bpy`, `from pathlib import Path`, `from config import PEACE_PALETTE, WORLD_STRENGTH, WORLD_CAMERA_STRENGTH, WORLD_LIGHT_COLOR, WORLD_CAMERA_COLOR, USE_HDRI_WORLD, HDRI_PATH, HDRI_STRENGTH, HDRI_ROT_Z, LIGHT_ENERGY_MIN, FLOOR_SIZE, FLOOR_RENDER_VISIBLE, FLOOR_VIEWPORT_VISIBLE, USE_SOFT_BACKDROP, BACKDROP_SIZE, BACKDROP_LOCATION, BACKDROP_ROT_X, USE_INVISIBLE_COLLISION_PLANE, INVISIBLE_COLLISION_PLANE_SIZE, INVISIBLE_COLLISION_PLANE_Z`, `from materials import build_reflective_floor_material, build_invisible_surface_material, build_soft_backdrop_material`, `from scene_utils import create_controller_empty`
- Functions: `configure_world(scene)` line 34; `create_floor_and_backdrop()` line 110; `create_area_lights()` line 175

## Content
```py
00001: import bpy
00002: from pathlib import Path
00003: 
00004: from config import (
00005:     PEACE_PALETTE,
00006:     WORLD_STRENGTH,
00007:     WORLD_CAMERA_STRENGTH,
00008:     WORLD_LIGHT_COLOR,
00009:     WORLD_CAMERA_COLOR,
00010:     USE_HDRI_WORLD,
00011:     HDRI_PATH,
00012:     HDRI_STRENGTH,
00013:     HDRI_ROT_Z,
00014:     LIGHT_ENERGY_MIN,
00015:     FLOOR_SIZE,
00016:     FLOOR_RENDER_VISIBLE,
00017:     FLOOR_VIEWPORT_VISIBLE,
00018:     USE_SOFT_BACKDROP,
00019:     BACKDROP_SIZE,
00020:     BACKDROP_LOCATION,
00021:     BACKDROP_ROT_X,
00022:     USE_INVISIBLE_COLLISION_PLANE,
00023:     INVISIBLE_COLLISION_PLANE_SIZE,
00024:     INVISIBLE_COLLISION_PLANE_Z,
00025: )
00026: from materials import (
00027:     build_reflective_floor_material,
00028:     build_invisible_surface_material,
00029:     build_soft_backdrop_material,
00030: )
00031: from scene_utils import create_controller_empty
00032: 
00033: 
00034: def configure_world(scene):
00035:     world = bpy.data.worlds.new("PeaceWorld") if scene.world is None else scene.world
00036:     scene.world = world
00037:     world.use_nodes = True
00038: 
00039:     nodes = world.node_tree.nodes
00040:     links = world.node_tree.links
00041: 
00042:     for n in list(nodes):
00043:         nodes.remove(n)
00044: 
00045:     out = nodes.new("ShaderNodeOutputWorld")
00046:     out.location = (900, 0)
00047: 
00048:     if USE_HDRI_WORLD and Path(HDRI_PATH).exists():
00049:         texcoord = nodes.new("ShaderNodeTexCoord")
00050:         texcoord.location = (-1200, 0)
00051: 
00052:         mapping = nodes.new("ShaderNodeMapping")
00053:         mapping.location = (-980, 0)
00054:         mapping.inputs["Rotation"].default_value[2] = HDRI_ROT_Z
00055: 
00056:         env = nodes.new("ShaderNodeTexEnvironment")
00057:         env.location = (-720, 0)
00058:         env.image = bpy.data.images.load(str(HDRI_PATH), check_existing=True)
00059: 
00060:         bg_hdri = nodes.new("ShaderNodeBackground")
00061:         bg_hdri.location = (-420, 80)
00062:         bg_hdri.inputs["Strength"].default_value = HDRI_STRENGTH
00063: 
00064:         bg_black = nodes.new("ShaderNodeBackground")
00065:         bg_black.location = (-420, -140)
00066:         bg_black.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
00067:         bg_black.inputs["Strength"].default_value = 1.0
00068: 
00069:         light_path = nodes.new("ShaderNodeLightPath")
00070:         light_path.location = (-720, -220)
00071: 
00072:         mix = nodes.new("ShaderNodeMixShader")
00073:         mix.location = (-120, 0)
00074: 
00075:         links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
00076:         links.new(mapping.outputs["Vector"], env.inputs["Vector"])
00077:         links.new(env.outputs["Color"], bg_hdri.inputs["Color"])
00078: 
00079:         links.new(light_path.outputs["Is Camera Ray"], mix.inputs[0])
00080:         links.new(bg_hdri.outputs["Background"], mix.inputs[1])
00081:         links.new(bg_black.outputs["Background"], mix.inputs[2])
00082:         links.new(mix.outputs["Shader"], out.inputs["Surface"])
00083:     else:
00084:         bg_camera = nodes.new("ShaderNodeBackground")
00085:         bg_camera.name = "WorldCameraAzzurro"
00086:         bg_camera.location = (-260, 80)
00087:         bg_camera.inputs["Strength"].default_value = WORLD_CAMERA_STRENGTH
00088:         bg_camera.inputs["Color"].default_value = WORLD_CAMERA_COLOR
00089: 
00090:         bg_light = nodes.new("ShaderNodeBackground")
00091:         bg_light.name = "WorldSceneLight"
00092:         bg_light.location = (-260, -130)
00093:         bg_light.inputs["Strength"].default_value = WORLD_STRENGTH
00094:         bg_light.inputs["Color"].default_value = WORLD_LIGHT_COLOR
00095: 
00096:         light_path = nodes.new("ShaderNodeLightPath")
00097:         light_path.location = (-560, -70)
00098: 
00099:         mix = nodes.new("ShaderNodeMixShader")
00100:         mix.location = (120, 0)
00101: 
00102:         links.new(light_path.outputs["Is Camera Ray"], mix.inputs[0])
00103:         links.new(bg_light.outputs["Background"], mix.inputs[1])
00104:         links.new(bg_camera.outputs["Background"], mix.inputs[2])
00105:         links.new(mix.outputs["Shader"], out.inputs["Surface"])
00106: 
00107:     return world
00108: 
00109: 
00110: def create_floor_and_backdrop():
00111:     floor_mat, floor_rough_output = build_reflective_floor_material()
00112: 
00113:     bpy.ops.mesh.primitive_plane_add(size=FLOOR_SIZE, location=(0, 0, 0))
00114:     floor = bpy.context.active_object
00115:     floor.name = "PeaceFloor"
00116:     floor.data.materials.append(floor_mat)
00117:     floor.hide_render = not FLOOR_RENDER_VISIBLE
00118:     floor.hide_viewport = not FLOOR_VIEWPORT_VISIBLE
00119: 
00120:     invisible_plane = None
00121:     if USE_INVISIBLE_COLLISION_PLANE:
00122:         invisible_mat = build_invisible_surface_material("InvisibleParticleFloorMaterial")
00123:         bpy.ops.mesh.primitive_plane_add(
00124:             size=INVISIBLE_COLLISION_PLANE_SIZE,
00125:             location=(0, 0, INVISIBLE_COLLISION_PLANE_Z),
00126:         )
00127:         invisible_plane = bpy.context.active_object
00128:         invisible_plane.name = "InvisibleParticleFloor"
00129:         invisible_plane.data.materials.append(invisible_mat)
00130:         invisible_plane.hide_render = True
00131:         invisible_plane.hide_viewport = True
00132:         invisible_plane.hide_select = True
00133: 
00134:     backdrop = None
00135:     backdrop_controls = {}
00136:     backdrop_controller = None
00137: 
00138:     if USE_SOFT_BACKDROP:
00139:         backdrop_mat, backdrop_controls = build_soft_backdrop_material()
00140:         bpy.ops.mesh.primitive_plane_add(
00141:             size=BACKDROP_SIZE,
00142:             location=BACKDROP_LOCATION,
00143:             rotation=(BACKDROP_ROT_X, 0.0, 0.0),
00144:         )
00145:         backdrop = bpy.context.active_object
00146:         backdrop.name = "SoftRhythmBackdrop"
00147:         backdrop.data.materials.append(backdrop_mat)
00148:         backdrop.hide_select = True
00149: 
00150:         try:
00151:             backdrop.visible_shadow = False
00152:         except Exception:
00153:             pass
00154: 
00155:         backdrop_controller = create_controller_empty(
00156:             "BackdropPulseController",
00157:             location=BACKDROP_LOCATION,
00158:             display_size=0.35,
00159:             hide_view=True,
00160:         )
00161: 
00162:     return {
00163:         "floor": floor,
00164:         "floor_material": floor_mat,
00165:         "floor_rough_socket": floor_rough_output,
00166:         "invisible_particle_floor": invisible_plane,
00167:         "backdrop": backdrop,
00168:         "backdrop_controller": backdrop_controller,
00169:         "backdrop_controls": backdrop_controls,
00170:         "backdrop_base_scale": backdrop.scale.copy() if backdrop else None,
00171:         "backdrop_base_location": backdrop.location.copy() if backdrop else None,
00172:     }
00173: 
00174: 
00175: def create_area_lights():
00176:     lights = []
00177: 
00178:     positions = [
00179:         (-6.0, -5.8, 5.8),
00180:         (6.0, -5.8, 5.8),
00181:         (0.0, 7.6, 4.8),
00182:     ]
00183:     colors = [
00184:         PEACE_PALETTE["soft_teal"],
00185:         PEACE_PALETTE["muted_gold"],
00186:         PEACE_PALETTE["dust_rose"],
00187:     ]
00188: 
00189:     for idx, (pos, col) in enumerate(zip(positions, colors)):
00190:         bpy.ops.object.light_add(type='AREA', location=pos)
00191:         light = bpy.context.active_object
00192:         light.name = f"AreaLight_{idx:02d}"
00193:         light.data.energy = LIGHT_ENERGY_MIN
00194:         light.data.color = (col[0], col[1], col[2])
00195:         light.scale = (4.5, 4.5, 4.5)
00196:         lights.append(light)
00197: 
00198:     return lights
```
