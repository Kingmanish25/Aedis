import os
from ibm_watsonx_ai.foundation_models import Model


class WatsonxClient:
    """
    Enterprise LLM Client using IBM watsonx.ai
    """

    def __init__(self):
        # Environment variables
        self.api_key = os.getenv("IBM_API_KEY")
        self.project_id = os.getenv("IBM_PROJECT_ID")
        self.url = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")

        if not self.api_key or not self.project_id:
            raise ValueError("❌ IBM_API_KEY and IBM_PROJECT_ID must be set")

        # Model (best default)
        self.model_id = "ibm/granite-13b-chat-v2"

        # Initialize model
        self.model = Model(
            model_id=self.model_id,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 300,
                "temperature": 0.5
            },
            credentials={
                "apikey": self.api_key,
                "url": self.url
            },
            project_id=self.project_id
        )

    def generate(self, prompt: str):
        """
        Generate response using watsonx
        """

        try:
            response = self.model.generate_text(prompt)

            if not response:
                raise ValueError("Empty response from IBM")

            return response

        except Exception as e:
            return self._fallback(str(e))

    def generate_structured(self, txn, risk):
        """
        AEIDS-specific structured output (fraud use case)
        """

        prompt = f"""
        You are an enterprise fraud detection AI.

        Transaction:
        {txn}

        Risk Score: {risk}

        Return ONLY valid JSON:
        {{
            "decision": "approve/block/review",
            "confidence": 0-1,
            "reason": "short explanation"
        }}
        """

        return self.generate(prompt)

    def _fallback(self, error):
        """
        Safe fallback (never crash system)
        """
        print("⚠️ Watsonx Error:", error)

        return {
            "status": "fallback",
            "decision": "review",
            "confidence": 0.5,
            "reason": "Watsonx unavailable, safe fallback triggered"
        }
