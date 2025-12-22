"""Create a summary from a transcript."""
from summarizer import summarise_to_file


def main() -> None:
    target = summarise_to_file("transcript.txt", "transcript.summary.txt")
    print(f"Готово: {target}")


if __name__ == "__main__":
    main()
