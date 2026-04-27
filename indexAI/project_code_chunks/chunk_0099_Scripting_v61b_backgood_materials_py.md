# Project Code Chunk 99/212

- File: `Scripting/v61b_backgood/materials.py`
- Part: `1`
- Lines: `1-307`

## Symbol Map
- Imports: `bpy`, `from config import PEACE_PALETTE, FOG_DENSITY_MIN, FOG_EMISSION_MIN, FOG_NOISE_SCALE_MIN, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_WAVE_SCALE_MIN, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_WEIGHT_MIN, AURA_EMIT_MIN, RING_EMIT_MIN, RIBBON_EMIT_MIN, BACKDROP_EMISSION_MIN`
- Functions: `build_reflective_floor_material()` line 21; `build_invisible_surface_material(name)` line 63; `build_soft_backdrop_material()` line 87; `build_aura_material()` line 136; `build_variant_material(name, color)` line 182; `build_ring_material(name, color)` line 222; `build_ribbon_material(name, color)` line 244; `build_atmosphere_volume_material()` line 266; `build_mist_particle_material(name, color)` line 474

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
00014:     AURA_EMIT_MIN,
00015:     RING_EMIT_MIN,
00016:     RIBBON_EMIT_MIN,
00017:     BACKDROP_EMISSION_MIN,
00018: )
00019: 
00020: 
00021: def build_reflective_floor_material():
00022:     mat = bpy.data.materials.new(name="PeaceFloorMaterial")
00023:     mat.use_nodes = True
00024: 
00025:     nodes = mat.node_tree.nodes
00026:     links = mat.node_tree.links
00027:     bsdf = nodes.get("Principled BSDF")
00028: 
00029:     texcoord = nodes.new("ShaderNodeTexCoord")
00030:     texcoord.location = (-900, -100)
00031: 
00032:     mapping = nodes.new("ShaderNodeMapping")
00033:     mapping.location = (-700, -100)
00034: 
00035:     noise = nodes.new("ShaderNodeTexNoise")
00036:     noise.location = (-470, -100)
00037:     noise.inputs["Scale"].default_value = 7.0
00038:     noise.inputs["Detail"].default_value = 9.0
00039:     noise.inputs["Roughness"].default_value = 0.58
00040: 
00041:     bump = nodes.new("ShaderNodeBump")
00042:     bump.location = (-220, -140)
00043:     bump.inputs["Strength"].default_value = 0.035
00044: 
00045:     rough_val = nodes.new("ShaderNodeValue")
00046:     rough_val.location = (-260, 110)
00047:     rough_val.outputs[0].default_value = 0.22
00048:     rough_val.name = "FloorRoughnessValue"
00049: 
00050:     bsdf.inputs["Base Color"].default_value = (0.055, 0.060, 0.070, 1.0)
00051:     bsdf.inputs["Metallic"].default_value = 0.08
00052:     bsdf.inputs["Roughness"].default_value = 0.22
00053: 
00054:     links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
00055:     links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
00056:     links.new(noise.outputs["Fac"], bump.inputs["Height"])
00057:     links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
00058:     links.new(rough_val.outputs[0], bsdf.inputs["Roughness"])
00059: 
00060:     return mat, rough_val.outputs[0]
00061: 
00062: 
00063: def build_invisible_surface_material(name="InvisibleSurfaceMaterial"):
00064:     mat = bpy.data.materials.new(name=name)
00065:     mat.use_nodes = True
00066: 
00067:     if hasattr(mat, "blend_method"):
00068:         mat.blend_method = 'BLEND'
00069:     if hasattr(mat, "shadow_method"):
00070:         mat.shadow_method = 'NONE'
00071: 
00072:     nodes = mat.node_tree.nodes
00073:     links = mat.node_tree.links
00074:     for node in list(nodes):
00075:         nodes.remove(node)
00076: 
00077:     out = nodes.new("ShaderNodeOutputMaterial")
00078:     out.location = (360, 0)
00079: 
00080:     transparent = nodes.new("ShaderNodeBsdfTransparent")
00081:     transparent.location = (120, 0)
00082: 
00083:     links.new(transparent.outputs["BSDF"], out.inputs["Surface"])
00084:     return mat
00085: 
00086: 
00087: def build_soft_backdrop_material():
00088:     mat = bpy.data.materials.new(name="SoftBackdropMaterial")
00089:     mat.use_nodes = True
00090: 
00091:     nodes = mat.node_tree.nodes
00092:     links = mat.node_tree.links
00093:     for node in list(nodes):
00094:         nodes.remove(node)
00095: 
00096:     out = nodes.new("ShaderNodeOutputMaterial")
00097:     out.location = (760, 0)
00098: 
00099:     texcoord = nodes.new("ShaderNodeTexCoord")
00100:     texcoord.location = (-760, 0)
00101: 
00102:     mapping = nodes.new("ShaderNodeMapping")
00103:     mapping.location = (-540, 0)
00104: 
00105:     noise = nodes.new("ShaderNodeTexNoise")
00106:     noise.location = (-320, 0)
00107:     noise.inputs["Scale"].default_value = 2.4
00108:     noise.inputs["Detail"].default_value = 8.0
00109:     noise.inputs["Roughness"].default_value = 0.55
00110: 
00111:     ramp = nodes.new("ShaderNodeValToRGB")
00112:     ramp.location = (-80, 0)
00113:     ramp.color_ramp.elements[0].position = 0.20
00114:     ramp.color_ramp.elements[0].color = PEACE_PALETTE["twilight_blue"]
00115:     ramp.color_ramp.elements[1].position = 1.00
00116:     ramp.color_ramp.elements[1].color = PEACE_PALETTE["soft_teal"]
00117: 
00118:     emission = nodes.new("ShaderNodeEmission")
00119:     emission.location = (280, 0)
00120:     emission.inputs["Strength"].default_value = BACKDROP_EMISSION_MIN
00121:     emission.name = "BackdropEmission"
00122: 
00123:     links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
00124:     links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
00125:     links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
00126:     links.new(ramp.outputs["Color"], emission.inputs["Color"])
00127:     links.new(emission.outputs["Emission"], out.inputs["Surface"])
00128: 
00129:     return mat, {
00130:         "emission_socket": emission.inputs["Strength"],
00131:         "mapping_location_socket": mapping.inputs["Location"],
00132:         "noise_scale_socket": noise.inputs["Scale"],
00133:     }
00134: 
00135: 
00136: def build_aura_material():
00137:     mat = bpy.data.materials.new(name="HeroAuraMaterial")
00138:     mat.use_nodes = True
00139: 
00140:     if hasattr(mat, "blend_method"):
00141:         mat.blend_method = 'BLEND'
00142:     if hasattr(mat, "shadow_method"):
00143:         mat.shadow_method = 'NONE'
00144: 
00145:     nodes = mat.node_tree.nodes
00146:     links = mat.node_tree.links
00147:     for n in list(nodes):
00148:         nodes.remove(n)
00149: 
00150:     out = nodes.new("ShaderNodeOutputMaterial")
00151:     out.location = (900, 0)
00152: 
00153:     mix = nodes.new("ShaderNodeMixShader")
00154:     mix.location = (650, 0)
00155: 
00156:     transparent = nodes.new("ShaderNodeBsdfTransparent")
00157:     transparent.location = (380, -120)
00158: 
00159:     emission = nodes.new("ShaderNodeEmission")
00160:     emission.location = (380, 120)
00161:     emission.inputs["Color"].default_value = PEACE_PALETTE["soft_teal"]
00162:     emission.inputs["Strength"].default_value = AURA_EMIT_MIN
00163:     emission.name = "AuraEmission"
00164: 
00165:     fresnel = nodes.new("ShaderNodeLayerWeight")
00166:     fresnel.location = (120, -260)
00167: 
00168:     ramp = nodes.new("ShaderNodeValToRGB")
00169:     ramp.location = (380, -300)
00170:     ramp.color_ramp.elements[0].position = 0.18
00171:     ramp.color_ramp.elements[1].position = 0.92
00172: 
00173:     links.new(fresnel.outputs["Facing"], ramp.inputs["Fac"])
00174:     links.new(ramp.outputs["Color"], mix.inputs[0])
00175:     links.new(emission.outputs["Emission"], mix.inputs[1])
00176:     links.new(transparent.outputs["BSDF"], mix.inputs[2])
00177:     links.new(mix.outputs["Shader"], out.inputs["Surface"])
00178: 
00179:     return mat, emission.inputs["Strength"], ramp.color_ramp.elements[0]
00180: 
00181: 
00182: def build_variant_material(name, color):
00183:     mat = bpy.data.materials.new(name=name)
00184:     mat.use_nodes = True
00185: 
00186:     nodes = mat.node_tree.nodes
00187:     links = mat.node_tree.links
00188:     for n in list(nodes):
00189:         nodes.remove(n)
00190: 
00191:     out = nodes.new("ShaderNodeOutputMaterial")
00192:     out.location = (700, 0)
00193: 
00194:     mix = nodes.new("ShaderNodeMixShader")
00195:     mix.location = (420, 0)
00196: 
00197:     principled = nodes.new("ShaderNodeBsdfPrincipled")
00198:     principled.location = (120, -120)
00199:     principled.inputs["Base Color"].default_value = color
00200:     principled.inputs["Metallic"].default_value = 0.18
00201:     principled.inputs["Roughness"].default_value = 0.32
00202: 
00203:     emission = nodes.new("ShaderNodeEmission")
00204:     emission.location = (120, 120)
00205:     emission.name = "VariantEmission"
00206:     emission.inputs["Color"].default_value = color
00207:     emission.inputs["Strength"].default_value = 0.32
00208: 
00209:     fac = nodes.new("ShaderNodeValue")
00210:     fac.location = (120, -300)
00211:     fac.name = "VariantEmissionMix"
00212:     fac.outputs[0].default_value = 0.20
00213: 
00214:     links.new(fac.outputs[0], mix.inputs[0])
00215:     links.new(principled.outputs["BSDF"], mix.inputs[1])
00216:     links.new(emission.outputs["Emission"], mix.inputs[2])
00217:     links.new(mix.outputs["Shader"], out.inputs["Surface"])
00218: 
00219:     return mat
00220: 
00221: 
00222: def build_ring_material(name, color):
00223:     mat = bpy.data.materials.new(name=name)
00224:     mat.use_nodes = True
00225: 
00226:     nodes = mat.node_tree.nodes
00227:     links = mat.node_tree.links
00228:     for n in list(nodes):
00229:         nodes.remove(n)
00230: 
00231:     out = nodes.new("ShaderNodeOutputMaterial")
00232:     out.location = (520, 0)
00233: 
00234:     emission = nodes.new("ShaderNodeEmission")
00235:     emission.location = (240, 0)
00236:     emission.inputs["Color"].default_value = color
00237:     emission.inputs["Strength"].default_value = RING_EMIT_MIN
00238:     emission.name = "RingEmission"
00239: 
00240:     links.new(emission.outputs["Emission"], out.inputs["Surface"])
00241:     return mat, emission.inputs["Strength"]
00242: 
00243: 
00244: def build_ribbon_material(name, color):
00245:     mat = bpy.data.materials.new(name=name)
00246:     mat.use_nodes = True
00247: 
00248:     nodes = mat.node_tree.nodes
00249:     links = mat.node_tree.links
00250:     for n in list(nodes):
00251:         nodes.remove(n)
00252: 
00253:     out = nodes.new("ShaderNodeOutputMaterial")
00254:     out.location = (520, 0)
00255: 
00256:     emission = nodes.new("ShaderNodeEmission")
00257:     emission.location = (240, 0)
00258:     emission.inputs["Color"].default_value = color
00259:     emission.inputs["Strength"].default_value = RIBBON_EMIT_MIN
00260:     emission.name = "RibbonEmission"
00261: 
00262:     links.new(emission.outputs["Emission"], out.inputs["Surface"])
00263:     return mat, emission.inputs["Strength"]
00264: 
00265: 
00266: def build_atmosphere_volume_material():
00267:     mat = bpy.data.materials.new(name="AtmosphereVolumeMaterial")
00268:     mat.use_nodes = True
00269:     mat["spaziotempo_volume_fog"] = True
00270: 
00271:     try:
00272:         mat.blend_method = 'BLEND'
00273:     except Exception:
00274:         pass
00275:     try:
00276:         mat.use_screen_refraction = False
00277:     except Exception:
00278:         pass
00279: 
00280:     nodes = mat.node_tree.nodes
00281:     links = mat.node_tree.links
00282:     for n in list(nodes):
00283:         nodes.remove(n)
00284: 
00285:     out = nodes.new("ShaderNodeOutputMaterial")
00286:     out.location = (980, 0)
00287: 
00288:     texcoord = nodes.new("ShaderNodeTexCoord")
00289:     texcoord.location = (-1000, 80)
00290: 
00291:     mapping = nodes.new("ShaderNodeMapping")
00292:     mapping.location = (-760, 80)
00293: 
00294:     noise = nodes.new("ShaderNodeTexNoise")
00295:     noise.location = (-520, 80)
00296:     noise.inputs["Scale"].default_value = FOG_NOISE_SCALE_MIN
00297:     noise.inputs["Detail"].default_value = 6.0
00298:     noise.inputs["Roughness"].default_value = 0.64
00299: 
00300:     ramp = nodes.new("ShaderNodeValToRGB")
00301:     ramp.location = (-280, 80)
00302:     ramp.color_ramp.elements[0].position = 0.28
00303:     ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
00304:     ramp.color_ramp.elements[1].position = 0.54
00305:     ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
00306: 
00307:     clump_noise = nodes.new("ShaderNodeTexNoise")
```
