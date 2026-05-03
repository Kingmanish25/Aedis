from llm.embedding_model import EmbeddingModel
from memory.memory_manager import MemoryManager
import numpy as np

class MemoryRetriever:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.memory = MemoryManager()
        self.index = []
        self.entries = []

        self._build_index()

    def _build_index(self):
        history = self.memory.get_all()

        if not history:
            return

        texts = [self._to_text(h) for h in history]
        embeddings = self.embedder.embed(texts)

        self.index = embeddings
        self.entries = history

    def _to_text(self, entry):
        return f"""
        Query: {entry.get('query')}
        Actions: {entry.get('actions')}
        Outcome: {entry.get('results')}
        """

    def retrieve(self, query, k=3):
        if not self.index:
            return []

        q_emb = self.embedder.embed([query])[0]

        sims = [
            (entry, np.dot(q_emb, emb))
            for entry, emb in zip(self.entries, self.index)
        ]

        sims = sorted(sims, key=lambda x: x[1], reverse=True)

        return [s[0] for s in sims[:k]]