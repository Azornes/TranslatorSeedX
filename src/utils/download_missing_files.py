"""
Download missing tokenizer files for Seed-X-PPO-7B model
"""

import os
from huggingface_hub import hf_hub_download


def download_missing_files():
    model_dir = "models/Seed-X-PPO-7B"
    repo_id = "ByteDance-Seed/Seed-X-PPO-7B"

    # List of files that should be present
    required_files = [
        "config.json",
        "generation_config.json",
        "model.safetensors",
        "tokenizer.json",
        "tokenizer_config.json",  # Missing
        "special_tokens_map.json",  # Missing
        "tokenizer.model",  # Missing for some tokenizers
    ]

    print(f"Checking model directory: {model_dir}")

    for filename in required_files:
        file_path = os.path.join(model_dir, filename)
        if not os.path.exists(file_path):
            print(f"Missing file: {filename}")
            try:
                print(f"Downloading {filename} from {repo_id}...")
                hf_hub_download(repo_id=repo_id, filename=filename, local_dir=model_dir, local_dir_use_symlinks=False)
                print(f"Downloaded: {filename}")
            except Exception as e:
                print(f"Failed to download {filename}: {e}")
        else:
            print(f"File exists: {filename}")

    print("\nDownload complete!")


if __name__ == "__main__":
    download_missing_files()
