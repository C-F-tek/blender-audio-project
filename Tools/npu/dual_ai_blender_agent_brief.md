# Dual AI Blender Agent Brief

Generated: `2026-04-28T20:54:04`

## Policy
- Full Blender keyframe JSON remains untouched.
- AI compact context is analysis only.
- Ollama model switch unloads the previous model before loading the next.

## Recommended Plan
{
  "raw_plan_response": "The provided JSON data represents a series of audio segments, each containing detailed information about its characteristics and corresponding visual effects controls. Here's a breakdown of the structure and key elements:\n\n### Structure Overview\n\n- **segments**: An array containing multiple objects, each representing an audio segment.\n- **index**: A unique identifier for each segment.\n- **start_sec** and **end_sec**: The start and end times of the segment in seconds.\n- **dominant_band**: The primary frequency band (low, mid, high) that is most prominent in the segment.\n- **intensity_score**: A numerical score indicating the intensity level of the audio.\n- **intensity**: A textual description of the intensity (e.g., quiet, low).\n- **beat_count**: The number of beats detected in the segment.\n- **stats**: An object containing statistical data about various features of the audio:\n  - **low**, **mid**, **high**: Statistics for each frequency band.\n  - **onset**: Statistics related to the onset (beginning) of sounds.\n  - **beat**: Statistics related to beats.\n- **controls**: Visual effects controls that should be applied based on the audio characteristics:\n  - **primary_band**: The primary visual effect corresponding to the dominant audio band.\n  - **intensity**: The intensity level for visual effects.\n  - **hero_deformation**, **material_shimmer**, **fog_motion**, **accent_emission**, **camera_pressure**: Specific control values for various visual elements.\n\n### Example Segment\n\nHere's an example of a single segment from the JSON data:\n\n```json\n{\n  \"index\": 0,\n  \"start_sec\": 0.0,\n  \"end_sec\": 14.0,\n  \"dominant_band\": \"low\",\n  \"intensity_score\": 0.2389,\n  \"intensity\": \"quiet\",\n  \"beat_count\": 6,\n  \"stats\": {\n    \"low\": {\n      \"avg\": 0.175,\n      \"min\": 0.0,\n      \"max\": 1.0,\n      \"std\": 0.2834,\n      \"p50\": 0.0,\n      \"p90\": 0.611,\n      \"p98\": 0.9463,\n      \"top10_avg\": 0.7936\n    },\n    \"mid\": {\n      \"avg\": 0.0575,\n      \"min\": 0.0,\n      \"max\": 0.8937,\n      \"std\": 0.1491,\n      \"p50\": 0.0,\n      \"p90\": 0.196,\n      \"p98\": 0.7337,\n      \"top10_avg\": 0.4277\n    },\n    \"high\": {\n      \"avg\": 0.0592,\n      \"min\": 0.0,\n      \"max\": 0.985,\n      \"std\": 0.1572,\n      \"p50\": 0.0125,\n      \"p90\": 0.1308,\n      \"p98\": 0.7251,\n      \"top10_avg\": 0.4477\n    },\n    \"onset\": {\n      \"avg\": 0.0666,\n      \"min\": 0.0,\n      \"max\": 1.0,\n      \"std\": 0.1723,\n      \"p50\": 0.0127,\n      \"p90\": 0.1441,\n      \"p98\": 0.8716,\n      \"top10_avg\": 0.4941\n    },\n    \"beat\": {\n      \"avg\": 0.0238,\n      \"min\": 0.0,\n      \"max\": 1.0,\n      \"std\": 0.1523,\n      \"p50\": 0.0,\n      \"p90\": 0.0,\n      \"p98\": 1.0,\n      \"top10_avg\": 0.2381\n    }\n  },\n  \"controls\": {\n    \"primary_band\": \"low\",\n    \"intensity\": \"quiet\",\n    \"hero_deformation\": 0.3649,\n    \"material_shimmer\": 0.134,\n    \"fog_motion\": 0.0835,\n    \"accent_emission\": 0.1475,\n    \"camera_pressure\": 0.2469\n  },\n  \"top_events\": [\n    {\n      \"time\": 311.267,\n      \"low\": 0.245,\n      \"mid\": 0.753,\n      \"high\": 0.818,\n      \"onset\": 1.0,\n      \"beat\": 1.0\n    },\n    // Additional top events...\n  ]\n}\n```\n\n### Key Points\n\n- **Dominant Band**: The audio segment is primarily characterized by the low frequency band.\n- **Intensity**: The intensity level is described as \"quiet,\" with a score of 0.2389.\n- **Beat Count**: There are 6 beats detected in this segment.\n- **Statistics**: Detailed statistics for each frequency band, onset, and beat provide insights into the audio's characteristics.\n- **Controls**: Specific visual effects controls are provided to match the audio characteristics, such as deformation of a hero element, shimmering materials, fog motion, accent emission, and camera pressure.\n\nThis data can be used in applications that synchronize audio with visual effects, ensuring that the visuals respond dynamically to changes in the audio.",
  "parse_error": true,
  "merge_model": "qwen2.5-coder:14b"
}

## Audio Mapping
{}

## Creative Source
{
  "raw_creative_response": "",
  "parse_error": true,
  "model": "gpt-oss:20b"
}

