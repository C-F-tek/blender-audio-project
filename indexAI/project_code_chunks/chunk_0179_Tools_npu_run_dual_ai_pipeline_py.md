# Project Code Chunk 179/212

- File: `Tools/npu/run_dual_ai_pipeline.py`
- Part: `4`
- Lines: `744-992`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `from datetime import datetime`, `from typing import Any`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_ai_service_packet import build_ai_service_packet, slugify`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 53; `read_json(path)` line 57; `write_json(path, data)` line 63; `read_optional_json(path)` line 68; `update_track_paths(track_stem, analysis_ai_context)` line 81; `apply_default_input_paths(args)` line 93; `validate_input_files(args)` line 106; `looks_degraded_text(text)` line 126; `deterministic_technical_notes(music_context, project_manifest, reason)` line 142; `run_npu_technical_pass(args)` line 191; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 235; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 317; `build_implementation_prompt(plan, npu_notes, include_manual, gpu_packet, scene_brief, asset_inventory)` line 379; `build_implementation_retry_prompt(plan, invalid_draft, validation)` line 491; `safe_parse_json(text, fallback_key)` line 580; `extract_python_script(text)` line 588; `draft_from_raw_python_script(text, model, reason)` line 608; `get_indexed_project_files()` line 659; `validate_implementation_draft(draft)` line 664; `generated_scene_script_relpath()` line 761; `generated_scene_script_abspath()` line 765; `deterministic_scene_builder_script(track_stem, analysis_json, music_context_json, ai_context_json, blender_keyframes_json, asset_inventory_json, scene_brief)` line 769; `deterministic_support_files(track_stem, scene_brief)` line 1152; `build_fallback_implementation_draft(reason, model, args, scene_brief, asset_inventory)` line 1205; `normalize_implementation_draft(draft, model, args, scene_brief, asset_inventory)` line 1292; `generate_implementation_draft_with_retry(manager, model_name, implementation_prompt, plan, max_new_tokens, args, scene_brief, asset_inventory)` line 1313; `write_brief(plan, creative, technical, npu_notes)` line 1376; `write_implementation_draft(draft)` line 1399; `main()` line 1453
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `DEFAULT_TRACK_STEM`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`, `ALLOWED_NEW_PREFIXES`, `PREFERRED_IMPLEMENTATION_FILES`

