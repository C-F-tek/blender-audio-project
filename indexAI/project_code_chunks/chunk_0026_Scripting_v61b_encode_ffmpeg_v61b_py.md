# Project Code Chunk 26/212

- File: `Scripting/v61b/encode_ffmpeg_v61b.py`
- Part: `2`
- Lines: `323-398`

## Symbol Map
- Imports: `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `from pathlib import Path`, `config`
- Functions: `resolve_script_dir()` line 15; `extract_frame_number(path)` line 82; `sorted_frame_files()` line 89; `contiguous_frame_files(frame_files)` line 109; `get_fps()` line 133; `candidate_path_values()` line 155; `find_ffmpeg()` line 175; `build_image_pattern(first_file, first_frame)` line 203; `source_frame_to_audio_offset(first_frame, fps)` line 216; `build_command(ffmpeg, pattern, first_frame, frame_count, fps, audio_offset)` line 222; `write_visible_shell_launcher(command, output, first_frame, frame_count, fps, audio_offset)` line 328; `launch_visible_shell(command, output, first_frame, frame_count, fps, audio_offset)` line 355; `main()` line 362
- Assignments: `SCRIPT_DIR`, `AUDIO_PATH`, `ANALYSIS_JSON_PATH`, `OUTPUT_IMAGE_SEQUENCE_DIR`, `OUTPUT_IMAGE_SEQUENCE_PREFIX`, `IMAGE_SEQUENCE_FORMAT`, `OUTPUT_MP4`, `FFMPEG_EXE_PATH`, `FFMPEG_CRF`, `FFMPEG_PRESET`, `FFMPEG_TUNE`, `FFMPEG_AUDIO_BITRATE`, `FFMPEG_PROFILE`, `FFMPEG_GPU_INDEX`, `FFMPEG_NVENC_PRESET`, `FFMPEG_NVENC_TUNE`, `FFMPEG_NVENC_CQ`, `FFMPEG_SVTAV1_PRESET`, `FFMPEG_SVTAV1_CRF`, `FFMPEG_THREADS`, `FFMPEG_VIDEO_FILTER`, `FFMPEG_AUDIO_SAMPLE_RATE`, `SYNC_AUDIO`, `AUDIO_ZERO_FRAME`, `SKIP_PLACEHOLDERS`, `LAUNCH_VISIBLE_SHELL`

## Content
```py
00323:         str(output),
00324:     ])
00325:     return command
00326: 
00327: 
00328: def write_visible_shell_launcher(command, output, first_frame, frame_count, fps, audio_offset):
00329:     output = Path(output)
00330:     output_dir = output.parent
00331:     launcher = output_dir / f"{output.stem}_run_ffmpeg.cmd"
00332:     command_line = subprocess.list2cmdline([str(part) for part in command]).replace("%", "%%")
00333: 
00334:     lines = [
00335:         "@echo off",
00336:         "title Spaziotempo FFmpeg Encode",
00337:         f'cd /d "{output_dir}"',
00338:         "echo Spaziotempo FFmpeg encode",
00339:         f"echo Frames: {frame_count} from source frame {first_frame}",
00340:         f"echo FPS: {fps:.6f}",
00341:         f"echo Audio zero frame: {AUDIO_ZERO_FRAME}",
00342:         f"echo Audio offset seconds: {audio_offset:.6f}",
00343:         f'echo Output: "{output}"',
00344:         "echo.",
00345:         command_line,
00346:         "set ST_FFMPEG_EXIT=%ERRORLEVEL%",
00347:         "echo.",
00348:         "echo FFmpeg exit code: %ST_FFMPEG_EXIT%",
00349:         'if not "%ST_FFMPEG_EXIT%"=="0" echo FFmpeg failed. Check the messages above.',
00350:     ]
00351:     launcher.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")
00352:     return launcher
00353: 
00354: 
00355: def launch_visible_shell(command, output, first_frame, frame_count, fps, audio_offset):
00356:     launcher = write_visible_shell_launcher(command, output, first_frame, frame_count, fps, audio_offset)
00357:     creationflags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
00358:     subprocess.Popen(["cmd.exe", "/k", str(launcher)], creationflags=creationflags)
00359:     return launcher
00360: 
00361: 
00362: def main():
00363:     frame_files = sorted_frame_files()
00364:     if not frame_files:
00365:         raise FileNotFoundError(f"Nessun frame trovato in: {OUTPUT_IMAGE_SEQUENCE_DIR}")
00366: 
00367:     frame_files, first_frame = contiguous_frame_files(frame_files)
00368:     if not frame_files or first_frame is None:
00369:         raise FileNotFoundError("Sequenza frame non numerata o non valida per ffmpeg.")
00370: 
00371:     if not Path(AUDIO_PATH).exists():
00372:         raise FileNotFoundError(f"Audio non trovato: {AUDIO_PATH}")
00373: 
00374:     fps = get_fps()
00375:     audio_offset = source_frame_to_audio_offset(first_frame, fps)
00376:     pattern = build_image_pattern(frame_files[0], first_frame)
00377:     ffmpeg = find_ffmpeg()
00378:     command = build_command(ffmpeg, pattern, first_frame, len(frame_files), fps, audio_offset)
00379: 
00380:     print("[INFO] FFmpeg encode:")
00381:     print(f"[INFO] ffmpeg: {ffmpeg}")
00382:     print(f"[INFO] frames: {len(frame_files)} from frame {first_frame}")
00383:     print(f"[INFO] fps:    {fps:.6f}")
00384:     print(f"[INFO] audio zero frame: {AUDIO_ZERO_FRAME}")
00385:     print(f"[INFO] audio offset seconds: {audio_offset:.6f}")
00386:     print(f"[INFO] output: {OUTPUT_MP4}")
00387: 
00388:     if LAUNCH_VISIBLE_SHELL:
00389:         launcher = launch_visible_shell(command, OUTPUT_MP4, first_frame, len(frame_files), fps, audio_offset)
00390:         print(f"[INFO] FFmpeg launched in visible shell: {launcher}")
00391:         return
00392: 
00393:     subprocess.run(command, check=True)
00394:     print("[INFO] FFmpeg MP4 complete.")
00395: 
00396: 
00397: if __name__ == "__main__":
00398:     main()
```
