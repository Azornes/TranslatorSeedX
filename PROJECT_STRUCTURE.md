# Seed-X Translation Application - Project Structure

## Overview
This project has been reorganized into a clean, modular structure that separates concerns and improves code maintainability.

## Directory Structure

```
TranslatorSeedX/
├── main.py                     # Main entry point
├── run.bat                     # Windows batch file to run the application
├── install.bat                 # Installation script
├── install.ps1                 # PowerShell installation script
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore file
│
├── src/                        # Source code directory
│   ├── __init__.py
│   │
│   ├── gui/                    # GUI components
│   │   ├── __init__.py
│   │   ├── translator_app.py   # Main application window
│   │   └── filterable_combobox.py  # Custom combo box widget
│   │
│   ├── backend/                # Backend logic
│   │   ├── __init__.py
│   │   ├── translation_backend.py      # Translation manager and threads
│   │   ├── model_handler.py            # GGUF model handler (llama.cpp)
│   │   └── model_handler_transformers.py  # Transformers model handler
│   │
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       ├── config.py           # Configuration settings
│       └── download_missing_files.py  # Model download utilities
│
└── models/                     # Model storage directory
    └── Seed-X-PPO-7B/         # Downloaded model files
```

## Architecture

### Separation of Concerns

1. **GUI Layer** (`src/gui/`)
   - Contains all PyQt6 user interface components
   - Main application window and custom widgets
   - Handles user interactions and display

2. **Backend Layer** (`src/backend/`)
   - Translation logic and model management
   - Threading for non-blocking operations
   - Model handlers for different backends (GGUF/Transformers)

3. **Utils Layer** (`src/utils/`)
   - Configuration management
   - Utility functions and helpers
   - Shared constants and settings

### Key Components

#### TranslationManager (`src/backend/translation_backend.py`)
- Central manager for all translation operations
- Handles model switching between backends
- Manages translation history
- Coordinates threading for non-blocking operations

#### Model Handlers
- **TranslationModel** (`src/backend/model_handler.py`): GGUF models via llama.cpp
- **TransformersTranslationModel** (`src/backend/model_handler_transformers.py`): HuggingFace models via Transformers

#### Threading
- **ModelLoadThread**: Non-blocking model loading
- **TranslationThread**: Non-blocking translation execution
- **ModelDownloadThread**: Non-blocking model downloads

## Benefits of New Structure

1. **Modularity**: Clear separation between GUI, backend, and utilities
2. **Maintainability**: Easier to locate and modify specific functionality
3. **Testability**: Components can be tested independently
4. **Scalability**: Easy to add new features or backends
5. **Code Reuse**: Backend components can be used without GUI

## Running the Application

### Method 1: Using the batch file (Windows)
```bash
run.bat
```

### Method 2: Direct Python execution
```bash
python main.py
```

### Method 3: From virtual environment
```bash
venv\Scripts\activate
python main.py
```

## Development

### Adding New Features

1. **GUI Features**: Add to `src/gui/`
2. **Backend Logic**: Add to `src/backend/`
3. **Configuration**: Modify `src/utils/config.py`

### Adding New Model Backends

1. Create new handler in `src/backend/`
2. Implement the same interface as existing handlers
3. Update `TranslationManager.switch_backend()` method

### Code Style

- Follow PEP 8 conventions
- Use type hints where appropriate
- Document classes and methods with docstrings
- Keep imports organized (standard library, third-party, local)

## Dependencies

The application uses relative imports with the `src` prefix to ensure proper module resolution across different execution contexts.

## Future Improvements

1. **Configuration Management**: Move more settings to config files
2. **Plugin System**: Allow dynamic loading of new model backends
3. **API Layer**: Expose translation functionality via REST API
4. **Testing**: Add comprehensive unit and integration tests
5. **Logging**: Implement structured logging throughout the application
