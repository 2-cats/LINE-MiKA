from flask import Flask, abort, current_app, render_template, request

from . import admin
from .. import db
from .auth import check_admin
from .dashboard import dashboard_index
from .card import get_card
from .activity import get_activity

app = Flask(__name__, instance_relative_config=True)

@admin.route("/admin", methods=['GET'])
def index():
    args = request.args.to_dict()
    result = check_admin(args)
    if result:
        data = dashboard_index()
        return render_template(
            'admin/index.html',
            data=data,
            args=args
        )
    else:
        return render_template('admin/error.html')

@admin.route("/admin/card", methods=['GET'])
def card():
    args = request.args.to_dict()
    result = check_admin(args)
    if result:
        cards = get_card()
        return render_template(
            'admin/card.html',
            cards=cards,
            args=args
        )
    else:
        return render_template('admin/error.html')

@admin.route("/admin/activity", methods=['GET'])
def activity():
    args = request.args.to_dict()
    result = check_admin(args)
    if result:
        activitys = get_activity()
        return render_template(
            'admin/activity.html',
            activitys=activitys,
            args=args
        )
    else:
        return render_template('admin/error.html')
