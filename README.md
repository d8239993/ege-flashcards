# Карточки (статический сайт)

Просмотр карточек в браузере. Разделы — папки `Задание №…`, внутри пары картинок: нечётный номер — вопрос, следующий чётный — ответ.

## Репозиторий и сайт

- **GitHub:** [d8239993/ege-flashcards](https://github.com/d8239993/ege-flashcards)
- **Сайт (GitHub Pages):** https://d8239993.github.io/ege-flashcards/

Локальная копия: **`C:\Users\82399\Documents\vk-cards-flashcards`**, ветка `main`. После `git push` workflow пересобирает `manifest.json` и публикует `_site`.

## Публикация на GitHub Pages (вручную)

1. Создайте репозиторий на GitHub и загрузите **содержимое этой папки** (вместе с папками `Задание №…` и картинками).
2. В репозитории: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Закоммитьте и запушьте в ветку `main` (или `master`). Workflow «Deploy GitHub Pages» соберёт `manifest.json` и опубликует сайт.
4. Через минуту откройте адрес вида `https://<user>.github.io/<repo>/`.

Локально без Git: дважды `start_server.bat` или `python build_manifest.py` и `python -m http.server 8765`.

### Ограничения GitHub

- Репозиторий не должен быть слишком тяжёлым (десятки тысяч больших файлов лучше хранить иначе или использовать [Git LFS](https://git-lfs.github.com/)).
- Один файл не больше **100 MB**.

После добавления или переименования картинок достаточно снова запушить — при деплое `manifest.json` пересоздаётся автоматически.
