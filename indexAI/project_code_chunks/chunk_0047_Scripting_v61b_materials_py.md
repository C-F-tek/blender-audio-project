# Project Code Chunk 47/212

- File: `Scripting/v61b/materials.py`
- Part: `1`
- Lines: `1-308`

## Symbol Map
- Imports: `bpy`, `from config import PEACE_PALETTE, FOG_DENSITY_MIN, FOG_EMISSION_MIN, FOG_NOISE_SCALE_MIN, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_WAVE_SCALE_MIN, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_WEIGHT_MIN, FOG_FILAMENT_ALPHA_MIN, FOG_FILAMENT_EMISSION_MIN, FOG_FILAMENT_NOISE_SCALE_MIN, FOG_FILAMENT_WAVE_SCALE_MIN, AURA_EMIT_MIN, RING_EMIT_MIN, RIBBON_EMIT_MIN, BACKDROP_EMISSION_MIN`
- Functions: `build_reflective_floor_material()` line 25; `build_invisible_surface_material(name)` line 67; `build_soft_backdrop_material()` line 91; `build_aura_material()` line 140; `build_variant_material(name, color)` line 186; `build_ring_material(name, color)` line 226; `build_ribbon_material(name, color)` line 248; `build_atmosphere_volume_material()` line 270; `build_fog_filament_material(name)` line 478; `build_mist_particle_material(name, color)` line 618

