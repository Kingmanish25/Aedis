import networkx as nx

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_causal_fact(self, cause, effect, weight=1.0):
        self.graph.add_edge(
            cause,
            effect,
            relation="causes",
            weight=weight
        )

    def add_memory(self, memory_entry):
        query = memory_entry.get("query", "")
        actions = memory_entry.get("actions", [])
        results = memory_entry.get("results", [])

        # 🔹 Extract basic relationships
        self.add_causal_fact(query, str(actions))

        for action in actions:
            self.add_causal_fact(action["name"], str(results))

    def query(self, node):
        if node not in self.graph:
            return []

        return list(self.graph.edges(node, data=True))

    def get_all(self):
        return list(self.graph.edges(data=True))