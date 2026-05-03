import networkx as nx

class CausalEngine:
    def __init__(self, graph):
        self.graph = graph.graph

    def propagate(self, start_node, steps=2):
        impacts = {}

        def dfs(node, depth, weight):
            if depth > steps:
                return

            for _, neighbor, data in self.graph.edges(node, data=True):
                new_weight = weight * data.get("weight", 1.0)

                impacts[neighbor] = impacts.get(neighbor, 0) + new_weight

                dfs(neighbor, depth + 1, new_weight)

        dfs(start_node, 0, 1.0)

        return impacts