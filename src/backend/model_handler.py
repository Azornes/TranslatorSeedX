"""
Model handler for Seed-X GGUF translation model
"""

import os
import json
from typing import Optional, Dict, Any, List
from llama_cpp import Llama
from src.utils.config import MODEL_CONFIG, GENERATION_CONFIG, LANGUAGES


class TranslationModel:
    """Handler for Seed-X translation model"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path
        self.is_loaded = False
        self.current_settings = GENERATION_CONFIG.copy()
        self.last_error = ""
        
        # Don't auto-load model in constructor to avoid crashes
        # Model will be loaded explicitly through GUI
        
    def load_model(self, model_path: str, **kwargs) -> bool:
        """
        Load the GGUF model
        
        Args:
            model_path: Path to the GGUF model file
            **kwargs: Additional model configuration parameters
            
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(model_path):
                msg = f"Error: Model file not found: {model_path}"
                print(msg)
                self.last_error = msg
                return False
            
            # Merge default config with provided kwargs
            config = MODEL_CONFIG.copy()
            config.update(kwargs)
            
            # For BF16 models, abort with a clear error (llama.cpp BF16 GGUF is unstable on Windows)
            if "bf16" in model_path.lower():
                msg = ("Detected BF16 GGUF. This format is not reliable with llama.cpp on Windows and may crash.\n"
                       "Recommended: use a quantized GGUF like Q4_K_M, or use the original model with vLLM.\n"
                       f"File: {model_path}")
                print(msg)
                self.last_error = msg
                return False
            
            print(f"Loading model: {model_path}")
            print(f"Config: n_ctx={config.get('n_ctx')}, n_gpu_layers={config.get('n_gpu_layers')}, n_threads={config.get('n_threads')}")
            
            # Load the model
            self.model = Llama(
                model_path=model_path,
                n_ctx=config.get("n_ctx", 2048),
                n_threads=config.get("n_threads", 8),
                n_gpu_layers=config.get("n_gpu_layers", -1),
                seed=config.get("seed", -1),
                verbose=config.get("verbose", True)  # Enable verbose for debugging
            )
            
            self.model_path = model_path
            self.is_loaded = True
            print("Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print(f"Error type: {type(e).__name__}")
            self.last_error = (
                f"Error loading model: {e}\n"
                f"Type: {type(e).__name__}\n"
                "If you're loading a BF16 GGUF, use Q4_K_M instead, or use vLLM with the original model."
            )
            
            # Try fallback with CPU only
            if "n_gpu_layers" in config and config["n_gpu_layers"] != 0:
                print("Trying fallback with CPU only...")
                try:
                    self.model = Llama(
                        model_path=model_path,
                        n_ctx=1024,
                        n_threads=4,
                        n_gpu_layers=0,  # CPU only
                        seed=-1,
                        verbose=True
                    )
                    self.model_path = model_path
                    self.is_loaded = True
                    print("Model loaded successfully with CPU fallback!")
                    return True
                except Exception as e2:
                    print(f"CPU fallback also failed: {e2}")
                    self.last_error += f"\nCPU fallback also failed: {e2}"
            
            self.is_loaded = False
            return False
    
    def unload_model(self):
        """Unload the current model to free memory"""
        if self.model:
            del self.model
            self.model = None
            self.is_loaded = False
    
    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        use_cot: bool = False,
        **kwargs
    ) -> str:
        """
        Translate text from source to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            use_cot: Use Chain-of-Thought mode for detailed translation
            **kwargs: Additional generation parameters
            
        Returns:
            str: Translated text
        """
        if not self.is_loaded or not self.model:
            raise RuntimeError("Model not loaded. Please load a model first.")
        
        # Get language codes
        source_code = self._get_language_code(source_lang)
        target_code = self._get_language_code(target_lang)
        
        # Build the prompt
        prompt = self._build_prompt(text, source_code, target_code, use_cot)
        
        # Merge generation settings
        gen_config = self.current_settings.copy()
        gen_config.update(kwargs)
        
        try:
            # Generate translation
            response = self.model(
                prompt,
                max_tokens=gen_config.get("max_tokens", 512),
                temperature=gen_config.get("temperature", 0.1),
                top_p=gen_config.get("top_p", 0.95),
                top_k=gen_config.get("top_k", 40),
                repeat_penalty=gen_config.get("repeat_penalty", 1.1),
                stop=gen_config.get("stop", ["</s>", "\n\n"])
            )
            
            # Extract the translated text
            translation = response["choices"][0]["text"].strip()
            return translation
            
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def _build_prompt(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        use_cot: bool
    ) -> str:
        """
        Build the translation prompt according to model requirements
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            use_cot: Use Chain-of-Thought mode
            
        Returns:
            str: Formatted prompt
        """
        # Get full language names
        source_name = self._get_language_name(source_lang)
        target_name = self._get_language_name(target_lang)
        
        if use_cot:
            # Chain-of-Thought prompt for detailed translation
            prompt = f"Translate the following {source_name} text into {target_name} and explain it in detail:\n{text} <{target_lang}>"
        else:
            # Standard translation prompt
            prompt = f"Translate the following {source_name} text into {target_name}:\n{text} <{target_lang}>"
        
        return prompt
    
    def _get_language_code(self, lang: str) -> str:
        """Get language code from language name or code"""
        # If it's already a code, return it
        if lang in LANGUAGES.values():
            return lang
        
        # If it's a language name, get the code
        for name, code in LANGUAGES.items():
            if name.lower() == lang.lower():
                return code
        
        # Default to the input if not found
        return lang.lower()
    
    def _get_language_name(self, lang: str) -> str:
        """Get language name from code or name"""
        # If it's a language name, return it
        if lang in LANGUAGES:
            return lang
        
        # If it's a code, get the name
        for name, code in LANGUAGES.items():
            if code == lang.lower():
                return name
        
        # Default to the input if not found
        return lang
    
    def update_settings(self, settings: Dict[str, Any]):
        """Update generation settings"""
        self.current_settings.update(settings)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.is_loaded:
            return {"status": "No model loaded"}
        
        return {
            "status": "Model loaded",
            "path": self.model_path,
            "context_size": MODEL_CONFIG.get("n_ctx", 2048),
            "gpu_layers": MODEL_CONFIG.get("n_gpu_layers", -1),
            "threads": MODEL_CONFIG.get("n_threads", 8)
        }
    
    def batch_translate(
        self,
        texts: List[str],
        source_lang: str,
        target_lang: str,
        use_cot: bool = False,
        **kwargs
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
            translation = self.translate(
                text, source_lang, target_lang, use_cot, **kwargs
            )
            translations.append(translation)
        
        return translations
