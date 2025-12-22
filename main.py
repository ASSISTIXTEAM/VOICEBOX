"""CLI entry point for VOICEBOX."""
from __future__ import annotations

import argparse
from pathlib import Path

from transcriber import Transcriber


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="VOICEBOX - транскрибация аудио и видео")
    parser.add_argument("input", help="Путь к аудио или видео файлу")
    parser.add_argument("--model", default="base", help="Размер модели Whisper")
    parser.add_argument("--language", default=None, help="Язык аудио (например, ru, en)")
    parser.add_argument("--task", default="transcribe", choices=["transcribe", "translate"], help="Режим работы")
    parser.add_argument("--device", default=None, help="Устройство (cpu или cuda)")
    parser.add_argument("--output-format", default="txt", choices=["txt", "json", "srt", "vtt", "tsv"], help="Формат вывода")
    parser.add_argument("--output", default=None, help="Путь для сохранения результата")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    transcriber = Transcriber(
        model_size=args.model,
        language=args.language,
        task=args.task,
        device=args.device,
    )
    result = transcriber.transcribe(args.input)
    output_path = (
        Path(args.output)
        if args.output
        else Path(args.input).with_suffix(f".{args.output_format}")
    )
    saved = transcriber.save_output(result, output_path, format=args.output_format)
    print(f"Готово! Результат сохранен в {saved}")


if __name__ == "__main__":
    main()
