import json
from datasets import load_dataset
from src import config

dataset = load_dataset("openai/openai_humaneval", split="test")
rows = [dict(item) for item in dataset]

with open(config.DATA_DIR / "humaneval.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)

print(len(rows), "problems saved")