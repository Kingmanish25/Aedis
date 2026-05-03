import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from llm.ollama_client import WatsonxClient
from ibm.bob_client import BobClient
from ibm.bob_api_client import BobAPIClient

from agents.planner_agent import PlannerAgent
from agents.retrieval_agent import RetrievalAgent
from agents.sql_agent import SQLAgent
from agents.ml_agent import MLAgent
from agents.critic_agent import CriticAgent
from agents.strategy_agent import StrategyAgent
from agents.explanation_agent import ExplanationAgent
from agents.insight_agent import InsightAgent
from agents.bob_orchestrator_agent import BobOrchestratorAgent
from orchestration.workflow import Workflow
from ui.streamlit_app import run_app
from event_bus.producer import EventProducer
from utils.service_checker import ServiceChecker
from app.config import Config

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
    llm = WatsonxClient()
    print("✓ LLM client initialized successfully")
except ValueError as e:
    print(f"✗ Error initializing LLM client: {e}")
    print("Please set IBM_API_KEY and IBM_PROJECT_ID environment variables")
    sys.exit(1)

bob = BobClient()
event_bus = EventProducer()

# Initialize Bob AI API client if enabled
bob_api = None
if Config.BOB_ENABLED:
    try:
        bob_api = BobAPIClient()
        print("✓ Bob AI Assistant API initialized successfully")
    except Exception as e:
        print(f"⚠️ Bob AI API initialization failed: {e}")
        print("  Continuing with standard agents only")

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

# Add Bob Orchestrator agent if Bob API is available
if bob_api and Config.BOB_ENABLED:
    agents["bob_orchestrator"] = BobOrchestratorAgent("bob_orchestrator", llm, bob, event_bus)
    print("✓ Bob Orchestrator agent added")

print(f"✓ {len(agents)} agents initialized")

bob.logs = []
workflow = Workflow(agents, event_bus)
print("✓ Workflow initialized")
print("=" * 60)


if __name__ == "__main__":
    run_app(workflow, bob, event_bus)