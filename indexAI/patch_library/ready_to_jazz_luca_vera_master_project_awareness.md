# Spaziotempo Project Awareness

Generated: `2026-04-27T14:41:02`

Track: `Ready To Jazz-Luca Vera_Master`

## Pipeline State
- `audio_already_loaded_by_pipeline`: `True`
- `wav_analysis_ready`: `True`
- `music_context_ready`: `True`
- `project_index_ready`: `True`
- `manual_index_ready`: `True`
- `service_packet_ready`: `True`
- `scene_brief_ready`: `True`
- `can_generate_scene_script`: `True`
- `segment_count`: `22`

## Director Rules
- Never suggest manually importing audio into Blender; the WAV is already represented by analysis/music/keyframe JSON.
- Never suggest opening Blender as the next generic step; the user decides when to run Blender.
- Do not suggest rebuilding from scratch if technical files already exist.
- When technical files exist, refer to the pipeline action: scene brief, dual AI plan, scene script draft, hot update, or review generated script.
- Use project asset roles. If user says ball, prefer primary_ball_asset.
- Full analysis_blender_keyframes JSON is authoritative and must not be summarized away.
- If unsure, say which technical file/chunk should be checked, not generic Blender advice.

## Primary Assets
- `primary_ball_asset`: `C:\Users\carmi\blender\assets\ball\source\ball.fbx`
- `animated_effect_asset`: `C:\Users\carmi\blender\assets\animated-effect\source\Animated effect.blend`
- `blend_scene_reference`: `C:\Users\carmi\blender\First good.blend`
- `blend_scene_reference`: `C:\Users\carmi\blender\second good.blend`
