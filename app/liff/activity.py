from .. import db
from ..models import Activity, User
from .map import convert_address

def add_activity(data):
    location = convert_address(data['address'])

    user = User.query.filter_by(
        line_user_id=data['line_user_id'],
        deleted_at=None
    ).first()
    activity = Activity(
        user_id=user.id,
        title=data['title'],
        description=data['description'],
        start_at=''.join([data['start_date_at'], ' ', data['start_time_at']]),
        end_at=''.join([data['end_date_at'], ' ', data['end_time_at']]),
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

