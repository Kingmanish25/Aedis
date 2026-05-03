import json
import os
from datetime import datetime

class MemoryManager:
    def __init__(self, path="memory_store.json"):
        self.path = path
        self.memory = self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load memory from {self.path}: {e}")
                return []
        return []

    def store(self, entry):
        structured = {
            "query": entry.get("query"),
            "actions": entry.get("actions"),
            "results": entry.get("results"),
            "confidence": entry.get("confidence"),
            "feedback": entry.get("feedback"),
            "timestamp": datetime.now().isoformat()
        }

        self.memory.append(structured)
        self._save()

    def _save(self):
        try:
            with open(self.path, "w") as f:
                json.dump(self.memory, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save memory to {self.path}: {e}")

    def get_all(self):
        return self.memory
    
    def search(self, query_text):
        """Search memory for entries matching query text"""
        results = []
        for entry in self.memory:
            if query_text.lower() in str(entry.get("query", "")).lower():
                results.append(entry)
        return results