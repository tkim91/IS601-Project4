"""A simple flask web app"""
import os

import flask_login
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_cors import CORS

from app.auth import auth
from app.cli import create_database
from app.db import db, database
from app.db.models import User
from app.error_handlers import error_handlers
from app.logging_configs import log_con
from app.simple_pages import simple_pages
from app.transactions import transactions
from app.context_processors import utility_text_processors

login_manager = flask_login.LoginManager()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")
#    app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf = CSRFProtect(app)
    bootstrap = Bootstrap5(app)

    app.register_blueprint(auth)
    app.register_blueprint(database)
    app.register_blueprint(simple_pages)
    app.register_blueprint(log_con)
    app.register_blueprint(error_handlers)
    app.register_blueprint(transactions)
    app.context_processor(utility_text_processors)

    db_dir = "database/db.sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # add command function to cli commands
    app.cli.add_command(create_database)
    api_v1_cors_config = {
        "methods": ["OPTIONS", "GET", "POST"],
    }
    CORS(app, resources={"/api/*": api_v1_cors_config})
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None