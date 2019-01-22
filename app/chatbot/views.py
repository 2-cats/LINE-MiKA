import json
import re

from flask import Flask, abort, current_app, render_template, request
from flask_mqtt import Mqtt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (AudioMessage, FollowEvent, ImageMessage, JoinEvent,
                            LocationMessage, MessageEvent, PostbackEvent,
                            StickerMessage, TextMessage, TextSendMessage,
                            UnfollowEvent)

from . import chatbot
from .. import db
from .activity import (add_group_activity, group_activity, join_group_activity,
                       my_activity)
from .card import card_management, delete_my_card, search_card, show_my_card
from .follow import follow

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# LINE ACCESS
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(app.config["LINE_CHANNEL_SECRET"])


@chatbot.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    '''
    Handle follow event
    '''
    follow()
    return 0

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    '''
    Handle unfollow event
    '''
    return 0

# Handle MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # Get common LINE user information
    line_user_id = event.source.user_id
    message_text = event.message.text
    if event.source.type == 'user':
        if message_text == "名片管理":
            card_management(line_user_id)
        elif message_text == "我的活動":
            my_activity(line_user_id)
        search_card(line_user_id)
    elif event.source.type == 'group':
        if message_text == "我的名片":
            show_my_card(line_user_id)
        elif message_text == "近期活動":
            group_activity(line_user_id)
        elif message_text == "新增活動":
            add_group_activity(line_user_id)
        elif bool(re.search('找名片', message_text)):
            search_card(line_user_id)
    return 0

# Postback Event
@handler.add(PostbackEvent)
def handle_postback(event):
    line_user_id = event.source.user_id
    # data="action, var1, var2, ... ,varN"
    # Convet to postback_data: [action, var1, var2, ... ,varN]
    postback_data = event.postback.data.split(",") 
    if postback_data[0] == "delete_my_card":
        delete_my_card(line_user_id)
    elif  postback_data[0] == "join_group_activity":
        join_group_activity(line_user_id)

    return 0

# Handle location message event
@handler.add(MessageEvent, message=LocationMessage)
def handle_loaction_message(event):
    """"
    Handle location message Event.
    """
    return 0

# Handle image message event
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    return 0

# Handle audio message event
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    return 0

# Handle sticker message event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    return 0
