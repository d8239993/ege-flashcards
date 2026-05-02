# Карточки (статический сайт)

Просмотр карточек в браузере. Разделы — папки `Задание №…`, внутри пары картинок: нечётный номер — вопрос, следующий чётный — ответ.

## Готовый репозиторий на диске

Проект собран в **`C:\Users\82399\Documents\vk-cards-flashcards`**: `git` инициализирован, ветка `main`, первый коммит с картинками и GitHub Actions.

**Осталось только привязать GitHub (нужен ваш логин в браузере):**

1. Откройте папку в Проводнике и запустите **`publish_to_github.ps1`** (если PowerShell ругается на политику: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` один раз).
2. Войдите в аккаунт в открывшемся браузере, если скрипт попросит.
3. На GitHub: **Settings → Pages → Source: GitHub Actions**. После зелёного workflow сайт: `https://<ваш-логин>.github.io/vk-cards-flashcards/`.

Альтернатива без скрипта: в папке проекта выполнить `gh auth login`, затем `gh repo create vk-cards-flashcards --public --source . --remote origin --push`.

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
