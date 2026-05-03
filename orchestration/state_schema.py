from typing import TypedDict, Any, Dict

class AgentState(TypedDict, total=False):
    query: str
    plan: str
    sql: str
    data: Any
    ml_result: Dict
    insights: str
    confidence: float
    iteration: int
    error: str