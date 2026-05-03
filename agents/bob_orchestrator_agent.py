from agents.base_agent import BaseAgent
from ibm.bob_api_client import BobAPIClient


class BobOrchestratorAgent(BaseAgent):
    """
    Bob AI Orchestrator Agent
    Uses IBM watsonx.ai Bob for intelligent orchestration and decision-making
    """
    
    def __init__(self, name, llm, bob, event_bus=None):
        super().__init__(name, llm, bob, event_bus)
        # Initialize Bob API client for advanced orchestration
        try:
            self.bob_api = BobAPIClient()
            self.bob.log("Bob Orchestrator", "✓ Bob API initialized successfully")
        except Exception as e:
            self.bob.log("Bob Orchestrator", f"⚠️ Bob API init failed: {e}")
            self.bob_api = None

    def run(self, state):
        """
        Use Bob AI to orchestrate the workflow intelligently
        """
        self.bob.log("Bob Orchestrator", "Starting intelligent orchestration")
        
        if not self.bob_api:
            return self._fallback_orchestration(state)
        
        # Prepare context for Bob
        context = {
            "query": state.get("query", ""),
            "current_step": state.get("current_step", "unknown"),
            "available_agents": state.get("available_agents", []),
            "previous_results": state.get("results", {}),
            "confidence_scores": state.get("confidence_scores", {})
        }
        
        # Get orchestration decision from Bob
        try:
            decision = self.bob_api.orchestrate(
                task=state.get("query", "Analyze and decide next steps"),
                context=context
            )
            
            state["bob_orchestration"] = decision
            state["next_agent"] = decision.get("next_agent", "planner")
            state["orchestration_reasoning"] = decision.get("reasoning", "")
            state["orchestration_confidence"] = decision.get("estimated_confidence", 0.5)
            
            self.emit("orchestration_complete", 
                     f"Next: {decision.get('next_agent')}", 
                     decision)
            
            self.bob.log("Bob Orchestrator",
                              f"Decision: {decision.get('next_agent')} (confidence: {decision.get('estimated_confidence')})")
            
        except Exception as e:
            self.bob.log("Bob Orchestrator", f"Error: {e}")
            return self._fallback_orchestration(state)
        
        return state

    def reason_about_evidence(self, question: str, evidence: list) -> dict:
        """
        Use Bob's advanced reasoning capabilities
        """
        if not self.bob_api:
            return {
                "conclusion": "Bob API unavailable",
                "confidence": 0.3,
                "recommendation": "Use fallback reasoning"
            }
        
        try:
            reasoning_result = self.bob_api.reason(question, evidence)
            self.bob.log("Bob Reasoning",
                              f"Confidence: {reasoning_result.get('confidence', 0)}")
            return reasoning_result
        except Exception as e:
            self.bob.log("Bob Reasoning", f"Error: {e}")
            return {
                "conclusion": f"Reasoning failed: {e}",
                "confidence": 0.2,
                "recommendation": "Manual review required"
            }

    def _fallback_orchestration(self, state):
        """
        Fallback orchestration when Bob API is unavailable
        """
        self.bob.log("Bob Orchestrator", "Using fallback orchestration")
        
        # Simple rule-based fallback
        query = state.get("query", "").lower()
        
        if "data" in query or "sql" in query or "database" in query:
            next_agent = "sql"
        elif "predict" in query or "forecast" in query or "ml" in query:
            next_agent = "ml"
        elif "document" in query or "report" in query or "pdf" in query:
            next_agent = "retrieval"
        else:
            next_agent = "planner"
        
        state["next_agent"] = next_agent
        state["orchestration_reasoning"] = "Fallback rule-based decision"
        state["orchestration_confidence"] = 0.5
        
        self.emit("orchestration_complete", f"Fallback: {next_agent}", {})
        
        return state

# Made with Bob
