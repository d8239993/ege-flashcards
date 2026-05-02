#!/usr/bin/env python3
"""Собирает папку _site для GitHub Pages (только статика, без скриптов и служебных каталогов)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "_site"

SKIP_NAMES = {
    "_site",
    "_rename_stage",
    "node_modules",
    ".git",
    ".github",
}
ROOT_FILES = ("index.html", "styles.css", "app.js", "manifest.json")


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    for name in ROOT_FILES:
        src = ROOT / name
        if not src.is_file():
            print(f"Нет файла: {src}", file=sys.stderr)
            sys.exit(1)
        shutil.copy2(src, SITE / name)

    for p in ROOT.iterdir():
        if not p.is_dir():
            continue
        if p.name.startswith(".") or p.name in SKIP_NAMES:
            continue
        shutil.copytree(p, SITE / p.name)

    (SITE / ".nojekyll").touch()

    print(f"OK: собрано в {SITE}", file=sys.stderr)


if __name__ == "__main__":
    main()
