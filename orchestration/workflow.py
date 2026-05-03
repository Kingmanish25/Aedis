from orchestration.reasoning_controller import ReasoningController
from decision.decision_engine import DecisionEngine
from execution.executor import Executor
from app.config import Config
from memory.memory_manager import MemoryManager
from memory.graph_builder import GraphBuilder

class Workflow:
    def __init__(self, agents, event_bus):
        self.agents = agents
        self.controller = ReasoningController()
        self.decision_engine = DecisionEngine()
        self.executor = Executor()
        self.event_bus = event_bus
        self.memory = MemoryManager()
        self.graph_builder = GraphBuilder()
        
    def run(self, query):
        state = {"query": query, "iteration": 0}

        # ===== Analysis Loop =====
        while True:
            state = self.agents["planner"].run(state)
            state = self.agents["sql"].run(state)
            state = self.agents["ml"].run(state)
            state = self.agents["insight"].run(state)
            state = self.agents["critic"].run(state)

            if not self.controller.should_continue(state):
                break

            state["query"] = f"Refine: {state['query']}"
            state["error"] = None

        # ===== Strategy =====
        state = self.agents["strategy"].run(state)

        # ===== Autonomous Mode =====
        if Config.AUTONOMOUS_MODE:
            actions = state.get("strategy_structured", {}).get("actions", [])

            selected, ranked = self.decision_engine.select(actions)

            state["ranked_actions"] = ranked
            state["selected_actions"] = selected

            approved = state.get("approved_actions", [])

            if not approved:
                # No approval → skip execution
                state["execution_results"] = []
                return state

            results = []

            for a in approved:
                res = self.executor.execute(a)
                results.append({"action": a, "result": res})

                from event_bus.schemas import Event
                self.event_bus.publish(Event(
                    "executor",
                    "action_executed",
                    a.get("name"),
                    res
                ))

            state["execution_results"] = results
            feedback = {
                "success": True if results else False,
                "impact": "positive" if results else "unknown"
            }

            self.memory.store({
                "query": state["query"],
                "actions": approved,
                "results": results,
                "confidence": state["confidence"],
                "feedback": feedback
            })

        return state