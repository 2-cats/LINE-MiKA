
from .. import db
from ..models import Activity, ActivityLog, User
from .map import convert_address


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

    activity = Activity.query.filter_by(source_id=data['source_id']).first()
    activity_log = ActivityLog(
        user_id=user.id,
        activity_id=activity.id
    )
    db.session.add(activity_log)
    try:
        db.session.commit()
    except:
        pass