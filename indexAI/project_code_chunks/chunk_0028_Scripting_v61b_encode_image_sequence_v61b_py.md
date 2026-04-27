# Project Code Chunk 28/212

- File: `Scripting/v61b/encode_image_sequence_v61b.py`
- Part: `2`
- Lines: `330-395`

## Symbol Map
- Imports: `re`, `sys`, `from pathlib import Path`, `bpy`, `config`
- Functions: `resolve_script_dir()` line 8; `extract_frame_number(path)` line 83; `sorted_frame_files()` line 90; `contiguous_frame_files(frame_files)` line 116; `get_sequence_collection(editor)` line 143; `all_editor_strips(editor)` line 151; `remove_editor_strip(editor, strip)` line 163; `force_visible_sequencer(scene, editor)` line 176; `clear_sequence_editor(scene)` line 224; `add_image_sequence(editor, frame_files)` line 235; `add_synced_audio(editor, first_frame)` line 258; `configure_video_output(scene, frame_count)` line 285; `print_strip_report(scene, editor)` line 327; `main()` line 342
- Assignments: `SCRIPT_DIR`, `ROOT`, `RENDERS_DIR`, `AUDIO_PATH`, `OUTPUT_MP4`, `OUTPUT_IMAGE_SEQUENCE_DIR`, `OUTPUT_IMAGE_SEQUENCE_PREFIX`, `IMAGE_SEQUENCE_FORMAT`, `VIDEO_BITRATE`, `VIDEO_MAXRATE`, `VIDEO_MINRATE`, `VIDEO_BUFFERSIZE`, `AUDIO_BITRATE`, `ENCODE_SEQUENCE_AUTO_RENDER`, `ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER`, `ENCODE_SEQUENCE_AUDIO_ZERO_FRAME`, `ENCODE_SEQUENCE_SKIP_PLACEHOLDERS`, `ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER`

## Content
```py
00330:     print(f"[INFO] Strip nel Video Sequencer: {len(strips)}")
00331:     for strip in strips:
00332:         try:
00333:             print(
00334:                 "[INFO] Strip: "
00335:                 f"{strip.name} | type={strip.type} | channel={strip.channel} | "
00336:                 f"start={strip.frame_start} | duration={strip.frame_final_duration}"
00337:             )
00338:         except Exception:
00339:             print(f"[INFO] Strip: {getattr(strip, 'name', '<senza nome>')}")
00340: 
00341: 
00342: def main():
00343:     print("[INFO] Encode config:")
00344:     print(f"[INFO] Frames dir: {OUTPUT_IMAGE_SEQUENCE_DIR}")
00345:     print(f"[INFO] Prefix:     {OUTPUT_IMAGE_SEQUENCE_PREFIX}")
00346:     print(f"[INFO] Format:     {IMAGE_SEQUENCE_FORMAT}")
00347:     print(f"[INFO] Sync audio: {ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER}")
00348:     print(f"[INFO] Skip empty: {ENCODE_SEQUENCE_SKIP_PLACEHOLDERS}")
00349:     print(f"[INFO] Switch VSE: {ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER}")
00350: 
00351:     frame_files = sorted_frame_files()
00352:     if not frame_files:
00353:         raise FileNotFoundError(f"Nessun frame trovato in: {OUTPUT_IMAGE_SEQUENCE_DIR}")
00354: 
00355:     frame_files, first_frame = contiguous_frame_files(frame_files)
00356:     if not frame_files:
00357:         raise FileNotFoundError(f"Nessun frame valido trovato in: {OUTPUT_IMAGE_SEQUENCE_DIR}")
00358: 
00359:     if not Path(AUDIO_PATH).exists():
00360:         raise FileNotFoundError(f"Audio non trovato: {AUDIO_PATH}")
00361: 
00362:     scene = bpy.context.scene
00363:     editor = clear_sequence_editor(scene)
00364:     image_strip = add_image_sequence(editor, frame_files)
00365: 
00366:     try:
00367:         audio_strip = add_synced_audio(editor, first_frame)
00368:     except Exception as exc:
00369:         audio_strip = None
00370:         print(f"[WARN] Audio strip non aggiunta: {exc}")
00371: 
00372:     configure_video_output(scene, len(frame_files))
00373:     force_visible_sequencer(scene, editor)
00374:     print_strip_report(scene, editor)
00375: 
00376:     print("=" * 68)
00377:     print("SPAZIOTEMPO IMAGE SEQUENCE ENCODE READY")
00378:     print(f"Frames: {len(frame_files)}")
00379:     print(f"Image strip: {getattr(image_strip, 'name', '<non creata>')}")
00380:     print(f"Audio strip: {getattr(audio_strip, 'name', '<non creata>')}")
00381:     if first_frame is not None:
00382:         print(f"First frame: {first_frame}")
00383:     print(f"Input:  {OUTPUT_IMAGE_SEQUENCE_DIR}")
00384:     print(f"Audio:  {AUDIO_PATH}")
00385:     print(f"MP4:    {OUTPUT_MP4}")
00386:     if ENCODE_SEQUENCE_AUTO_RENDER:
00387:         print("AUTO_RENDER attivo: avvio encoding MP4.")
00388:         bpy.ops.render.render(animation=True)
00389:     else:
00390:         print("Premi Render > Render Animation per creare l'MP4 dalla sequenza.")
00391:     print("=" * 68)
00392: 
00393: 
00394: if __name__ == "__main__":
00395:     main()
```
