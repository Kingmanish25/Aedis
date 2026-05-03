from orchestration.reasoning_controller import ReasoningController
from decision.decision_engine import DecisionEngine
from execution.executor import Executor
from app.config import Config
from memory.memory_manager import MemoryManager
from memory.graph_builder import GraphBuilder
from event_bus.schemas import Event
import traceback

class Workflow:
    def __init__(self, agents, event_bus):
        self.agents = agents
        self.controller = ReasoningController()
        self.decision_engine = DecisionEngine()
        self.executor = Executor()
        self.event_bus = event_bus
        self.memory = MemoryManager()
        self.graph_builder = GraphBuilder()
        
    def _run_agent_safely(self, agent_name, state):
        """Run an agent with error handling"""
        try:
            agent = self.agents.get(agent_name)
            if not agent:
                raise ValueError(f"Agent '{agent_name}' not found")
            
            return agent.run(state)
        except Exception as e:
            error_msg = f"Error in {agent_name} agent: {str(e)}"
            print(f"[WORKFLOW ERROR] {error_msg}")
            traceback.print_exc()
            
            # Add error to state but don't crash
            state["error"] = error_msg
            state["failed_agent"] = agent_name
            
            # Publish error event
            self.event_bus.publish(Event(
                "workflow",
                "agent_error",
                agent_name,
                {"error": error_msg}
            ))
            
            return state
        
    def run(self, query):
        """
        Execute the workflow with comprehensive error handling.
        Returns state dict with results or error information.
        """
        state = {
            "query": query,
            "iteration": 0,
            "confidence": 0.0,
            "error": None
        }
        
        try:
            # ===== Analysis Loop =====
            self.controller.reset()
            
            while True:
                state["iteration"] += 1
                
                # Run agents in sequence with error handling
                state = self._run_agent_safely("planner", state)
                if state.get("error") and state.get("failed_agent") == "planner":
                    # Critical failure in planner - can't continue
                    break
                
                state = self._run_agent_safely("sql", state)
                state = self._run_agent_safely("ml", state)
                state = self._run_agent_safely("insight", state)
                state = self._run_agent_safely("critic", state)

                if not self.controller.should_continue(state):
                    break

                # Prepare for next iteration
                state["query"] = f"Refine: {state['query']}"
                state["error"] = None  # Clear non-critical errors for retry

            # ===== Strategy =====
            state = self._run_agent_safely("strategy", state)

            # ===== Autonomous Mode =====
            if Config.AUTONOMOUS_MODE and not state.get("error"):
                try:
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
                        try:
                            res = self.executor.execute(a)
                            results.append({"action": a, "result": res})

                            self.event_bus.publish(Event(
                                "executor",
                                "action_executed",
                                a.get("name"),
                                res
                            ))
                        except Exception as e:
                            error_result = {
                                "action": a,
                                "result": {"status": "error", "error": str(e)}
                            }
                            results.append(error_result)
                            
                            self.event_bus.publish(Event(
                                "executor",
                                "action_failed",
                                a.get("name"),
                                {"error": str(e)}
                            ))

                    state["execution_results"] = results
                    
                    # Determine feedback based on results
                    successful_results = [r for r in results if r["result"].get("status") != "error"]
                    feedback = {
                        "success": len(successful_results) > 0,
                        "impact": "positive" if successful_results else "negative",
                        "total_actions": len(results),
                        "successful_actions": len(successful_results)
                    }

                    # Store in memory
                    self.memory.store({
                        "query": state["query"],
                        "actions": approved,
                        "results": results,
                        "confidence": state.get("confidence", 0),
                        "feedback": feedback
                    })
                    
                except Exception as e:
                    error_msg = f"Error in autonomous execution: {str(e)}"
                    print(f"[WORKFLOW ERROR] {error_msg}")
                    traceback.print_exc()
                    state["execution_error"] = error_msg
                    state["execution_results"] = []

            return state
            
        except Exception as e:
            # Catastrophic failure
            error_msg = f"Critical workflow error: {str(e)}"
            print(f"[WORKFLOW CRITICAL ERROR] {error_msg}")
            traceback.print_exc()
            
            state["critical_error"] = error_msg
            state["execution_results"] = []
            
            self.event_bus.publish(Event(
                "workflow",
                "critical_error",
                "workflow",
                {"error": error_msg}
            ))
            
            return state