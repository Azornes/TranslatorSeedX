@echo off
echo ========================================
echo Seed-X Translation GUI - Installation
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists, removing old one...
    rmdir /s /q venv 2>nul
    timeout /t 2 /nobreak >nul
)
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip

echo.
echo Installing required packages...
venv\Scripts\python.exe -m pip install -r requirements.txt --no-cache-dir
if errorlevel 1 (
    echo WARNING: Batch installation failed, trying individual packages...
    venv\Scripts\python.exe -m pip install PyQt6 --no-cache-dir
    venv\Scripts\python.exe -m pip install llama-cpp-python --no-cache-dir
)

echo.
echo Creating models directory...
if not exist "models" mkdir models

echo.
echo Verifying installation...
venv\Scripts\python.exe -c "import PyQt6; print('PyQt6 installed successfully')"
if errorlevel 1 (
    echo ERROR: PyQt6 installation failed!
    pause
    exit /b 1
)

venv\Scripts\python.exe -c "import llama_cpp; print('llama-cpp-python installed successfully')"
if errorlevel 1 (
    echo ERROR: llama-cpp-python installation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo To run the application:
echo   - Double-click run.bat
echo   OR
echo   - Run: venv\Scripts\activate && python translator_app.py
echo.
echo IMPORTANT: Download a GGUF model from:
echo https://huggingface.co/Mungert/Seed-X-PPO-7B-GGUF
echo And place it in the models/ directory
echo.
pause
