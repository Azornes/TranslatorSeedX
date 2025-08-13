"""
Model handler using Transformers library (works on Windows)
"""

import os
import re
from typing import Any, Dict, List, Optional

import torch
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.utils.config import GENERATION_CONFIG, LANGUAGES


class TransformersTranslationModel:
    """Handler for Seed-X translation model using Transformers library"""

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.tokenizer = None
        self.model_path = model_path
        self.is_loaded = False
        self.current_settings = GENERATION_CONFIG.copy()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def ensure_model_downloaded(self, model_path: str, repo_id: str = "ByteDance/Seed-X-PPO-7B") -> bool:
        """
        Ensure model is downloaded, auto-download if not exists
        """
        if not os.path.exists(model_path):
            print(f"Model directory does not exist: {model_path}")
            print(f"Downloading model from Hugging Face: {repo_id}")
            try:
                # Create parent directory
                os.makedirs(os.path.dirname(model_path), exist_ok=True)

                # Download model
                snapshot_download(repo_id=repo_id, local_dir=model_path, local_dir_use_symlinks=False, resume_download=True)
                print(f"Model download completed: {model_path}")
                return True
            except Exception as e:
                print(f"Model download failed: {e}")
                return False
        else:
            print(f"Model already exists: {model_path}")
            return True

    def load_model(self, model_path: str, **kwargs) -> bool:
        """
        Load the model using Transformers

        Args:
            model_path: Path to the model directory
            **kwargs: Additional model configuration parameters

        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            print(f"Loading model with Transformers: {model_path}")

            # For GGUF files, we need the original model
            if model_path.endswith(".gguf"):
                print("Error: Transformers doesn't support GGUF files directly.")
                print("Please use the original model from HuggingFace.")
                return False

            # Ensure model is downloaded
            if not self.ensure_model_downloaded(model_path):
                return False

            # Determine dtype
            dtype = torch.float16 if self.device == "cuda" else torch.float32

            # Load model and tokenizer
            print(f"Loading model to {self.device} with dtype {dtype}")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path, torch_dtype=dtype, device_map="auto" if self.device == "cuda" else None, trust_remote_code=True
            )

            if self.device == "cuda":
                self.model = self.model.to(self.device)

            self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

            # Set pad token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model_path = model_path
            self.is_loaded = True
            print(f"Model loaded successfully with Transformers on {self.device}!")
            return True

        except Exception as e:
            print(f"Error loading model with Transformers: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback

            traceback.print_exc()
            self.is_loaded = False
            return False

    def unload_model(self):
        """Unload the current model to free memory"""
        if self.model:
            del self.model
            self.model = None
        if self.tokenizer:
            del self.tokenizer
            self.tokenizer = None
        self.is_loaded = False
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

    def _extract_with_patterns(self, output: str, target_code: str) -> str:
        """Extract translation using regex patterns"""
        patterns = [
            f"<{target_code}>(.*?)(?:<(?!/)|$)",
            f"<{target_code}>(.*)",
            f"{target_code}>(.*?)(?:<|$)",
            f"<{target_code}>\\s*(.*?)(?:\\n\\n|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, output, re.DOTALL | re.IGNORECASE)
            if match:
                result = match.group(1).strip()
                if result and len(result) > 0:
                    return result
        return ""

    def _extract_line_by_line(self, output: str, target_code: str) -> str:
        """Extract translation by parsing line by line"""
        lines = output.split("\n")
        found_marker = False
        result_lines = []

        for line in lines:
            if f"<{target_code}>" in line or f"{target_code}>" in line:
                found_marker = True
                parts = re.split(f"<{target_code}>|{target_code}>", line, 1)
                if len(parts) > 1 and parts[1].strip():
                    result_lines.append(parts[1].strip())
                continue

            if found_marker:
                if re.search(r"<[a-z]{2}>", line, re.IGNORECASE):
                    break
                result_lines.append(line)

        return "\n".join(result_lines).strip() if result_lines else ""

    def _extract_fallback(self, output: str) -> str:
        """Fallback extraction method"""
        if "Translation in" in output:
            parts = output.split("Translation in", 1)
            if len(parts) > 1:
                result = parts[1].strip()
                # Remove language markers
                result = re.sub(r"<[a-z]{2}>", "", result, flags=re.IGNORECASE)
                result = re.sub(r"^[a-zA-Z]+:", "", result).strip()
                if result:
                    return result
        return ""

    def extract_translation_from_output(self, output: str, target_code: str) -> str:
        """Extract translation from model output"""
        # Try pattern-based extraction
        result = self._extract_with_patterns(output, target_code)
        if result:
            return result

        # Try line-by-line extraction
        result = self._extract_line_by_line(output, target_code)
        if result:
            return result

        # Try fallback method
        return self._extract_fallback(output)

    def translate(self, text: str, source_lang: str, target_lang: str, use_cot: bool = False, **kwargs) -> str:
        """
        Translate text from source to target language

        Args:
            text: Text to translate
            source_lang: Source language code or name
            target_lang: Target language code or name
            use_cot: Use Chain-of-Thought mode for detailed translation
            **kwargs: Additional generation parameters

        Returns:
            str: Translated text
        """
        if not self.is_loaded or not self.model:
            raise RuntimeError("Model not loaded. Please load a model first.")

        # Get language codes
        target_code = self._get_language_code(target_lang)
        source_name = self._get_language_name(source_lang)
        target_name = self._get_language_name(target_lang)

        # Build the prompt
        if use_cot:
            prompt = f"Translate the following {source_name} text into {target_name} and explain it in detail:\n{text} <{target_code}>"
        else:
            # Simplified prompt for better results
            prompt = f"Translate from {source_name} to {target_name}:\n{text}\n\nTranslation in {target_name} <{target_code}>:"

        # Merge generation settings
        gen_config = self.current_settings.copy()
        gen_config.update(kwargs)

        try:
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

            # Calculate max tokens
            max_tokens = min(gen_config.get("max_tokens", 512), max(150, len(text) * 2))

            print(f"Translating text (length: {len(text)}), max_tokens: {max_tokens}")

            # Generate translation
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=gen_config.get("temperature", 0.1) if gen_config.get("temperature", 0.1) > 0 else 1.0,
                    do_sample=gen_config.get("temperature", 0.1) > 0,
                    top_p=gen_config.get("top_p", 0.95),
                    top_k=gen_config.get("top_k", 40),
                    repetition_penalty=gen_config.get("repeat_penalty", 1.1),
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )

            # Decode output
            full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract translation
            translation = self.extract_translation_from_output(full_output, target_code)

            if translation:
                return translation
            else:
                # Fallback: remove the prompt from output
                if prompt in full_output:
                    translation = full_output.replace(prompt, "").strip()
                else:
                    translation = full_output

                # Clean up any remaining markers
                translation = re.sub(r"<[a-z]{2}>", "", translation, flags=re.IGNORECASE)
                return translation if translation else "Translation failed"

        except Exception as e:
            return f"Translation error: {str(e)}"

    def _get_language_code(self, lang: str) -> str:
        """Get language code from language name or code"""
        if lang in LANGUAGES.values():
            return lang

        for name, code in LANGUAGES.items():
            if name.lower() == lang.lower():
                return code

        return lang.lower()

    def _get_language_name(self, lang: str) -> str:
        """Get language name from code or name"""
        if lang in LANGUAGES:
            return lang

        for name, code in LANGUAGES.items():
            if code == lang.lower():
                return name

        return lang

    def update_settings(self, settings: Dict[str, Any]):
        """Update generation settings"""
        self.current_settings.update(settings)

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.is_loaded:
            return {"status": "No model loaded"}

        return {
            "status": "Model loaded (Transformers)",
            "path": self.model_path,
            "backend": "Transformers",
            "device": self.device,
            "supports_gguf": False,
        }

    def batch_translate(
        self, texts: List[str], source_lang: str, target_lang: str, use_cot: bool = False, **kwargs
    ) -> List[str]:
        """
        Translate multiple texts

        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
            use_cot: Use Chain-of-Thought mode
            **kwargs: Additional generation parameters

        Returns:
            List[str]: List of translated texts
        """
        translations = []
        for text in texts:
            translation = self.translate(text, source_lang, target_lang, use_cot, **kwargs)
            translations.append(translation)

        return translations
