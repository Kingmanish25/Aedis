"""
Agent dependency management for workflow orchestration.
Defines dependencies between agents and validates execution order.
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass


@dataclass
class AgentDependency:
    """Defines dependencies for an agent"""
    agent_name: str
    requires: List[str]  # List of agent names that must run before this one
    provides: List[str]  # List of state keys this agent provides
    optional_requires: Optional[List[str]] = None  # Optional dependencies
    
    def __post_init__(self):
        if self.optional_requires is None:
            self.optional_requires = []


class DependencyManager:
    """Manages agent dependencies and execution order"""
    
    # Define agent dependencies
    DEPENDENCIES = {
        "planner": AgentDependency(
            agent_name="planner",
            requires=[],  # No dependencies - runs first
            provides=["plan", "confidence"]
        ),
        "retrieval": AgentDependency(
            agent_name="retrieval",
            requires=["planner"],
            provides=["retrieved_docs"],
            optional_requires=[]
        ),
        "sql": AgentDependency(
            agent_name="sql",
            requires=["planner"],
            provides=["sql_result", "sql_query"],
            optional_requires=["retrieval"]
        ),
        "ml": AgentDependency(
            agent_name="ml",
            requires=["sql"],  # Needs data from SQL
            provides=["ml_result", "predictions"],
            optional_requires=["retrieval"]
        ),
        "insight": AgentDependency(
            agent_name="insight",
            requires=["sql", "ml"],  # Needs both data and predictions
            provides=["insights"],
            optional_requires=["retrieval"]
        ),
        "critic": AgentDependency(
            agent_name="critic",
            requires=["planner", "sql", "ml", "insight"],  # Reviews all previous work
            provides=["critique", "confidence"],
            optional_requires=[]
        ),
        "strategy": AgentDependency(
            agent_name="strategy",
            requires=["critic"],  # Needs critique to form strategy
            provides=["strategy", "strategy_structured"],
            optional_requires=["insight"]
        ),
        "explanation": AgentDependency(
            agent_name="explanation",
            requires=["strategy"],  # Explains the strategy
            provides=["explanation"],
            optional_requires=["insight", "critique"]
        )
    }
    
    @classmethod
    def get_dependency(cls, agent_name: str) -> Optional[AgentDependency]:
        """Get dependency info for an agent"""
        return cls.DEPENDENCIES.get(agent_name)
    
    @classmethod
    def validate_execution_order(cls, agent_order: List[str]) -> tuple[bool, Optional[str]]:
        """
        Validate that agents are executed in correct dependency order.
        
        Args:
            agent_order: List of agent names in execution order
            
        Returns:
            (is_valid, error_message)
        """
        executed = set()
        
        for agent_name in agent_order:
            dep = cls.get_dependency(agent_name)
            
            if not dep:
                return False, f"Unknown agent: {agent_name}"
            
            # Check required dependencies
            for required in dep.requires:
                if required not in executed:
                    return False, f"Agent '{agent_name}' requires '{required}' to run first"
            
            executed.add(agent_name)
        
        return True, None
    
    @classmethod
    def get_execution_order(cls, agents: List[str]) -> List[str]:
        """
        Get optimal execution order for given agents based on dependencies.
        Uses topological sort.
        
        Args:
            agents: List of agent names to order
            
        Returns:
            Ordered list of agent names
        """
        # Build dependency graph
        graph = {agent: [] for agent in agents}
        in_degree = {agent: 0 for agent in agents}
        
        for agent in agents:
            dep = cls.get_dependency(agent)
            if dep:
                for required in dep.requires:
                    if required in agents:
                        graph[required].append(agent)
                        in_degree[agent] += 1
        
        # Topological sort using Kahn's algorithm
        queue = [agent for agent in agents if in_degree[agent] == 0]
        result = []
        
        while queue:
            # Sort queue for consistent ordering
            queue.sort()
            current = queue.pop(0)
            result.append(current)
            
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(agents):
            # Circular dependency detected
            raise ValueError("Circular dependency detected in agent graph")
        
        return result
    
    @classmethod
    def check_state_requirements(cls, agent_name: str, state: Dict) -> tuple[bool, List[str]]:
        """
        Check if state has all required data for an agent to run.
        
        Args:
            agent_name: Name of the agent
            state: Current workflow state
            
        Returns:
            (has_requirements, missing_keys)
        """
        dep = cls.get_dependency(agent_name)
        if not dep:
            return True, []
        
        missing = []
        
        # Check that required agents have provided their outputs
        for required_agent in dep.requires:
            required_dep = cls.get_dependency(required_agent)
            if required_dep:
                for provided_key in required_dep.provides:
                    if provided_key not in state or state[provided_key] is None:
                        missing.append(f"{provided_key} (from {required_agent})")
        
        return len(missing) == 0, missing
    
    @classmethod
    def get_dependency_graph(cls) -> Dict[str, List[str]]:
        """
        Get a simple dependency graph representation.
        
        Returns:
            Dict mapping agent names to their dependencies
        """
        return {
            name: dep.requires
            for name, dep in cls.DEPENDENCIES.items()
        }
    
    @classmethod
    def get_agents_ready_to_run(cls, executed_agents: Set[str], all_agents: List[str]) -> List[str]:
        """
        Get list of agents that can run given what has already executed.
        
        Args:
            executed_agents: Set of agent names that have already run
            all_agents: List of all available agent names
            
        Returns:
            List of agent names ready to run
        """
        ready = []
        
        for agent in all_agents:
            if agent in executed_agents:
                continue
            
            dep = cls.get_dependency(agent)
            if not dep:
                continue
            
            # Check if all required dependencies have executed
            if all(req in executed_agents for req in dep.requires):
                ready.append(agent)
        
        return ready

# Made with Bob
