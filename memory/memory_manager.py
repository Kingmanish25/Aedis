import json
import os
import datetime

class MemoryManager:
    def __init__(self, path="memory_store.json"):
        self.path = path
        self.memory = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return []

    def store(self, entry):
        structured = {
            "query": entry.get("query"),
            "actions": entry.get("actions"),
            "results": entry.get("results"),
            "confidence": entry.get("confidence"),
            "timestamp": str(datetime.now())
        }

        self.memory.append(structured)
        self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.memory, f, indent=2)

    def get_all(self):
        return self.memory