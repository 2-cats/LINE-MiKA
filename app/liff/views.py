from flask import Flask, abort, current_app, render_template, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (AudioMessage, FollowEvent, ImageMessage,
                            LocationMessage, MessageEvent, StickerMessage,
                            TextMessage, TextSendMessage, UnfollowEvent)

from . import liff
from .. import db
from .activity import (add_activity, add_group_activity,
                       who_join_group_activity)
from .card import add_card, report_card_issue

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(app.config["LINE_CHANNEL_SECRET"])

@liff.route("/line/add_card", methods=['GET', 'POST'])
def line_add_card():
    if request.method == 'GET':
        data = request.args.to_dict()
        return render_template(
            'line/add_card.html',
            data=data
        )
    elif request.method == 'POST':
        result = add_card(request.form.to_dict())
        if result['status'] == "success":
            return render_template('line/add_card_success.html')
        else:
            return render_template('line/add_card_fail.html', message=result['message'])


@liff.route("/line/add_activity", methods=['GET', 'POST'])
def line_add_activity():
    if request.method == 'GET':
        return render_template('line/add_activity.html')
    elif request.method == 'POST':
        add_activity(request.form.to_dict())
        return render_template('line/add_activity_success.html')

@liff.route("/line/add_group_activity", methods=['GET', 'POST'])
def line_add_group_activity():
    if request.method == 'GET':
        data = request.args.to_dict()
        return render_template(
            'line/add_group_activity.html',
            data=data
        )
    elif request.method == 'POST':
        add_group_activity(request.form.to_dict())
        return render_template('line/add_group_activity_success.html')

@liff.route("/line/report_card", methods=['GET', 'POST'])
def line_report_card():
    if request.method == 'GET':
        data = request.args.to_dict()
        return render_template(
            'line/report_card.html',
            data=data
        )
    elif request.method == 'POST':
        report_card_issue(request.form.to_dict())
        return render_template('line/report_card_success.html')

@liff.route("/line/who_join_activity", methods=['GET'])
def line_who_join_activity():
    if request.method == 'GET':
        data = request.args.to_dict()
        users = who_join_group_activity(data['activity_id'])
        return render_template(
            'line/who_join_group_activity.html',
            users=users
        )