## Content
```py
00744:     if any(token in script_lower for token in ["placeholder", "todo", "can't assist", "cannot assist"]):
00745:         issues.append("scene_script contains placeholder/refusal text.")
00746:     if "\n    pass" in script or "\n\tpass" in script:
00747:         issues.append("scene_script contains pass blocks instead of implementation.")
00748:     if "analysis_blender_keyframes" in script and "write" in script.lower():
00749:         issues.append("Candidate script appears to write keyframe analysis data; review required.")
00750:     if any(token in script for token in ["apply_patch", "git ", "Remove-Item", "shutil.rmtree"]):
00751:         issues.append("Candidate script contains project/file mutation commands outside Blender scene creation.")
00752: 
00753:     return {
00754:         "ok": not issues,
00755:         "issues": issues,
00756:         "indexed_file_count": len(indexed_files),
00757:         "allowed_new_prefixes": list(ALLOWED_NEW_PREFIXES),
00758:     }
00759: 
00760: 
00761: def generated_scene_script_relpath() -> str:
00762:     return f"indexAI/scene_scripts/{packet_slugify(TRACK_STEM)}_scene_builder_candidate.py"
00763: 
00764: 
00765: def generated_scene_script_abspath() -> Path:
00766:     return ROOT / generated_scene_script_relpath()
00767: 
00768: 
00769: def deterministic_scene_builder_script(
00770:     track_stem: str,
00771:     analysis_json: str,
00772:     music_context_json: str,
00773:     ai_context_json: str,
00774:     blender_keyframes_json: str,
00775:     asset_inventory_json: str = "",
00776:     scene_brief: dict[str, Any] | None = None,
00777: ) -> str:
00778:     brief_text = json.dumps(scene_brief or {}, ensure_ascii=False).lower()
00779:     use_dual_focus = any(token in brief_text for token in ["dualismo", "doppio", "doppi fuoco", "due oggetti", "contrappost"])
00780:     return f'''# Standalone Blender scene builder generated from Spaziotempo JSON context.
00781: # Review-only draft: run inside Blender Text Editor with Alt+P.
00782: from __future__ import annotations
00783: 
00784: import json
00785: import math
00786: from pathlib import Path
00787: 
00788: import bpy
00789: from mathutils import Vector
00790: 
00791: 
00792: TRACK_STEM = {track_stem!r}
00793: ANALYSIS_JSON = Path({analysis_json!r})
00794: MUSIC_CONTEXT_JSON = Path({music_context_json!r})
00795: AI_CONTEXT_JSON = Path({ai_context_json!r})
00796: BLENDER_KEYFRAMES_JSON = Path({blender_keyframes_json!r})
00797: ASSET_INVENTORY_JSON = Path({asset_inventory_json!r}) if {bool(asset_inventory_json)!r} else None
00798: USE_DUAL_FOCUS = {use_dual_focus!r}
00799: 
00800: 
00801: def load_json(path: Path) -> dict:
00802:     if not path.exists():
00803:         raise FileNotFoundError(f"Missing JSON: {{path}}")
00804:     with path.open("r", encoding="utf-8") as handle:
00805:         data = json.load(handle)
00806:     return data if isinstance(data, dict) else {{}}
00807: 
00808: 
00809: def clear_scene() -> None:
00810:     bpy.ops.object.select_all(action="SELECT")
00811:     bpy.ops.object.delete()
00812: 
00813: 
00814: def preferred_ball_asset_path(inventory: dict) -> Path | None:
00815:     for asset in inventory.get("assets", []):
00816:         if asset.get("role") == "primary_ball_asset":
00817:             path = Path(asset.get("path") or "")
00818:             if path.exists():
00819:                 return path
00820:     return None
00821: 
00822: 
00823: def import_asset_file(asset_file: Path) -> list[bpy.types.Object]:
00824:     before = set(bpy.data.objects.keys())
00825:     ext = asset_file.suffix.lower()
00826:     if ext == ".fbx":
00827:         bpy.ops.import_scene.fbx(filepath=str(asset_file))
00828:     elif ext in {{".glb", ".gltf"}}:
00829:         bpy.ops.import_scene.gltf(filepath=str(asset_file))
00830:     elif ext == ".obj":
00831:         try:
00832:             bpy.ops.wm.obj_import(filepath=str(asset_file))
00833:         except Exception:
00834:             bpy.ops.import_scene.obj(filepath=str(asset_file))
00835:     elif ext == ".blend":
00836:         with bpy.data.libraries.load(str(asset_file), link=False) as (data_from, data_to):
00837:             data_to.objects = data_from.objects
00838:         for obj in data_to.objects:
00839:             if obj:
00840:                 bpy.context.collection.objects.link(obj)
00841:     else:
00842:         raise RuntimeError(f"Unsupported asset format: {{asset_file}}")
00843:     new_names = set(bpy.data.objects.keys()) - before
00844:     return [bpy.data.objects[name] for name in new_names if name in bpy.data.objects]
00845: 
00846: 
00847: def get_world_bbox(objects: list[bpy.types.Object]):
00848:     coords = []
00849:     bpy.context.view_layer.update()
00850:     for obj in objects:
00851:         if obj.type == "EMPTY":
00852:             coords.append(obj.matrix_world.translation.copy())
00853:             continue
00854:         if not hasattr(obj, "bound_box"):
00855:             continue
00856:         try:
00857:             coords.extend([obj.matrix_world @ Vector(corner) for corner in obj.bound_box])
00858:         except Exception:
00859:             coords.append(obj.matrix_world.translation.copy())
00860:     if not coords:
00861:         return Vector((0, 0, 0)), Vector((1, 1, 1)), Vector((0, 0, 0))
00862:     min_v = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
00863:     max_v = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
00864:     return (min_v + max_v) * 0.5, max_v - min_v, min_v
00865: 
00866: 
00867: def make_asset_focus(name: str, asset_path: Path, location, material: bpy.types.Material, fallback_radius: float = 1.0) -> bpy.types.Object:
00868:     try:
00869:         objects = import_asset_file(asset_path)
00870:     except Exception as exc:
00871:         print(f"Asset import failed, using procedural sphere: {{asset_path}} / {{exc}}")
00872:         return add_uv_sphere(name, fallback_radius, location, material, segments=96)
00873:     meshes = [obj for obj in objects if obj.type == "MESH"]
00874:     focus = meshes[0] if meshes else objects[0]
00875:     focus.name = name
00876:     for obj in objects:
00877:         if obj != focus:
00878:             matrix = obj.matrix_world.copy()
00879:             obj.parent = focus
00880:             obj.matrix_world = matrix
00881:         if hasattr(obj.data, "materials"):
00882:             obj.data.materials.clear()
00883:             obj.data.materials.append(material)
00884: 
00885:     center, size, min_v = get_world_bbox(objects)
00886:     max_dim = max(size.x, size.y, size.z, 0.0001)
00887:     target_dim = fallback_radius * 2.0
00888:     focus.scale = (target_dim / max_dim, target_dim / max_dim, target_dim / max_dim)
00889:     bpy.context.view_layer.update()
00890:     center, _size, min_v = get_world_bbox(objects)
00891:     focus.location += Vector(location) - center
00892:     focus.location.z += float(location[2]) - min_v.z
00893:     focus["imported_asset_children"] = len(objects)
00894:     return focus
00895: 
00896: 
00897: def make_collection(name: str) -> bpy.types.Collection:
00898:     collection = bpy.data.collections.new(name)
00899:     bpy.context.scene.collection.children.link(collection)
00900:     return collection
00901: 
00902: 
00903: def link_to(collection: bpy.types.Collection, obj: bpy.types.Object) -> None:
00904:     for parent in list(obj.users_collection):
00905:         parent.objects.unlink(obj)
00906:     collection.objects.link(obj)
00907: 
00908: 
00909: def create_material(name: str, color, emission_strength: float = 0.0) -> bpy.types.Material:
00910:     mat = bpy.data.materials.new(name)
00911:     mat.use_nodes = True
00912:     nodes = mat.node_tree.nodes
00913:     bsdf = nodes.get("Principled BSDF")
00914:     if bsdf:
00915:         if "Base Color" in bsdf.inputs:
00916:             bsdf.inputs["Base Color"].default_value = color
00917:         if "Emission Color" in bsdf.inputs:
00918:             bsdf.inputs["Emission Color"].default_value = color
00919:         if "Emission Strength" in bsdf.inputs:
00920:             bsdf.inputs["Emission Strength"].default_value = emission_strength
00921:         if "Roughness" in bsdf.inputs:
00922:             bsdf.inputs["Roughness"].default_value = 0.42
00923:     return mat
00924: 
00925: 
00926: def add_uv_sphere(name: str, radius: float, location, material: bpy.types.Material, segments: int = 64) -> bpy.types.Object:
00927:     bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=max(16, segments // 2), radius=radius, location=location)
00928:     obj = bpy.context.object
00929:     obj.name = name
00930:     obj.data.name = name + "Mesh"
00931:     obj.data.materials.append(material)
00932:     return obj
00933: 
00934: 
00935: def add_text_label(text: str, location, size: float, material: bpy.types.Material) -> bpy.types.Object:
00936:     bpy.ops.object.text_add(location=location, rotation=(math.radians(72), 0.0, 0.0))
00937:     obj = bpy.context.object
00938:     obj.name = "AlbumTitle_Text"
00939:     obj.data.body = text
00940:     obj.data.align_x = "CENTER"
00941:     obj.data.align_y = "CENTER"
00942:     obj.data.size = size
00943:     obj.data.extrude = 0.025
00944:     obj.data.materials.append(material)
00945:     return obj
00946: 
00947: 
00948: def animate_value(obj: bpy.types.Object, data_path: str, frames: list[tuple[int, float]], index: int | None = None) -> None:
00949:     for frame, value in frames:
00950:         if index is None:
00951:             setattr(obj, data_path, value)
00952:             obj.keyframe_insert(data_path=data_path, frame=frame)
00953:         else:
00954:             current = getattr(obj, data_path)
00955:             current[index] = value
00956:             obj.keyframe_insert(data_path=data_path, frame=frame, index=index)
00957: 
00958: 
00959: def keyframe_material_emission(mat: bpy.types.Material, frame: int, strength: float) -> None:
00960:     if not mat.use_nodes or not mat.node_tree:
00961:         return
00962:     bsdf = mat.node_tree.nodes.get("Principled BSDF")
00963:     if not bsdf or "Emission Strength" not in bsdf.inputs:
00964:         return
00965:     socket = bsdf.inputs["Emission Strength"]
00966:     socket.default_value = strength
00967:     socket.keyframe_insert(data_path="default_value", frame=frame)
00968: 
00969: 
00970: def apply_full_audio_keyframes(hero: bpy.types.Object, disp: bpy.types.Modifier, hero_mat: bpy.types.Material, keyframes: dict, fps: float) -> int:
00971:     audio_frames = keyframes.get("frames") or []
00972:     inserted = 0
00973:     for audio in audio_frames:
00974:         time_sec = float(audio.get("time") or 0.0)
00975:         frame = int(round(time_sec * fps)) + 1
00976:         low = float(audio.get("low") or 0.0)
00977:         mid = float(audio.get("mid") or 0.0)
00978:         high = float(audio.get("high") or 0.0)
00979:         onset = float(audio.get("onset") or 0.0)
00980:         beat = float(audio.get("beat") or 0.0)
00981: 
00982:         # Full-frame audio deformation: not only uniform scale, but an asymmetric pulse plus displacement.
00983:         hero.scale = (
00984:             1.0 + low * 0.12 + beat * 0.025,
00985:             1.0 + mid * 0.075 + onset * 0.018,
00986:             1.0 + high * 0.055 + low * 0.035,
00987:         )
00988:         hero.keyframe_insert(data_path="scale", frame=frame)
00989: 
00990:         disp.strength = 0.035 + low * 0.11 + mid * 0.045 + onset * 0.025 + beat * 0.018
00991:         disp.keyframe_insert(data_path="strength", frame=frame)
00992: 
```
