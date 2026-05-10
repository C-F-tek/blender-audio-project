# Dual AI Blender Agent Brief

Generated: `2026-04-28T23:04:21`

## Policy
- Full Blender keyframe JSON remains untouched.
- AI compact context is analysis only.
- Ollama model switch unloads the previous model before loading the next.

## Recommended Plan
{
  "index": 0,
  "start_sec": 0.0,
  "end_sec": 5.0,
  "dominant_band": "mid",
  "intensity_score": 75,
  "intensity": "medium",
  "beat_count": 12,
  "stats": {
    "low": {
      "avg": 0.3,
      "min": 0.1,
      "max": 0.6,
      "std": 0.15,
      "p50": 0.4,
      "p90": 0.5,
      "p98": 0.6,
      "top10_avg": 0.55
    },
    "mid": {
      "avg": 0.7,
      "min": 0.5,
      "max": 0.9,
      "std": 0.1,
      "p50": 0.8,
      "p90": 0.9,
      "p98": 0.95,
      "top10_avg": 0.85
    },
    "high": {
      "avg": 0.2,
      "min": 0.1,
      "max": 0.4,
      "std": 0.05,
      "p50": 0.3,
      "p90": 0.35,
      "p98": 0.4,
      "top10_avg": 0.35
    },
    "onset": {
      "avg": 0.6,
      "min": 0.4,
      "max": 0.8,
      "std": 0.1,
      "p50": 0.7,
      "p90": 0.75,
      "p98": 0.8,
      "top10_avg": 0.75
    }
  },
  "controls": {
    "primary_band": "mid",
    "intensity": "medium",
    "hero_deformation": 0.2,
    "material_shimmer": 0.3,
    "fog_motion": 0.1,
    "accent_emission": 0.4,
    "camera_pressure": 0.5
  },
  "top_events": [
    {
      "time": 1.0,
      "low": 0.6,
      "mid": 0.9,
      "high": 0.3,
      "onset": 0.8,
      "beat": true
    },
    {
      "time": 2.5,
      "low": 0.4,
      "mid": 0.7,
      "high": 0.2,
      "onset": 0.6,
      "beat": false
    }
  ],
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
  "raw_technical_response": "This JSON data represents a series of audio segments, each with detailed information about its characteristics and corresponding visual effects controls. Here's a breakdown of the structure and key elements:\n\n1. **Segments**: The main container is an array called \"segments,\" which holds individual segment objects.\n\n2. **Segment Object**:\n   - `index`: A unique identifier for each segment.\n   - `start_sec` and `end_sec`: The start and end times of the segment in seconds.\n   - `dominant_band`: The primary frequency band (low, mid, high) that is most prominent in the audio.\n   - `intensity_score`: A numerical value representing the intensity or loudness of the segment.\n   - `intensity`: A textual description of the intensity level (e.g., \"quiet\", \"medium\").\n   - `beat_count`: The number of beats detected in the segment.\n\n3. **Stats**:\n   - Contains statistical information about the audio features across different bands (low, mid, high) and onset.\n   - Each band has metrics like average (`avg`), minimum (`min`), maximum (`max`), standard deviation (`std`), percentiles (`p50`, `p90`, `p98`), and top 10 average (`top10_avg`).\n\n4. **Controls**:\n   - Visual effects parameters that are mapped to the audio characteristics.\n   - These include:\n     - `primary_band`: The main band influencing the visual effects.\n     - `intensity`: The intensity level of the visual effects.\n     - `hero_deformation`, `material_shimmer`, `fog_motion`, `accent_emission`, and `camera_pressure`: Specific control values for different visual elements.\n\n5. **Top Events**:\n   - A list of significant audio events within the segment, such as beats or strong onsets.\n   - Each event includes its time (`time`), levels in low, mid, and high bands, onset value, and beat status (`beat`).\n\nThis data is likely used to synchronize visual effects with audio content in a media production environment, ensuring that the visuals respond dynamically to changes in the audio.",
  "parse_error": true,
  "model": "qwen2.5-coder:14b"
}

## NPU Notes
# Deterministic Technical Notes

Reason: NPU output was not trusted (`npu_skipped_gpu_heavy_mode`).

## Track Map
- Duration: `196.80009070294784` seconds.
- FPS: `30.0`.
- BPM: `99.38401442307692`.
- Segment count: `13`.

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
