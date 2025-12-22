"""
Простейший summarizer: извлекает ключевые предложения и считает ключевые слова.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Dict, List

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    return re.split(r"(?<=[.!?])\s+", text)


def summarize(text: str, max_sentences: int = 3) -> Dict[str, object]:
    sentences = split_sentences(text)
    if not sentences:
        return {"summary": "", "keywords": []}

    # Простая эвристика: берём первые предложения и самые частые слова
    summary = " ".join(sentences[:max_sentences]).strip()

    words = re.findall(r"\b\w+\b", text.lower())
    common = [word for word, _ in Counter(words).most_common(5)]

    return {"summary": summary, "keywords": common}


__all__ = ["summarize", "split_sentences"]
