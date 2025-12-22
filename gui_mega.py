"""
Полная версия интерфейса VOICEBOX. Для текущего обновления использует
тот же базовый функционал, что и Desktop, чтобы гарантировать работоспособность.
"""
from __future__ import annotations

from gui_desktop import main as desktop_main


def main():
    desktop_main()


if __name__ == "__main__":
    main()
