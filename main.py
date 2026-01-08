from monitor.facebook import get_page_state, validate_token
from storage.db import init_db, save_state, get_last_state, SessionLocal
from app.services.page_token_service import PageToken, init_page_token_db
from alerts.slack import send_slack_alert, format_status_message

def run():
    # Inicializa DB de estados e tokens
    init_db()
    init_page_token_db()

    with SessionLocal() as session:
        pages = session.query(PageToken).all()

    for page in pages:
        page_id = page.page_id
        token = page.access_token

        print(f"\n🔎 Validando token da página {page_id}...")

        debug = validate_token(token)
        if not debug:
            print("❌ Não foi possível validar o token (falha após retries). Pulando página.")
            continue

        data = debug.get("data", {})
        if not data.get("is_valid"):
            print(f"❌ Token inválido/expirado para página {page_id}.")
            try:
                send_slack_alert(f"❌ Token inválido/expirado para a página `{page_id}`. Atualize o token via sincronização.")
            except Exception as e:
                print(f"Falha ao enviar alerta Slack: {e}")
            continue

        print("✅ Token válido. Consultando estado da página...")

        current_state = get_page_state(page_id)
        if current_state is None:
            print("❌ Falha ao consultar estado da página após retries. Sem alerta.")
            continue

        print("📡 Estado atual:", current_state)

        last_state = get_last_state(page_id)
        print("💾 Último estado salvo:", last_state)

        if last_state != current_state:
            print("⚠️ Mudança detectada!")
            save_state(page_id, current_state)
            print("✅ Novo estado salvo no banco.")

            message = format_status_message(page_id, current_state, last_state)
            try:
                send_slack_alert(message)
            except Exception as e:
                print(f"Falha ao enviar alerta Slack: {e}")
        else:
            print("✅ Nenhuma mudança detectada.")

if __name__ == "__main__":
    run()
