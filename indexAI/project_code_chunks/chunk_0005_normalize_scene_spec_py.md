# Project Code Chunk 5/212

- File: `normalize_scene_spec.py`
- Part: `2`
- Lines: `316-487`

## Symbol Map
- Imports: `from pathlib import Path`, `json`, `re`, `sys`
- Functions: `load_json(path)` line 41; `slugify(text)` line 48; `safe_scene_name(name)` line 55; `safe_visual_concept(text)` line 64; `normalize_palette(values)` line 73; `normalize_camera_style(camera_style)` line 93; `build_object_specs(brief)` line 123; `build_materials(brief)` line 200; `build_node_animation(brief)` line 275; `build_audio_mapping(brief)` line 329; `build_optimization()` line 376; `build_render_strategy()` line 393; `normalize_brief(brief)` line 401; `safe_scene_name(name)` line 436; `safe_visual_concept(text)` line 445; `main()` line 454
- Assignments: `ROOT`, `PROJECT_DIR`, `IN_JSON`, `OUT_JSON`, `DEFAULT_SCENE_NAME`, `DEFAULT_VISUAL_CONCEPT`, `PALETTE_MAP`, `CAMERA_PRESETS`

## Content
```py
00316:             "intent": "subtle reflective breathing",
00317:             "strength": 0.30
00318:         },
00319:         {
00320:             "target": "volume_material",
00321:             "parameter": "density",
00322:             "band": "beat",
00323:             "intent": "volumetric pulse",
00324:             "strength": 0.18
00325:         }
00326:     ]
00327: 
00328: 
00329: def build_audio_mapping(brief: dict):
00330:     return [
00331:         {
00332:             "target": "hero_core",
00333:             "property": "scale",
00334:             "band": "low",
00335:             "intent": "central body pulse",
00336:             "strength": 0.55
00337:         },
00338:         {
00339:             "target": "hero_core",
00340:             "property": "rotation",
00341:             "band": "mid",
00342:             "intent": "gentle musical sway",
00343:             "strength": 0.25
00344:         },
00345:         {
00346:             "target": "light_architecture",
00347:             "property": "rotation",
00348:             "band": "mid",
00349:             "intent": "architectural motion",
00350:             "strength": 0.40
00351:         },
00352:         {
00353:             "target": "light_architecture",
00354:             "property": "emission",
00355:             "band": "high",
00356:             "intent": "harmonic brightness accents",
00357:             "strength": 0.72
00358:         },
00359:         {
00360:             "target": "floating_lights",
00361:             "property": "intensity",
00362:             "band": "high",
00363:             "intent": "sparkle accents",
00364:             "strength": 0.70
00365:         },
00366:         {
00367:             "target": "camera",
00368:             "property": "pulse",
00369:             "band": "beat",
00370:             "intent": "subtle rhythmic camera bump",
00371:             "strength": 0.28
00372:         }
00373:     ]
00374: 
00375: 
00376: def build_optimization():
00377:     return {
00378:         "use_instancing": True,
00379:         "use_procedural_materials": True,
00380:         "avoid_heavy_geometry": True,
00381:         "animate_nodes_more_than_meshes": True,
00382:         "geometry_budget": "low_geometry_high_shading",
00383:         "notes": [
00384:             "keep hero object simple",
00385:             "use instanced ring architecture",
00386:             "prefer procedural shading",
00387:             "use one volumetric shell only",
00388:             "avoid subdivision-heavy meshes"
00389:         ]
00390:     }
00391: 
00392: 
00393: def build_render_strategy():
00394:     return {
00395:         "engine": "BLENDER_EEVEE",
00396:         "priority": "fast iteration with rich shading",
00397:         "notes": "use emission, procedural shaders and moderate volumetrics"
00398:     }
00399: 
00400: 
00401: def normalize_brief(brief: dict):
00402:     scene_name = safe_scene_name(brief.get("scene_name"))
00403:     style_mode = str(brief.get("style_mode", "stylized_cinematic_abstract")).strip() or "stylized_cinematic_abstract"
00404:     visual_concept = safe_visual_concept(brief.get("visual_concept"))
00405:     hero_object = str(brief.get("hero_object", "central_core")).strip() or "central_core"
00406:     environment = str(brief.get("environment", "abstract_stage")).strip() or "abstract_stage"
00407:     lighting_style = str(brief.get("lighting_style", "soft_volumetric_glow")).strip() or "soft_volumetric_glow"
00408: 
00409:     palette = normalize_palette(brief.get("palette", []))
00410:     camera_style = normalize_camera_style(brief.get("camera_style", {}))
00411:     objects = build_object_specs(brief)
00412:     materials = build_materials(brief)
00413:     node_animation = build_node_animation(brief)
00414:     audio_mapping = build_audio_mapping(brief)
00415:     optimization = build_optimization()
00416:     render_strategy = build_render_strategy()
00417: 
00418:     return {
00419:         "scene_name": scene_name,
00420:         "style_mode": style_mode,
00421:         "visual_concept": visual_concept,
00422:         "hero_object": hero_object,
00423:         "environment": environment,
00424:         "lighting_style": lighting_style,
00425:         "palette": palette,
00426:         "camera_style": camera_style,
00427:         "objects": objects,
00428:         "materials": materials,
00429:         "node_animation": node_animation,
00430:         "audio_mapping": audio_mapping,
00431:         "optimization": optimization,
00432:         "render_strategy": render_strategy
00433:     }
00434: 
00435: 
00436: def safe_scene_name(name: str) -> str:
00437:     if not isinstance(name, str):
00438:         return DEFAULT_SCENE_NAME
00439:     name = name.strip()
00440:     if not name or name == ".":
00441:         return DEFAULT_SCENE_NAME
00442:     return name
00443: 
00444: 
00445: def safe_visual_concept(text: str) -> str:
00446:     if not isinstance(text, str):
00447:         return DEFAULT_VISUAL_CONCEPT
00448:     text = text.strip()
00449:     if not text or text == ".":
00450:         return DEFAULT_VISUAL_CONCEPT
00451:     return text
00452: 
00453: 
00454: def main():
00455:     brief = load_json(IN_JSON)
00456:     normalized = normalize_brief(brief)
00457: 
00458:     with open(OUT_JSON, "w", encoding="utf-8") as f:
00459:         json.dump(normalized, f, indent=2, ensure_ascii=False)
00460: 
00461:     print(f"[OK] Scene spec normalizzato salvato in: {OUT_JSON}")
00462:     print(json.dumps(normalized, indent=2, ensure_ascii=False))
00463: 
00464:     tools_dir = PROJECT_DIR / "Tools" / "npu"
00465:     if tools_dir.exists():
00466:         if str(tools_dir) not in sys.path:
00467:             sys.path.insert(0, str(tools_dir))
00468:         try:
00469:             from build_music_context import build_music_context
00470: 
00471:             manifest = build_music_context(
00472:                 scene_files=[
00473:                     IN_JSON,
00474:                     OUT_JSON,
00475:                     PROJECT_DIR / "scene_spec_album_driven_raw.txt",
00476:                     PROJECT_DIR / "scene_spec_from_npu.json",
00477:                     PROJECT_DIR / "scene_spec_from_npu_raw.txt",
00478:                 ],
00479:             )
00480:         except Exception as exc:
00481:             print(f"[WARN] Contesto musicale NPU non aggiornato: {exc}")
00482:         else:
00483:             print(f"[OK] Contesto musicale NPU aggiornato: {manifest['context_md']}")
00484: 
00485: 
00486: if __name__ == "__main__":
00487:     main()
```
