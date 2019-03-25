from flask import Flask, abort, current_app, render_template, request

from . import liff
from .. import db
from .activity import add_activity
from .card import add_card, edit_card, get_card, report_card_issue, update_card
from .group_activity import (add_group_activity, group_activity_join_companion,
                             who_join_group_activity)

app = Flask(__name__, instance_relative_config=True)

@liff.route("/line/card/add", methods=['GET', 'POST'])
def line_add_card():
    if request.method == 'GET':
        data = request.args.to_dict()
        return render_template(
            'line/card/add.html',
            data=data
        )
    elif request.method == 'POST':
        result = add_card(request.form.to_dict())
        if result['status'] == "success":
            return render_template('line/card/add_success.html')
        else:
            return render_template('line/card/add_fail.html', messages=result['messages'])

@liff.route("/line/card/edit", methods=['GET', 'POST'])
def line_edit_card():
    if request.method == 'GET':
        data = edit_card(request.args.to_dict())
        return render_template(
            'line/card/update.html',
            data=data
        )
    elif request.method == 'POST':
        result = update_card(request.form.to_dict())
        return render_template('line/card/update_success.html')

@liff.route("/line/card/send", methods=['GET'])
def send_anime():
    if request.method == 'GET':
        card = get_card(request.args.to_dict())
        return render_template(
            'line/card/send_anime.html',
            card=card
        )

@liff.route("/line/activity/add", methods=['GET', 'POST'])
def line_add_activity():
    if request.method == 'GET':
        return render_template('line/activity/add.html')
    elif request.method == 'POST':
        add_activity(request.form.to_dict())
        return render_template('line/activity/add_success.html')

@liff.route("/line/group_activity/add", methods=['GET', 'POST'])
def line_add_group_activity():
    if request.method == 'GET':
        data = request.args.to_dict()
        return render_template(
            'line/group_activity/add.html',
            data=data
        )
    elif request.method == 'POST':
        add_group_activity(request.form.to_dict())
        return render_template('line/group_activity/add_success.html')

@liff.route("/line/card/report", methods=['GET', 'POST'])
def line_report_card():
    if request.method == 'GET':
        data = request.args.to_dict()
        return render_template(
            'line/report/card.html',
            data=data
        )
    elif request.method == 'POST':
        report_card_issue(request.form.to_dict())
        return render_template('line/report/card_success.html')

@liff.route("/line/activity/user", methods=['GET'])
def line_who_join_activity():
    if request.method == 'GET':
        data = request.args.to_dict()
        datas = who_join_group_activity(data['activity_id'])
        return render_template(
            'line/group_activity/who_join.html',
            datas=datas,
            activity_id=data['activity_id']
        )

@liff.route("/line/activity/user/companion", methods=['POST'])
def line_edit_group_activity_companion():
    if request.method == 'POST':
        data = request.form.to_dict()
        messages = group_activity_join_companion(
            data['companion'],
            data['line_user_id'],
            data['activity_id']
        )
        return render_template(
            'line/group_activity/join_companion.html',
            messages=messages
        )
