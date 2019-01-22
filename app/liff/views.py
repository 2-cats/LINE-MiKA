from flask import Flask, abort, current_app, render_template, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (AudioMessage, FollowEvent, ImageMessage,
                            LocationMessage, MessageEvent, StickerMessage,
                            TextMessage, TextSendMessage, UnfollowEvent)

from . import liff
from .. import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(app.config["LINE_CHANNEL_SECRET"])

@liff.route("/line/auto_add_card", methods=['GET'])
def line_auto_add_card():
    data=request.args.get('data')
    return render_template(
        'line/auto_add_card.html',
        card_data=data
    )

@liff.route("/line/add_card_manual", methods=['GET'])
def line_manual_add_card():
    return render_template('line/manual_add_card.html')

@liff.route("/line/add_activity", methods=['GET'])
def line_add_activity():
    return render_template('line/add_activity.html')
