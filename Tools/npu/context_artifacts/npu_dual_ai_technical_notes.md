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
- `Tools/workflow/workflow_core/__init__.py`

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
