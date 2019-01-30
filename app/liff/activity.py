import json

from flask import Flask
from linebot import LineBotApi

from .. import db
from ..models import Activity, ActivityLog, User
from .map import convert_address

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])


def add_activity(data):
    location = convert_address(data['address'])

    user = User.query.filter_by(line_user_id=data['line_user_id']).first()
    activity = Activity(
        source_type='user',
        source_id=data['line_user_id'],
        title=data['title'],
        description=data['description'],
        activity_time=data['activity_time'],
        organizer=data['organizer'],
        address=data['address'],
        lat=location[0],
        lng=location[1],
        rel_link=data['rel_link'],
        session_limit=1,
        session_count=1
    )
    db.session.add(activity)
    try:
        db.session.commit()
    except:
        pass

def add_group_activity(data):
    location = convert_address(data['address'])

    user = User.query.filter_by(line_user_id=data['line_user_id']).first()
    activity = Activity(
        source_type='group',
        source_id=data['source_id'],
        title=data['title'],
        description=data['description'],
        activity_time=data['activity_time'],
        organizer=data['organizer'],
        address=data['address'],
        lat=location[0],
        lng=location[1],
        rel_link=data['rel_link'],
        session_limit=data['session_limit'],
        session_count=1
    )
    db.session.add(activity)
    try:
        db.session.commit()
    except:
        pass

    activity = Activity.query.filter_by(source_id=data['source_id']).order_by(Activity.created_at.desc()).first()
    activity_log = ActivityLog(
        user_id=user.id,
        activity_id=activity.id
    )
    db.session.add(activity_log)
    try:
        db.session.commit()
    except:
        pass

def who_join_group_activity(activity_id):
    activity_logs = User.query.join(ActivityLog, User.id==ActivityLog.user_id).filter(ActivityLog.activity_id==str(activity_id)).all()
    users = []
    for activity_log in activity_logs:
        try:
            user = line_bot_api.get_profile(activity_log.line_user_id)
            user_dict = json.loads(str(user))
            users.append(user_dict)
        except:
            pass
    return users
