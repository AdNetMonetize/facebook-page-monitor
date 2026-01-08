import os, requests
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SLACK_WEBHOOK_URL")

payload = {"text": "🚀 Teste Slack Webhook funcionando!"}
r = requests.post(url, json=payload)

print("Status:", r.status_code)
print("Resposta:", r.text)
