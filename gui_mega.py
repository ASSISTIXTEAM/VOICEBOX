"""Feature-rich Tkinter interface combining all modules."""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from audio_analyzer import analyse_file, render_report
from subtitle_generator import generate_subtitles
from summarizer import summarise_to_file
from transcriber import Transcriber


class MegaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("VOICEBOX MEGA")
        self.geometry("720x540")
        self.resizable(False, False)

        self.model_var = tk.StringVar(value="base")
        self.language_var = tk.StringVar(value="")
        self.input_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        header = tk.Label(self, text="VOICEBOX MEGA — Транскрибация, субтитры и конспекты", font=("Arial", 14, "bold"))
        header.pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        notebook.add(self._transcribe_tab(notebook), text="Транскрибация")
        notebook.add(self._subtitles_tab(notebook), text="Субтитры")
        notebook.add(self._summary_tab(notebook), text="Конспект")
        notebook.add(self._analyze_tab(notebook), text="Анализ текста")

    def _file_selector(self, frame: tk.Widget, variable: tk.StringVar, title: str) -> None:
        row = tk.Frame(frame)
        row.pack(fill="x", pady=5)
        tk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Выбрать", command=lambda: variable.set(filedialog.askopenfilename(title=title))).pack(side="left", padx=5)

    def _settings_block(self, frame: tk.Widget) -> None:
        tk.Label(frame, text="Модель", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Entry(frame, textvariable=self.model_var).pack(fill="x")
        tk.Label(frame, text="Язык (опционально)").pack(anchor="w", pady=(5, 0))
        tk.Entry(frame, textvariable=self.language_var).pack(fill="x")

    # Tabs
    def _transcribe_tab(self, parent: ttk.Notebook) -> tk.Frame:
        frame = tk.Frame(parent)
        self._file_selector(frame, self.input_var, "Выберите аудио/видео")
        self._settings_block(frame)
        tk.Button(frame, text="Начать транскрибацию", command=self._start_transcription).pack(pady=10)
        self.transcribe_status = tk.Label(frame, text="Готов", fg="green")
        self.transcribe_status.pack(anchor="w")
        return frame

    def _subtitles_tab(self, parent: ttk.Notebook) -> tk.Frame:
        frame = tk.Frame(parent)
        self.subtitle_input = tk.StringVar()
        self._file_selector(frame, self.subtitle_input, "Выберите аудио для субтитров")
        tk.Button(frame, text="Создать SRT", command=self._start_subtitles).pack(pady=10)
        self.subtitle_status = tk.Label(frame, text="Ожидание", fg="blue")
        self.subtitle_status.pack(anchor="w")
        return frame

    def _summary_tab(self, parent: ttk.Notebook) -> tk.Frame:
        frame = tk.Frame(parent)
        self.summary_input = tk.StringVar()
        self._file_selector(frame, self.summary_input, "Выберите текст для конспекта")
        tk.Button(frame, text="Сохранить конспект", command=self._start_summary).pack(pady=10)
        self.summary_status = tk.Label(frame, text="Ожидание")
        self.summary_status.pack(anchor="w")
        return frame

    def _analyze_tab(self, parent: ttk.Notebook) -> tk.Frame:
        frame = tk.Frame(parent)
        self.analysis_input = tk.StringVar()
        self._file_selector(frame, self.analysis_input, "Выберите текст для анализа")
        tk.Button(frame, text="Показать статистику", command=self._start_analysis).pack(pady=10)
        self.analysis_text = tk.Text(frame, height=12)
        self.analysis_text.pack(fill="both", expand=True)
        return frame

    # Actions
    def _start_transcription(self) -> None:
        if not self.input_var.get():
            messagebox.showwarning("Ошибка", "Выберите файл")
            return
        threading.Thread(target=self._run_transcription, daemon=True).start()

    def _run_transcription(self) -> None:
        try:
            self.transcribe_status.config(text="Обработка...", fg="blue")
            transcriber = Transcriber(
                model_size=self.model_var.get() or "base",
                language=self.language_var.get() or None,
            )
            result = transcriber.transcribe(self.input_var.get())
            output = Path(self.input_var.get()).with_suffix(".txt")
            transcriber.save_output(result, output)
            self.transcribe_status.config(text=f"Готово: {output}", fg="green")
        except Exception as exc:  # noqa: BLE001
            self.transcribe_status.config(text="Ошибка", fg="red")
            messagebox.showerror("Ошибка", str(exc))

    def _start_subtitles(self) -> None:
        if not self.subtitle_input.get():
            messagebox.showwarning("Ошибка", "Выберите файл")
            return
        threading.Thread(target=self._run_subtitles, daemon=True).start()

    def _run_subtitles(self) -> None:
        try:
            self.subtitle_status.config(text="Создание субтитров...", fg="blue")
            output = generate_subtitles(self.subtitle_input.get(), format="srt", model_size=self.model_var.get() or "base")
            self.subtitle_status.config(text=f"Готово: {output}", fg="green")
        except Exception as exc:  # noqa: BLE001
            self.subtitle_status.config(text="Ошибка", fg="red")
            messagebox.showerror("Ошибка", str(exc))

    def _start_summary(self) -> None:
        if not self.summary_input.get():
            messagebox.showwarning("Ошибка", "Выберите файл")
            return
        threading.Thread(target=self._run_summary, daemon=True).start()

    def _run_summary(self) -> None:
        try:
            source = Path(self.summary_input.get())
            target = source.with_suffix(".summary.txt")
            summarise_to_file(source, target)
            self.summary_status.config(text=f"Конспект сохранен: {target}", fg="green")
        except Exception as exc:  # noqa: BLE001
            self.summary_status.config(text="Ошибка", fg="red")
            messagebox.showerror("Ошибка", str(exc))

    def _start_analysis(self) -> None:
        if not self.analysis_input.get():
            messagebox.showwarning("Ошибка", "Выберите файл")
            return
        threading.Thread(target=self._run_analysis, daemon=True).start()

    def _run_analysis(self) -> None:
        try:
            stats = analyse_file(self.analysis_input.get())
            report = render_report(stats)
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, report)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Ошибка", str(exc))


def main() -> None:
    MegaApp().mainloop()


if __name__ == "__main__":
    main()
