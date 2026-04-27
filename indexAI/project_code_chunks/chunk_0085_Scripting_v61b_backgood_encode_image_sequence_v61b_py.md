# Project Code Chunk 85/212

- File: `Scripting/v61b_backgood/encode_image_sequence_v61b.py`
- Part: `2`
- Lines: `328-376`

## Symbol Map
- Imports: `re`, `sys`, `from pathlib import Path`, `bpy`, `config`
- Functions: `extract_frame_number(path)` line 67; `sorted_frame_files()` line 74; `contiguous_frame_files(frame_files)` line 100; `get_sequence_collection(editor)` line 127; `all_editor_strips(editor)` line 135; `remove_editor_strip(editor, strip)` line 147; `force_visible_sequencer(scene, editor)` line 160; `clear_sequence_editor(scene)` line 208; `add_image_sequence(editor, frame_files)` line 219; `add_synced_audio(editor, first_frame)` line 242; `configure_video_output(scene, frame_count)` line 268; `print_strip_report(scene, editor)` line 308; `main()` line 323
- Assignments: `SCRIPT_DIR`, `ROOT`, `RENDERS_DIR`, `AUDIO_PATH`, `OUTPUT_MP4`, `OUTPUT_IMAGE_SEQUENCE_DIR`, `OUTPUT_IMAGE_SEQUENCE_PREFIX`, `IMAGE_SEQUENCE_FORMAT`, `VIDEO_BITRATE`, `VIDEO_MAXRATE`, `VIDEO_MINRATE`, `VIDEO_BUFFERSIZE`, `AUDIO_BITRATE`, `ENCODE_SEQUENCE_AUTO_RENDER`, `ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER`, `ENCODE_SEQUENCE_SKIP_PLACEHOLDERS`, `ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER`

## Content
```py
00328:     print(f"[INFO] Sync audio: {ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER}")
00329:     print(f"[INFO] Skip empty: {ENCODE_SEQUENCE_SKIP_PLACEHOLDERS}")
00330:     print(f"[INFO] Switch VSE: {ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER}")
00331: 
00332:     frame_files = sorted_frame_files()
00333:     if not frame_files:
00334:         raise FileNotFoundError(f"Nessun frame trovato in: {OUTPUT_IMAGE_SEQUENCE_DIR}")
00335: 
00336:     frame_files, first_frame = contiguous_frame_files(frame_files)
00337:     if not frame_files:
00338:         raise FileNotFoundError(f"Nessun frame valido trovato in: {OUTPUT_IMAGE_SEQUENCE_DIR}")
00339: 
00340:     if not Path(AUDIO_PATH).exists():
00341:         raise FileNotFoundError(f"Audio non trovato: {AUDIO_PATH}")
00342: 
00343:     scene = bpy.context.scene
00344:     editor = clear_sequence_editor(scene)
00345:     image_strip = add_image_sequence(editor, frame_files)
00346: 
00347:     try:
00348:         audio_strip = add_synced_audio(editor, first_frame)
00349:     except Exception as exc:
00350:         audio_strip = None
00351:         print(f"[WARN] Audio strip non aggiunta: {exc}")
00352: 
00353:     configure_video_output(scene, len(frame_files))
00354:     force_visible_sequencer(scene, editor)
00355:     print_strip_report(scene, editor)
00356: 
00357:     print("=" * 68)
00358:     print("SPAZIOTEMPO IMAGE SEQUENCE ENCODE READY")
00359:     print(f"Frames: {len(frame_files)}")
00360:     print(f"Image strip: {getattr(image_strip, 'name', '<non creata>')}")
00361:     print(f"Audio strip: {getattr(audio_strip, 'name', '<non creata>')}")
00362:     if first_frame is not None:
00363:         print(f"First frame: {first_frame}")
00364:     print(f"Input:  {OUTPUT_IMAGE_SEQUENCE_DIR}")
00365:     print(f"Audio:  {AUDIO_PATH}")
00366:     print(f"MP4:    {OUTPUT_MP4}")
00367:     if ENCODE_SEQUENCE_AUTO_RENDER:
00368:         print("AUTO_RENDER attivo: avvio encoding MP4.")
00369:         bpy.ops.render.render(animation=True)
00370:     else:
00371:         print("Premi Render > Render Animation per creare l'MP4 dalla sequenza.")
00372:     print("=" * 68)
00373: 
00374: 
00375: if __name__ == "__main__":
00376:     main()
```
