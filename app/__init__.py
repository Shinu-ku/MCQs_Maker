# app/__init__.py
from flask import Flask
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))

    from .route import main
    app.register_blueprint(main)

    return app
