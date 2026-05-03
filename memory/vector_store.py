import faiss
import numpy as np
from llm.embedding_model import EmbeddingModel

class VectorStore:
    def __init__(self):
        self.embedder = EmbeddingModel()
        sample = self.embedder.embed(["test"])
        dim = len(sample[0])

        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embeddings, texts):
        self.index.add(np.array(embeddings))
        self.texts.extend(texts)

    def search(self, emb):
        _, idx = self.index.search(np.array([emb]), k=3)
        return [self.texts[i] for i in idx[0]]