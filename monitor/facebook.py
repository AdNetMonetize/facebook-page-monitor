import requests
from config.settings import GRAPH_API_VERSION, APP_ID, APP_SECRET
from utils.errors import call_api_with_retry
from storage.db import SessionLocal
from app.services.page_token_service import PageToken

BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

def get_page_token(page_id: str):
    with SessionLocal() as session:
        page = session.get(PageToken, page_id)
        if not page:
            raise ValueError(f"Token não encontrado para a página {page_id}")
        return page.access_token

def get_page_state(page_id: str):
    token = get_page_token(page_id)
    fields = "id,name,is_published,category,verification_status"
    url = f"{BASE_URL}/{page_id}"
    params = {"fields": fields, "access_token": token}
    return call_api_with_retry(url, params)

def validate_token(input_token: str):
    """
    Valida o token (user/page) com /debug_token.
    """
    url = "https://graph.facebook.com/debug_token"
    app_access_token = f"{APP_ID}|{APP_SECRET}"
    params = {
        "input_token": input_token,
        "access_token": app_access_token
    }
    return call_api_with_retry(url, params)

def get_page_roles(page_id: str):
    token = get_page_token(page_id)
    url = f"{BASE_URL}/{page_id}/roles"
    params = {"access_token": token}
    return call_api_with_retry(url, params)

def get_subscribed_apps(page_id: str):
    token = get_page_token(page_id)
    url = f"{BASE_URL}/{page_id}/subscribed_apps"
    params = {"access_token": token}
    return call_api_with_retry(url, params)
