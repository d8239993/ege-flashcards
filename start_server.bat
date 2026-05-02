@echo off
chcp 65001 >nul
cd /d "%~dp0"
python build_manifest.py
echo.
echo Откройте в браузере: http://127.0.0.1:8765/
echo Остановка: Ctrl+C
python -m http.server 8765
