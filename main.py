import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

response = requests.post(
    OLLAMA_URL,
    json={
        "model": "llama3.2",
        "messages": [
            {"role": "user", "content": "Hi"}
        ],
        "stream": False
    },
    timeout=120
)

response.raise_for_status()
answer = response.json()["message"]["content"]
print(answer)
