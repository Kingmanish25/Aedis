import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from llm.ollama_client import GroqClient
from ibm.bob_client import BobClient

from agents.planner_agent import PlannerAgent
from agents.retrieval_agent import RetrievalAgent
from agents.sql_agent import SQLAgent
from agents.ml_agent import MLAgent
from agents.critic_agent import CriticAgent
from agents.strategy_agent import StrategyAgent
from agents.explanation_agent import ExplanationAgent
from agents.insight_agent import InsightAgent
from orchestration.workflow import Workflow
from ui.streamlit_app import run_app
from event_bus.producer import EventProducer
from utils.service_checker import ServiceChecker

# Validate services before starting
print("=" * 60)
print("AEDIS AI - Autonomous Decision Intelligence System")
print("=" * 60)

# Check all services
try:
    ServiceChecker.validate_or_exit()
except SystemExit:
    # Service check failed, exit gracefully
    sys.exit(1)

# Initialize LLM client with error handling
try:
    llm = GroqClient()
    print("✓ LLM client initialized successfully")
except ValueError as e:
    print(f"✗ Error initializing LLM client: {e}")
    print("Please set GROQ_API_KEY environment variable")
    sys.exit(1)

bob = BobClient()
event_bus = EventProducer()

# Initialize agents
print("Initializing agents...")
agents = {
    "planner": PlannerAgent("planner", llm, bob, event_bus),
    "retrieval": RetrievalAgent("retrieval", llm, bob, event_bus),
    "sql": SQLAgent("sql", llm, bob, event_bus),
    "ml": MLAgent("ml", llm, bob, event_bus),
    "critic": CriticAgent("critic", llm, bob, event_bus),
    "strategy": StrategyAgent("strategy", llm, bob, event_bus),
    "explanation": ExplanationAgent("explanation", llm, bob, event_bus),
    "insight": InsightAgent("insight", llm, bob, event_bus),
}
print(f"✓ {len(agents)} agents initialized")

bob.logs = []
workflow = Workflow(agents, event_bus)
print("✓ Workflow initialized")
print("=" * 60)


if __name__ == "__main__":
    run_app(workflow, bob, event_bus)