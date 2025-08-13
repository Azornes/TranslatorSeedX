# Seed-X Translation GUI

Professional Python GUI application for using the Seed-X-PPO-7B translation model.

## Features

- Support for translations between 28 languages
- Modern GUI interface with PyQt6
- Multi-threaded model loading and translation (non-blocking UI)
- Chain-of-Thought (CoT) mode with detailed explanations
- Adjustable generation parameters (temperature, top-p, top-k, etc.)
- Translation history with export/import functionality
- Dockable panels for settings and history
- Persistent application settings
- Keyboard shortcuts for frequent actions
- Automatic model downloading from Hugging Face
- GPU (CUDA) support for fast translations

## Backends

The application supports two backends:

1. **GGUF (llama.cpp)** - Recommended for most users
   - Uses quantized GGUF models
   - Lower memory usage
   - Good performance on CPU and GPU
   - Works on Windows

2. **Transformers** - For original models
   - Uses full precision models
   - Higher memory usage
   - Best quality
   - Works on Windows with CUDA

## Requirements

- Python 3.8+
- GPU with CUDA support (recommended) or CPU (slower)
- At least 8GB RAM (16GB recommended)
- About 5GB disk space for Q4_K_M model

## Installation

### Option 1: Automatic Installation (Recommended)

**For Windows Command Prompt:**
```cmd
install.bat
```

**For PowerShell:**
```powershell
.\install.ps1
```

### Option 2: Manual Installation

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
```cmd
run.bat
```

### Manual Start
```bash
# First activate virtual environment
venv\Scripts\activate

# Run application
python main.py
```

## Model Download

The application will automatically detect and load available models. If you don't have any models:

1. Run the application
2. Click "Download Model"
3. Select a model (recommended: Q4_K_M - 4.6GB)
4. Wait for download to complete
5. Model will be automatically loaded

### Available GGUF Models:

- **Q4_K_M (4.6GB)** - Recommended balance of quality/speed
- **Q5_K_M (5.4GB)** - Better quality, slower
- **Q8_0 (8.0GB)** - Best quality, requires more RAM

### Original Model (for Transformers):

- **Original Seed-X-PPO-7B (15GB)** - Full precision, requires more VRAM

## Supported Languages

- Arabic (ar), Czech (cs), Danish (da), German (de)
- English (en), Spanish (es), Finnish (fi), French (fr)
- Croatian (hr), Hungarian (hu), Indonesian (id), Italian (it)
- Japanese (ja), Korean (ko), Malay (ms), Norwegian Bokmål (nb)
- Dutch (nl), Norwegian (no), Polish (pl), Portuguese (pt)
- Romanian (ro), Russian (ru), Swedish (sv), Thai (th)
- Turkish (tr), Ukrainian (uk), Vietnamese (vi), Chinese (zh)

## Project Structure

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
    └── README.md               # Model information
```

## Troubleshooting

### Model Won't Load
- Check if you have enough RAM/VRAM
- Try a smaller model (Q4_K_M instead of Q8_0)
- Check console logs for error details
- For Transformers models: ensure CUDA is installed

### Slow Translation
- Use GPU instead of CPU (check if CUDA is available)
- Reduce "Max Tokens" parameter in settings
- Use a smaller model
- Switch to Transformers backend for better GPU performance

### CUDA Errors
- Ensure you have PyTorch with CUDA support installed
- Check if GPU drivers are up to date
- Try reinstalling PyTorch: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/Azornes/TranslatorSeedX/wiki/Contributing) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The Seed-X-PPO-7B model is licensed under OpenMDW.

## Acknowledgments

- [ByteDance Seed Team](https://github.com/ByteDance/Seed) for the Seed-X-PPO-7B model
- [Mungert](https://huggingface.co/Mungert) for GGUF quantization on Hugging Face
- [llama.cpp](https://github.com/ggerganov/llama.cpp) for GGUF support
- [Hugging Face](https://huggingface.co/) for model hosting

## Support

- 🐛 [Report a Bug](https://github.com/Azornes/TranslatorSeedX/issues/new?template=bug_report.md)
- 💡 [Request a Feature](https://github.com/Azornes/TranslatorSeedX/issues/new?template=feature_request.md)
- 💬 [Discussions](https://github.com/Azornes/TranslatorSeedX/discussions)
