# Local Model Inference & Hardware Profiler

## Project Overview

This project explores local Large Language Model (LLM) inference using Python and Ollama. It measures response-generation performance and monitors system RAM usage at different context window settings.

## Tools and Technologies

- Python
- Ollama
- Qwen 2.5 3B
- Requests
- psutil
- CSV

## Performance Metrics

The profiling script records:

- **Time to First Token (TTFT):** The elapsed time until the first non-empty response text is received.
- **Average Token Latency:** Average generation time per output token, based on Ollama's reported generation statistics.
- **System RAM Usage:** System memory usage before and after each run.
- **Context Window Settings:** Tests configured for 1,024, 2,048, 4,096, and 8,192 tokens.

## How It Works

1. The script sends a prompt to the local Ollama API.
2. It measures the time until the first response text arrives.
3. It collects generation statistics and system RAM measurements.
4. It saves the collected results to `profiling_results.csv`.

## How to Run

1. Install Python.
2. Install the required packages:

   ```bash
   pip install requests psutil
   ```

3. Install and run Ollama.
4. Make sure the model is available locally:

   ```bash
   ollama pull qwen2.5:3b
   ```

5. Run the profiler:

   ```bash
   python profiler.py
   ```

## Limitations

- The current experiment uses Qwen 2.5 3B, not a 7B or 8B model.
- Context window settings do not guarantee that the prompt contains exactly the same number of tokens.
- TTFT includes the time observed by the Python client and may include model-loading and request overhead.
- RAM measurements represent system RAM, not GPU VRAM.
- Average token latency is calculated from total generation time and token count; individual inter-token delays are not measured separately.

## Project Status

This is an initial local profiling experiment. Further work is needed to measure GPU VRAM usage and improve the accuracy of token-level latency measurements.

