#!/usr/bin/env python3
"""Переименование папок КАРТОЧКИ... → Задание №N (Тема)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Точное соответствие старых имён (из manifest) → новое имя папки
RENAME_MAP: dict[str, str] = {
    "КАРТОЧКИ ПО ЗАДАНИЮ 1 (планиметрия)": "Задание №1 (Планиметрия)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 2 (векторы)": "Задание №2 (Векторы)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 3 (стереометрия)": "Задание №3 (Стереометрия)",
    "КАРТОЧКИ ПО ЗАДАНИЯМ 4 И 5 (теория вероятностей)": "Задание №4-5 (Теория вероятностей)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 6 (уравнения)": "Задание №6 (Уравнения)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 7 (выражения)": "Задание №7 (Выражения)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 8 (графики производных)": "Задание №8 (Графики производных)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 9 (подстановка)": "Задание №9 (Подстановка)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 10 (текстовые задачи)": "Задание №10 (Текстовые задачи)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 11 (графики)": "Задание №11 (Графики)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 12 (производные)": "Задание №12 (Производные)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 13 (уравнения второй части)": "Задание №13 (Уравнения второй части)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 14 (стереометрия второй части)": "Задание №14 (Стереометрия второй части)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 15 (неравенства второй части)": "Задание №15 (Неравенства второй части)",
    "КАРТОЧКИ ПО ЗАДАНИЮ 17 (планиметрия второй части)": "Задание №17 (Планиметрия второй части)",
}


def main() -> None:
    todo: list[tuple[Path, str]] = []
    for old_name, new_name in RENAME_MAP.items():
        src = ROOT / old_name
        if not src.is_dir():
            continue
        dst = ROOT / new_name
        if src.resolve() == dst.resolve():
            continue
        if dst.exists():
            print(f"SKIP: цель уже есть: {new_name}", file=sys.stderr)
            continue
        todo.append((src, new_name))

    # В два шага — на случай частичного пересечения имён
    stage = ROOT / "_rename_stage"
    stage.mkdir(exist_ok=True)
    staged: list[tuple[Path, Path]] = []
    for i, (src, new_name) in enumerate(todo):
        mid = stage / f"_{i}"
        src.rename(mid)
        staged.append((mid, ROOT / new_name))

    for mid, final in staged:
        mid.rename(final)

    try:
        stage.rmdir()
    except OSError:
        pass

    print(f"Переименовано папок: {len(staged)}", file=sys.stderr)


if __name__ == "__main__":
    main()
