import datetime

from .. import db
from ..models import Group, GroupActivity


def bot_leave_group(group_id):
    group = Group.query.filter_by(
        group_id=group_id,
        deleted_at=None
    ).first()

    group.deleted_at = datetime.datetime.now()
    db.session.add(group)

    activitys = GroupActivity.query.filter_by(
        group_id=group.id,
        deleted_at=None
    ).all()
    
    for activity in activitys:
        activity.deleted_at = datetime.datetime.now()
        db.session.add(activity)
    try:
        db.session.commit()
    except:
        pass