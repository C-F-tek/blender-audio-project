# Project Code Chunk 54/212

- File: `Scripting/v61b/render_setup.py`
- Part: `1`
- Lines: `1-270`

## Symbol Map
- Imports: `bpy`, `from pathlib import Path`, `from config import RENDER_RESOLUTION_X, RENDER_RESOLUTION_Y, USE_4K, RENDER_PERCENT, USE_MOTION_BLUR, EEVEE_TAA_RENDER_SAMPLES, USE_BLOOM, BLOOM_THRESHOLD, BLOOM_INTENSITY, VIEW_EXPOSURE, VIEW_GAMMA, VIDEO_BITRATE, VIDEO_MAXRATE, VIDEO_MINRATE, VIDEO_BUFFERSIZE, AUDIO_BITRATE, RENDER_OUTPUT_MODE, OUTPUT_IMAGE_SEQUENCE_DIR, OUTPUT_IMAGE_SEQUENCE_PREFIX, IMAGE_SEQUENCE_FORMAT, IMAGE_SEQUENCE_COLOR_DEPTH, IMAGE_SEQUENCE_COMPRESSION, VOLUMETRIC_SAMPLES, VOLUMETRIC_TILE_SIZE, FOG_VOLUME_ENABLED, USE_COMPOSITING, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_GLARE_MIX, COMPOSITOR_GLARE_SIZE, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISPERSION_MIN`
- Functions: `configure_scene_physics(scene)` line 39; `get_scene_compositor_tree(scene)` line 67; `configure_compositor(scene)` line 75; `configure_render(scene, output_mp4, fps)` line 157

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
00029:     FOG_VOLUME_ENABLED,
00030:     USE_COMPOSITING,
00031:     COMPOSITOR_GLARE_THRESHOLD_MAX,
00032:     COMPOSITOR_GLARE_MIX,
00033:     COMPOSITOR_GLARE_SIZE,
00034:     COMPOSITOR_LENS_DISTORT_MIN,
00035:     COMPOSITOR_LENS_DISPERSION_MIN,
00036: )
00037: 
00038: 
00039: def configure_scene_physics(scene):
00040:     try:
00041:         scene.use_gravity = False
00042:     except Exception:
00043:         pass
00044: 
00045:     if scene.rigidbody_world is None:
00046:         bpy.ops.rigidbody.world_add()
00047: 
00048:     rbw = scene.rigidbody_world
00049:     rbw.enabled = True
00050: 
00051:     if hasattr(rbw, "time_scale"):
00052:         rbw.time_scale = 1.0
00053: 
00054:     if hasattr(rbw, "steps_per_second"):
00055:         rbw.steps_per_second = 120
00056:     elif hasattr(rbw, "substeps_per_frame"):
00057:         rbw.substeps_per_frame = 10
00058: 
00059:     if hasattr(rbw, "solver_iterations"):
00060:         rbw.solver_iterations = 25
00061: 
00062:     if hasattr(rbw, "point_cache") and rbw.point_cache is not None:
00063:         rbw.point_cache.frame_start = 1
00064:         rbw.point_cache.frame_end = scene.frame_end
00065: 
00066: 
00067: def get_scene_compositor_tree(scene):
00068:     for attr in ("node_tree", "compositor_node_tree"):
00069:         tree = getattr(scene, attr, None)
00070:         if tree is not None:
00071:             return tree
00072:     return None
00073: 
00074: 
00075: def configure_compositor(scene):
00076:     if not USE_COMPOSITING:
00077:         return
00078: 
00079:     tree = get_scene_compositor_tree(scene)
00080:     if tree is None:
00081:         print("[WARN] Compositor saltato: questa build non espone un node tree compositor compatibile.")
00082:         return
00083: 
00084:     nodes = tree.nodes
00085:     links = tree.links
00086: 
00087:     for node in list(nodes):
00088:         nodes.remove(node)
00089: 
00090:     render_layers = nodes.new("CompositorNodeRLayers")
00091:     render_layers.location = (-820, 0)
00092: 
00093:     glare = nodes.new("CompositorNodeGlare")
00094:     glare.name = "AudioSoftGlare"
00095:     glare.label = "Audio Soft Glare"
00096:     glare.location = (-520, 0)
00097:     try:
00098:         glare.glare_type = 'FOG_GLOW'
00099:     except Exception:
00100:         pass
00101:     try:
00102:         glare.quality = 'MEDIUM'
00103:     except Exception:
00104:         pass
00105:     try:
00106:         glare.threshold = COMPOSITOR_GLARE_THRESHOLD_MAX
00107:     except Exception:
00108:         pass
00109:     try:
00110:         glare.mix = COMPOSITOR_GLARE_MIX
00111:     except Exception:
00112:         pass
00113:     try:
00114:         glare.size = COMPOSITOR_GLARE_SIZE
00115:     except Exception:
00116:         pass
00117: 
00118:     lens = nodes.new("CompositorNodeLensdist")
00119:     lens.name = "AudioLensBreath"
00120:     lens.label = "Audio Lens Breath"
00121:     lens.location = (-220, 0)
00122:     if "Distort" in lens.inputs:
00123:         lens.inputs["Distort"].default_value = COMPOSITOR_LENS_DISTORT_MIN
00124:     if "Dispersion" in lens.inputs:
00125:         lens.inputs["Dispersion"].default_value = COMPOSITOR_LENS_DISPERSION_MIN
00126: 
00127:     color_balance = nodes.new("CompositorNodeColorBalance")
00128:     color_balance.name = "AudioColorBalance"
00129:     color_balance.label = "Audio Color Balance"
00130:     color_balance.location = (80, 0)
00131:     try:
00132:         color_balance.lift = (0.985, 0.990, 1.010)
00133:         color_balance.gamma = (0.985, 1.000, 1.020)
00134:         color_balance.gain = (1.035, 1.020, 0.985)
00135:     except Exception:
00136:         pass
00137: 
00138:     composite = nodes.new("CompositorNodeComposite")
00139:     composite.location = (410, 70)
00140: 
00141:     viewer = nodes.new("CompositorNodeViewer")
00142:     viewer.location = (410, -110)
00143: 
00144:     try:
00145:         links.new(render_layers.outputs["Image"], glare.inputs["Image"])
00146:         links.new(glare.outputs["Image"], lens.inputs["Image"])
00147:         links.new(lens.outputs["Image"], color_balance.inputs["Image"])
00148:         links.new(color_balance.outputs["Image"], composite.inputs["Image"])
00149:         links.new(color_balance.outputs["Image"], viewer.inputs["Image"])
00150:     except Exception:
00151:         try:
00152:             links.new(render_layers.outputs["Image"], composite.inputs["Image"])
00153:         except Exception:
00154:             pass
00155: 
00156: 
00157: def configure_render(scene, output_mp4, fps):
00158:     scene.render.fps = int(round(fps))
00159:     scene.render.use_file_extension = True
00160:     scene.render.engine = 'BLENDER_EEVEE'
00161: 
00162:     scene.render.resolution_x = RENDER_RESOLUTION_X
00163:     scene.render.resolution_y = RENDER_RESOLUTION_Y
00164: 
00165:     scene.render.resolution_percentage = RENDER_PERCENT
00166: 
00167:     output_mode = str(RENDER_OUTPUT_MODE).upper()
00168:     if output_mode == "IMAGE_SEQUENCE":
00169:         frame_dir = Path(OUTPUT_IMAGE_SEQUENCE_DIR)
00170:         frame_dir.mkdir(parents=True, exist_ok=True)
00171:         scene.render.filepath = str(frame_dir / OUTPUT_IMAGE_SEQUENCE_PREFIX)
00172:         scene.render.use_overwrite = False
00173:         try:
00174:             scene.render.use_placeholder = True
00175:         except Exception:
00176:             pass
00177:         scene.render.use_sequencer = False
00178: 
00179:         try:
00180:             scene.render.image_settings.media_type = 'IMAGE'
00181:         except Exception:
00182:             pass
00183:         try:
00184:             scene.render.image_settings.file_format = IMAGE_SEQUENCE_FORMAT
00185:             scene.render.image_settings.color_mode = 'RGB'
00186:             scene.render.image_settings.color_depth = IMAGE_SEQUENCE_COLOR_DEPTH
00187:             scene.render.image_settings.compression = IMAGE_SEQUENCE_COMPRESSION
00188:         except Exception:
00189:             pass
00190:     else:
00191:         Path(output_mp4).parent.mkdir(parents=True, exist_ok=True)
00192:         scene.render.filepath = str(output_mp4)
00193:         scene.render.use_overwrite = True
00194:         scene.render.use_sequencer = True
00195: 
00196:         try:
00197:             scene.render.image_settings.media_type = 'VIDEO'
00198:         except Exception:
00199:             pass
00200: 
00201:         try:
00202:             scene.render.image_settings.file_format = 'FFMPEG'
00203:             scene.render.image_settings.color_mode = 'RGB'
00204:         except Exception:
00205:             pass
00206: 
00207:         scene.render.ffmpeg.format = 'MPEG4'
00208:         scene.render.ffmpeg.codec = 'H264'
00209:         scene.render.ffmpeg.audio_codec = 'AAC'
00210:         scene.render.ffmpeg.audio_bitrate = AUDIO_BITRATE
00211: 
00212:         for crf in ('PERC_LOSSLESS', 'HIGH'):
00213:             try:
00214:                 scene.render.ffmpeg.constant_rate_factor = crf
00215:                 break
00216:             except Exception:
00217:                 pass
00218: 
00219:         try:
00220:             scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
00221:         except Exception:
00222:             pass
00223: 
00224:         try:
00225:             scene.render.ffmpeg.video_bitrate = VIDEO_BITRATE
00226:             scene.render.ffmpeg.maxrate = VIDEO_MAXRATE
00227:             scene.render.ffmpeg.minrate = VIDEO_MINRATE
00228:             scene.render.ffmpeg.buffersize = VIDEO_BUFFERSIZE
00229:         except Exception:
00230:             pass
00231: 
00232:     scene.render.use_motion_blur = USE_MOTION_BLUR
00233: 
00234:     eevee = scene.eevee
00235: 
00236:     if hasattr(eevee, "taa_render_samples"):
00237:         eevee.taa_render_samples = EEVEE_TAA_RENDER_SAMPLES
00238: 
00239:     if hasattr(eevee, "use_bloom"):
00240:         eevee.use_bloom = USE_BLOOM
00241:         if hasattr(eevee, "bloom_threshold"):
00242:             eevee.bloom_threshold = BLOOM_THRESHOLD
00243:         if hasattr(eevee, "bloom_intensity"):
00244:             eevee.bloom_intensity = BLOOM_INTENSITY
00245: 
00246:     if hasattr(eevee, "use_gtao"):
00247:         eevee.use_gtao = True
00248:     if hasattr(eevee, "gtao_quality"):
00249:         eevee.gtao_quality = 0.25
00250: 
00251:     if hasattr(eevee, "use_volumetric_lights"):
00252:         eevee.use_volumetric_lights = bool(FOG_VOLUME_ENABLED)
00253:     if hasattr(eevee, "use_volumetric_shadows"):
00254:         eevee.use_volumetric_shadows = False
00255:     if hasattr(eevee, "volumetric_samples"):
00256:         eevee.volumetric_samples = VOLUMETRIC_SAMPLES
00257:     if hasattr(eevee, "volumetric_tile_size"):
00258:         eevee.volumetric_tile_size = VOLUMETRIC_TILE_SIZE
00259: 
00260:     try:
00261:         scene.view_settings.exposure = VIEW_EXPOSURE
00262:     except Exception:
00263:         pass
00264: 
00265:     try:
00266:         scene.view_settings.gamma = VIEW_GAMMA
00267:     except Exception:
00268:         pass
00269: 
00270:     configure_compositor(scene)
```
