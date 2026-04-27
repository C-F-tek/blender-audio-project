# Project Code Chunk 43/212

- File: `Scripting/v61b/hotpatch/render_patch.py`
- Part: `1`
- Lines: `1-206`

## Symbol Map
- Imports: `from render_setup import configure_render`, `from common import OUTPUT_MP4, cfg_value`
- Functions: `normalize_runtime_profile(profile)` line 6; `get_scene_compositor_tree(scene)` line 49; `current_runtime_profile(scene)` line 57; `apply_runtime_profile_to_scene(scene, profile)` line 72; `configure_existing_render(scene, meta)` line 201

## Content
```py
00001: from render_setup import configure_render
00002: 
00003: from .common import OUTPUT_MP4, cfg_value
00004: 
00005: 
00006: def normalize_runtime_profile(profile):
00007:     profile = str(profile or "PREVIEW").upper().replace(" ", "_").replace("-", "_")
00008:     aliases = {
00009:         "FINAL": "YOUTUBE_1440P",
00010:         "YOUTUBE": "YOUTUBE_1440P",
00011:         "YOUTUBE_FINAL": "YOUTUBE_1440P",
00012:         "YOUTUBE_FINAL_1440P": "YOUTUBE_1440P",
00013:         "YOUTUBE_FAST": "YOUTUBE_FAST_1440P",
00014:         "YOUTUBE_FAST_1440P": "YOUTUBE_FAST_1440P",
00015:         "YT_FAST": "YOUTUBE_FAST_1440P",
00016:         "YT_FAST_1440": "YOUTUBE_FAST_1440P",
00017:         "YT_FAST_1440P": "YOUTUBE_FAST_1440P",
00018:         "YT_FINAL": "YOUTUBE_1440P",
00019:         "YT_1440": "YOUTUBE_1440P",
00020:         "YT_1440P": "YOUTUBE_1440P",
00021:         "1440": "YOUTUBE_1440P",
00022:         "1440P": "YOUTUBE_1440P",
00023:         "YT_4K": "YOUTUBE_4K",
00024:         "YOUTUBE_FINAL_4K": "YOUTUBE_4K",
00025:         "YOUTUBE_FAST_4K": "YOUTUBE_FAST_4K",
00026:         "YT_FAST_4K": "YOUTUBE_FAST_4K",
00027:         "4K": "YOUTUBE_4K",
00028:         "YT_1080": "YOUTUBE_1080P",
00029:         "YT_1080P": "YOUTUBE_1080P",
00030:         "YOUTUBE_FINAL_1080P": "YOUTUBE_1080P",
00031:         "YOUTUBE_FAST_1080P": "YOUTUBE_FAST_1080P",
00032:         "YT_FAST_1080": "YOUTUBE_FAST_1080P",
00033:         "YT_FAST_1080P": "YOUTUBE_FAST_1080P",
00034:         "1080": "YOUTUBE_1080P",
00035:         "1080P": "YOUTUBE_1080P",
00036:     }
00037:     valid = {
00038:         "PREVIEW",
00039:         "YOUTUBE_FAST_1080P",
00040:         "YOUTUBE_FAST_1440P",
00041:         "YOUTUBE_FAST_4K",
00042:         "YOUTUBE_1080P",
00043:         "YOUTUBE_1440P",
00044:         "YOUTUBE_4K",
00045:     }
00046:     return aliases.get(profile, profile if profile in valid else "PREVIEW")
00047: 
00048: 
00049: def get_scene_compositor_tree(scene):
00050:     for attr in ("node_tree", "compositor_node_tree"):
00051:         tree = getattr(scene, attr, None)
00052:         if tree is not None:
00053:             return tree
00054:     return None
00055: 
00056: 
00057: def current_runtime_profile(scene):
00058:     if "spaziotempo_runtime_profile" in scene:
00059:         return normalize_runtime_profile(scene["spaziotempo_runtime_profile"])
00060: 
00061:     tune = getattr(scene, "spaziotempo_tuning", None)
00062:     if tune is not None:
00063:         label = getattr(tune, "runtime_profile", "")
00064:         if label:
00065:             return normalize_runtime_profile(label)
00066:         if getattr(tune, "youtube_final", False):
00067:             return "YOUTUBE_1440P"
00068: 
00069:     return "PREVIEW"
00070: 
00071: 
00072: def apply_runtime_profile_to_scene(scene, profile):
00073:     profile = normalize_runtime_profile(profile)
00074:     render = scene.render
00075: 
00076:     if profile == "YOUTUBE_FAST_4K":
00077:         width, height = 3840, 2160
00078:         video_bitrate, video_maxrate = 40000, 45000
00079:         motion_blur = False
00080:         fstop = 3.8
00081:         taa_samples = 48
00082:         volumetric_samples = 24
00083:         bloom_intensity = 0.020
00084:         compositor_threshold = 1.62
00085:         lens_distort = 0.010
00086:         lens_dispersion = 0.012
00087:     elif profile == "YOUTUBE_FAST_1440P":
00088:         width, height = 2560, 1440
00089:         video_bitrate, video_maxrate = 24000, 30000
00090:         motion_blur = False
00091:         fstop = 3.8
00092:         taa_samples = 48
00093:         volumetric_samples = 24
00094:         bloom_intensity = 0.020
00095:         compositor_threshold = 1.62
00096:         lens_distort = 0.010
00097:         lens_dispersion = 0.012
00098:     elif profile == "YOUTUBE_FAST_1080P":
00099:         width, height = 1920, 1080
00100:         video_bitrate, video_maxrate = 18000, 22000
00101:         motion_blur = False
00102:         fstop = 3.8
00103:         taa_samples = 48
00104:         volumetric_samples = 24
00105:         bloom_intensity = 0.020
00106:         compositor_threshold = 1.62
00107:         lens_distort = 0.010
00108:         lens_dispersion = 0.012
00109:     elif profile == "YOUTUBE_4K":
00110:         width, height = 3840, 2160
00111:         video_bitrate, video_maxrate = 40000, 45000
00112:         motion_blur = True
00113:         fstop = 3.8
00114:         taa_samples = 80
00115:         volumetric_samples = 48
00116:         bloom_intensity = 0.020
00117:         compositor_threshold = 1.62
00118:         lens_distort = 0.010
00119:         lens_dispersion = 0.012
00120:     elif profile == "YOUTUBE_1440P":
00121:         width, height = 2560, 1440
00122:         video_bitrate, video_maxrate = 24000, 30000
00123:         motion_blur = True
00124:         fstop = 3.8
00125:         taa_samples = 80
00126:         volumetric_samples = 48
00127:         bloom_intensity = 0.020
00128:         compositor_threshold = 1.62
00129:         lens_distort = 0.010
00130:         lens_dispersion = 0.012
00131:     elif profile == "YOUTUBE_1080P":
00132:         width, height = 1920, 1080
00133:         video_bitrate, video_maxrate = 18000, 22000
00134:         motion_blur = True
00135:         fstop = 3.8
00136:         taa_samples = 80
00137:         volumetric_samples = 48
00138:         bloom_intensity = 0.020
00139:         compositor_threshold = 1.62
00140:         lens_distort = 0.010
00141:         lens_dispersion = 0.012
00142:     else:
00143:         width, height = 1920, 1080
00144:         video_bitrate, video_maxrate = 12000, 16000
00145:         motion_blur = False
00146:         fstop = 6.5
00147:         taa_samples = 48
00148:         volumetric_samples = 32
00149:         bloom_intensity = 0.018
00150:         compositor_threshold = 1.48
00151:         lens_distort = 0.0045
00152:         lens_dispersion = 0.0052
00153: 
00154:     render.resolution_x = width
00155:     render.resolution_y = height
00156:     render.resolution_percentage = 100 if profile.startswith("YOUTUBE_") else 75
00157:     render.use_motion_blur = motion_blur
00158: 
00159:     try:
00160:         scene.camera.data.dof.aperture_fstop = fstop
00161:     except Exception:
00162:         pass
00163: 
00164:     eevee = getattr(scene, "eevee", None)
00165:     if eevee is not None:
00166:         if hasattr(eevee, "taa_render_samples"):
00167:             eevee.taa_render_samples = taa_samples
00168:         if hasattr(eevee, "volumetric_samples"):
00169:             eevee.volumetric_samples = volumetric_samples
00170:         if hasattr(eevee, "volumetric_tile_size"):
00171:             eevee.volumetric_tile_size = '8'
00172:         if hasattr(eevee, "use_bloom"):
00173:             eevee.use_bloom = True
00174:         if hasattr(eevee, "bloom_intensity"):
00175:             eevee.bloom_intensity = bloom_intensity
00176: 
00177:     try:
00178:         render.ffmpeg.video_bitrate = video_bitrate
00179:         render.ffmpeg.maxrate = video_maxrate
00180:         render.ffmpeg.minrate = 0
00181:         render.ffmpeg.buffersize = 1792
00182:         render.ffmpeg.audio_bitrate = 320
00183:     except Exception:
00184:         pass
00185: 
00186:     compositor_tree = get_scene_compositor_tree(scene)
00187:     if compositor_tree is not None:
00188:         glare = compositor_tree.nodes.get("AudioSoftGlare")
00189:         if glare is not None and hasattr(glare, "threshold"):
00190:             glare.threshold = compositor_threshold
00191:         lens = compositor_tree.nodes.get("AudioLensBreath")
00192:         if lens is not None:
00193:             if "Distort" in lens.inputs:
00194:                 lens.inputs["Distort"].default_value = lens_distort
00195:             if "Dispersion" in lens.inputs:
00196:                 lens.inputs["Dispersion"].default_value = lens_dispersion
00197: 
00198:     scene["spaziotempo_runtime_profile"] = profile
00199: 
00200: 
00201: def configure_existing_render(scene, meta):
00202:     profile = current_runtime_profile(scene)
00203:     fps = cfg_value("FPS_OVERRIDE", None) or meta.get("fps") or scene.render.fps or 30
00204:     configure_render(scene, OUTPUT_MP4, fps)
00205:     apply_runtime_profile_to_scene(scene, profile)
00206:     return fps
```
