# VOICEBOX API

## transcriber.Transcriber
- `transcribe(path, language=None, task=None, temperature=None, beam_size=None, best_of=None)` → raw Whisper результат.
- `save_output(result, output, format="txt")` → сохраняет в TXT/JSON/SRT/VTT/TSV.
- `batch_transcribe(paths, output_dir)` → список путей сохраненных файлов.

## subtitle_generator.generate_subtitles
- Генерирует субтитры в формате SRT/VTT для аудио/видео.

## video_processor
- `extract_audio(video_path, output_path=None)` → извлекает WAV дорожку.
- `add_subtitles(video_path, subtitles_path, output_path=None)` → прожигает субтитры в видео.

## summarizer
- `build_summary(text, sentence_limit=5)` → краткий конспект.
- `summarise_to_file(source, target, sentence_limit=5)` → сохраняет конспект.

## audio_analyzer
- `analyse_text(text)` → базовая статистика (слова, символы, предложения, топ-слова).
- `render_report(stats)` → человекочитаемый отчет.
