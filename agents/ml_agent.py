from .base_agent import BaseAgent
from tools.ml_tool import run_advanced_analysis

class MLAgent(BaseAgent):
    def run(self, state):
        data = state.get("data")

        if not data:
            state["error"] = "No data for ML"
            return state

        result = run_advanced_analysis(data)

        if "error" in result:
            state["error"] = result["error"]
            return state

        state["ml_result"] = result
        state["analysis"] = result["summary"]

        self.bob.log("ML", result["summary"])

        return state