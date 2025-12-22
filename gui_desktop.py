"""Simplified desktop GUI for single-file transcription."""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading

from transcriber import Transcriber


class DesktopApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("VOICEBOX Desktop")
        self.geometry("500x260")
        self.resizable(False, False)

        self.model_var = tk.StringVar(value="base")
        self.language_var = tk.StringVar(value="")
        self.file_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        tk.Label(self, text="Файл для транскрибации:").pack(anchor="w", padx=10, pady=(10, 0))
        file_frame = tk.Frame(self)
        file_frame.pack(fill="x", padx=10)
        tk.Entry(file_frame, textvariable=self.file_var, width=40).pack(side="left", expand=True, fill="x")
        tk.Button(file_frame, text="Выбрать", command=self.choose_file).pack(side="left", padx=5)

        tk.Label(self, text="Размер модели (tiny/base/small/medium/large):").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(self, textvariable=self.model_var).pack(fill="x", padx=10)

        tk.Label(self, text="Язык (опционально, например ru):").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(self, textvariable=self.language_var).pack(fill="x", padx=10)

        tk.Button(self, text="Начать", command=self.start_transcription).pack(pady=15)
        self.status_label = tk.Label(self, text="Готов", fg="green")
        self.status_label.pack()

    def choose_file(self) -> None:
        path = filedialog.askopenfilename(title="Выберите аудио или видео")
        if path:
            self.file_var.set(path)

    def start_transcription(self) -> None:
        if not self.file_var.get():
            messagebox.showwarning("Ошибка", "Сначала выберите файл")
            return
        thread = threading.Thread(target=self._run_transcription, daemon=True)
        thread.start()

    def _run_transcription(self) -> None:
        try:
            self.status_label.config(text="Транскрибация...", fg="blue")
            transcriber = Transcriber(
                model_size=self.model_var.get() or "base",
                language=self.language_var.get() or None,
            )
            result = transcriber.transcribe(self.file_var.get())
            output = Path(self.file_var.get()).with_suffix(".txt")
            transcriber.save_output(result, output)
            self.status_label.config(text=f"Готово: {output}", fg="green")
        except Exception as exc:  # noqa: BLE001
            self.status_label.config(text="Ошибка", fg="red")
            messagebox.showerror("Ошибка", str(exc))


def main() -> None:
    DesktopApp().mainloop()


if __name__ == "__main__":
    main()
