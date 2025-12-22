#!/usr/bin/env bash
set -e

echo "[VOICEBOX] Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[VOICEBOX] Запуск лаунчера"
python launcher_gui.py
