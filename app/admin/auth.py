from .. import db
from ..models import Admin

def check_admin(data):
    admin = Admin.query.filter_by(
        line_user_id=data['line_user_id'],
        deleted_at=None
    ).first()

    if admin:
        return True

    return False