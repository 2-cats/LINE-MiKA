from flask import Flask, abort, current_app, render_template, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (AudioMessage, FollowEvent, ImageMessage,
                            LocationMessage, MessageEvent, StickerMessage,
                            TextMessage, TextSendMessage, UnfollowEvent)

from . import liff
from .. import db
from .card import add_card
from .activity import add_activity
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(app.config["LINE_CHANNEL_SECRET"])

@liff.route("/line/add_card", methods=['GET'])
def line_auto_add_card():
    data = request.args.to_dict()
    return render_template(
        'line/add_card.html',
        data=data
    )

@liff.route("/line/add_card", methods=['POST'])
def line_add_card_success():
    add_card(request.form.to_dict())
    return render_template('line/add_card_success.html')



@liff.route("/line/add_activity", methods=['GET'])
def line_add_activity():

    return render_template('line/add_activity.html')



@liff.route("/line/add_activity", methods=['POST'])
def line_add_activity_success():
    add_activity(request.form.to_dict())
    return render_template('line/add_activity_success.html')
