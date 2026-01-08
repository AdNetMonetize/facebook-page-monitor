import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

DEFAULT_RETRIES = 3
DEFAULT_DELAY = 2
DEFAULT_TIMEOUT = 10


def send_slack_alert(message: str, retries: int = DEFAULT_RETRIES, delay: int = DEFAULT_DELAY):
    """
    Envia alerta ao Slack com retries simples em caso de falha.
    """
    if not SLACK_WEBHOOK_URL:
        raise ValueError("Webhook do Slack não configurado no .env")

    payload = {"text": message}
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=DEFAULT_TIMEOUT)

            if response.status_code == 200:
                return True  # sucesso
            else:
                print(f"Tentativa {attempt} falhou: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            last_error = e
            print(f"Erro de rede na tentativa {attempt}: {e}")

        time.sleep(delay)

    print(f"Todas as tentativas de envio ao Slack falharam. Último erro: {last_error}")
    return False


def format_status_message(page_id, current_state, last_state=None, last_roles=None, current_roles=None, last_apps=None, current_apps=None):
    """
    Formata mensagens personalizadas para o Slack dependendo da alteração detectada.
    """
    name = current_state.get("name", "Página desconhecida")
    is_published = current_state.get("is_published")
    verification_status = current_state.get("verification_status")

    # Primeira vez monitorando
    if not last_state:
        return (
            f"🆕 Nova página monitorada!\n"
            f"• Nome: *{name}*\n"
            f"• ID: `{page_id}`\n"
            f"• Publicada: `{is_published}`\n"
            f"• Verificação: `{verification_status}`"
        )

    # Mudança de publicação
    if last_state.get("is_published") != is_published:
        if is_published:
            return f"✅ Página *{name}* (ID: `{page_id}`)\nA página foi **ativada** e está publicada novamente."
        else:
            return f"⛔ Página *{name}* (ID: `{page_id}`)\nA página foi **desativada** e não está mais publicada."

    # Mudança de verificação
    if last_state.get("verification_status") != verification_status:
        if verification_status == "disabled":
            return f"🚫 Página *{name}* (ID: `{page_id}`)\nA página foi **bloqueada** pelo Facebook."
        elif verification_status == "unverified":
            return f"⚠️ Página *{name}* (ID: `{page_id}`)\nA página está **com restrição** (não verificada)."
        else:
            return f"ℹ️ Página *{name}* (ID: `{page_id}`)\nStatus de verificação alterado para: `{verification_status}`"

    # Mudança de administradores
    if last_roles and current_roles and last_roles != current_roles:
        return f"👤 Página *{name}* (ID: `{page_id}`)\nMudança na lista de administradores detectada."

    # Mudança de apps conectados
    if last_apps and current_apps and last_apps != current_apps:
        return f"🔌 Página *{name}* (ID: `{page_id}`)\nMudança nos aplicativos conectados à página."

    # Mudança de categoria
    if last_state.get("category") != current_state.get("category"):
        return (
            f"🔄 Página *{name}* (ID: `{page_id}`)\n"
            f"Categoria alterada: `{last_state.get('category')}` → `{current_state.get('category')}`"
        )

    return f"🚨 Página *{name}* (ID: `{page_id}`)\nMudança detectada, mas não foi possível classificar."
