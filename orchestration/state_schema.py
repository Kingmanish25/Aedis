"""
State validation schema for workflow state management.
Provides type checking and validation for state dictionaries.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class WorkflowState:
    """
    Structured state object for workflow execution.
    Replaces the mutable dictionary approach with a validated dataclass.
    """
    query: str
    iteration: int = 0
    confidence: float = 0.0
    error: Optional[str] = None
    failed_agent: Optional[str] = None
    
    # Agent outputs
    plan: Optional[Dict[str, Any]] = None
    sql_result: Optional[Dict[str, Any]] = None
    ml_result: Optional[Dict[str, Any]] = None
    insights: Optional[List[str]] = None
    critique: Optional[Dict[str, Any]] = None
    strategy: Optional[str] = None
    strategy_structured: Optional[Dict[str, Any]] = None
    explanation: Optional[str] = None
    
    # Decision and execution
    ranked_actions: Optional[List[tuple]] = None
    selected_actions: Optional[List[Dict[str, Any]]] = None
    approved_actions: Optional[List[Dict[str, Any]]] = None
    execution_results: List[Dict[str, Any]] = field(default_factory=list)
    execution_error: Optional[str] = None
    
    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    critical_error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowState':
        """Create WorkflowState from dictionary"""
        # Filter out keys that aren't in the dataclass
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)
    
    def has_error(self) -> bool:
        """Check if state has any error"""
        return bool(self.error or self.critical_error or self.execution_error)
    
    def is_complete(self) -> bool:
        """Check if workflow has completed successfully"""
        return (
            self.confidence >= 0.8 and
            not self.has_error() and
            self.strategy is not None
        )
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the current state"""
        return {
            "query": self.query,
            "iteration": self.iteration,
            "confidence": self.confidence,
            "has_error": self.has_error(),
            "is_complete": self.is_complete(),
            "agents_completed": [
                k for k in ["plan", "sql_result", "ml_result", "insights", "critique", "strategy"]
                if getattr(self, k) is not None
            ],
            "actions_executed": len(self.execution_results)
        }


def validate_state(state: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate a state dictionary.
    
    Returns:
        (is_valid, error_message)
    """
    required_fields = ["query"]
    
    for field in required_fields:
        if field not in state:
            return False, f"Missing required field: {field}"
    
    # Type validation
    if not isinstance(state.get("query"), str):
        return False, "Query must be a string"
    
    if "iteration" in state and not isinstance(state["iteration"], int):
        return False, "Iteration must be an integer"
    
    if "confidence" in state:
        conf = state["confidence"]
        if not isinstance(conf, (int, float)) or not (0 <= conf <= 1):
            return False, "Confidence must be a number between 0 and 1"
    
    return True, None


def merge_states(base_state: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safely merge state updates into base state.
    
    Args:
        base_state: Original state dictionary
        updates: Updates to apply
        
    Returns:
        Merged state dictionary
    """
    merged = base_state.copy()
    merged.update(updates)
    return merged

# Made with Bob
