from .base_agent import BaseAgent
from memory.graph_builder import GraphBuilder

class InsightAgent(BaseAgent):
    def __init__(self, name, llm, bob, event_bus=None):
        super().__init__(name, llm, bob, event_bus)
        self.graph = GraphBuilder().get_graph()

    def run(self, state):
        self.emit("start", "Generating insights")

        ml = state.get("ml_result", {})

        related = self.graph.query(state["query"])

        graph_context = "\n".join([
            f"{src} → {data['relation']} → {dst}"
            for src, dst, data in related
        ]) if related else "No graph knowledge"

        prompt = f"""
Business analysis:

Graph:
{graph_context}

ML Summary:
{ml.get("summary")}

Region:
{ml.get("region_impact")}

Product:
{ml.get("product_impact")}

Generate insights, risks, root cause.
"""

        insights = self.llm.generate(prompt)

        state["insights"] = insights

        self.emit("done", "Insights generated")
        self.bob.log("Insight", "Insights generated")

        return state