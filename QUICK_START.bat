@echo off
chcp 65001 >nul
REM ═══════════════════════════════════════════════════════════════════
REM
REM   VOICEBOX - Быстрый старт
REM
REM   Этот скрипт автоматически:
REM   1. Проверяет Python
REM   2. Создает виртуальное окружение
REM   3. Устанавливает все зависимости
REM   4. Запускает лаунчер
REM
REM   Использование:
REM     Просто запустите двойным кликом
REM
REM ═══════════════════════════════════════════════════════════════════

title VOICEBOX - Быстрый старт

color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║                     VOICEBOX MEGA                                ║
echo ║              Быстрый старт и установка                           ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo.

REM ───────────────────────────────────────────────────────────────────
REM Проверка Python
REM ───────────────────────────────────────────────────────────────────

echo [1/4] Проверка Python...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python не найден!
    echo.
    echo Установите Python:
    echo   1. Перейдите на https://python.org
    echo   2. Скачайте Python 3.8 или новее
    echo   3. При установке отметьте "Add Python to PATH"
    echo   4. Запустите этот файл снова
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python установлен
echo.
pause

REM ───────────────────────────────────────────────────────────────────
REM Создание виртуального окружения
REM ───────────────────────────────────────────────────────────────────

echo [2/4] Создание виртуального окружения...
echo.

if exist venv (
    echo Виртуальное окружение уже существует
) else (
    echo Создание venv...
    python -m venv venv
    if errorlevel 1 (
        color 0C
        echo [ERROR] Не удалось создать виртуальное окружение
        pause
        exit /b 1
    )
    echo [OK] Виртуальное окружение создано
)

echo.
echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo [OK] Виртуальное окружение активировано
echo.
pause

REM ───────────────────────────────────────────────────────────────────
REM Установка зависимостей
REM ───────────────────────────────────────────────────────────────────

echo [3/4] Установка зависимостей...
echo.
echo [!] Это может занять 5-15 минут
echo [!] НЕ ЗАКРЫВАЙТЕ ЭТО ОКНО!
echo.
pause

REM Обновление pip
echo Обновление pip...
python -m pip install --upgrade pip --quiet

REM Установка из requirements.txt
echo.
echo Установка зависимостей из requirements.txt...
echo (прогресс отображается ниже)
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    color 0E
    echo.
    echo [WARNING] Некоторые пакеты не установились
    echo Попробуем продолжить...
    echo.
) else (
    echo.
    echo [OK] Все зависимости установлены
    echo.
)

pause

REM ───────────────────────────────────────────────────────────────────
REM Запуск лаунчера
REM ───────────────────────────────────────────────────────────────────

echo [4/4] Запуск VOICEBOX...
echo.

if exist launcher_gui.py (
    echo Запуск GUI лаунчера...
    python launcher_gui.py
) else (
    color 0C
    echo [ERROR] Файл launcher_gui.py не найден!
    echo.
    echo Убедитесь что все файлы находятся в папке:
    echo   - launcher_gui.py
    echo   - gui_mega.py
    echo   - transcriber.py
    echo   - и другие...
    echo.
    pause
    exit /b 1
)

REM ───────────────────────────────────────────────────────────────────
REM Завершение
REM ───────────────────────────────────────────────────────────────────

echo.
echo.
echo ══════════════════════════════════════════════════════════════════
echo.
echo VOICEBOX закрыт.
echo.
echo Для следующего запуска:
echo   - Запустите QUICK_START.bat снова
echo   - Или: venv\Scripts\activate.bat и python launcher_gui.py
echo.
echo ══════════════════════════════════════════════════════════════════
echo.
pause
