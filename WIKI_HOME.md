# Seed-X Translation Application Wiki

Welcome to the Seed-X Translation Application wiki! This application provides a user-friendly PyQt6 interface for multilingual translation using the Seed-X-PPO-7B model.

## Quick Links

- [Installation Guide](https://github.com/Azornes/TranslatorSeedX/wiki/Installation)
- [User Guide](https://github.com/Azornes/TranslatorSeedX/wiki/User-Guide)
- [Developer Guide](https://github.com/Azornes/TranslatorSeedX/wiki/Developer-Guide)
- [Model Information](https://github.com/Azornes/TranslatorSeedX/wiki/Model-Information)
- [Troubleshooting](https://github.com/Azornes/TranslatorSeedX/wiki/Troubleshooting)
- [FAQ](https://github.com/Azornes/TranslatorSeedX/wiki/FAQ)

## Features

- 🌍 **28 Language Support**: Translate between Arabic, Czech, Danish, German, English, Spanish, Finnish, French, Croatian, Hungarian, Indonesian, Italian, Japanese, Korean, Malay, Norwegian, Dutch, Polish, Portuguese, Romanian, Russian, Swedish, Thai, Turkish, Ukrainian, Vietnamese, and Chinese
- 🚀 **Multiple Backends**: Support for both GGUF (llama.cpp) and Transformers
- 💾 **Auto-download Models**: Automatically download models from Hugging Face
- 📝 **Translation History**: Keep track of all your translations
- ⚙️ **Customizable Settings**: Adjust generation parameters for optimal results
- 🎨 **Modern UI**: Clean and intuitive PyQt6 interface
- 🔄 **Real-time Translation**: Non-blocking translation with progress indicators

## System Requirements

### Minimum Requirements
- Windows 10/11, Linux, or macOS
- Python 3.8 or higher
- 8GB RAM
- 10GB free disk space (for models)

### Recommended Requirements
- Windows 11 or Ubuntu 22.04
- Python 3.11
- 16GB RAM
- NVIDIA GPU with CUDA support
- 20GB free disk space

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/Azornes/TranslatorSeedX.git
   cd TranslatorSeedX
   ```

2. Install dependencies:
   ```bash
   # Windows
   install.bat
   
   # PowerShell
   .\install.ps1
   
   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   # Windows
   run.bat
   
   # Any platform
   python main.py
   ```

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/Azornes/TranslatorSeedX/wiki/Contributing) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 🐛 [Report a Bug](https://github.com/Azornes/TranslatorSeedX/issues/new?template=bug_report.md)
- 💡 [Request a Feature](https://github.com/Azornes/TranslatorSeedX/issues/new?template=feature_request.md)
- 💬 [Discussions](https://github.com/Azornes/TranslatorSeedX/discussions)

## Acknowledgments

- [ByteDance Seed Team](https://github.com/ByteDance/Seed) for the Seed-X-PPO-7B model
- [llama.cpp](https://github.com/ggerganov/llama.cpp) for GGUF support
- [Hugging Face](https://huggingface.co/) for model hosting
