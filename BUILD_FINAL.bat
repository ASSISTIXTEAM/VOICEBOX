@echo off
chcp 65001 >nul
REM ═══════════════════════════════════════════════════════════════════
REM
REM   VOICEBOX - Скрипт сборки EXE
REM
REM   Этот скрипт автоматически собирает VOICEBOX в standalone EXE
REM   со всеми необходимыми зависимостями
REM
REM   Что делает скрипт:
REM   1. Проверяет наличие Python
REM   2. Устанавливает PyInstaller
REM   3. Очищает предыдущие сборки
REM   4. Собирает EXE в папку dist/VOICEBOX/
REM   5. Открывает папку с результатом
REM
REM   Использование:
REM     Просто запустите этот файл двойным кликом
REM
REM   Автор: VOICEBOX Team
REM   Лицензия: MIT
REM
REM ═══════════════════════════════════════════════════════════════════

title VOICEBOX - Финальная сборка

echo.
echo ═══════════════════════════════════════════════════════════════════
echo                   VOICEBOX - Финальная сборка EXE
echo ═══════════════════════════════════════════════════════════════════
echo.

REM ───────────────────────────────────────────────────────────────────
REM ШАГ 1: Проверка Python
REM ───────────────────────────────────────────────────────────────────

echo [ШАГ 1/4] Проверка Python...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python не найден!
    echo.
    echo Установите Python с https://python.org
    echo При установке отметьте "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Показываем версию Python
python --version
echo [OK] Python найден
echo.

REM ───────────────────────────────────────────────────────────────────
REM ШАГ 2: Установка PyInstaller
REM ───────────────────────────────────────────────────────────────────

echo [ШАГ 2/4] Установка PyInstaller...
echo.

python -m pip install pyinstaller --upgrade --quiet
if errorlevel 1 (
    color 0E
    echo [WARNING] Не удалось обновить PyInstaller
    echo Продолжаем с текущей версией...
    echo.
) else (
    echo [OK] PyInstaller готов
    echo.
)

REM ───────────────────────────────────────────────────────────────────
REM ШАГ 3: Очистка предыдущих сборок
REM ───────────────────────────────────────────────────────────────────

echo [ШАГ 3/4] Очистка предыдущих сборок...
echo.

REM Удаление старых папок если существуют
if exist build (
    echo Удаление папки build...
    rmdir /s /q build
)

if exist dist (
    echo Удаление папки dist...
    rmdir /s /q dist
)

REM Удаление старого spec файла
if exist VOICEBOX.spec (
    echo Удаление VOICEBOX.spec...
    del /q VOICEBOX.spec
)

echo [OK] Очищено
echo.

REM ───────────────────────────────────────────────────────────────────
REM ШАГ 4: Сборка EXE
REM ───────────────────────────────────────────────────────────────────

echo [ШАГ 4/4] Сборка EXE (это займет 3-5 минут)...
echo.
echo [!] НЕ ЗАКРЫВАЙТЕ ЭТО ОКНО!
echo [!] Процесс может показаться "зависшим" - это нормально
echo.
echo Начало сборки...
echo.

REM ═══════════════════════════════════════════════════════════════════
REM КОМАНДА PYINSTALLER
REM
REM Параметры:
REM   --name=VOICEBOX          - Имя исполняемого файла
REM   --windowed               - Без консольного окна
REM   --onedir                 - Сборка в папку (НЕ один файл!)
REM   --noconfirm              - Без подтверждений
REM   --clean                  - Очистка кеша
REM
REM   --add-data               - Включение Python модулей
REM                              Формат: "source;destination"
REM
REM   --hidden-import          - Явный импорт скрытых зависимостей
REM                              PyInstaller может не найти автоматически
REM
REM   --collect-all            - Сбор всех файлов пакета
REM                              Особенно важно для customtkinter
REM
REM   launcher_gui.py          - Главный файл программы
REM ═══════════════════════════════════════════════════════════════════

pyinstaller ^
    --name=VOICEBOX ^
    --windowed ^
    --onedir ^
    --noconfirm ^
    --clean ^
    --add-data="gui_mega.py;." ^
    --add-data="gui_desktop.py;." ^
    --add-data="gui_web.py;." ^
    --add-data="transcriber.py;." ^
    --add-data="video_processor.py;." ^
    --add-data="subtitle_generator.py;." ^
    --add-data="summarizer.py;." ^
    --add-data="audio_analyzer.py;." ^
    --add-data="config.py;." ^
    --add-data="utils.py;." ^
    --hidden-import=whisper ^
    --hidden-import=torch ^
    --hidden-import=customtkinter ^
    --hidden-import=gradio ^
    --hidden-import=PIL ^
    --hidden-import=numpy ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.scrolledtext ^
    --collect-all=customtkinter ^
    launcher_gui.py

REM ───────────────────────────────────────────────────────────────────
REM Проверка результата
REM ───────────────────────────────────────────────────────────────────

if errorlevel 1 (
    echo.
    color 0C
    echo ═══════════════════════════════════════════════════════════════════
    echo                        ОШИБКА СБОРКИ!
    echo ═══════════════════════════════════════════════════════════════════
    echo.
    echo Возможные причины:
    echo   1. Не все Python файлы скопированы
    echo   2. Недостаточно места на диске
    echo   3. Антивирус блокирует PyInstaller
    echo.
    echo Решения:
    echo   1. Проверьте наличие всех .py файлов в папке
    echo   2. Освободите место на диске (нужно ~5GB)
    echo   3. Временно отключите антивирус
    echo.
    pause
    exit /b 1
)

REM ───────────────────────────────────────────────────────────────────
REM УСПЕХ!
REM ───────────────────────────────────────────────────────────────────

color 0A
echo.
echo ═══════════════════════════════════════════════════════════════════
echo                      СБОРКА ЗАВЕРШЕНА УСПЕШНО!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Готовая программа находится в:
echo    📁 dist\VOICEBOX\
echo.
echo Главный файл:
echo    🚀 dist\VOICEBOX\VOICEBOX.exe
echo.
echo ═══════════════════════════════════════════════════════════════════
echo                    ЧТО ДЕЛАТЬ ДАЛЬШЕ:
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 1. Скопируйте ВСЮ ПАПКУ "dist\VOICEBOX"
echo    (не только VOICEBOX.exe, а всю папку!)
echo.
echo 2. Запакуйте папку в ZIP архив:
echo    Правый клик → Отправить → Сжатая папка (ZIP)
echo.
echo 3. Передайте пользователям ZIP файл
echo.
echo 4. Пользователь должен:
echo    - Распаковать ZIP
echo    - Запустить VOICEBOX.exe
echo    - Нажать "Установить зависимости"
echo    - Нажать "Запустить VOICEBOX"
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Размер папки: 
dir dist\VOICEBOX /s | find "байт"
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

pause

REM Открыть папку с результатом
explorer dist\VOICEBOX

echo.
echo Готово! Окно можно закрыть.
echo.