## Technical Source
{
  "raw_technical_response": "This JSON data represents a series of audio segments, each with detailed information about its characteristics and corresponding visual effects controls. Here's a breakdown of the structure and key elements:\n\n### Structure Overview\n\n- **segments**: An array containing multiple objects, each representing an audio segment.\n- **index**: A unique identifier for each segment.\n- **start_sec** and **end_sec**: The start and end times of the segment in seconds.\n- **dominant_band**: The primary frequency band (low, mid, high) that is most prominent in the segment.\n- **intensity_score**: A numerical score indicating the intensity level of the audio.\n- **intensity**: A textual description of the intensity (e.g., quiet, low).\n- **beat_count**: The number of beats detected in the segment.\n- **stats**: An object containing statistical data about various features of the audio:\n  - **low**, **mid**, **high**: Statistics for each frequency band.\n  - **onset**: Statistics related to the onset (beginning) of sounds.\n  - **beat**: Statistics related to beats.\n- **controls**: Visual effects controls that should be applied based on the audio characteristics:\n  - **primary_band**: The primary visual effect corresponding to the dominant audio band.\n  - **intensity**: The intensity level for visual effects.\n  - **hero_deformation**, **material_shimmer**, **fog_motion**, **accent_emission**, **camera_pressure**: Specific control values for various visual elements.\n\n### Example Segment\n\nHere's an example of a single segment from the JSON data:\n\n```json\n{\n  \"index\": 0,\n  \"start_sec\": 0.0,\n  \"end_sec\": 14.0,\n  \"dominant_band\": \"low\",\n  \"intensity_score\": 0.2389,\n  \"intensity\": \"quiet\",\n  \"beat_count\": 6,\n  \"stats\": {\n    \"low\": {\n      \"avg\": 0.175,\n      \"min\": 0.0,\n      \"max\": 1.0,\n      \"std\": 0.2834,\n      \"p50\": 0.0,\n      \"p90\": 0.611,\n      \"p98\": 0.9463,\n      \"top10_avg\": 0.7936\n    },\n    \"mid\": {\n      \"avg\": 0.0575,\n      \"min\": 0.0,\n      \"max\": 0.8937,\n      \"std\": 0.1491,\n      \"p50\": 0.0,\n      \"p90\": 0.196,\n      \"p98\": 0.7337,\n      \"top10_avg\": 0.4277\n    },\n    \"high\": {\n      \"avg\": 0.0592,\n      \"min\": 0.0,\n      \"max\": 0.985,\n      \"std\": 0.1572,\n      \"p50\": 0.0125,\n      \"p90\": 0.1308,\n      \"p98\": 0.7251,\n      \"top10_avg\": 0.4477\n    },\n    \"onset\": {\n      \"avg\": 0.0666,\n      \"min\": 0.0,\n      \"max\": 1.0,\n      \"std\": 0.1723,\n      \"p50\": 0.0127,\n      \"p90\": 0.1441,\n      \"p98\": 0.8716,\n      \"top10_avg\": 0.4941\n    },\n    \"beat\": {\n      \"avg\": 0.0238,\n      \"min\": 0.0,\n      \"max\": 1.0,\n      \"std\": 0.1523,\n      \"p50\": 0.0,\n      \"p90\": 0.0,\n      \"p98\": 1.0,\n      \"top10_avg\": 0.2381\n    }\n  },\n  \"controls\": {\n    \"primary_band\": \"low\",\n    \"intensity\": \"quiet\",\n    \"hero_deformation\": 0.3649,\n    \"material_shimmer\": 0.134,\n    \"fog_motion\": 0.0835,\n    \"accent_emission\": 0.1475,\n    \"camera_pressure\": 0.2469\n  },\n  \"top_events\": [\n    {\n      \"time\": 311.267,\n      \"low\": 0.245,\n      \"mid\": 0.753,\n      \"high\": 0.818,\n      \"onset\": 1.0,\n      \"beat\": 1.0\n    },\n    // Additional top events...\n  ]\n}\n```\n\n### Key Points\n\n- **Dominant Band**: The audio segment is primarily characterized by the low frequency band.\n- **Intensity**: The intensity level is described as \"quiet,\" with a score of 0.2389.\n- **Beat Count**: There are 6 beats detected in this segment.\n- **Statistics**: Detailed statistics for each frequency band, onset, and beat provide insights into the audio's characteristics.\n- **Controls**: Specific visual effects controls are provided to match the audio characteristics, such as deformation of a hero element, shimmering materials, fog motion, accent emission, and camera pressure.\n\nThis data can be used in applications that synchronize audio with visual effects, ensuring that the visuals respond dynamically to changes in the audio.",
  "parse_error": true,
  "model": "qwen2.5-coder:14b"
}

## NPU Notes
# Deterministic Technical Notes

Reason: NPU output was not trusted (`npu_skipped_gpu_heavy_mode`).

## Track Map
- Duration: `318.00027210884355` seconds.
- FPS: `30.0`.
- BPM: `79.50721153846153`.
- Segment count: `20`.

## Project Primary Files
- `Scripting/v61b/config.py`
- `Scripting/v61b/fog_dynamics.py`
- `Scripting/v61b/materials.py`
- `Scripting/v61b/physics_setup.py`
- `Scripting/v61b/scene_tuning_panel.py`
- `Tools/npu/run_dual_ai_pipeline.py`
- `Tools/workflow/workflow_state.py`

## Safe Implementation Policy
- Use full frame-by-frame Blender keyframe JSON as data input only.
- Generate patch plans against existing project files, not monolithic replacement scripts.
- Prefer hotpatch/panel/update modules for materials, fog, lights and render changes.
- Require a reload only when primary object creation or scene topology changes.

## Audio Control Map
- Low band: hero mesh deformation scale, gravity/attractor strength, fog density body.
- Mid band: material roughness/emission mix, secondary object motion, fog filament drift.
- High band: small emission accents, glints, particle sparkle, sharp camera micro motion.
- Onset/beat: short impulses, never a constant global light flash.


