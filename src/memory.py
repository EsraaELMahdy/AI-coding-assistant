import json
import re
from src import config

MEMORY_FILE = config.ROOT / "memory.json"
MAX_MESSAGES = 12

LANGUAGES = ["python", "javascript", "java", "typescript", "rust"]
FRAMEWORKS = ["flask", "django", "fastapi", "pytorch", "tensorflow", "keras", "streamlit"]


class Memory:
    def __init__(self):
        self.history = []
        self.preferences = {}
        self.load()

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        self.save()

    def update_preferences(self, text):
        lower = text.lower()
        for name in LANGUAGES:
            if re.search(r"\b" + re.escape(name) + r"\b", lower):
                self.preferences["language"] = name
        for name in FRAMEWORKS:
            if re.search(r"\b" + re.escape(name) + r"\b", lower):
                self.preferences["framework"] = name
        self.save()

    def get_context(self):
        lines = []
        if self.preferences:
            items = [key + ": " + value for key, value in self.preferences.items()]
            lines.append("User preferences - " + ", ".join(items))
        for item in self.history[-MAX_MESSAGES:]:
            lines.append(item["role"] + ": " + item["content"])
        return "\n".join(lines)

    def clear(self):
        self.history = []
        self.preferences = {}
        self.save()

    def save(self):
        data = {"history": self.history, "preferences": self.preferences}
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not MEMORY_FILE.exists():
            return
        with open(MEMORY_FILE, encoding="utf-8") as f:
            data = json.load(f)
        self.history = data.get("history", [])
        self.preferences = data.get("preferences", {})