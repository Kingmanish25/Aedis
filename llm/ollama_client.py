import requests
import os
import time


class GroqClient:
    """Multi-LLM Client: Groq (primary) + Together AI (fallback)"""

    def __init__(self):
        # API Keys
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.together_api_key = os.getenv("TOGETHER_API_KEY")

        if not self.groq_api_key and not self.together_api_key:
            raise ValueError("❌ At least one API key (GROQ or TOGETHER) must be set")

        # Endpoints
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.together_url = "https://api.together.xyz/v1/chat/completions"

        # Models
        self.groq_model = "llama3-8b-8192"
        self.together_model = "meta-llama/Llama-3-8b-chat-hf"

    def generate(self, prompt):
        """Smart routing: Groq → Together → Fallback"""

        # 1️⃣ Try Groq first
        if self.groq_api_key:
            try:
                return self._call_groq(prompt)
            except Exception as e:
                print("⚠️ Groq failed:", e)

        # 2️⃣ Fallback to Together AI
        if self.together_api_key:
            try:
                return self._call_together(prompt)
            except Exception as e:
                print("⚠️ Together AI failed:", e)

        # 3️⃣ Final fallback (never crash)
        return self._fallback("All LLM providers failed")

    # ---------------- GROQ ----------------
    def _call_groq(self, prompt):
        res = requests.post(
            self.groq_url,
            headers={
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.groq_model,
                "messages": [
                    
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            timeout=30
        )

        if res.status_code != 200:
            raise Exception(f"Groq Error {res.status_code}: {res.text}")

        data = res.json()

        if "choices" not in data or not data["choices"]:
            raise Exception(f"Invalid Groq response: {data}")

        return data["choices"][0]["message"]["content"]

    # ---------------- TOGETHER AI ----------------
    def _call_together(self, prompt):
        res = requests.post(
            self.together_url,
            headers={
                "Authorization": f"Bearer {self.together_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.together_model,
                "messages": [
                    {"role": "system", "content": "You are a fraud detection AI. Respond clearly."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 512
            },
            timeout=30
        )

        if res.status_code != 200:
            raise Exception(f"Together Error {res.status_code}: {res.text}")

        data = res.json()

        if "choices" not in data or not data["choices"]:
            raise Exception(f"Invalid Together response: {data}")

        return data["choices"][0]["message"]["content"]

    # ---------------- FALLBACK ----------------
    def _fallback(self, error):
        print("⚠️ FINAL FALLBACK:", error)

        return {
            "status": "fallback",
            "decision": "review",
            "confidence": 0.5,
            "reason": "LLM unavailable, using safe fallback"
        }
