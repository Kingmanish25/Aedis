import requests
import os

class GroqClient:
    """Client for Groq API using llama3-8b-8192 model"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        #self.model = "llama3-8b-8192"
    
    def generate(self, prompt):
        try:
            res = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7
                },
                timeout=120
            )
            
            
            if res.status_code != 200:
                return f"Groq Error: {res.status_code} - {res.text}"

            data = res.json()

            if "choices" not in data:
                return f"Invalid response: {data}"

            return data["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            return f"LLM API error: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"LLM response parsing error: {str(e)}"
        except Exception as e:
            return f"LLM unexpected error: {str(e)}"
