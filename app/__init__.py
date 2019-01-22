from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    from .chatbot import chatbot as chatbot_blueprint
    app.register_blueprint(chatbot_blueprint)
    from .liff import liff as liff_blueprint
    app.register_blueprint(liff_blueprint)
    return app
