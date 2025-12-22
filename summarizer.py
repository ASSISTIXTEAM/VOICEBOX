"""Lightweight text summarisation utilities.

The implementation intentionally avoids external machine learning
libraries so it works out-of-the-box on offline machines. It uses a
simple frequency-based approach to select the most informative
sentences.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Iterable, List

from utils import read_text

SENTENCE_REGEX = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> List[str]:
    sentences = [segment.strip() for segment in SENTENCE_REGEX.split(text) if segment.strip()]
    return sentences if sentences else [text.strip()]


def build_summary(text: str, sentence_limit: int = 5) -> str:
    """Return a short summary based on word frequency."""
    sentences = split_sentences(text)
    words = re.findall(r"\w+", text.lower())
    frequencies = Counter(words)
    scores = []
    for sentence in sentences:
        tokens = re.findall(r"\w+", sentence.lower())
        score = sum(frequencies[token] for token in tokens)
        scores.append((score, sentence))
    top_sentences = [sentence for _, sentence in sorted(scores, reverse=True)[:sentence_limit]]
    return "\n".join(top_sentences)


def summarise_file(path: str | Path, sentence_limit: int = 5) -> str:
    """Load ``path`` and return its summary."""
    text = read_text(Path(path))
    return build_summary(text, sentence_limit=sentence_limit)


def save_summary(path: str | Path, summary: str) -> Path:
    target = Path(path)
    target.write_text(summary.strip() + "\n", encoding="utf-8")
    return target


def summarise_to_file(source: str | Path, target: str | Path, sentence_limit: int = 5) -> Path:
    summary = summarise_file(source, sentence_limit=sentence_limit)
    return save_summary(target, summary)
