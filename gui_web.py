"""
Веб-интерфейс на Gradio для транскрибации через VOICEBOX.
"""
from __future__ import annotations

import tempfile
from typing import Tuple

import gradio as gr

from config import Config
from summarizer import summarize
from transcriber import WhisperTranscriber
from utils import is_video_file
from video_processor import extract_audio_to_wav


_transcriber = WhisperTranscriber()


def _prepare_file(file_obj) -> Tuple[str, tempfile._TemporaryFileWrapper]:
    if file_obj is None:
        raise ValueError("Файл не передан")
    path = file_obj.name
    if is_video_file(path):
        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        extract_audio_to_wav(path, temp.name)
        return temp.name, temp
    return path, None


def transcribe_file(file_obj):
    path, temp = _prepare_file(file_obj)
    try:
        text, segments = _transcriber.transcribe(path, Config())
        summary = summarize(text)
        return text, "\n".join(f"{s['start']:.1f}-{s['end']:.1f}: {s['text']}" for s in segments), summary.get("summary", "")
    finally:
        if temp:
            temp.close()


def main():
    with gr.Blocks(title="VOICEBOX Web") as demo:
        gr.Markdown("## 🎙️ VOICEBOX Web\nЗагрузите аудио или видео для транскрибации")
        with gr.Row():
            input_file = gr.File(label="Медиа файл", file_types=["audio", "video"])
        with gr.Row():
            transcript = gr.Textbox(label="Транскрипт")
            segments = gr.Textbox(label="Сегменты")
        summary_box = gr.Textbox(label="Краткое резюме")

        input_file.change(transcribe_file, inputs=[input_file], outputs=[transcript, segments, summary_box])

    demo.launch()


if __name__ == "__main__":
    main()
