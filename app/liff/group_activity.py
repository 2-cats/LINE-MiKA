import json

from flask import Flask
from linebot import LineBotApi

from .. import db
from ..models import Group, GroupActivity, GroupActivityLog, User
from .map import convert_address

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])


def add_group_activity(data):
    location = convert_address(data['address'])

    user = User.query.filter_by(
        line_user_id=data['line_user_id'],
        deleted_at=None
    ).first()
    group = Group.query.filter_by(
        group_id=data['source_id'],
        deleted_at=None
    ).first()
    public = False
    group_link = None
    if 'public' in data:
        public = True
        group_link = data['group_link']
        

    # Check user is exist, Create user if not
    if user is None:
        user = User(
                line_user_id=data['line_user_id']
            )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            pass

    # Insert activity
    activity = GroupActivity(
        group_id=group.id,
        title=data['title'],
        description=data['description'],
        start_at=''.join([data['start_date_at'], ' ', data['start_time_at']]),
        end_at=''.join([data['end_date_at'], ' ', data['end_time_at']]),
        organizer=data['organizer'],
        address=data['address'],
        lat=location[0],
        lng=location[1],
        rel_link=data['rel_link'],
        group_link=group_link,
        public=public,
        session_limit=data['session_limit'],
        session_count=1
    )
    db.session.add(activity)
    try:
        db.session.commit()
    except:
        pass

    # Log activity
    activity_log = GroupActivityLog(
        user_id=user.id,
        group_activity_id=activity.id
    )
    db.session.add(activity_log)
    try:
        db.session.commit()
    except:
        pass

def who_join_group_activity(activity_id):
    activity_logs = User.query.join(
        GroupActivityLog, User.id==GroupActivityLog.user_id
    ).filter(
        GroupActivityLog.group_activity_id==str(activity_id),
        GroupActivityLog.deleted_at==None
    ).all()
    users = []
    for activity_log in activity_logs:
        try:
            user = line_bot_api.get_profile(activity_log.line_user_id)
            user_dict = json.loads(str(user))
            users.append(user_dict)
        except:
            pass
    return users