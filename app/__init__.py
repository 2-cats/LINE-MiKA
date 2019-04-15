from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_mqtt import Mqtt

bootstrap = Bootstrap()
db = SQLAlchemy()

mqtt = Mqtt()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mqtt.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    from .chatbot import chatbot as chatbot_blueprint
    app.register_blueprint(chatbot_blueprint)
    from .liff import liff as liff_blueprint
    app.register_blueprint(liff_blueprint)
    from .store import store as store_blueprint
    app.register_blueprint(store_blueprint)
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    return app
