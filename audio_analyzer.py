"""Basic text analysis utilities."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Dict, List
import re

from utils import read_text


WORD_REGEX = re.compile(r"\w+")


def analyse_text(text: str) -> Dict[str, object]:
    words = WORD_REGEX.findall(text.lower())
    sentences = re.split(r"[.!?]+", text)
    frequencies = Counter(words)
    return {
        "words": len(words),
        "characters": len(text),
        "sentences": len([s for s in sentences if s.strip()]),
        "top_words": frequencies.most_common(10),
    }


def analyse_file(path: str | Path) -> Dict[str, object]:
    return analyse_text(read_text(Path(path)))


def render_report(stats: Dict[str, object]) -> str:
    lines: List[str] = [
        "Статистика текста:",
        f"- Слов: {stats['words']}",
        f"- Символов: {stats['characters']}",
        f"- Предложений: {stats['sentences']}",
        "- Топ-10 слов:",
    ]
    for word, count in stats.get("top_words", []):
        lines.append(f"  • {word}: {count}")
    return "\n".join(lines)
