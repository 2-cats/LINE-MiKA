import json
import re

from flask import Flask, abort, current_app, render_template, request
from flask_mqtt import Mqtt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (AudioMessage, FollowEvent, ImageMessage, JoinEvent,
                            LeaveEvent, LocationMessage, MessageEvent,
                            PostbackEvent, StickerMessage, TextMessage,
                            TextSendMessage, UnfollowEvent)

from . import chatbot
from .. import db
from .activity import delete_my_activity, my_activity_message
from .admin import admin_door_message
from .card import (card_management_message, delete_my_card_message,
                   nearby_card_message, search_card_message,
                   show_my_card_message)
from .error_message import alert_no_action_message
from .follow import follow_message, unfollow
from .group_activity import (group_activity_message,
                             join_group_activity_message,
                             leave_group_activity_message,
                             my_join_group_activity, search_activity_message,
                             user_leave_and_private_activity)
from .helper import group_helper_message, store_helper_message
from .image import scan_card_confirm_message, scan_card_image_message
from .join import bot_join_group
from .leave import bot_leave_group
from .keyword import keyword_query

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
    message = follow_message(event.source.user_id)
    line_bot_api.reply_message(event.reply_token, message)
    return 0

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    '''
    Handle unfollow event
    '''
    unfollow(event.source.user_id)
    return 0

# Handle MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # Get common LINE user information
    line_user_id = event.source.user_id
    message_text = event.message.text
    source_type = event.source.type

    if source_type == 'user':
        if message_text == "我的名片":
            message = card_management_message(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        elif message_text == "我的活動":
            message = my_activity_message(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        elif message_text == "我的群組活動":
            message = my_join_group_activity(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        elif message_text == "更換角色":
            message = store_helper_message(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        elif message_text == "谷林發大財":
            message = admin_door_message(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        elif bool(re.search('找名片 ', message_text)):
            keywords = message_text.replace('找名片 ', '')
            keyword_list = keywords.split(' ')
            message = search_card_message(keyword_list[0], line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        elif bool(re.search('找活動', message_text)):
            message_text = message_text.replace('找活動', '')
            message_text = message_text.replace(' ', '')
            message = search_activity_message(message_text, line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        message = keyword_query(message_text)
        if message :
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        message = search_card_message(message_text, line_user_id)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
        
    elif source_type == 'group':
        message_text = message_text.replace(' ', '')
        message_text = message_text.lower()
        group_id = event.source.group_id
        if message_text == "我的名片" or message_text == "教練我想發名片":
            message = show_my_card_message(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        elif message_text == "近期活動":
            message = group_activity_message(group_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        elif message_text == "@mika" or message_text == "咪卡" or message_text == "mika":
            message = group_helper_message(group_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        message = keyword_query(message_text)
        if message :
            line_bot_api.reply_message(event.reply_token, message)
            return 0
    elif source_type == 'room':
        if message_text == "我的名片":
            message = show_my_card_message(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        message = keyword_query(message_text)
        if message :
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        

# Postback Event
@handler.add(PostbackEvent)
def handle_postback(event):
    line_user_id = event.source.user_id
    # data="action, var1, var2, ... ,varN"
    # Convet to postback_data: [action, var1, var2, ... ,varN]
    postback_data = event.postback.data.split(",")
    if postback_data[0] == 'delete_my_card':
        message = delete_my_card_message(postback_data[1])
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    elif postback_data[0] == 'join_group_activity':
        # postback_data[1] is activity_id
        message = join_group_activity_message(postback_data[1], line_user_id)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    elif postback_data[0] == 'leave_group_activity':
        # postback_data[1] is activity_id
        message = leave_group_activity_message(postback_data[1], line_user_id)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    elif postback_data[0] == 'delete_my_activity':
        # postback_data[1] is activity_id
        message = delete_my_activity(postback_data[1])
        line_bot_api.reply_message(event.reply_token, message)
    elif postback_data[0] == 'scan_card_confirm':
        message = scan_card_confirm_message()
        line_bot_api.reply_message(event.reply_token, message)
        return 0

# Handle image message event
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    if event.source.type == 'user':
        line_user_id = event.source.user_id
        image_id = event.message.id
        message = scan_card_image_message(image_id, line_user_id) 
        line_bot_api.reply_message(event.reply_token, message)
        return 0

# Handle location message event
@handler.add(MessageEvent, message=LocationMessage)
def handle_loaction_message(event):
    """"
    Handle location message Event.
    """
    if event.source.type == 'user':
        line_user_id = event.source.user_id
        message = nearby_card_message(event.message.latitude, event.message.longitude, line_user_id)
        line_bot_api.reply_message(event.reply_token, message)
        return 0

# Handle audio message event
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    if event.source.type == 'user':
        line_user_id = event.source.user_id
        message = alert_no_action_message(line_user_id)
        line_bot_api.reply_message(event.reply_token, message)
        return 0

# Handle sticker message event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    if event.source.type == 'user':
        line_user_id = event.source.user_id
        message = alert_no_action_message(line_user_id)
        line_bot_api.reply_message(event.reply_token, message)
        return 0

@handler.add(LeaveEvent)
def handle_leave(event):
    '''
    Handle leave event
    '''
    bot_leave_group(event.source.group_id)
    return 0

@handler.add(JoinEvent)
def handle_join(event):
    '''
    Handle join event
    '''
    bot_join_group(event.source.group_id)
    message = group_helper_message(event.source.group_id)
    line_bot_api.reply_message(event.reply_token, message)
    return 0
