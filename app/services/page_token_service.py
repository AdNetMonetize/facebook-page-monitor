import requests
import os
from storage.db import SessionLocal, engine
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

FACEBOOK_API_VERSION = os.getenv("GRAPH_API_VERSION", "v23.0")
APP_ID = os.getenv("FB_APP_ID")
APP_SECRET = os.getenv("FB_APP_SECRET")

Base = declarative_base()

class PageToken(Base):
    __tablename__ = "page_tokens"
    page_id = Column(String, primary_key=True)
    page_name = Column(String)
    access_token = Column(String)

def init_page_token_db():
    Base.metadata.create_all(bind=engine)

def exchange_for_long_lived_token(user_token: str) -> str:
    """
    Troca User Token por Long-Lived Token (60 dias)
    """
    url = f"https://graph.facebook.com/{FACEBOOK_API_VERSION}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": user_token
    }
    res = requests.get(url, params=params)
    data = res.json()
    if "access_token" not in data:
        raise Exception(f"Erro ao trocar token: {data}")
    return data["access_token"]

def get_pages(long_lived_token: str):
    """
    Lista todas as páginas que o usuário administra
    """
    url = f"https://graph.facebook.com/{FACEBOOK_API_VERSION}/me/accounts"
    params = {
        "fields": "id,name,access_token",
        "access_token": long_lived_token
    }
    res = requests.get(url, params=params)
    data = res.json()
    if "data" not in data:
        raise Exception(f"Erro ao buscar páginas: {data}")
    return data["data"]

def synchronize_page_tokens(user_token: str):
    """
    Fluxo completo:
    1. Troca User Token por Long-Lived Token
    2. Busca páginas e tokens
    3. Salva/atualiza no banco
    """
    long_lived_token = exchange_for_long_lived_token(user_token)
    pages = get_pages(long_lived_token)

    with SessionLocal() as session:
        for page in pages:
            page_id = page["id"]
            page_name = page["name"]
            page_token = page["access_token"]

            existing = session.get(PageToken, page_id)
            if not existing:
                session.add(PageToken(page_id=page_id, page_name=page_name, access_token=page_token))
            else:
                existing.page_name = page_name
                existing.access_token = page_token
            session.commit()
    return pages
