from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def run(self, state):
        prompt = f"""
You are a senior data strategist.

User Query: {state['query']}

Break into:
1. Data needed
2. Analysis type
3. Expected output

Be structured.
"""
        plan = self.llm.generate(prompt)

        state["plan"] = plan
        state["iteration"] = state.get("iteration", 0) + 1

        self.bob.log("Planner", plan)

        return state