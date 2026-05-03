import requests
import os

class OllamaClient:
    def generate(self, prompt):
        try:
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('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')}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=20
            )

            return res.json()["choices"][0]["message"]["content"]

        except Exception as e:
            return f"LLM error: {str(e)}"