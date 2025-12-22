"""
Мини-анализ текста транскрибации для отображения статистики.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Dict


def analyze_text(text: str) -> Dict[str, object]:
    words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    sentences = re.split(r"(?<=[.!?])\s+", text.strip()) if text.strip() else []

    return {
        "word_count": len(words),
        "unique_words": len(set(words)),
        "character_count": len(text),
        "sentence_count": len([s for s in sentences if s]),
        "top_words": Counter(w.lower() for w in words).most_common(5),
    }


__all__ = ["analyze_text"]
