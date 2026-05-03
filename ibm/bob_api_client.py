import os
import requests
from typing import Dict, Any, Optional


class BobAPIClient:
    """
    IBM watsonx.ai Bob AI Assistant API Client
    Provides advanced AI capabilities for orchestration and reasoning
    """

    def __init__(self):
        # Environment variables for Bob API
        self.api_key = os.getenv("BOB_API_KEY")
        self.project_id = os.getenv("IBM_PROJECT_ID")
        self.url = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
        
        if not self.api_key:
            raise ValueError("❌ BOB_API_KEY must be set in environment variables")
        
        self.base_url = f"{self.url}/ml/v1/text/generation"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Bob-specific model configuration
        self.model_id = "ibm/granite-20b-multilingual"  # Bob's preferred model
        self.logs = []

    def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Generate response using Bob AI Assistant
        
        Args:
            prompt: Input prompt for Bob
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            
        Returns:
            Generated text response
        """
        try:
            payload = {
                "model_id": self.model_id,
                "input": prompt,
                "parameters": {
                    "decoding_method": "sample",
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,
                    "top_k": 50
                },
                "project_id": self.project_id
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("results", [{}])[0].get("generated_text", "")
                self.log("Bob Generate", f"Success: {len(generated_text)} chars")
                return generated_text
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                self.log("Bob Generate", f"Failed: {error_msg}")
                return self._fallback(error_msg)
                
        except Exception as e:
            error_msg = f"Exception: {str(e)}"
            self.log("Bob Generate", f"Error: {error_msg}")
            return self._fallback(error_msg)

    def orchestrate(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Bob for intelligent orchestration decisions
        
        Args:
            task: The task to orchestrate
            context: Current context and state
            
        Returns:
            Orchestration decision with next steps
        """
        prompt = f"""You are Bob, an advanced AI orchestration assistant.

Task: {task}

Current Context:
{self._format_context(context)}

Analyze the task and context, then provide orchestration guidance in JSON format:
{{
    "next_agent": "agent_name",
    "reasoning": "why this agent should be next",
    "priority": "high/medium/low",
    "estimated_confidence": 0.0-1.0,
    "suggested_parameters": {{}}
}}
"""
        
        response = self.generate(prompt, max_tokens=300, temperature=0.5)
        self.log("Bob Orchestrate", f"Task: {task[:50]}...")
        
        try:
            # Try to parse JSON response
            import json
            return json.loads(response)
        except:
            # Fallback to structured response
            return {
                "next_agent": "planner",
                "reasoning": "Default fallback to planner",
                "priority": "medium",
                "estimated_confidence": 0.5,
                "suggested_parameters": {}
            }

    def reason(self, question: str, evidence: list) -> Dict[str, Any]:
        """
        Use Bob for advanced reasoning over evidence
        
        Args:
            question: Question to reason about
            evidence: List of evidence items
            
        Returns:
            Reasoning result with conclusion and confidence
        """
        evidence_text = "\n".join([f"- {e}" for e in evidence])
        
        prompt = f"""You are Bob, an advanced reasoning AI assistant.

Question: {question}

Evidence:
{evidence_text}

Analyze the evidence and provide your reasoning in JSON format:
{{
    "conclusion": "your conclusion",
    "confidence": 0.0-1.0,
    "supporting_evidence": ["key points"],
    "potential_issues": ["concerns if any"],
    "recommendation": "what to do next"
}}
"""
        
        response = self.generate(prompt, max_tokens=400, temperature=0.6)
        self.log("Bob Reason", f"Question: {question[:50]}...")
        
        try:
            import json
            return json.loads(response)
        except:
            return {
                "conclusion": "Unable to parse reasoning",
                "confidence": 0.3,
                "supporting_evidence": [],
                "potential_issues": ["Response parsing failed"],
                "recommendation": "Review manually"
            }

    def log(self, step: str, msg: str):
        """Log Bob's activities"""
        entry = f"[BOB AI] {step}: {msg}"
        self.logs.append(entry)
        print(entry)

    def get_logs(self) -> list:
        """Get all Bob logs"""
        return self.logs

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary for prompt"""
        lines = []
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{key}: {str(value)[:100]}...")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)

    def _fallback(self, error: str) -> str:
        """Safe fallback response"""
        return f"Bob AI Assistant temporarily unavailable. Error: {error}"

# Made with Bob
