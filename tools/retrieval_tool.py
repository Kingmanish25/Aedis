import os
from llm.embedding_model import EmbeddingModel
from memory.vector_store import VectorStore

class RetrievalTool:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.store = VectorStore()

        # 🔹 Preload sample documents (can be replaced with real docs)
        self._load_documents()

    def _load_documents(self):
        folder = "data/documents"

        docs = []

        for file in os.listdir(folder):
            if file.endswith(".pdf") or file.endswith(".txt"):
                with open(os.path.join(folder, file), "rb") as f:
                    text = f.read().decode(errors="ignore")
                    docs.append(text[:1000])  # chunk

        if docs:
            embeddings = self.embedder.embed(docs)
            self.store.add(embeddings, docs)

    def retrieve(self, query):
        try:
            emb = self.embedder.embed([query])[0]
            results = self.store.search(emb)
            return results
        except Exception as e:
            return ["Retrieval fallback: Unable to fetch documents"]