# Project Code Chunk 104/212

- File: `Scripting/v61b_backgood/render_setup.py`
- Part: `1`
- Lines: `1-267`

## Symbol Map
- Imports: `bpy`, `from pathlib import Path`, `from config import RENDER_RESOLUTION_X, RENDER_RESOLUTION_Y, USE_4K, RENDER_PERCENT, USE_MOTION_BLUR, EEVEE_TAA_RENDER_SAMPLES, USE_BLOOM, BLOOM_THRESHOLD, BLOOM_INTENSITY, VIEW_EXPOSURE, VIEW_GAMMA, VIDEO_BITRATE, VIDEO_MAXRATE, VIDEO_MINRATE, VIDEO_BUFFERSIZE, AUDIO_BITRATE, RENDER_OUTPUT_MODE, OUTPUT_IMAGE_SEQUENCE_DIR, OUTPUT_IMAGE_SEQUENCE_PREFIX, IMAGE_SEQUENCE_FORMAT, IMAGE_SEQUENCE_COLOR_DEPTH, IMAGE_SEQUENCE_COMPRESSION, VOLUMETRIC_SAMPLES, VOLUMETRIC_TILE_SIZE, USE_COMPOSITING, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_GLARE_MIX, COMPOSITOR_GLARE_SIZE, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISPERSION_MIN`
- Functions: `configure_scene_physics(scene)` line 38; `get_scene_compositor_tree(scene)` line 66; `configure_compositor(scene)` line 74; `configure_render(scene, output_mp4, fps)` line 156

