# Dual AI Blender Agent Brief

Generated: `2026-04-28T20:30:05`

## Policy
- Full Blender keyframe JSON remains untouched.
- AI compact context is analysis only.
- Ollama model switch unloads the previous model before loading the next.

## Recommended Plan
{
  "index": 0,
  "start_sec": 0.0,
  "end_sec": 3.0,
  "dominant_band": "mid",
  "intensity_score": 50,
  "intensity": "medium",
  "beat_count": 4,
  "low": {
    "average": 12.3,
    "min": 8.9,
    "max": 16.7,
    "std_dev": 2.4,
    "p50": 13.5,
    "p90": 15.0,
    "p98": 16.0
  },
  "mid": {
    "average": 25.6,
    "min": 20.0,
    "max": 30.0,
    "std_dev": 1.8,
    "p50": 24.0,
    "p90": 27.0,
    "p98": 29.0
  },
  "high": {
    "average": 10.2,
    "min": 6.0,
    "max": 15.0,
    "std_dev": 2.1,
    "p50": 10.0,
    "p90": 13.0,
    "p98": 14.0
  },
  "onset": {
    "average": 0.5,
    "min": 0.3,
    "max": 0.7,
    "std_dev": 0.1,
    "p50": 0.5,
    "p90": 0.6,
    "p98": 0.7
  },
  "beat": {
    "average": 0.2,
    "min": 0.1,
    "max": 0.3,
    "std_dev": 0.05,
    "p50": 0.2,
    "p90": 0.25,
    "p98": 0.3
  },
  "hero_deformation": {
    "average": 1.0,
    "min": 0.8,
    "max": 1.2,
    "std_dev": 0.1,
    "p50": 1.0,
    "p90": 1.1,
    "p98": 1.2
  },
  "material_shimmer": {
    "average": 0.3,
    "min": 0.2,
    "max": 0.4,
    "std_dev": 0.05,
    "p50": 0.3,
    "p90": 0.35,
    "p98": 0.4
  },
  "fog_motion": {
    "average": 0.1,
    "min": 0.05,
    "max": 0.15,
    "std_dev": 0.02,
    "p50": 0.1,
    "p90": 0.13,
    "p98": 0.14
  },
  "accent_emission": {
    "average": 0.7,
    "min": 0.6,
    "max": 0.8,
    "std_dev": 0.05,
    "p50": 0.7,
    "p90": 0.75,
    "p98": 0.8
  },
  "camera_pressure": {
    "average": 0.4,
    "min": 0.3,
    "max": 0.5,
    "std_dev": 0.05,
    "p50": 0.4,
    "p90": 0.45,
    "p98": 0.5
  },
  "top_events": [
    {
      "timestamp_sec": 1.2,
      "low": 16.7,
      "mid": 30.0,
      "high": 15.0,
      "onset": 0.7,
      "beat": 0.3
    },
    {
      "timestamp_sec": 2.8,
      "low": 14.0,
      "mid": 28.0,
      "high": 13.0,
      "onset": 0.6,
      "beat": 0.25
    }
  ],
  "merge_model": "qwen2.5-coder:14b"
}

## Audio Mapping
{}

## Creative Source
{
  "raw_creative_response": "**Answer:**\n\nThe function that checks whether a given string is a valid number is called **`isValid`**.",
  "parse_error": true,
  "model": "gpt-oss:20b"
}

## Technical Source
{
  "raw_technical_response": "This JSON data represents a series of audio analysis segments for a song or music track. Each segment is divided into 3-second intervals, and the data includes various metrics and control parameters derived from the audio content within those intervals. Here's a breakdown of the key components:\n\n1. **Segment Information**:\n   - `index`: The sequence number of the segment.\n   - `start_sec` and `end_sec`: The start and end times of the segment in seconds.\n\n2. **Audio Features**:\n   - `dominant_band`: The primary frequency band (low, mid, high) that is most prominent in the segment.\n   - `intensity_score`: A numerical score indicating the intensity or loudness level of the segment.\n   - `intensity`: A textual description of the intensity level (e.g., \"quiet\", \"low\", \"medium\", \"high\").\n\n3. **Beat Information**:\n   - `beat_count`: The number of beats detected in the segment.\n\n4. **Statistics**:\n   - For each frequency band (`low`, `mid`, `high`), there are statistical measures such as average, minimum, maximum, standard deviation, and percentiles (p50, p90, p98).\n   - `onset`: Measures related to the onset of sounds or beats.\n   - `beat`: Additional beat-related statistics.\n\n5. **Control Parameters**:\n   - These are parameters that might be used to control visual or audio effects in a music video or interactive experience based on the audio analysis.\n     - `hero_deformation`: Likely controls the deformation or animation of a main character or object.\n     - `material_shimmer`: Controls shimmering effects on materials.\n     - `fog_motion`: Controls motion or changes in fog or atmospheric conditions.\n     - `accent_emission`: Controls emission or highlighting of accents or highlights.\n     - `camera_pressure`: Likely controls camera movement or pressure effects.\n\n6. **Top Events**:\n   - A list of significant audio events within the segment, including their timestamps and associated metrics (low, mid, high, onset, beat).\n\nThis data can be used for various applications such as music visualization, interactive experiences, or even machine learning models that analyze and respond to music in real-time.",
  "parse_error": true,
  "model": "qwen2.5-coder:14b"
}

## NPU Notes
# Deterministic Technical Notes

Reason: NPU output was not trusted (`npu_skipped_gpu_heavy_mode`).

## Track Map
- Duration: `345.60009070294785` seconds.
- FPS: `30.0`.
- BPM: `126.04801829268293`.
- Segment count: `22`.

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


