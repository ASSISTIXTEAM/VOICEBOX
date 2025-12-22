"""
CLI-обёртка для быстрого запуска транскрибации без GUI.
"""
from __future__ import annotations

import argparse
import sys

from config import Config
from subtitle_generator import segments_to_srt
from transcriber import WhisperTranscriber
from utils import ensure_file_exists


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="VOICEBOX CLI")
    parser.add_argument("path", help="Путь к аудио/видео файлу")
    parser.add_argument("--model", default="base", help="Размер модели whisper")
    parser.add_argument("--srt", action="store_true", help="Сохранить SRT рядом с файлом")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    path = ensure_file_exists(args.path)

    transcriber = WhisperTranscriber(model_size=args.model)
    config = Config(model_size=args.model)
    text, segments = transcriber.transcribe(path, config)

    print(text)

    if args.srt:
        srt = segments_to_srt(segments)
        with open(path + "_transcript.srt", "w", encoding="utf-8") as f:
            f.write(srt)
        print("SRT сохранён", file=sys.stderr)


if __name__ == "__main__":
    main()
