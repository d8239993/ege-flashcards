#!/usr/bin/env python3
"""Сканирует подпапки с изображениями и создаёт manifest.json для просмотрщика."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
SKIP_DIRS = {".git", "node_modules", "_rename_stage"}
SKIP_FILES = {"manifest.json", "index.html", "app.js", "styles.css", "build_manifest.py"}


def section_order_key(p: Path) -> tuple:
    """Порядок: Задание №1, №2, … №10, №4-5 после №3 и т.д. по числу задания."""
    m = re.search(r"№\s*(\d+)(?:-(\d+))?", p.name)
    if m:
        a = int(m.group(1))
        b = int(m.group(2)) if m.group(2) else a
        return (a, b, p.name.casefold())
    return (10**9, 10**9, p.name.casefold())


def num_key(name: str) -> tuple[int, str]:
    m = re.match(r"^(\d+)", Path(name).stem)
    if m:
        return (int(m.group(1)), name.lower())
    return (10**9, name.lower())


def main() -> None:
    root = Path(__file__).resolve().parent
    sections: list[dict] = []

    dirs = [
        d
        for d in root.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name not in SKIP_DIRS
    ]
    dirs.sort(key=section_order_key)

    for d in dirs:
        files = [
            f
            for f in d.iterdir()
            if f.is_file() and f.suffix.lower() in IMAGE_EXT
        ]
        files.sort(key=lambda f: num_key(f.name))
        pairs: list[dict] = []
        i = 0
        while i < len(files):
            q = f"{d.name}/{files[i].name}"
            if i + 1 < len(files):
                a = f"{d.name}/{files[i + 1].name}"
                pairs.append({"q": q, "a": a})
                i += 2
            else:
                pairs.append({"q": q, "a": None})
                i += 1
        sections.append({"title": d.name, "pairs": pairs})

    out = {"generated": True, "sections": sections}
    out_path = root / "manifest.json"
    out_path.write_text(
        json.dumps(out, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    n_pairs = sum(len(s["pairs"]) for s in sections)
    print(f"OK: {len(sections)} разделов, {n_pairs} карточек → {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
