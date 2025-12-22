"""
Базовый настольный GUI для VOICEBOX.
"""
from __future__ import annotations

import logging
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from typing import Optional

from audio_analyzer import analyze_text
from config import Config
from subtitle_generator import segments_to_srt, segments_to_vtt
from summarizer import summarize
from transcriber import WhisperTranscriber
from utils import ensure_file_exists, is_audio_file, is_video_file, temp_wav_path
from video_processor import extract_audio_to_wav, has_audio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceBoxDesktop:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("VOICEBOX Desktop")
        self.transcriber: Optional[WhisperTranscriber] = None
        self.selected_file: Optional[str] = None

        self._build_ui()

    def _build_ui(self) -> None:
        file_frame = tk.Frame(self.root)
        file_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(file_frame, text="Выбрать файл", command=self._pick_file).pack(side="left")
        self.file_label = tk.Label(file_frame, text="Файл не выбран", anchor="w")
        self.file_label.pack(side="left", padx=10)

        options_frame = tk.Frame(self.root)
        options_frame.pack(fill="x", padx=10)

        tk.Label(options_frame, text="Модель:").pack(side="left")
        self.model_var = tk.StringVar(value="base")
        tk.OptionMenu(options_frame, self.model_var, "tiny", "base", "small", "medium", "large-v3").pack(side="left")

        tk.Button(options_frame, text="Транскрибировать", command=self._run_transcribe).pack(side="right")

        self.log = scrolledtext.ScrolledText(self.root, height=14, state="disabled")
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

    def _append_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _pick_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Выберите аудио или видео файл",
            filetypes=[("Media", "*.mp3 *.wav *.m4a *.flac *.ogg *.aac *.mp4 *.mkv *.mov *.avi *.webm"), ("Все", "*.*")],
        )
        if path:
            self.selected_file = path
            self.file_label.config(text=path)
            self._append_log(f"Выбран файл: {path}")

    def _run_transcribe(self) -> None:
        if not self.selected_file:
            messagebox.showwarning("Нет файла", "Выберите файл для транскрибации")
            return

        self._append_log("Запуск транскрибации...")
        thread = threading.Thread(target=self._transcribe_selected, daemon=True)
        thread.start()

    def _transcribe_selected(self) -> None:
        try:
            file_path = ensure_file_exists(self.selected_file)
            model_name = self.model_var.get()
            self._append_log(f"Используем модель: {model_name}")
            self.transcriber = WhisperTranscriber(model_size=model_name)

            working_path = file_path
            temp_holder = None

            if is_video_file(file_path):
                if not has_audio(file_path):
                    raise RuntimeError("В видео отсутствует аудио дорожка")
                working_path, temp_holder = temp_wav_path()
                extract_audio_to_wav(file_path, working_path)
                self._append_log("Аудио извлечено во временный WAV")

            config = Config(model_size=model_name)
            text, segments = self.transcriber.transcribe(working_path, config=config)

            srt = segments_to_srt(segments)
            vtt = segments_to_vtt(segments)
            summary = summarize(text)
            stats = analyze_text(text)

            self._append_log("=== РЕЗУЛЬТАТЫ ===")
            self._append_log(text or "(пустой результат)")
            self._append_log("")
            self._append_log("Ключевые слова: " + ", ".join(summary.get("keywords", [])))
            self._append_log(f"Слов: {stats['word_count']}, Уникальных: {stats['unique_words']}")

            # Сохраняем вывод
            base = file_path + "_transcript"
            with open(base + ".txt", "w", encoding="utf-8") as f:
                f.write(text)
            with open(base + ".srt", "w", encoding="utf-8") as f:
                f.write(srt)
            with open(base + ".vtt", "w", encoding="utf-8") as f:
                f.write(vtt)
            self._append_log(f"Файлы сохранены рядом с исходником: {base}.[txt|srt|vtt]")

        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка транскрибации")
            self._append_log(f"Ошибка: {exc}")
            messagebox.showerror("Ошибка", str(exc))
        finally:
            if temp_holder:
                temp_holder.close()


def main():
    root = tk.Tk()
    app = VoiceBoxDesktop(root)
    root.mainloop()


if __name__ == "__main__":
    main()
