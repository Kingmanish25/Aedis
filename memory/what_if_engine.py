from memory.causal_engine import CausalEngine
from memory.graph_builder import GraphBuilder

class WhatIfEngine:
    def __init__(self):
        self.graph = GraphBuilder().get_graph()
        self.engine = CausalEngine(self.graph)

    def simulate(self, intervention, intensity=1.0):
        """
        intervention: string (e.g. "Increase Marketing East")
        intensity: strength of intervention
        """

        # simulate causal propagation
        impacts = self.engine.propagate(intervention)

        # apply intensity scaling
        scaled = {
            k: round(v * intensity * 100, 2)
            for k, v in impacts.items()
        }

        return {
            "intervention": intervention,
            "impact": scaled
        }