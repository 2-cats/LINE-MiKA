import datetime

from .. import db
from ..models import Activity, User


def bot_leave_group(group_id):
    activitys = Activity.query.filter_by(
        source_id=group_id,
        deleted_at=None).all()
    
    for activity in activitys:
        activity.deleted_at = datetime.datetime.now()
        db.session.add(activity)
    try:
        db.session.commit()
    except:
        pass