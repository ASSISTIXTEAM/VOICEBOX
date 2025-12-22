"""Batch processing example."""
from transcriber import Transcriber


def main() -> None:
    transcriber = Transcriber(model_size="base")
    files = ["audio1.wav", "audio2.wav"]
    outputs = transcriber.batch_transcribe(files, output_dir="outputs")
    for path in outputs:
        print(f"Сохранено: {path}")


if __name__ == "__main__":
    main()
