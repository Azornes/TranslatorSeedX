@echo off
echo Starting Seed-X Translation GUI...
echo.

if exist "venv\Scripts\activate" (
    call venv\Scripts\activate
    python main.py
) else (
    echo Virtual environment not found!
    echo Please run install.bat first.
    pause
)
