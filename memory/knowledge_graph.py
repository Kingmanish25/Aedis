import networkx as nx
import json
from datetime import datetime

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_data = {}  # Store structured data for nodes

    def add_causal_fact(self, cause, effect, weight=1.0, metadata=None):
        """
        Add a causal relationship to the graph.
        
        Args:
            cause: Source node (can be string or dict)
            effect: Target node (can be string or dict)
            weight: Strength of the relationship
            metadata: Additional structured data about the relationship
        """
        # Create node IDs
        cause_id = self._get_node_id(cause)
        effect_id = self._get_node_id(effect)
        
        # Store structured data
        self.node_data[cause_id] = cause if isinstance(cause, dict) else {"value": cause}
        self.node_data[effect_id] = effect if isinstance(effect, dict) else {"value": effect}
        
        # Add edge with metadata
        edge_data = {
            "relation": "causes",
            "weight": weight,
            "timestamp": datetime.now().isoformat()
        }
        if metadata:
            edge_data.update(metadata)
        
        self.graph.add_edge(cause_id, effect_id, **edge_data)

    def add_memory(self, memory_entry):
        """
        Add a memory entry to the knowledge graph, preserving structure.
        
        Args:
            memory_entry: Dict containing query, actions, results, etc.
        """
        query = memory_entry.get("query", "")
        actions = memory_entry.get("actions", [])
        results = memory_entry.get("results", [])
        confidence = memory_entry.get("confidence", 0)
        feedback = memory_entry.get("feedback", {})
        
        # Create query node
        query_id = f"query_{hash(query)}"
        self.node_data[query_id] = {
            "type": "query",
            "text": query,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add actions and their relationships
        for idx, action in enumerate(actions):
            action_id = f"action_{hash(json.dumps(action, sort_keys=True))}_{idx}"
            self.node_data[action_id] = {
                "type": "action",
                "name": action.get("name", "unknown"),
                "action_type": action.get("type", "unknown"),
                "payload": action.get("payload", {})
            }
            
            # Link query to action
            self.graph.add_edge(
                query_id,
                action_id,
                relation="triggers",
                weight=confidence,
                timestamp=datetime.now().isoformat()
            )
            
            # Link actions to results
            if idx < len(results):
                result = results[idx]
                result_id = f"result_{action_id}"
                self.node_data[result_id] = {
                    "type": "result",
                    "action_name": action.get("name", "unknown"),
                    "result": result.get("result", {}),
                    "feedback": feedback
                }
                
                self.graph.add_edge(
                    action_id,
                    result_id,
                    relation="produces",
                    weight=1.0 if feedback.get("success") else 0.5,
                    timestamp=datetime.now().isoformat()
                )

    def _get_node_id(self, node):
        """Generate a consistent node ID"""
        if isinstance(node, dict):
            return f"node_{hash(json.dumps(node, sort_keys=True))}"
        return f"node_{hash(str(node))}"

    def query(self, node):
        """
        Query the graph for relationships of a node.
        
        Returns list of (source, target, edge_data) tuples
        """
        node_id = self._get_node_id(node)
        if node_id not in self.graph:
            return []

        edges = list(self.graph.edges(node_id, data=True))
        
        # Enrich with node data
        enriched = []
        for source, target, edge_data in edges:
            enriched.append({
                "source": self.node_data.get(source, {}),
                "target": self.node_data.get(target, {}),
                "relationship": edge_data
            })
        
        return enriched

    def get_all(self):
        """Get all edges with enriched node data"""
        edges = list(self.graph.edges(data=True))
        
        enriched = []
        for source, target, edge_data in edges:
            enriched.append({
                "source": self.node_data.get(source, {}),
                "target": self.node_data.get(target, {}),
                "relationship": edge_data
            })
        
        return enriched
    
    def get_node_data(self, node_id):
        """Get structured data for a specific node"""
        return self.node_data.get(node_id, {})
    
    def find_similar_queries(self, query_text, limit=5):
        """Find similar queries in the graph"""
        similar = []
        for node_id, data in self.node_data.items():
            if data.get("type") == "query":
                # Simple similarity based on word overlap
                query_words = set(query_text.lower().split())
                node_words = set(data.get("text", "").lower().split())
                overlap = len(query_words & node_words)
                if overlap > 0:
                    similar.append((node_id, data, overlap))
        
        # Sort by overlap and return top results
        similar.sort(key=lambda x: x[2], reverse=True)
        return [{"node_id": nid, "data": data, "similarity": sim}
                for nid, data, sim in similar[:limit]]