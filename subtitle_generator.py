"""Wrapper for generating SRT/VTT subtitles using Whisper."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from transcriber import Transcriber
from utils import ensure_directory


def generate_subtitles(
    audio_path: str | Path,
    *,
    output: Optional[str | Path] = None,
    language: Optional[str] = None,
    format: str = "srt",
    model_size: str = "base",
) -> Path:
    """Transcribe ``audio_path`` and save subtitles to ``output``."""
    transcriber = Transcriber(model_size=model_size, language=language, task="transcribe")
    result = transcriber.transcribe(audio_path)

    output_path = (
        Path(output).expanduser().resolve()
        if output
        else Path(audio_path).with_suffix(f".{format}")
    )
    ensure_directory(output_path.parent)
    transcriber.save_output(result, output_path, format=format)
    return output_path
