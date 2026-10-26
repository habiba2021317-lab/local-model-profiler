
import requests
import json
import time
import psutil
import csv

model = "qwen2.5:3b"
url = "http://localhost:11434/api/generate"

context_lengths = [1024, 2048, 4096, 8192]
results = []

for context in context_lengths:
    prompt = "Explain artificial intelligence. " * (context // 5)

    data = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_ctx": context,
            "num_predict": 100
        }
    }

    ram_before = psutil.virtual_memory().used / (1024 ** 3)

    start_time = time.perf_counter()
    ttft = 0
    token_count = 0
    generation_time = 0
    prompt_tokens = 0

    response = requests.post(
        url,
        json=data,
        stream=True,
        timeout=900
    )

    response.raise_for_status()

    for line in response.iter_lines():
        if line:
            result = json.loads(line)

            if result.get("response") and ttft == 0:
                ttft = time.perf_counter() - start_time

            if result.get("done"):
                token_count = result.get("eval_count", 0)
                generation_time = result.get("eval_duration", 0)
                prompt_tokens = result.get("prompt_eval_count", 0)

    response.close()

    ram_after = psutil.virtual_memory().used / (1024 ** 3)

    if token_count > 0:
        latency = generation_time / token_count / 1_000_000_000
    else:
        latency = 0

    print("Context setting:", context)
    print("Actual prompt tokens:", prompt_tokens)
    print("TTFT:", round(ttft, 3), "seconds")
    print("Average token latency:", round(latency, 4), "seconds")
    print("System RAM used before:", round(ram_before, 2), "GB")
    print("System RAM used after:", round(ram_after, 2), "GB")
    print("--------------------")

    results.append({
        "context_setting": context,
        "actual_prompt_tokens": prompt_tokens,
        "ttft_seconds": round(ttft, 3),
        "average_token_latency_seconds": round(latency, 4),
        "system_ram_used_before_gb": round(ram_before, 2),
        "system_ram_used_after_gb": round(ram_after, 2)
    })

with open(
    "profiling_results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:
    fieldnames = [
        "context_setting",
        "actual_prompt_tokens",
        "ttft_seconds",
        "average_token_latency_seconds",
        "system_ram_used_before_gb",
        "system_ram_used_after_gb"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("Results saved to profiling_results.csv")
