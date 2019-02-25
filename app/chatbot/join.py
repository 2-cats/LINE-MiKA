from .. import db
from ..models import Group


def bot_join_group(group_id):
    group = Group(
        group_id=group_id
    )
    db.session.add(group)
    try:
        db.session.commit()
    except:
        pass
