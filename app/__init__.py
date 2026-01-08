from flask import Flask
from routes.facebook_routes import facebook_bp

def create_app():
    app = Flask(__name__)

    # registra rotas
    app.register_blueprint(facebook_bp)

    return app
