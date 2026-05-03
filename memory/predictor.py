from memory.causal_engine import CausalEngine
from memory.graph_builder import GraphBuilder

class Predictor:
    def __init__(self):
        self.graph = GraphBuilder().get_graph()
        self.engine = CausalEngine(self.graph)

    def predict(self, action_name):
        impacts = self.engine.propagate(action_name)

        # Focus on revenue
        revenue_impact = impacts.get("Revenue", 0)

        return {
            "predicted_revenue_impact": round(revenue_impact * 100, 2)
        }