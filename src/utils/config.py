"""
Configuration settings for the Seed-X Translation application
"""

# Model settings
DEFAULT_MODEL_PATH = "models/"
DEFAULT_MODEL_NAME = "seed-x-ppo-7b.gguf"

# Model parameters
MODEL_CONFIG = {
    "n_ctx": 2048,          # Context window size
    "n_threads": 8,         # Number of CPU threads
    "n_gpu_layers": -1,     # -1 = all layers on GPU, 0 = all on CPU
    "seed": -1,             # Random seed (-1 for random)
    "verbose": False        # Print verbose output
}

# Generation parameters
GENERATION_CONFIG = {
    "max_tokens": 512,
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 40,
    "repeat_penalty": 1.1,
    "stop": ["</s>", "\n\n"]
}

# Supported languages
LANGUAGES = {
    "Arabic": "ar",
    "Czech": "cs",
    "Danish": "da",
    "German": "de",
    "English": "en",
    "Spanish": "es",
    "Finnish": "fi",
    "French": "fr",
    "Croatian": "hr",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Malay": "ms",
    "Norwegian Bokmål": "nb",
    "Dutch": "nl",
    "Norwegian": "no",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Swedish": "sv",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Vietnamese": "vi",
    "Chinese": "zh"
}

# UI Configuration
UI_CONFIG = {
    "window_width": 1200,
    "window_height": 700,
    "font_size": 11,
    "max_history": 100
}

# Application themes
THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "input_bg": "#ffffff",
        "output_bg": "#f8f8f8",
        "button_bg": "#0084ff",
        "button_fg": "#ffffff"
    },
    "dark": {
        "bg": "#2b2b2b",
        "fg": "#ffffff",
        "input_bg": "#3c3c3c",
        "output_bg": "#404040",
        "button_bg": "#0084ff",
        "button_fg": "#ffffff"
    }
}
