"""
Генерация субтитров (SRT/VTT) из сегментов Whisper.
"""
from __future__ import annotations

from typing import Iterable, List, Mapping


def _format_timestamp(seconds: float, for_vtt: bool = False) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    separator = "." if for_vtt else ","
    return f"{hours:02}:{minutes:02}:{secs:06.3f}".replace(".", separator, 1)


def segments_to_srt(segments: Iterable[Mapping]) -> str:
    lines: List[str] = []
    for idx, seg in enumerate(segments, start=1):
        start = _format_timestamp(seg.get("start", 0.0))
        end = _format_timestamp(seg.get("end", 0.0))
        text = seg.get("text", "")
        lines.append(f"{idx}")
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


def segments_to_vtt(segments: Iterable[Mapping]) -> str:
    lines: List[str] = ["WEBVTT", ""]
    for seg in segments:
        start = _format_timestamp(seg.get("start", 0.0), for_vtt=True)
        end = _format_timestamp(seg.get("end", 0.0), for_vtt=True)
        text = seg.get("text", "")
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


__all__ = ["segments_to_srt", "segments_to_vtt"]
