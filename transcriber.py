"""
Модуль для транскрибации аудио/видео файлов с помощью OpenAI Whisper.

Предоставляет простой класс-обёртку, который загружает модель единожды
и использует параметры из config.Config для выполнения транскрибации.
"""
from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Dict, Iterable, List, Optional, Tuple

import torch
import whisper

from config import Config

logger = logging.getLogger(__name__)


class WhisperTranscriber:
    """Упрощённая обёртка над ``whisper`` с разумными настройками по умолчанию."""

    def __init__(self, model_size: str = "base", device: Optional[str] = None) -> None:
        self.model_size = model_size
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        logger.info("Загружаем модель Whisper %s на устройство %s", model_size, self.device)
        self.model = whisper.load_model(model_size, device=self.device)

    def _build_options(self, config: Optional[Config]) -> Dict:
        if config is None:
            return {}

        raw = asdict(config)
        options: Dict[str, object] = {
            # Параметры задачи
            "language": raw.get("language"),
            "task": raw.get("task", "transcribe"),
            "beam_size": raw.get("beam_size"),
            "best_of": raw.get("best_of"),
            "temperature": raw.get("temperature"),
            "no_speech_threshold": raw.get("no_speech_threshold"),
            "condition_on_previous_text": raw.get("condition_on_previous_text"),
            "initial_prompt": raw.get("initial_prompt"),
            "verbose": raw.get("verbose", False),
        }

        # Удаляем значения None, чтобы whisper использовал дефолты
        return {k: v for k, v in options.items() if v is not None}

    def transcribe(self, file_path: str, config: Optional[Config] = None) -> Tuple[str, List[Dict]]:
        """Транскрибирует файл и возвращает текст и список сегментов."""

        options = self._build_options(config)
        logger.debug("Параметры транскрибации: %s", options)

        result = self.model.transcribe(file_path, **options)
        text = result.get("text", "").strip()

        segments: List[Dict] = []
        for seg in result.get("segments", []):
            segments.append(
                {
                    "start": float(seg["start"]),
                    "end": float(seg["end"]),
                    "text": seg.get("text", "").strip(),
                }
            )

        return text, segments

    def transcribe_many(self, files: Iterable[str], config: Optional[Config] = None) -> Dict[str, Tuple[str, List[Dict]]]:
        """Последовательно транскрибирует набор файлов."""

        output: Dict[str, Tuple[str, List[Dict]]] = {}
        for path in files:
            logger.info("Транскрибация файла %s", path)
            output[path] = self.transcribe(path, config)
        return output


__all__ = ["WhisperTranscriber"]
