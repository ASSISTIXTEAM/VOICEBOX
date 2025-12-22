"""Gradio interface for VOICEBOX."""
from __future__ import annotations

from pathlib import Path
import gradio as gr

from transcriber import Transcriber


def transcribe_file(file_path: str, model_size: str, language: str) -> tuple[str, str]:
    if not file_path:
        return "", "Файл не выбран"
    transcriber = Transcriber(model_size=model_size or "base", language=language or None)
    result = transcriber.transcribe(file_path)
    output_path = Path(file_path).with_suffix(".txt")
    transcriber.save_output(result, output_path)
    return result.get("text", ""), f"Сохранено: {output_path}"


def build_interface() -> gr.Blocks:
    with gr.Blocks(title="VOICEBOX Web UI") as demo:
        gr.Markdown("# 🎙️ VOICEBOX Web UI\nЗагрузите аудио или видео и получите текст")
        with gr.Row():
            with gr.Column():
                audio = gr.File(label="Аудио/Видео файл", file_types=["audio", "video"])
                model_size = gr.Dropdown(
                    ["tiny", "base", "small", "medium", "large"],
                    value="base",
                    label="Размер модели",
                )
                language = gr.Textbox(label="Язык (опционально)")
                run = gr.Button("Транскрибировать")
            with gr.Column():
                output = gr.Textbox(label="Результат", lines=12)
                status = gr.Markdown()
        run.click(transcribe_file, inputs=[audio, model_size, language], outputs=[output, status])
    return demo


def main() -> None:
    build_interface().launch()


if __name__ == "__main__":
    main()
