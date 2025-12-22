"""Basic usage of Transcriber."""
from transcriber import Transcriber


def main() -> None:
    transcriber = Transcriber(model_size="tiny")
    result = transcriber.transcribe("example.wav")
    transcriber.save_output(result, "example.txt")
    print("Готово! См. example.txt")


if __name__ == "__main__":
    main()
