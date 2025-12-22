"""Video helpers built on top of ``ffmpeg-python``."""
from __future__ import annotations

from pathlib import Path
from typing import Optional
import ffmpeg

from utils import detect_ffmpeg, ensure_directory, ensure_file_exists


def extract_audio(video_path: str | Path, output_path: Optional[str | Path] = None) -> Path:
    """Extract audio track from ``video_path`` using FFmpeg."""
    input_path = ensure_file_exists(video_path)
    output_file = (
        Path(output_path).expanduser().resolve()
        if output_path
        else input_path.with_suffix(".wav")
    )
    ensure_directory(output_file.parent)
    detect_ffmpeg()

    (
        ffmpeg
        .input(str(input_path))
        .output(str(output_file), acodec="pcm_s16le", ac=1, ar="16k")
        .overwrite_output()
        .run(quiet=True)
    )
    return output_file


def add_subtitles(video_path: str | Path, subtitles_path: str | Path, output_path: Optional[str | Path] = None) -> Path:
    """Burn subtitles into a video file using FFmpeg."""
    input_path = ensure_file_exists(video_path)
    subtitle_file = ensure_file_exists(subtitles_path)
    output_file = (
        Path(output_path).expanduser().resolve()
        if output_path
        else input_path.with_name(f"{input_path.stem}_subtitled{input_path.suffix}")
    )
    ensure_directory(output_file.parent)
    detect_ffmpeg()

    (
        ffmpeg
        .input(str(input_path))
        .output(str(output_file), vf=f"subtitles={subtitle_file}")
        .overwrite_output()
        .run(quiet=True)
    )
    return output_file
