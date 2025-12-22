#!/usr/bin/env bash
set -e

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "[VOICEBOX] Устанавливаю PyInstaller..."
  pip install pyinstaller
fi

rm -rf build dist

echo "[VOICEBOX] Сборка VOICEBOX..."
pyinstaller \
  --name=VOICEBOX \
  --windowed \
  --onedir \
  --add-data="gui_mega.py;." \
  --add-data="transcriber.py;." \
  --hidden-import=whisper \
  --hidden-import=torch \
  --collect-all=customtkinter \
  launcher_gui.py

echo "[VOICEBOX] Готово! Исполняемый файл лежит в dist/VOICEBOX/"
