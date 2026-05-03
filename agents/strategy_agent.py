import json
from agents.base_agent import BaseAgent
from memory.memory_retriever import MemoryRetriever
from memory.predictor import Predictor
from memory.what_if_engine import WhatIfEngine

class StrategyAgent(BaseAgent):
    def __init__(self, name, llm, bob, event_bus=None):
        super().__init__(name, llm, bob, event_bus)
        self.retriever = MemoryRetriever()
        self.predictor = Predictor()
        self.what_if = WhatIfEngine()

    def run(self, state):
        self.emit("start", "Generating strategy")

        ml = state.get("ml_result", {})

        if not ml:
            state["strategy"] = "No data available for strategy"
            return state

        region = ml.get("region_impact", {})
        product = ml.get("product_impact", {})
        summary = ml.get("summary", "")

        past = self.retriever.retrieve(state["query"])

        memory_context = "\n".join([
            f"Past decision: {p.get('actions')} → Result: {p.get('results')}"
            for p in past
        ])

        prompt = f"""
You are a senior strategy consultant.
Use past decisions to improve strategy.

{memory_context}

Context:
{summary}

Weak regions: {region}
Weak products: {product}

Return STRICT JSON:
- executive_summary
- actions (list)
"""

        raw = self.llm.generate(prompt)

        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {
                "executive_summary": f"Revenue decline driven by {region} and {product}.",
                "actions": [
                    {
                        "name": "Notify regional leads",
                        "type": "notify",
                        "priority": 4,
                        "expected_impact": "10-15%",
                        "payload": {"region": list(region.keys())}
                    }
                ]
            }

        # 🔥 Enrich with prediction + what-if
        for action in parsed.get("actions", []):
            action["predicted_impact"] = self.predictor.predict(action["name"])
            action["what_if"] = self.what_if.simulate(action["name"], intensity=1.2)

        state["strategy_structured"] = parsed
        state["strategy"] = parsed.get("executive_summary", "")

        self.emit("strategy_ready", "Actions prepared", parsed.get("actions"))
        self.bob.log("Strategy", "Structured strategy generated")

        return state