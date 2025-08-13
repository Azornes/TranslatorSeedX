"""
Backend logic for translation application
Separates model handling, translation, and history from GUI
"""

import json
from typing import Optional, Dict, List

from PyQt6.QtCore import QThread, pyqtSignal, QSettings
from src.backend.model_handler import TranslationModel
from src.backend.model_handler_transformers import TransformersTranslationModel


class ModelLoadThread(QThread):
    """Thread for loading the model without blocking"""

    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, model_path: str, model_handler: TranslationModel):
        super().__init__()
        self.model_path = model_path
        self.model_handler = model_handler

    def run(self):
        self.progress.emit("Loading model...")
        success = self.model_handler.load_model(self.model_path)
        if success:
            self.progress.emit("Model loaded successfully!")
        else:
            self.progress.emit("Failed to load model.")
        self.finished.emit(success)


class TranslationThread(QThread):
    """Thread for running translation without blocking"""

    result = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(
        self, model: TranslationModel, text: str, source_lang: str, target_lang: str, use_cot: bool = False, **kwargs
    ):
        super().__init__()
        self.model = model
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.use_cot = use_cot
        self.kwargs = kwargs

    def run(self):
        try:
            self.progress.emit("Translating...")
            translation = self.model.translate(self.text, self.source_lang, self.target_lang, self.use_cot, **self.kwargs)
            self.result.emit(translation)
        except Exception as e:
            self.error.emit(str(e))


class ModelDownloadThread(QThread):
    """Thread for downloading models without blocking"""

    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, repo_id: str, filename: str = None):
        super().__init__()
        self.repo_id = repo_id
        self.filename = filename

    def run(self):
        try:
            import os
            from huggingface_hub import hf_hub_download, snapshot_download

            # Ensure models directory exists
            os.makedirs("models", exist_ok=True)

            if self.filename:
                # Download specific GGUF file
                self.progress.emit(f"Downloading {self.filename}...")
                path_to_check = hf_hub_download(
                    repo_id=self.repo_id,
                    filename=self.filename,
                    local_dir=os.path.abspath("models"),
                    local_dir_use_symlinks=False,
                )
            else:
                # Download entire repository
                self.progress.emit(f"Downloading repository {self.repo_id}...")
                path_to_check = os.path.abspath(os.path.join("models", self.repo_id.split("/")[-1]))
                snapshot_download(
                    repo_id=self.repo_id, local_dir=path_to_check, local_dir_use_symlinks=False, repo_type="model"
                )

            if path_to_check and os.path.exists(path_to_check):
                self.finished.emit(True, path_to_check)
            else:
                self.progress.emit("Download path not found")
                self.finished.emit(False, "")
        except Exception as e:
            self.progress.emit(f"Error: {str(e)}")
            self.finished.emit(False, "")


class TranslationManager:
    """Manages translation logic, model, and history"""

    def __init__(self):
        self.model = None
        self.translation_history: List[Dict] = []
        self.settings = QSettings("SeedX", "Translator")
        self.current_backend = "GGUF"

    def switch_backend(self, backend: str):
        """Switch between backends"""
        if self.model and self.model.is_loaded:
            self.model.unload_model()
        if "Transformers" in backend:
            self.model = TransformersTranslationModel()
        else:
            self.model = TranslationModel()
        self.current_backend = backend

    def load_model(self, model_path: str, progress_callback, finished_callback):
        """Load model in thread"""
        thread = ModelLoadThread(model_path, self.model)
        thread.progress.connect(progress_callback)
        thread.finished.connect(finished_callback)
        thread.start()
        return thread

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        use_cot: bool,
        settings: Dict,
        result_callback,
        error_callback,
        progress_callback,
    ):
        """Perform translation in thread"""
        thread = TranslationThread(self.model, text, source_lang, target_lang, use_cot, **settings)
        thread.result.connect(result_callback)
        thread.error.connect(error_callback)
        thread.progress.connect(progress_callback)
        thread.start()
        return thread

    def download_model(self, repo_id: str, filename: Optional[str], progress_callback, finished_callback):
        """Download model in thread"""
        thread = ModelDownloadThread(repo_id, filename)
        thread.progress.connect(progress_callback)
        thread.finished.connect(finished_callback)
        thread.start()
        return thread

    def add_to_history(self, entry: Dict):
        """Add entry to history"""
        self.translation_history.append(entry)
        # Limit size
        max_history = 50  # Configurable
        if len(self.translation_history) > max_history:
            self.translation_history.pop(0)

    def get_history(self) -> List[Dict]:
        """Get translation history"""
        return self.translation_history

    def clear_history(self):
        """Clear history"""
        self.translation_history.clear()

    def save_history(self, file_path: str) -> bool:
        """Save history to file"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.translation_history, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def load_history(self, file_path: str) -> bool:
        """Load history from file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translation_history = json.load(f)
            return True
        except Exception:
            return False

    def update_settings(self, settings: Dict):
        """Update model settings"""
        if self.model:
            self.model.update_settings(settings)

    def get_model_info(self) -> Dict:
        """Get model information"""
        if self.model:
            return self.model.get_model_info()
        return {}

    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model.is_loaded if self.model else False

    def unload_model(self):
        """Unload the model"""
        if self.model:
            self.model.unload_model()
