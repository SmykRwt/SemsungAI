from flask import Flask
from app.routes.main import main

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.register_blueprint(main)
    return app
