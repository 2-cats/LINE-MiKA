from .. import db
from ..models import User, Group

def dashboard_index():
    user_count = User.query.filter_by(
        deleted_at=None
    ).count()

    group_count = Group.query.filter_by(
        deleted_at=None
    ).count()

    data = {
        "user_count": user_count,
        "group_count": group_count
    }

    return data