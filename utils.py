"""
Вспомогательные функции, используемые в разных интерфейсах VOICEBOX.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Tuple


def is_video_file(path: str) -> bool:
    video_ext = {".mp4", ".mkv", ".mov", ".avi", ".webm"}
    return Path(path).suffix.lower() in video_ext


def is_audio_file(path: str) -> bool:
    audio_ext = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"}
    return Path(path).suffix.lower() in audio_ext


def temp_wav_path() -> Tuple[str, tempfile._TemporaryFileWrapper]:
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    return tmp.name, tmp


def ensure_file_exists(path: str) -> str:
    resolved = Path(path).expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Файл не найден: {resolved}")
    return str(resolved)
