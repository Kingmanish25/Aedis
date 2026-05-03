from .base_agent import BaseAgent

class CriticAgent(BaseAgent):
    def run(self, state):
        confidence = 0.0

        if state.get("data"):
            confidence += 0.3

        if state.get("ml_result"):
            confidence += 0.4

        if state.get("insights"):
            confidence += 0.3
        
        if state.get("memory_used"):
            confidence += 0.1

        state["confidence"] = round(confidence, 2)

        self.bob.log("Critic", f"Confidence: {confidence}")

        return state