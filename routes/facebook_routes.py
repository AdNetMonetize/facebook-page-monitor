from flask import Blueprint, request, jsonify
from app.services.page_token_service import synchronize_page_tokens

facebook_bp = Blueprint("facebook", __name__)

@facebook_bp.route("/facebook/sync-pages", methods=["POST"])
def sync_pages():
    """
    Endpoint para sincronizar tokens das páginas da BM.
    Espera receber no body JSON:
    {
        "user_token": "EAAB..."
    }
    """
    data = request.get_json()
    user_token = data.get("user_token")

    if not user_token:
        return jsonify({"error": "user_token é obrigatório"}), 400

    try:
        pages = synchronize_page_tokens(user_token)
        return jsonify({
            "message": "Sincronização concluída",
            "pages": pages
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
