# Models Directory

Place your model files in this directory.

## IMPORTANT: Model Compatibility Issues

**BF16 GGUF models have compatibility issues with llama-cpp-python and may cause crashes.**

## Recommended Solutions:

### Option 1: Use Quantized GGUF Models (Recommended)
1. Visit: https://huggingface.co/Mungert/Seed-X-PPO-7B-GGUF
2. Download a quantized version (NOT BF16):
   - **Q4_K_M** (4.64 GB) - Recommended for balanced quality and performance
   - **Q5_K_M** (5.39 GB) - Better quality, slightly slower
   - **Q3_K_M** (3.79 GB) - Faster but lower quality
   - **Q8_0** (7.99 GB) - Best quality but requires more RAM

### Option 2: Use Original Model with vLLM (For BF16/F16)
1. Install vLLM: `pip install vllm transformers`
2. Download the original model from: https://huggingface.co/ByteDance/Seed-X-PPO-7B
3. Use the model directory path (not .gguf file)

## Current Issue with Your BF16 Model
The `Seed-X-PPO-7B-bf16.gguf` file you downloaded is causing access violations. This is a known issue with BF16 GGUF files.

**Solutions:**
1. **Replace with Q4_K_M**: Download `seed-x-ppo-7b-q4-k-m.gguf` instead
2. **Use vLLM**: Install vLLM and download the original model (not GGUF)

## Hardware Requirements

- **Q3/Q4 models**: 8GB RAM minimum
- **Q5/Q6 models**: 12GB RAM recommended  
- **Q8/F16 models**: 16GB+ RAM recommended
- **Original models**: 16GB+ RAM, GPU recommended

## GPU Acceleration

For faster inference with GPU:
- NVIDIA GPU with CUDA support recommended
- The application will automatically use GPU if available
- CPU-only mode is supported but will be slower
