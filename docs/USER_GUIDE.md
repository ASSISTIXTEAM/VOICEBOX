# VOICEBOX Руководство пользователя

## Базовый сценарий
1. Установите зависимости: `pip install -r requirements.txt`.
2. Запустите лаунчер: `python launcher_gui.py`.
3. Нажмите «Запустить VOICEBOX» и выберите нужный интерфейс.

## GUI Desktop
- Файл: `gui_desktop.py`
- Подходит для быстрой транскрибации одного файла.
- Выберите аудио/видео, при необходимости укажите язык и модель, нажмите «Начать».

## GUI MEGA
- Файл: `gui_mega.py`
- Вкладки: транскрибация, субтитры, конспекты и анализ текста.
- Использует `Transcriber`, `subtitle_generator`, `summarizer` и `audio_analyzer`.

## Веб-интерфейс
- Файл: `gui_web.py`
- Команда запуска: `python gui_web.py`
- Откроется Gradio UI в браузере.

## CLI
- Файл: `main.py`
- Пример: `python main.py sample.wav --model small --language ru --output-format srt`

## Пакетная обработка
- Используйте `Transcriber.batch_transcribe` в своих скриптах или смотрите пример `examples/batch_processing.py`.
