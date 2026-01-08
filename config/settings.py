import os
from dotenv import load_dotenv

load_dotenv()

# Versão da Graph API (padrão v19.0). Pode ser ajustada via .env: GRAPH_API_VERSION=v19.0
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v19.0")

# Credenciais do app (usadas na validação de token /debug_token)
APP_ID = os.getenv("FB_APP_ID", "")
APP_SECRET = os.getenv("FB_APP_SECRET", "")

# Mapa de tokens de página: FB_PAGE_TOKENS="123:EAAB...,456:EAAB..."
raw_tokens = os.getenv("FB_PAGE_TOKENS", "")
PAGE_TOKEN_MAP = {}

if raw_tokens:
    for pair in raw_tokens.split(","):
        # Ignora pares malformados
        if ":" not in pair:
            continue
        page_id, token = pair.split(":", 1)  # 1 para não quebrar tokens que contêm ':'
        PAGE_TOKEN_MAP[page_id.strip()] = token.strip()
