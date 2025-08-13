# Visual Studio Code Setup for Seed-X Translation Project

This guide will help you set up Visual Studio Code with proper linting and formatting for the Seed-X Translation project.

## Quick Setup

1. **Install recommended extensions** (VS Code will prompt you automatically):
   - Python
   - Ruff (modern replacement for flake8 + black)
   - JSON Language Features
   - YAML
   - PowerShell
   - Jupyter

2. **Open the project** in VS Code - settings are already configured!

## What's Configured

### Ruff Integration
- **Linting**: Real-time code quality checks
- **Formatting**: Automatic code formatting on save
- **Import sorting**: Automatic import organization
- **Error fixing**: Automatic fixes for common issues

### Editor Settings
- **Line length**: 127 characters (shown with ruler)
- **Tab size**: 4 spaces
- **Auto-formatting**: On save
- **Trailing whitespace**: Automatically trimmed
- **Final newline**: Automatically added

## How to Use

### Automatic Features
- **Save file** → Code is automatically formatted and imports organized
- **Type code** → Real-time linting shows errors and warnings
- **Hover over errors** → See detailed explanations and suggested fixes

### Manual Commands
Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run:

- `Ruff: Fix all auto-fixable problems` - Fix all issues that can be automatically resolved
- `Ruff: Format document` - Format the current file
- `Python: Select Interpreter` - Choose the virtual environment

### Keyboard Shortcuts
- `Shift+Alt+F` - Format document
- `Ctrl+Shift+O` - Organize imports
- `F8` - Go to next error/warning
- `Shift+F8` - Go to previous error/warning

## Configuration Files

The project includes these configuration files:

### `.vscode/settings.json`
- VS Code workspace settings
- Ruff integration
- Python interpreter path
- Editor preferences

### `pyproject.toml`
- Ruff configuration (linting rules, formatting options)
- Project metadata
- Tool settings for black, isort compatibility

### `.vscode/extensions.json`
- Recommended extensions list
- VS Code will prompt to install missing extensions

## Troubleshooting

### Ruff Not Working
1. Install the Ruff extension: `charliermarsh.ruff`
2. Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"
3. Check Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"

### Python Interpreter Issues
1. Make sure virtual environment is activated
2. Select correct interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose: `./venv/Scripts/python.exe` (Windows) or `./venv/bin/python` (Linux/Mac)

### Linting Too Strict
Edit `pyproject.toml` to adjust Ruff rules:
```toml
[tool.ruff.lint]
ignore = [
    "E203",  # Add more rules to ignore
    "W503",
    "E501",
]
```

## Benefits of This Setup

### For Development
- **Consistent code style** across the project
- **Early error detection** before running code
- **Automatic formatting** saves time
- **Import organization** keeps code clean

### For Collaboration
- **Same formatting** for all contributors
- **Consistent linting rules** reduce review time
- **Automatic fixes** reduce manual work
- **Professional code quality**

## Ruff vs Flake8

We use **Ruff** instead of the traditional flake8 + black + isort combination because:

- **10-100x faster** than flake8
- **Single tool** replaces multiple tools
- **Better error messages** with suggestions
- **Modern Python support** (3.10+)
- **Active development** and maintenance

## Additional Tips

### Code Quality
- Fix all Ruff warnings before committing
- Use type hints where possible
- Write descriptive docstrings
- Keep functions focused and small

### VS Code Features
- Use `Ctrl+Click` to navigate to definitions
- Use `F12` to go to definition
- Use `Shift+F12` to find all references
- Use `Ctrl+Space` for auto-completion

### Git Integration
- VS Code shows git changes in the sidebar
- Use built-in git commands or terminal
- Review changes before committing
- Write descriptive commit messages

## Getting Help

- **Ruff Documentation**: https://docs.astral.sh/ruff/
- **VS Code Python**: https://code.visualstudio.com/docs/python/python-tutorial
- **Project Issues**: https://github.com/Azornes/TranslatorSeedX/issues
