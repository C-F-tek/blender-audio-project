# Spaziotempo NPU Service Capsule

Generated: `2026-04-28T20:30:45`

## Routing
{
  "heavy_reasoning": "GPU_OLLAMA",
  "code_generation": "GPU_OLLAMA_SCENE_SCRIPT_WRITER",
  "npu_role": "service_data_router_compact_capsule",
  "npu_heavy_generation": false,
  "full_keyframes_policy": "reference_only_never_compact_for_blender",
  "memory_policy": "Every AI call receives compact user memory, scene brief, asset inventory and project/audio chunk references."
}

## Track
{
  "stem": "Ready To Jazz-Luca Vera_Master",
  "duration": 345.6001,
  "fps": 30.0,
  "bpm": 126.048,
  "frames": 10369,
  "segments": 22
}

## Project Files
- `F001` `Scripting/v61b/config.py`: CFG profile/path/render/audio constants
- `F002` `Scripting/v61b/main_v61b.py`: MAIN build orchestration
- `F003` `Scripting/v61b/animation.py`: ANIM keyframes/audio driven transforms
- `F004` `Scripting/v61b/materials.py`: MAT shader/node/material setup
- `F005` `Scripting/v61b/fog_dynamics.py`: FOG audio reactive volume controls
- `F006` `Scripting/v61b/fog_filaments.py`: FOG_FILAMENT procedural fog strands
- `F007` `Scripting/v61b/physics_setup.py`: PHYS orbit/force/particle setup
- `F008` `Scripting/v61b/render_setup.py`: RENDER compositor/quality profiles
- `F009` `Scripting/v61b/scene_tuning_panel.py`: PANEL Blender UI/operators
- `F010` `Scripting/v61b/hot_update_scene_v61b.py`: HOT_UPDATE partial scene refresh
- `F011` `Tools/workflow/workflow_state.py`: WF shell/GUI operation orchestration
- `F012` `Tools/npu/run_dual_ai_pipeline.py`: AI_PIPELINE NPU/GPU routing

## Audio Segments
- `S001` t=[0.0, 16.0] b=high i=low ctl={'hero': 0.347, 'mat': 0.2897, 'fog': 0.0889, 'emit': 0.5305, 'cam': 0.2557}
- `S002` t=[16.0, 32.0] b=high i=low ctl={'hero': 0.3481, 'mat': 0.3377, 'fog': 0.1166, 'emit': 0.52, 'cam': 0.2427}
- `S003` t=[32.0, 48.0] b=mid i=low ctl={'hero': 0.3454, 'mat': 0.4017, 'fog': 0.1703, 'emit': 0.5364, 'cam': 0.2375}
- `S004` t=[48.0, 64.0] b=mid i=low ctl={'hero': 0.3339, 'mat': 0.4459, 'fog': 0.1806, 'emit': 0.5475, 'cam': 0.2424}
- `S005` t=[64.0, 80.0] b=mid i=low ctl={'hero': 0.3253, 'mat': 0.4882, 'fog': 0.2041, 'emit': 0.5392, 'cam': 0.2389}
- `S006` t=[80.0, 96.0] b=mid i=low ctl={'hero': 0.3425, 'mat': 0.5368, 'fog': 0.2076, 'emit': 0.5775, 'cam': 0.2159}
- `S007` t=[96.0, 112.0] b=mid i=low ctl={'hero': 0.3386, 'mat': 0.5202, 'fog': 0.2083, 'emit': 0.5566, 'cam': 0.2119}
- `S008` t=[112.0, 128.0] b=mid i=low ctl={'hero': 0.3324, 'mat': 0.5276, 'fog': 0.2096, 'emit': 0.5619, 'cam': 0.2375}
- `S009` t=[128.0, 144.0] b=mid i=low ctl={'hero': 0.3359, 'mat': 0.5229, 'fog': 0.2163, 'emit': 0.5776, 'cam': 0.2187}
- `S010` t=[144.0, 160.0] b=mid i=medium ctl={'hero': 0.3515, 'mat': 0.5356, 'fog': 0.2259, 'emit': 0.5858, 'cam': 0.2392}
- `S011` t=[160.0, 176.0] b=mid i=medium ctl={'hero': 0.3924, 'mat': 0.6476, 'fog': 0.259, 'emit': 0.582, 'cam': 0.2019}
- `S012` t=[176.0, 192.0] b=mid i=medium ctl={'hero': 0.3432, 'mat': 0.5951, 'fog': 0.2385, 'emit': 0.6035, 'cam': 0.2064}
- `S013` t=[192.0, 208.0] b=mid i=medium ctl={'hero': 0.3408, 'mat': 0.6031, 'fog': 0.2324, 'emit': 0.6438, 'cam': 0.2109}
- `S014` t=[208.0, 224.0] b=mid i=medium ctl={'hero': 0.3276, 'mat': 0.6159, 'fog': 0.2445, 'emit': 0.6235, 'cam': 0.2256}
- `S015` t=[224.0, 240.0] b=mid i=medium ctl={'hero': 0.3465, 'mat': 0.6019, 'fog': 0.2441, 'emit': 0.5919, 'cam': 0.2467}
- `S016` t=[240.0, 256.0] b=mid i=medium ctl={'hero': 0.34, 'mat': 0.5986, 'fog': 0.2573, 'emit': 0.5534, 'cam': 0.2329}
- `S017` t=[256.0, 272.0] b=mid i=medium ctl={'hero': 0.3466, 'mat': 0.594, 'fog': 0.2405, 'emit': 0.589, 'cam': 0.2454}
- `S018` t=[272.0, 288.0] b=mid i=medium ctl={'hero': 0.3494, 'mat': 0.5575, 'fog': 0.2391, 'emit': 0.5601, 'cam': 0.2618}
- `S019` t=[288.0, 304.0] b=mid i=low ctl={'hero': 0.3405, 'mat': 0.5442, 'fog': 0.216, 'emit': 0.5529, 'cam': 0.2609}
- `S020` t=[304.0, 320.0] b=high i=low ctl={'hero': 0.3607, 'mat': 0.3601, 'fog': 0.1287, 'emit': 0.5271, 'cam': 0.2508}
- `S021` t=[320.0, 336.0] b=high i=low ctl={'hero': 0.3549, 'mat': 0.3347, 'fog': 0.0985, 'emit': 0.5286, 'cam': 0.2573}
- `S022` t=[336.0, 345.6] b=high i=quiet ctl={'hero': 0.0301, 'mat': 0.0868, 'fog': 0.0063, 'emit': 0.182, 'cam': 0.1308}
