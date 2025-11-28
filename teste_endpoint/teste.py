import requests
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

payload = {
    "model": "sonar",
    "messages": [
        {"role": "user", "content": "responda em menos de 100 caracteres quais os 3 heroes mais jogados no dota em 2025"}
    ]
}
headers = {
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json"
}
r = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=payload)
print(r.status_code, r.text)