from flask import Flask, request, redirect, render_template
import requests

app = Flask(__name__)

APP_ID = "1408735340913911"
APP_SECRET = "77457113c6ba028762c76ee8346b546c"
REDIRECT_URI = "https://brecken-nontheosophic-denice.ngrok-free.dev/callback"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    fb_login_url = (
        f"https://www.facebook.com/v23.0/dialog/oauth?"
        f"client_id={APP_ID}&redirect_uri={REDIRECT_URI}&"
        f"scope=pages_show_list,pages_read_engagement"
    )
    return redirect(fb_login_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Erro: nenhum code recebido", 400

    # Token curto
    token_url = "https://graph.facebook.com/v23.0/oauth/access_token"
    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "client_secret": APP_SECRET,
        "code": code
    }
    res = requests.get(token_url, params=params)
    short_token_data = res.json()

    if "access_token" not in short_token_data:
        return f"Erro ao obter token curto: {short_token_data}", 400

    short_token = short_token_data["access_token"]

    # Troca por token longo
    exchange_url = "https://graph.facebook.com/v23.0/oauth/access_token"
    exchange_params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": short_token
    }
    exchange_res = requests.get(exchange_url, params=exchange_params)
    long_token_data = exchange_res.json()

    return {
        "token_curto": short_token_data,
        "token_longo": long_token_data
    }

if __name__ == "__main__":
    app.run(port=5000, debug=True)