## Content
```py
00001: import bpy
00002: 
00003: from config import (
00004:     PEACE_PALETTE,
00005:     FOG_DENSITY_MIN,
00006:     FOG_EMISSION_MIN,
00007:     FOG_NOISE_SCALE_MIN,
00008:     FOG_CLUMP_SCALE_MIN,
00009:     FOG_CLUMP_RAMP_LOW_BASE,
00010:     FOG_CLUMP_RAMP_HIGH_BASE,
00011:     FOG_WAVE_SCALE_MIN,
00012:     FOG_WAVE_DISTORTION_MIN,
00013:     FOG_WAVE_WEIGHT_MIN,
00014:     FOG_FILAMENT_ALPHA_MIN,
00015:     FOG_FILAMENT_EMISSION_MIN,
00016:     FOG_FILAMENT_NOISE_SCALE_MIN,
00017:     FOG_FILAMENT_WAVE_SCALE_MIN,
00018:     AURA_EMIT_MIN,
00019:     RING_EMIT_MIN,
00020:     RIBBON_EMIT_MIN,
00021:     BACKDROP_EMISSION_MIN,
00022: )
00023: 
00024: 
00025: def build_reflective_floor_material():
00026:     mat = bpy.data.materials.new(name="PeaceFloorMaterial")
00027:     mat.use_nodes = True
00028: 
00029:     nodes = mat.node_tree.nodes
00030:     links = mat.node_tree.links
00031:     bsdf = nodes.get("Principled BSDF")
00032: 
00033:     texcoord = nodes.new("ShaderNodeTexCoord")
00034:     texcoord.location = (-900, -100)
00035: 
00036:     mapping = nodes.new("ShaderNodeMapping")
00037:     mapping.location = (-700, -100)
00038: 
00039:     noise = nodes.new("ShaderNodeTexNoise")
00040:     noise.location = (-470, -100)
00041:     noise.inputs["Scale"].default_value = 7.0
00042:     noise.inputs["Detail"].default_value = 9.0
00043:     noise.inputs["Roughness"].default_value = 0.58
00044: 
00045:     bump = nodes.new("ShaderNodeBump")
00046:     bump.location = (-220, -140)
00047:     bump.inputs["Strength"].default_value = 0.035
00048: 
00049:     rough_val = nodes.new("ShaderNodeValue")
00050:     rough_val.location = (-260, 110)
00051:     rough_val.outputs[0].default_value = 0.22
00052:     rough_val.name = "FloorRoughnessValue"
00053: 
00054:     bsdf.inputs["Base Color"].default_value = (0.055, 0.060, 0.070, 1.0)
00055:     bsdf.inputs["Metallic"].default_value = 0.08
00056:     bsdf.inputs["Roughness"].default_value = 0.22
00057: 
00058:     links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
00059:     links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
00060:     links.new(noise.outputs["Fac"], bump.inputs["Height"])
00061:     links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
00062:     links.new(rough_val.outputs[0], bsdf.inputs["Roughness"])
00063: 
00064:     return mat, rough_val.outputs[0]
00065: 
00066: 
00067: def build_invisible_surface_material(name="InvisibleSurfaceMaterial"):
00068:     mat = bpy.data.materials.new(name=name)
00069:     mat.use_nodes = True
00070: 
00071:     if hasattr(mat, "blend_method"):
00072:         mat.blend_method = 'BLEND'
00073:     if hasattr(mat, "shadow_method"):
00074:         mat.shadow_method = 'NONE'
00075: 
00076:     nodes = mat.node_tree.nodes
00077:     links = mat.node_tree.links
00078:     for node in list(nodes):
00079:         nodes.remove(node)
00080: 
00081:     out = nodes.new("ShaderNodeOutputMaterial")
00082:     out.location = (360, 0)
00083: 
00084:     transparent = nodes.new("ShaderNodeBsdfTransparent")
00085:     transparent.location = (120, 0)
00086: 
00087:     links.new(transparent.outputs["BSDF"], out.inputs["Surface"])
00088:     return mat
00089: 
00090: 
00091: def build_soft_backdrop_material():
00092:     mat = bpy.data.materials.new(name="SoftBackdropMaterial")
00093:     mat.use_nodes = True
00094: 
00095:     nodes = mat.node_tree.nodes
00096:     links = mat.node_tree.links
00097:     for node in list(nodes):
00098:         nodes.remove(node)
00099: 
00100:     out = nodes.new("ShaderNodeOutputMaterial")
00101:     out.location = (760, 0)
00102: 
00103:     texcoord = nodes.new("ShaderNodeTexCoord")
00104:     texcoord.location = (-760, 0)
00105: 
00106:     mapping = nodes.new("ShaderNodeMapping")
00107:     mapping.location = (-540, 0)
00108: 
00109:     noise = nodes.new("ShaderNodeTexNoise")
00110:     noise.location = (-320, 0)
00111:     noise.inputs["Scale"].default_value = 1.18
00112:     noise.inputs["Detail"].default_value = 6.0
00113:     noise.inputs["Roughness"].default_value = 0.46
00114: 
00115:     ramp = nodes.new("ShaderNodeValToRGB")
00116:     ramp.location = (-80, 0)
00117:     ramp.color_ramp.elements[0].position = 0.14
00118:     ramp.color_ramp.elements[0].color = (0.012, 0.055, 0.064, 1.0)
00119:     ramp.color_ramp.elements[1].position = 1.00
00120:     ramp.color_ramp.elements[1].color = (0.085, 0.245, 0.255, 1.0)
00121: 
00122:     emission = nodes.new("ShaderNodeEmission")
00123:     emission.location = (280, 0)
00124:     emission.inputs["Strength"].default_value = BACKDROP_EMISSION_MIN
00125:     emission.name = "BackdropEmission"
00126: 
00127:     links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
00128:     links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
00129:     links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
00130:     links.new(ramp.outputs["Color"], emission.inputs["Color"])
00131:     links.new(emission.outputs["Emission"], out.inputs["Surface"])
00132: 
00133:     return mat, {
00134:         "emission_socket": emission.inputs["Strength"],
00135:         "mapping_location_socket": mapping.inputs["Location"],
00136:         "noise_scale_socket": noise.inputs["Scale"],
00137:     }
00138: 
00139: 
00140: def build_aura_material():
00141:     mat = bpy.data.materials.new(name="HeroAuraMaterial")
00142:     mat.use_nodes = True
00143: 
00144:     if hasattr(mat, "blend_method"):
00145:         mat.blend_method = 'BLEND'
00146:     if hasattr(mat, "shadow_method"):
00147:         mat.shadow_method = 'NONE'
00148: 
00149:     nodes = mat.node_tree.nodes
00150:     links = mat.node_tree.links
00151:     for n in list(nodes):
00152:         nodes.remove(n)
00153: 
00154:     out = nodes.new("ShaderNodeOutputMaterial")
00155:     out.location = (900, 0)
00156: 
00157:     mix = nodes.new("ShaderNodeMixShader")
00158:     mix.location = (650, 0)
00159: 
00160:     transparent = nodes.new("ShaderNodeBsdfTransparent")
00161:     transparent.location = (380, -120)
00162: 
00163:     emission = nodes.new("ShaderNodeEmission")
00164:     emission.location = (380, 120)
00165:     emission.inputs["Color"].default_value = PEACE_PALETTE["soft_teal"]
00166:     emission.inputs["Strength"].default_value = AURA_EMIT_MIN
00167:     emission.name = "AuraEmission"
00168: 
00169:     fresnel = nodes.new("ShaderNodeLayerWeight")
00170:     fresnel.location = (120, -260)
00171: 
00172:     ramp = nodes.new("ShaderNodeValToRGB")
00173:     ramp.location = (380, -300)
00174:     ramp.color_ramp.elements[0].position = 0.18
00175:     ramp.color_ramp.elements[1].position = 0.92
00176: 
00177:     links.new(fresnel.outputs["Facing"], ramp.inputs["Fac"])
00178:     links.new(ramp.outputs["Color"], mix.inputs[0])
00179:     links.new(emission.outputs["Emission"], mix.inputs[1])
00180:     links.new(transparent.outputs["BSDF"], mix.inputs[2])
00181:     links.new(mix.outputs["Shader"], out.inputs["Surface"])
00182: 
00183:     return mat, emission.inputs["Strength"], ramp.color_ramp.elements[0]
00184: 
00185: 
00186: def build_variant_material(name, color):
00187:     mat = bpy.data.materials.new(name=name)
00188:     mat.use_nodes = True
00189: 
00190:     nodes = mat.node_tree.nodes
00191:     links = mat.node_tree.links
00192:     for n in list(nodes):
00193:         nodes.remove(n)
00194: 
00195:     out = nodes.new("ShaderNodeOutputMaterial")
00196:     out.location = (700, 0)
00197: 
00198:     mix = nodes.new("ShaderNodeMixShader")
00199:     mix.location = (420, 0)
00200: 
00201:     principled = nodes.new("ShaderNodeBsdfPrincipled")
00202:     principled.location = (120, -120)
00203:     principled.inputs["Base Color"].default_value = color
00204:     principled.inputs["Metallic"].default_value = 0.18
00205:     principled.inputs["Roughness"].default_value = 0.32
00206: 
00207:     emission = nodes.new("ShaderNodeEmission")
00208:     emission.location = (120, 120)
00209:     emission.name = "VariantEmission"
00210:     emission.inputs["Color"].default_value = color
00211:     emission.inputs["Strength"].default_value = 0.32
00212: 
00213:     fac = nodes.new("ShaderNodeValue")
00214:     fac.location = (120, -300)
00215:     fac.name = "VariantEmissionMix"
00216:     fac.outputs[0].default_value = 0.20
00217: 
00218:     links.new(fac.outputs[0], mix.inputs[0])
00219:     links.new(principled.outputs["BSDF"], mix.inputs[1])
00220:     links.new(emission.outputs["Emission"], mix.inputs[2])
00221:     links.new(mix.outputs["Shader"], out.inputs["Surface"])
00222: 
00223:     return mat
00224: 
00225: 
00226: def build_ring_material(name, color):
00227:     mat = bpy.data.materials.new(name=name)
00228:     mat.use_nodes = True
00229: 
00230:     nodes = mat.node_tree.nodes
00231:     links = mat.node_tree.links
00232:     for n in list(nodes):
00233:         nodes.remove(n)
00234: 
00235:     out = nodes.new("ShaderNodeOutputMaterial")
00236:     out.location = (520, 0)
00237: 
00238:     emission = nodes.new("ShaderNodeEmission")
00239:     emission.location = (240, 0)
00240:     emission.inputs["Color"].default_value = color
00241:     emission.inputs["Strength"].default_value = RING_EMIT_MIN
00242:     emission.name = "RingEmission"
00243: 
00244:     links.new(emission.outputs["Emission"], out.inputs["Surface"])
00245:     return mat, emission.inputs["Strength"]
00246: 
00247: 
00248: def build_ribbon_material(name, color):
00249:     mat = bpy.data.materials.new(name=name)
00250:     mat.use_nodes = True
00251: 
00252:     nodes = mat.node_tree.nodes
00253:     links = mat.node_tree.links
00254:     for n in list(nodes):
00255:         nodes.remove(n)
00256: 
00257:     out = nodes.new("ShaderNodeOutputMaterial")
00258:     out.location = (520, 0)
00259: 
00260:     emission = nodes.new("ShaderNodeEmission")
00261:     emission.location = (240, 0)
00262:     emission.inputs["Color"].default_value = color
00263:     emission.inputs["Strength"].default_value = RIBBON_EMIT_MIN
00264:     emission.name = "RibbonEmission"
00265: 
00266:     links.new(emission.outputs["Emission"], out.inputs["Surface"])
00267:     return mat, emission.inputs["Strength"]
00268: 
00269: 
00270: def build_atmosphere_volume_material():
00271:     mat = bpy.data.materials.new(name="AtmosphereVolumeMaterial")
00272:     mat.use_nodes = True
00273:     mat["spaziotempo_volume_fog"] = True
00274: 
00275:     try:
00276:         mat.blend_method = 'BLEND'
00277:     except Exception:
00278:         pass
00279:     try:
00280:         mat.use_screen_refraction = False
00281:     except Exception:
00282:         pass
00283: 
00284:     nodes = mat.node_tree.nodes
00285:     links = mat.node_tree.links
00286:     for n in list(nodes):
00287:         nodes.remove(n)
00288: 
00289:     out = nodes.new("ShaderNodeOutputMaterial")
00290:     out.location = (980, 0)
00291: 
00292:     texcoord = nodes.new("ShaderNodeTexCoord")
00293:     texcoord.location = (-1000, 80)
00294: 
00295:     mapping = nodes.new("ShaderNodeMapping")
00296:     mapping.location = (-760, 80)
00297: 
00298:     noise = nodes.new("ShaderNodeTexNoise")
00299:     noise.location = (-520, 80)
00300:     noise.inputs["Scale"].default_value = FOG_NOISE_SCALE_MIN
00301:     noise.inputs["Detail"].default_value = 6.0
00302:     noise.inputs["Roughness"].default_value = 0.64
00303: 
00304:     ramp = nodes.new("ShaderNodeValToRGB")
00305:     ramp.location = (-280, 80)
00306:     ramp.color_ramp.elements[0].position = 0.28
00307:     ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
00308:     ramp.color_ramp.elements[1].position = 0.54
```
