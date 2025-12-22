"""
Инструменты для работы с видеофайлами: извлечение аудио дорожки.
"""
from __future__ import annotations

import logging
from pathlib import Path

import ffmpeg

logger = logging.getLogger(__name__)


def extract_audio_to_wav(video_path: str, output_path: str) -> str:
    """Извлекает аудио из видео в формате WAV."""
    logger.info("Извлекаем аудио из %s", video_path)
    input_stream = ffmpeg.input(video_path)
    audio = input_stream.audio
    ffmpeg.output(audio, output_path, acodec="pcm_s16le", ar=16000).run(quiet=True, overwrite_output=True)
    return output_path


def has_audio(video_path: str) -> bool:
    """Быстрая проверка наличия аудио дорожки."""
    try:
        probe = ffmpeg.probe(video_path)
        return any(stream.get("codec_type") == "audio" for stream in probe.get("streams", []))
    except ffmpeg.Error:
        return False


__all__ = ["extract_audio_to_wav", "has_audio"]
