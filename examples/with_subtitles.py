"""Generate subtitles for a media file."""
from subtitle_generator import generate_subtitles


def main() -> None:
    output = generate_subtitles("lecture.mp4", format="srt", model_size="small")
    print(f"Субтитры сохранены: {output}")


if __name__ == "__main__":
    main()
