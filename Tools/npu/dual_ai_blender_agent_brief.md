# Dual AI Blender Agent Brief

Generated: `2026-04-28T21:38:53`

## Policy
- Full Blender keyframe JSON remains untouched.
- AI compact context is analysis only.
- Ollama model switch unloads the previous model before loading the next.

## Recommended Plan
{
  "raw_plan_response": "The provided JSON data contains information about a creative response and technical analysis of an audio file. Here's a breakdown of the key components:\n\n### Creative Response (ollama_creative)\n- **raw_creative_response**: The raw text output from the creative model, which in this case is a statement about a script file named `animation.py` with 1080 lines.\n- **parse_error**: A boolean indicating whether there was an error parsing the response. Here, it's set to `true`.\n- **model**: The model used for generating the creative response, which is \"gpt-oss:20b\".\n\n### Technical Analysis (ollama_technical)\n- **index**: An identifier for the analysis, here set to 0.\n- **start_sec** and **end_sec**: The start and end times of the audio segment analyzed, in seconds. Here, it's from 0.0 to 14.0 seconds.\n- **dominant_band**: The dominant frequency band detected in the audio, which is \"low\".\n- **intensity_score**: A numerical score representing the intensity of the audio, here 0.2357.\n- **intensity**: A qualitative description of the audio intensity, described as \"quiet\".\n- **beat_count**: The number of beats detected in the audio segment, here 6.\n\n#### Statistics (stats)\n- **low**, **mid**, and **high** frequency bands:\n  - **avg**: Average value for the band.\n  - **min** and **max**: Minimum and maximum values for the band.\n  - **std**: Standard deviation of the band.\n  - **p50**, **p90**, and **p98**: Percentiles (50th, 90th, and 98th) of the band values.\n  - **top10_avg**: Average value of the top 10% highest values in the band.\n\n#### Controls\n- Parameters that might control some aspect of a visual or audio output based on the technical analysis:\n  - **primary_band**: The primary frequency band, here \"low\".\n  - **intensity**: The intensity level, described as \"quiet\".\n  - **hero_deformation**, **material_shimmer**, **fog_motion**, **accent_emission**, and **camera_pressure**: Specific control parameters with numerical values.\n\n#### Top Events\n- A list of significant events detected in the audio segment:\n  - Each event includes a timestamp (`time`) and values for the low, mid, high frequency bands, onset, and beat.\n  - These events are sorted by their occurrence time within the analyzed segment.\n\n### Summary\nThe data provides both a creative response about a script file and a detailed technical analysis of an audio clip. The technical analysis includes information on the audio's intensity, dominant frequencies, and specific events detected, which could be used to guide further processing or visualization tasks.",
  "parse_error": true,
  "merge_model": "qwen2.5-coder:14b"
}

## Audio Mapping
{}

## Creative Source
{
  "raw_creative_response": "**Scripting/v61b/animation.py**  \n- **Line count:** **1080** lines.",
  "parse_error": true,
  "model": "gpt-oss:20b"
}

## Technical Source
{
  "index": 0,
  "start_sec": 0.0,
  "end_sec": 14.0,
  "dominant_band": "low",
  "intensity_score": 0.2357,
  "intensity": "quiet",
  "beat_count": 6,
  "stats": {
    "low": {
      "avg": 0.198,
      "min": 0.0,
      "max": 1.0,
      "std": 0.275,
      "p50": 0.0,
      "p90": 0.61,
      "p98": 0.946,
      "top10_avg": 0.793
    },
    "mid": {
      "avg": 0.057,
      "min": 0.0,
      "max": 0.894,
      "std": 0.149,
      "p50": 0.0,
      "p90": 0.196,
      "p98": 0.734,
      "top10_avg": 0.428
    },
    "high": {
      "avg": 0.059,
      "min": 0.0,
      "max": 0.985,
      "std": 0.157,
      "p50": 0.013,
      "p90": 0.131,
      "p98": 0.725,
      "top10_avg": 0.448
    },
    "onset": {
      "avg": 0.067,
      "min": 0.0,
      "max": 1.0,
      "std": 0.172,
      "p50": 0.013,
      "p90": 0.144,
      "p98": 0.872,
      "top10_avg": 0.494
    },
    "beat": {
      "avg": 0.024,
      "min": 0.0,
      "max": 1.0,
      "std": 0.152,
      "p50": 0.0,
      "p90": 0.0,
      "p98": 1.0,
      "top10_avg": 0.238
    }
  },
  "controls": {
    "primary_band": "low",
    "intensity": "quiet",
    "hero_deformation": 0.365,
    "material_shimmer": 0.134,
    "fog_motion": 0.084,
    "accent_emission": 0.148,
    "camera_pressure": 0.247
  },
  "top_events": [
    {
      "time": 11.267,
      "low": 0.245,
      "mid": 0.753,
      "high": 0.818,
      "onset": 1.0,
      "beat": 1.0
    },
    {
      "time": 9.767,
      "low": 0.55,
      "mid": 0.776,
      "high": 0.749,
      "onset": 1.0,
      "beat": 1.0
    },
    {
      "time": 8.267,
      "low": 0.244,
      "mid": 0.743,
      "high": 0.784,
      "onset": 1.0,
      "beat": 0.0
    },
    {
      "time": 6.767,
      "low": 0.543,
      "mid": 0.783,
      "high": 0.73,
      "onset": 1.0,
      "beat": 0.0
    },
    {
      "time": 5.267,
      "low": 0.234,
      "mid": 0.719,
      "high": 0.718,
      "onset": 1.0,
      "beat": 0.0
    },
    {
      "time": 7.767,
      "low": 0.846,
      "mid": 0.134,
      "high": 0.461,
      "onset": 1.0,
      "beat": 0.0
    },
    {
      "time": 9.0,
      "low": 0.585,
      "mid": 0.176,
      "high": 0.364,
      "onset": 1.0,
      "beat": 0.0
    },
    {
      "time": 6.033,
      "low": 0.871,
      "mid": 0.193,
      "high": 0.512,
      "onset": 0.627,
      "beat": 1.0
    }
  ],
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


