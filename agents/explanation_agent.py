from .base_agent import BaseAgent

class ExplanationAgent(BaseAgent):
    def __init__(self, name, llm, bob, event_bus=None):
        super().__init__(name, llm, bob, event_bus)

    def run(self, state):
        self.emit("start", "Generating explanation")

        ml = state.get("ml_result", {})

        if not ml:
            state["final"] = "No explanation available"
            return state

        explanation = f"""
Revenue analysis shows anomalies.

Key drivers:
- Regions: {ml.get('region_impact')}
- Products: {ml.get('product_impact')}

Conclusion:
Revenue drop driven by region & product decline.
"""

        state["final"] = explanation

        self.emit("done", "Explanation generated")
        self.bob.log("Explanation", "Insight generated")

        return state