## Content
```py
00001: import bpy
00002: from pathlib import Path
00003: 
00004: from config import (
00005:     RENDER_RESOLUTION_X,
00006:     RENDER_RESOLUTION_Y,
00007:     USE_4K,
00008:     RENDER_PERCENT,
00009:     USE_MOTION_BLUR,
00010:     EEVEE_TAA_RENDER_SAMPLES,
00011:     USE_BLOOM,
00012:     BLOOM_THRESHOLD,
00013:     BLOOM_INTENSITY,
00014:     VIEW_EXPOSURE,
00015:     VIEW_GAMMA,
00016:     VIDEO_BITRATE,
00017:     VIDEO_MAXRATE,
00018:     VIDEO_MINRATE,
00019:     VIDEO_BUFFERSIZE,
00020:     AUDIO_BITRATE,
00021:     RENDER_OUTPUT_MODE,
00022:     OUTPUT_IMAGE_SEQUENCE_DIR,
00023:     OUTPUT_IMAGE_SEQUENCE_PREFIX,
00024:     IMAGE_SEQUENCE_FORMAT,
00025:     IMAGE_SEQUENCE_COLOR_DEPTH,
00026:     IMAGE_SEQUENCE_COMPRESSION,
00027:     VOLUMETRIC_SAMPLES,
00028:     VOLUMETRIC_TILE_SIZE,
00029:     USE_COMPOSITING,
00030:     COMPOSITOR_GLARE_THRESHOLD_MAX,
00031:     COMPOSITOR_GLARE_MIX,
00032:     COMPOSITOR_GLARE_SIZE,
00033:     COMPOSITOR_LENS_DISTORT_MIN,
00034:     COMPOSITOR_LENS_DISPERSION_MIN,
00035: )
00036: 
00037: 
00038: def configure_scene_physics(scene):
00039:     try:
00040:         scene.use_gravity = False
00041:     except Exception:
00042:         pass
00043: 
00044:     if scene.rigidbody_world is None:
00045:         bpy.ops.rigidbody.world_add()
00046: 
00047:     rbw = scene.rigidbody_world
00048:     rbw.enabled = True
00049: 
00050:     if hasattr(rbw, "time_scale"):
00051:         rbw.time_scale = 1.0
00052: 
00053:     if hasattr(rbw, "steps_per_second"):
00054:         rbw.steps_per_second = 120
00055:     elif hasattr(rbw, "substeps_per_frame"):
00056:         rbw.substeps_per_frame = 10
00057: 
00058:     if hasattr(rbw, "solver_iterations"):
00059:         rbw.solver_iterations = 25
00060: 
00061:     if hasattr(rbw, "point_cache") and rbw.point_cache is not None:
00062:         rbw.point_cache.frame_start = 1
00063:         rbw.point_cache.frame_end = scene.frame_end
00064: 
00065: 
00066: def get_scene_compositor_tree(scene):
00067:     for attr in ("node_tree", "compositor_node_tree"):
00068:         tree = getattr(scene, attr, None)
00069:         if tree is not None:
00070:             return tree
00071:     return None
00072: 
00073: 
00074: def configure_compositor(scene):
00075:     if not USE_COMPOSITING:
00076:         return
00077: 
00078:     tree = get_scene_compositor_tree(scene)
00079:     if tree is None:
00080:         print("[WARN] Compositor saltato: questa build non espone un node tree compositor compatibile.")
00081:         return
00082: 
00083:     nodes = tree.nodes
00084:     links = tree.links
00085: 
00086:     for node in list(nodes):
00087:         nodes.remove(node)
00088: 
00089:     render_layers = nodes.new("CompositorNodeRLayers")
00090:     render_layers.location = (-820, 0)
00091: 
00092:     glare = nodes.new("CompositorNodeGlare")
00093:     glare.name = "AudioSoftGlare"
00094:     glare.label = "Audio Soft Glare"
00095:     glare.location = (-520, 0)
00096:     try:
00097:         glare.glare_type = 'FOG_GLOW'
00098:     except Exception:
00099:         pass
00100:     try:
00101:         glare.quality = 'MEDIUM'
00102:     except Exception:
00103:         pass
00104:     try:
00105:         glare.threshold = COMPOSITOR_GLARE_THRESHOLD_MAX
00106:     except Exception:
00107:         pass
00108:     try:
00109:         glare.mix = COMPOSITOR_GLARE_MIX
00110:     except Exception:
00111:         pass
00112:     try:
00113:         glare.size = COMPOSITOR_GLARE_SIZE
00114:     except Exception:
00115:         pass
00116: 
00117:     lens = nodes.new("CompositorNodeLensdist")
00118:     lens.name = "AudioLensBreath"
00119:     lens.label = "Audio Lens Breath"
00120:     lens.location = (-220, 0)
00121:     if "Distort" in lens.inputs:
00122:         lens.inputs["Distort"].default_value = COMPOSITOR_LENS_DISTORT_MIN
00123:     if "Dispersion" in lens.inputs:
00124:         lens.inputs["Dispersion"].default_value = COMPOSITOR_LENS_DISPERSION_MIN
00125: 
00126:     color_balance = nodes.new("CompositorNodeColorBalance")
00127:     color_balance.name = "AudioColorBalance"
00128:     color_balance.label = "Audio Color Balance"
00129:     color_balance.location = (80, 0)
00130:     try:
00131:         color_balance.lift = (0.985, 0.990, 1.010)
00132:         color_balance.gamma = (0.985, 1.000, 1.020)
00133:         color_balance.gain = (1.035, 1.020, 0.985)
00134:     except Exception:
00135:         pass
00136: 
00137:     composite = nodes.new("CompositorNodeComposite")
00138:     composite.location = (410, 70)
00139: 
00140:     viewer = nodes.new("CompositorNodeViewer")
00141:     viewer.location = (410, -110)
00142: 
00143:     try:
00144:         links.new(render_layers.outputs["Image"], glare.inputs["Image"])
00145:         links.new(glare.outputs["Image"], lens.inputs["Image"])
00146:         links.new(lens.outputs["Image"], color_balance.inputs["Image"])
00147:         links.new(color_balance.outputs["Image"], composite.inputs["Image"])
00148:         links.new(color_balance.outputs["Image"], viewer.inputs["Image"])
00149:     except Exception:
00150:         try:
00151:             links.new(render_layers.outputs["Image"], composite.inputs["Image"])
00152:         except Exception:
00153:             pass
00154: 
00155: 
00156: def configure_render(scene, output_mp4, fps):
00157:     scene.render.fps = int(round(fps))
00158:     scene.render.use_file_extension = True
00159:     scene.render.engine = 'BLENDER_EEVEE'
00160: 
00161:     scene.render.resolution_x = RENDER_RESOLUTION_X
00162:     scene.render.resolution_y = RENDER_RESOLUTION_Y
00163: 
00164:     scene.render.resolution_percentage = RENDER_PERCENT
00165: 
00166:     output_mode = str(RENDER_OUTPUT_MODE).upper()
00167:     if output_mode == "IMAGE_SEQUENCE":
00168:         frame_dir = Path(OUTPUT_IMAGE_SEQUENCE_DIR)
00169:         frame_dir.mkdir(parents=True, exist_ok=True)
00170:         scene.render.filepath = str(frame_dir / OUTPUT_IMAGE_SEQUENCE_PREFIX)
00171:         scene.render.use_overwrite = False
00172:         try:
00173:             scene.render.use_placeholder = True
00174:         except Exception:
00175:             pass
00176:         scene.render.use_sequencer = False
00177: 
00178:         try:
00179:             scene.render.image_settings.media_type = 'IMAGE'
00180:         except Exception:
00181:             pass
00182:         try:
00183:             scene.render.image_settings.file_format = IMAGE_SEQUENCE_FORMAT
00184:             scene.render.image_settings.color_mode = 'RGB'
00185:             scene.render.image_settings.color_depth = IMAGE_SEQUENCE_COLOR_DEPTH
00186:             scene.render.image_settings.compression = IMAGE_SEQUENCE_COMPRESSION
00187:         except Exception:
00188:             pass
00189:     else:
00190:         Path(output_mp4).parent.mkdir(parents=True, exist_ok=True)
00191:         scene.render.filepath = str(output_mp4)
00192:         scene.render.use_overwrite = True
00193:         scene.render.use_sequencer = True
00194: 
00195:         try:
00196:             scene.render.image_settings.media_type = 'VIDEO'
00197:         except Exception:
00198:             pass
00199: 
00200:         try:
00201:             scene.render.image_settings.file_format = 'FFMPEG'
00202:             scene.render.image_settings.color_mode = 'RGB'
00203:         except Exception:
00204:             pass
00205: 
00206:         scene.render.ffmpeg.format = 'MPEG4'
00207:         scene.render.ffmpeg.codec = 'H264'
00208:         scene.render.ffmpeg.audio_codec = 'AAC'
00209:         scene.render.ffmpeg.audio_bitrate = AUDIO_BITRATE
00210: 
00211:         try:
00212:             scene.render.ffmpeg.constant_rate_factor = 'HIGH'
00213:         except Exception:
00214:             pass
00215: 
00216:         try:
00217:             scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
00218:         except Exception:
00219:             pass
00220: 
00221:         try:
00222:             scene.render.ffmpeg.video_bitrate = VIDEO_BITRATE
00223:             scene.render.ffmpeg.maxrate = VIDEO_MAXRATE
00224:             scene.render.ffmpeg.minrate = VIDEO_MINRATE
00225:             scene.render.ffmpeg.buffersize = VIDEO_BUFFERSIZE
00226:         except Exception:
00227:             pass
00228: 
00229:     scene.render.use_motion_blur = USE_MOTION_BLUR
00230: 
00231:     eevee = scene.eevee
00232: 
00233:     if hasattr(eevee, "taa_render_samples"):
00234:         eevee.taa_render_samples = EEVEE_TAA_RENDER_SAMPLES
00235: 
00236:     if hasattr(eevee, "use_bloom"):
00237:         eevee.use_bloom = USE_BLOOM
00238:         if hasattr(eevee, "bloom_threshold"):
00239:             eevee.bloom_threshold = BLOOM_THRESHOLD
00240:         if hasattr(eevee, "bloom_intensity"):
00241:             eevee.bloom_intensity = BLOOM_INTENSITY
00242: 
00243:     if hasattr(eevee, "use_gtao"):
00244:         eevee.use_gtao = True
00245:     if hasattr(eevee, "gtao_quality"):
00246:         eevee.gtao_quality = 0.25
00247: 
00248:     if hasattr(eevee, "use_volumetric_lights"):
00249:         eevee.use_volumetric_lights = True
00250:     if hasattr(eevee, "use_volumetric_shadows"):
00251:         eevee.use_volumetric_shadows = True
00252:     if hasattr(eevee, "volumetric_samples"):
00253:         eevee.volumetric_samples = VOLUMETRIC_SAMPLES
00254:     if hasattr(eevee, "volumetric_tile_size"):
00255:         eevee.volumetric_tile_size = VOLUMETRIC_TILE_SIZE
00256: 
00257:     try:
00258:         scene.view_settings.exposure = VIEW_EXPOSURE
00259:     except Exception:
00260:         pass
00261: 
00262:     try:
00263:         scene.view_settings.gamma = VIEW_GAMMA
00264:     except Exception:
00265:         pass
00266: 
00267:     configure_compositor(scene)
```
