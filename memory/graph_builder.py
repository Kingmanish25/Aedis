from memory.knowledge_graph import KnowledgeGraph
from memory.memory_manager import MemoryManager

class GraphBuilder:
    def __init__(self):
        self.memory = MemoryManager()
        self.kg = KnowledgeGraph()
        self.build()

    def build(self):
        history = self.memory.get_all()

        for entry in history:
            self.kg.add_memory(entry)

    def get_graph(self):
        return self.kg