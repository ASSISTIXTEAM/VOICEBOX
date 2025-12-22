"""Utility helpers for VOICEBOX.

The module centralises small reusable helpers used across the
transcription, subtitle and GUI layers. Functions are intentionally kept
simple so they work in offline environments and are easy to unit test.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence
import json
import shutil


def ensure_file_exists(path: Path) -> Path:
    """Validate that a file exists.

    Args:
        path: Path to validate.

    Returns:
        The normalised path if it exists.

    Raises:
        FileNotFoundError: If the path does not exist or is not a file.
    """
    resolved = Path(path).expanduser().resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Файл не найден: {resolved}")
    return resolved


def ensure_directory(path: Path) -> Path:
    """Create a directory if it does not exist and return its path."""
    resolved = Path(path).expanduser().resolve()
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def format_timestamp(seconds: float) -> str:
    """Convert floating-point seconds to SRT/VTT friendly timestamp."""
    milliseconds = int(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1_000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


@dataclass
class TranscriptSegment:
    """Simple container representing a transcript segment."""

    start: float
    end: float
    text: str


def segments_to_srt(segments: Sequence[TranscriptSegment]) -> str:
    """Render transcript segments into SRT formatted text."""
    lines: List[str] = []
    for index, segment in enumerate(segments, start=1):
        start_ts = format_timestamp(segment.start)
        end_ts = format_timestamp(segment.end)
        lines.append(str(index))
        lines.append(f"{start_ts} --> {end_ts}")
        lines.append(segment.text.strip())
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def segments_to_vtt(segments: Sequence[TranscriptSegment]) -> str:
    """Render transcript segments into VTT formatted text."""
    lines: List[str] = ["WEBVTT", ""]
    for segment in segments:
        start_ts = format_timestamp(segment.start).replace(",", ".")
        end_ts = format_timestamp(segment.end).replace(",", ".")
        lines.append(f"{start_ts} --> {end_ts}")
        lines.append(segment.text.strip())
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def save_json(path: Path, payload: object) -> None:
    """Serialise ``payload`` into ``path`` with UTF-8 encoding."""
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def read_text(path: Path) -> str:
    """Read a UTF-8 text file."""
    return Path(path).read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    """Write UTF-8 text to ``path`` creating parent directories."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")


def detect_ffmpeg() -> str:
    """Return the detected ffmpeg binary path or raise an error."""
    executable = shutil.which("ffmpeg")
    if not executable:
        raise EnvironmentError(
            "FFmpeg не найден в PATH. Установите FFmpeg и повторите попытку."
        )
    return executable


def normalise_paths(items: Iterable[str | Path]) -> List[Path]:
    """Expand and resolve a collection of filesystem paths."""
    return [Path(item).expanduser().resolve() for item in items]
