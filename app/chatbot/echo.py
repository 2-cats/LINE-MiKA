import json

from flask import Flask
from linebot.models import TextSendMessage

from .. import db, mqtt

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
def gtts_echo(text):
    if app.config['ECHO_SWITCH']:
        content = {
            "text": text
        }
        mqtt.publish('/mika/echo', json.dumps(content).encode("UTF-8"))
        return TextSendMessage(text='已送出！')
    return TextSendMessage(text='這個功能被關閉了')
