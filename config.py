from flask import Flask
import os
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

class Config:
   SQLALCHEMY_COMMIT_ON_TEARDOWN = True
   @staticmethod
   def init_app(app):
       pass

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_HOST'],
        app.config['DB_PORT'],
        app.config['DB_NAME']
    )
    MQTT_CLIENT_ID = app.config['MQTT_CLIENT_ID']
    MQTT_BROKER_URL = app.config['MQTT_HOSTNAME']
    MQTT_BROKER_PORT = app.config['MQTT_PORT']
    MQTT_USERNAME = app.config['MQTT_USERNAME']
    MQTT_PASSWORD = app.config['MQTT_PASSWORD']

class TestingConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_HOST'],
        app.config['DB_PORT'],
        app.config['DB_NAME']
    )
    MQTT_CLIENT_ID = app.config['MQTT_CLIENT_ID']
    MQTT_BROKER_URL = app.config['MQTT_HOSTNAME']
    MQTT_BROKER_PORT = app.config['MQTT_PORT']
    MQTT_USERNAME = app.config['MQTT_USERNAME']
    MQTT_PASSWORD = app.config['MQTT_PASSWORD']

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_HOST'],
        app.config['DB_PORT'],
        app.config['DB_NAME']
    )
    MQTT_CLIENT_ID = app.config['MQTT_CLIENT_ID']
    MQTT_BROKER_URL = app.config['MQTT_HOSTNAME']
    MQTT_BROKER_PORT = app.config['MQTT_PORT']
    MQTT_USERNAME = app.config['MQTT_USERNAME']
    MQTT_PASSWORD = app.config['MQTT_PASSWORD']

config = {
   'development': DevelopmentConfig,
   'testing': TestingConfig,
   'production': ProductionConfig,
   'default': DevelopmentConfig
}
