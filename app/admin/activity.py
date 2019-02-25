from .. import db
from ..models import GroupActivity

def get_activity():
    activitys = GroupActivity.query.filter_by(
        deleted_at=None,
        public=1
    ).order_by(
        GroupActivity.created_at.desc()
    ).all()
    data = []
    for activity in activitys:
        item = {
            "id": activity.id,
            "title": activity.title,
            "organizer": activity.organizer,
            "description": activity.description
        }
        data.append(item)
    return data