# 📦 Установка VOICEBOX

Подробное руководство по установке VOICEBOX на различных платформах.

---

## 📋 Содержание

- [Требования](#требования)
- [Windows](#windows)
- [Linux](#linux)
- [macOS](#macos)
- [Docker](#docker)
- [Проверка установки](#проверка-установки)
- [Решение проблем](#решение-проблем)

---

## Требования

### Минимальные

- **Python:** 3.8 или выше
- **RAM:** 4 GB
- **Диск:** 5 GB свободного места
- **Интернет:** для установки зависимостей

### Рекомендуемые

- **Python:** 3.10 или выше
- **RAM:** 8+ GB
- **GPU:** NVIDIA с CUDA support
- **Диск:** 10+ GB

---

## Windows

### Способ 1: Готовый EXE (Рекомендуется)

Самый простой способ для пользователей.

1. **Скачайте релиз**
   ```
   Перейдите на: https://github.com/yourusername/voicebox/releases
   Скачайте: VOICEBOX-windows-x64.zip
   ```

2. **Распакуйте архив**
   ```
   Правый клик на ZIP → Извлечь всё
   ```

3. **Запустите VOICEBOX.exe**
   ```
   Двойной клик на VOICEBOX.exe
   ```

4. **Установите зависимости**
   ```
   В открывшемся окне нажмите "Установить зависимости"
   Дождитесь завершения (5-15 минут)
   ```

5. **Запустите программу**
   ```
   Нажмите "Запустить VOICEBOX"
   ```

**Готово! 🎉**

---

### Способ 2: Из исходного кода

Для разработчиков и опытных пользователей.

#### Шаг 1: Установка Python

1. Перейдите на https://python.org
2. Скачайте Python 3.10 или новее
3. **Важно:** При установке отметьте ☑ "Add Python to PATH"
4. Установите Python

**Проверка:**
```cmd
python --version
```
Должно вывести: `Python 3.10.x`

---

#### Шаг 2: Установка Git (опционально)

Для клонирования репозитория:

1. Скачайте Git с https://git-scm.com
2. Установите с настройками по умолчанию

---

#### Шаг 3: Клонирование репозитория

**С Git:**
```cmd
git clone https://github.com/yourusername/voicebox.git
cd voicebox
```

**Без Git:**
1. Перейдите на https://github.com/yourusername/voicebox
2. Нажмите "Code" → "Download ZIP"
3. Распакуйте в удобное место
4. Откройте командную строку в этой папке

---

#### Шаг 4: Создание виртуального окружения

```cmd
# Создание venv
python -m venv venv

# Активация
venv\Scripts\activate

# В командной строке должно появиться (venv)
```

---

#### Шаг 5: Установка зависимостей

```cmd
# Обновление pip
python -m pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt
```

Это займет 5-15 минут в зависимости от скорости интернета.

---

#### Шаг 6: Установка FFmpeg (опционально)

Для обработки видео:

**Автоматически:**
```cmd
install_ffmpeg.bat
```

**Вручную:**
1. Скачайте FFmpeg: https://ffmpeg.org/download.html
2. Распакуйте в `C:\ffmpeg\`
3. Добавьте `C:\ffmpeg\bin` в PATH

**Проверка:**
```cmd
ffmpeg -version
```

---

#### Шаг 7: Запуск

```cmd
# Запуск лаунчера
python launcher_gui.py

# Или MEGA интерфейс напрямую
python gui_mega.py
```

---

### Способ 3: Быстрый старт (Автоматический)

Для максимальной простоты:

```cmd
# Просто запустите:
QUICK_START.bat
```

Скрипт автоматически:
- ✅ Проверит Python
- ✅ Создаст venv
- ✅ Установит зависимости
- ✅ Запустит программу

---

## Linux

### Ubuntu / Debian

#### Шаг 1: Установка системных зависимостей

```bash
# Обновление пакетов
sudo apt update

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv

# Установка FFmpeg
sudo apt install ffmpeg

# Установка зависимостей для PyTorch
sudo apt install libgomp1
```

---

#### Шаг 2: Клонирование репозитория

```bash
git clone https://github.com/yourusername/voicebox.git
cd voicebox
```

---

#### Шаг 3: Создание виртуального окружения

```bash
# Создание venv
python3 -m venv venv

# Активация
source venv/bin/activate
```

---

#### Шаг 4: Установка зависимостей

```bash
# Обновление pip
pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt
```

---

#### Шаг 5: Запуск

```bash
# Запуск лаунчера
python launcher_gui.py

# Или MEGA интерфейс
python gui_mega.py
```

---

### Arch Linux

```bash
# Установка зависимостей
sudo pacman -S python python-pip ffmpeg

# Клонирование и установка
git clone https://github.com/yourusername/voicebox.git
cd voicebox
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Запуск
python launcher_gui.py
```

---

### Fedora / CentOS / RHEL

```bash
# Установка зависимостей
sudo dnf install python3 python3-pip ffmpeg

# Или для CentOS:
# sudo yum install python3 python3-pip ffmpeg

# Клонирование и установка
git clone https://github.com/yourusername/voicebox.git
cd voicebox
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Запуск
python launcher_gui.py
```

---

## macOS

### Шаг 1: Установка Homebrew

Если еще не установлен:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### Шаг 2: Установка зависимостей

```bash
# Python и FFmpeg
brew install python@3.10 ffmpeg

# Git (если нужен)
brew install git
```

---

### Шаг 3: Клонирование репозитория

```bash
git clone https://github.com/yourusername/voicebox.git
cd voicebox
```

---

### Шаг 4: Создание виртуального окружения

```bash
# Создание venv
python3 -m venv venv

# Активация
source venv/bin/activate
```

---

### Шаг 5: Установка зависимостей

```bash
# Обновление pip
pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt
```

---

### Шаг 6: Запуск

```bash
# Запуск лаунчера
python launcher_gui.py

# Или MEGA интерфейс
python gui_mega.py
```

---

## Docker

Для изолированной установки.

### Использование готового образа

```bash
# Pull образа
docker pull voicebox/voicebox:latest

# Запуск
docker run -it --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  voicebox/voicebox:latest
```

---

### Сборка из исходного кода

```bash
# Клонирование
git clone https://github.com/yourusername/voicebox.git
cd voicebox

# Сборка образа
docker build -t voicebox .

# Запуск
docker run -it --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  voicebox
```

---

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  voicebox:
    image: voicebox/voicebox:latest
    volumes:
      - ./input:/app/input
      - ./output:/app/output
    environment:
      - WHISPER_MODEL=medium
      - DEVICE=cuda
```

```bash
# Запуск
docker-compose up
```

---

## Проверка установки

### Проверка Python

```bash
python --version
# Должно быть: Python 3.8.x или выше
```

### Проверка pip

```bash
pip --version
# Должно показать версию pip
```

### Проверка Whisper

```python
python -c "import whisper; print(whisper.__version__)"
# Должно показать версию
```

### Проверка PyTorch

```python
python -c "import torch; print(torch.__version__)"
# Должно показать версию
```

### Проверка CUDA (для GPU)

```python
python -c "import torch; print(torch.cuda.is_available())"
# True - если GPU доступна
# False - если только CPU
```

### Проверка FFmpeg

```bash
ffmpeg -version
# Должно показать версию FFmpeg
```

---

## Решение проблем

### Python не найден

**Проблема:** `'python' is not recognized as an internal or external command`

**Решение:**
1. Переустановите Python
2. Отметьте "Add Python to PATH"
3. Или используйте `python3` вместо `python`

---

### pip не найден

**Проблема:** `No module named pip`

**Решение:**
```bash
# Windows
python -m ensurepip --upgrade

# Linux/macOS
python3 -m ensurepip --upgrade
```

---

### Ошибка установки openai-whisper

**Проблема:** Конфликт с пакетом `whisper`

**Решение:**
```bash
# Удалить конфликтный пакет
pip uninstall whisper -y

# Установить правильный
pip install openai-whisper
```

---

### Ошибка установки PyTorch

**Проблема:** Timeout или ошибка загрузки

**Решение:**
```bash
# Установить отдельно с увеличенным timeout
pip install torch torchvision torchaudio --timeout 300
```

**Для GPU (CUDA 11.8):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

### GUI не запускается

**Проблема:** Ошибка при импорте customtkinter

**Решение:**
```bash
# Переустановить customtkinter
pip uninstall customtkinter -y
pip install customtkinter --no-cache-dir
```

---

### FFmpeg не найден

**Проблема:** `ffmpeg not found`

**Решение:**

**Windows:**
- Используйте `install_ffmpeg.bat`
- Или скачайте вручную и добавьте в PATH

**Linux:**
```bash
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

---

### Недостаточно памяти

**Проблема:** `Out of memory` при обработке

**Решение:**
- Используйте меньшую модель (tiny, base, small)
- Закройте другие программы
- Используйте CPU вместо GPU

---

### Медленная обработка

**Проблема:** Транскрибация занимает много времени

**Решение:**
- Используйте GPU (CUDA)
- Выберите меньшую модель
- Проверьте что CUDA работает: `torch.cuda.is_available()`

---

## Обновление

### Обновление из репозитория

```bash
# Получить последние изменения
git pull origin main

# Обновить зависимости
pip install -r requirements.txt --upgrade
```

### Обновление конкретного пакета

```bash
# Обновление Whisper
pip install openai-whisper --upgrade

# Обновление всех пакетов
pip install -r requirements.txt --upgrade
```

---

## Удаление

### Полное удаление

**Windows:**
```cmd
# Деактивировать venv если активирован
deactivate

# Удалить папку
rmdir /s /q voicebox
```

**Linux/macOS:**
```bash
# Деактивировать venv
deactivate

# Удалить папку
rm -rf voicebox
```

---

## Следующие шаги

После установки:

1. 📖 Прочитайте [USER_GUIDE.md](USER_GUIDE.md)
2. 🎯 Попробуйте [примеры](../examples/)
3. ⚙️ Настройте [config.py](../config.py)
4. 🚀 Начните использовать VOICEBOX!

---

**Нужна помощь?** 

- 📝 [FAQ](FAQ.md)
- 💬 [GitHub Discussions](https://github.com/yourusername/voicebox/discussions)
- 🐛 [Issues](https://github.com/yourusername/voicebox/issues)
