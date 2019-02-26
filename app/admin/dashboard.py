from .. import db
from ..models import Activity, Card, Group, GroupActivity, User


def dashboard_index():
    user_count = User.query.filter_by(
        deleted_at=None
    ).count()

    group_count = Group.query.filter_by(
        deleted_at=None
    ).count()

    card_count = Card.query.count()

    activity_count = Activity.query.count()

    group_activity_count = GroupActivity.query.count()

    data = {
        "user_count": user_count,
        "group_count": group_count,
        "card_count": card_count,
        "activity_count": activity_count,
        "group_activity_count": group_activity_count
    }

    return data
