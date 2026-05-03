import requests
import os

class GroqClient:
    """Client for Groq API using llama3-8b-8192 model"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"
    
    def generate(self, prompt):
        try:
            res = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=200
            )
            print(res.text)
            
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            return f"LLM API error: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"LLM response parsing error: {str(e)}"
        except Exception as e:
            return f"LLM unexpected error: {str(e)}"
