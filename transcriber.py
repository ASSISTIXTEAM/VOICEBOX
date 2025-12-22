"""Core transcription utilities powered by OpenAI Whisper.

The :class:`Transcriber` class is intentionally lightweight: it lazily
loads the Whisper model, exposes a small ergonomic API and provides
helpers to persist results in popular formats (TXT, JSON, SRT, VTT and
TSV).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import json

import torch
import whisper

from config import Config
from utils import (
    TranscriptSegment,
    ensure_directory,
    ensure_file_exists,
    segments_to_srt,
    segments_to_vtt,
    write_text,
    save_json,
)


class Transcriber:
    """High-level helper around ``whisper.transcribe``.

    Parameters mirror :class:`config.Config` to keep configuration
    discoverable for GUI and CLI layers. The device is automatically
    selected: CUDA is used when available unless explicitly overridden.
    """

    def __init__(
        self,
        model_size: str = "base",
        language: Optional[str] = None,
        task: str = "transcribe",
        device: Optional[str] = None,
        beam_size: int = 5,
        best_of: int = 5,
        temperature: float = 0.0,
        no_speech_threshold: float = 0.6,
        condition_on_previous_text: bool = True,
        initial_prompt: Optional[str] = None,
        verbose: bool = False,
    ) -> None:
        self.config = Config(
            model_size=model_size,
            language=language,
            task=task,
            device=device,
            beam_size=beam_size,
            best_of=best_of,
            temperature=temperature,
            no_speech_threshold=no_speech_threshold,
            condition_on_previous_text=condition_on_previous_text,
            initial_prompt=initial_prompt,
            verbose=verbose,
        )
        self._model: Optional[whisper.model.Whisper] = None

    @property
    def device(self) -> str:
        """Return the selected compute device."""
        if self.config.device:
            return self.config.device
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _load_model(self) -> whisper.model.Whisper:
        if self._model is None:
            self._model = whisper.load_model(self.config.model_size, device=self.device)
        return self._model

    def transcribe(
        self,
        audio_path: str | Path,
        *,
        language: Optional[str] = None,
        task: Optional[str] = None,
        temperature: Optional[float] = None,
        beam_size: Optional[int] = None,
        best_of: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Transcribe ``audio_path`` returning Whisper's raw result."""
        audio_file = ensure_file_exists(audio_path)
        model = self._load_model()
        return model.transcribe(
            str(audio_file),
            language=language or self.config.language,
            task=task or self.config.task,
            temperature=temperature if temperature is not None else self.config.temperature,
            beam_size=beam_size if beam_size is not None else self.config.beam_size,
            best_of=best_of if best_of is not None else self.config.best_of,
            no_speech_threshold=self.config.no_speech_threshold,
            condition_on_previous_text=self.config.condition_on_previous_text,
            initial_prompt=self.config.initial_prompt,
            verbose=self.config.verbose,
        )

    def _segments_from_result(self, result: Dict[str, Any]) -> List[TranscriptSegment]:
        return [
            TranscriptSegment(start=segment["start"], end=segment["end"], text=segment["text"].strip())
            for segment in result.get("segments", [])
        ]

    def save_output(self, result: Dict[str, Any], output: str | Path, format: str = "txt") -> Path:
        """Persist a transcription result in a human friendly format."""
        output_path = Path(output)
        ensure_directory(output_path.parent)
        format_lower = format.lower()
        segments = self._segments_from_result(result)

        if format_lower == "txt":
            write_text(output_path, result.get("text", "").strip() + "\n")
        elif format_lower == "json":
            save_json(output_path, result)
        elif format_lower == "srt":
            write_text(output_path, segments_to_srt(segments))
        elif format_lower == "vtt":
            write_text(output_path, segments_to_vtt(segments))
        elif format_lower == "tsv":
            lines = ["start\tend\ttext"]
            for segment in segments:
                lines.append(f"{segment.start}\t{segment.end}\t{segment.text}")
            write_text(output_path, "\n".join(lines) + "\n")
        else:
            raise ValueError(f"Неизвестный формат вывода: {format}")

        return output_path

    def batch_transcribe(self, paths: Iterable[str | Path], output_dir: str | Path) -> List[Path]:
        """Transcribe multiple files saving TXT outputs in ``output_dir``."""
        output_root = ensure_directory(output_dir)
        saved: List[Path] = []
        for path in paths:
            audio_path = ensure_file_exists(path)
            result = self.transcribe(audio_path)
            output_path = output_root / f"{audio_path.stem}.txt"
            saved.append(self.save_output(result, output_path, format="txt"))
        return saved


def load_config_from_dict(options: Dict[str, Any]) -> Transcriber:
    """Helper used by CLI/GUI to create a ``Transcriber`` from raw data."""
    config = Config(**{**options})
    return Transcriber(
        model_size=config.model_size,
        language=config.language,
        task=config.task,
        device=config.device,
        beam_size=config.beam_size,
        best_of=config.best_of,
        temperature=config.temperature,
        no_speech_threshold=config.no_speech_threshold,
        condition_on_previous_text=config.condition_on_previous_text,
        initial_prompt=config.initial_prompt,
        verbose=config.verbose,
    )
