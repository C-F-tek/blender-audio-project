def write_visible_shell_launcher(command, output, first_frame, frame_count, fps, audio_offset):
    output = Path(output)
    output_dir = output.parent
    launcher = output_dir / f"{output.stem}_run_ffmpeg.cmd"
    command_line = subprocess.list2cmdline([str(part) for part in command]).replace("%", "%%")

    lines = [
        "@echo off",
        "title Spaziotempo FFmpeg Encode",
        f'cd /d "{output_dir}"',
        "echo Spaziotempo FFmpeg encode",
        f"echo Frames: {frame_count} from source frame {first_frame}",
        f"echo FPS: {fps:.6f}",
        f"echo Audio zero frame: {AUDIO_ZERO_FRAME}",
        f"echo Audio offset seconds: {audio_offset:.6f}",
        f'echo Output: "{output}"',
        "echo.",
        command_line,
        "set ST_FFMPEG_EXIT=%ERRORLEVEL%",
        "echo.",
        "echo FFmpeg exit code: %ST_FFMPEG_EXIT%",
        'if not "%ST_FFMPEG_EXIT%"=="0" echo FFmpeg failed. Check the messages above.',
    ]
    launcher.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")
    return launcher


def launch_visible_shell(command, output, first_frame, frame_count, fps, audio_offset):
    launcher = write_visible_shell_launcher(
        command, output, first_frame, frame_count, fps, audio_offset
    )
    creationflags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    subprocess.Popen(["cmd.exe", "/k", str(launcher)], creationflags=creationflags)
    return launcher


def main():
    frame_files = sorted_frame_files()
    if not frame_files:
        raise FileNotFoundError(f"Nessun frame trovato in: {OUTPUT_IMAGE_SEQUENCE_DIR}")

    frame_files, first_frame = contiguous_frame_files(frame_files)
    if not frame_files or first_frame is None:
        raise FileNotFoundError("Sequenza frame non numerata o non valida per ffmpeg.")

    if not Path(AUDIO_PATH).exists():
        raise FileNotFoundError(f"Audio non trovato: {AUDIO_PATH}")

    fps = get_fps()
    audio_offset = source_frame_to_audio_offset(first_frame, fps)
    pattern = build_image_pattern(frame_files[0], first_frame)
    ffmpeg = find_ffmpeg()
    command = build_command(ffmpeg, pattern, first_frame, len(frame_files), fps, audio_offset)

    print("[INFO] FFmpeg encode:")
    print(f"[INFO] ffmpeg: {ffmpeg}")
    print(f"[INFO] frames: {len(frame_files)} from frame {first_frame}")
    print(f"[INFO] fps:    {fps:.6f}")
    print(f"[INFO] audio zero frame: {AUDIO_ZERO_FRAME}")
    print(f"[INFO] audio offset seconds: {audio_offset:.6f}")
    print(f"[INFO] output: {OUTPUT_MP4}")

    if LAUNCH_VISIBLE_SHELL:
        launcher = launch_visible_shell(
            command, OUTPUT_MP4, first_frame, len(frame_files), fps, audio_offset
        )
        print(f"[INFO] FFmpeg launched in visible shell: {launcher}")
        return

    subprocess.run(command, check=True)
    print("[INFO] FFmpeg MP4 complete.")


if __name__ == "__main__":
    main()
