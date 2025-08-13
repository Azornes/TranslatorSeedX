# Seed-X Translation GUI - PowerShell Installation Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Seed-X Translation GUI - Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Remove existing virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, removing old one..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "venv" -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

# Create new virtual environment
try {
    python -m venv venv
    Write-Host "Virtual environment created successfully!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to create virtual environment!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
try {
    & "venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
    Write-Host "Pip upgraded successfully!" -ForegroundColor Green
} catch {
    Write-Host "Warning: Failed to upgrade pip, continuing..." -ForegroundColor Yellow
}

# Install packages
Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
Write-Host "This may take several minutes, please wait..." -ForegroundColor Yellow

try {
    & "venv\Scripts\python.exe" -m pip install -r requirements.txt --no-cache-dir
    Write-Host "All packages installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to install packages!" -ForegroundColor Red
    Write-Host "Trying individual installation..." -ForegroundColor Yellow
    
    # Fallback to individual installation
    Write-Host "Installing PyQt6..." -ForegroundColor Cyan
    try {
        & "venv\Scripts\python.exe" -m pip install PyQt6 --no-cache-dir
        Write-Host "PyQt6 installed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to install PyQt6!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }

    Write-Host "Installing llama-cpp-python..." -ForegroundColor Cyan
    Write-Host "This will take longer as it needs to compile..." -ForegroundColor Yellow
    try {
        & "venv\Scripts\python.exe" -m pip install llama-cpp-python --no-cache-dir
        Write-Host "llama-cpp-python installed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to install llama-cpp-python!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Create models directory
Write-Host ""
Write-Host "Creating models directory..." -ForegroundColor Yellow
if (!(Test-Path "models")) {
    New-Item -ItemType Directory -Name "models" | Out-Null
    Write-Host "Models directory created!" -ForegroundColor Green
} else {
    Write-Host "Models directory already exists!" -ForegroundColor Green
}

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow

try {
    & "venv\Scripts\python.exe" -c "import PyQt6; print('PyQt6 verification successful')"
    Write-Host "PyQt6 verification: OK" -ForegroundColor Green
} catch {
    Write-Host "ERROR: PyQt6 verification failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    & "venv\Scripts\python.exe" -c "import llama_cpp; print('llama-cpp-python verification successful')"
    Write-Host "llama-cpp-python verification: OK" -ForegroundColor Green
} catch {
    Write-Host "ERROR: llama-cpp-python verification failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "  - Double-click run.bat" -ForegroundColor White
Write-Host "  OR" -ForegroundColor White
Write-Host "  - Run: .\run.bat" -ForegroundColor White
Write-Host "  OR" -ForegroundColor White
Write-Host "  - Run: venv\Scripts\activate; python translator_app.py" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANT: Download a GGUF model from:" -ForegroundColor Yellow
Write-Host "https://huggingface.co/Mungert/Seed-X-PPO-7B-GGUF" -ForegroundColor Cyan
Write-Host "And place it in the models/ directory" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue"
