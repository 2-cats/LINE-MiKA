import json, datetime

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
        activity_type=data['activity_type'],
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
    activitys = GroupActivityLog.query.filter(
        GroupActivityLog.group_activity_id == str(activity_id),
        GroupActivityLog.deleted_at == None
    ).all()
    datas = []
    for activity in activitys:
        try:
            user = line_bot_api.get_profile(activity.user.line_user_id)
            user_dict = json.loads(str(user))
            data = {
                'user_data': user_dict,
                'companion': activity.companion,
            }
            datas.append(data)
        except:
            pass
    return datas

def group_activity_join_companion(companion, line_user_id, group_activity_id):
    """group_activity_join_companion function.

    Group activity join companion.

    :param companion: string for companion
    :param line_user_id: string for LINE user id
    :param group_activity_id: string for group activity id
    :return: result
    """
    now = datetime.datetime.now()
    messages = []

    # Query User
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    
    # Query group activity
    group_activity = GroupActivity.query.filter(
        GroupActivity.id == group_activity_id,
        GroupActivity.deleted_at == None,
        GroupActivity.end_at > now
    ).first()

    # If group activit is exist
    if group_activity:
        # Query LINE user is join group activit
        group_activity_log = GroupActivityLog.query.filter(
            GroupActivityLog.group_activity_id == group_activity.id,
            GroupActivityLog.user_id == user.id,
            GroupActivity.deleted_at == None
        ).first()

        # If LINE user was joined
        if group_activity_log:
            # check companion number
            companion_num = int(group_activity.session_count) - int(group_activity_log.companion) + int(companion)

            # error check: companion number is a positive number
            if int(companion) < 0:
                messages.append('編輯失敗，輸入了負數')
            # error check: companion number is less than the maximum number of session limit
            elif companion_num > group_activity.session_limit:
                messages.append('編輯失敗，超過活動人數上限。')
            # success: commit group activity
            else:
                group_activity.session_count = companion_num
                group_activity_log.companion = companion
                db.session.add(group_activity, group_activity_log)
                try:
                    db.session.commit()
                except:
                    pass
                messages.append('新增成功')
        # If LINE user was not joined
        else:
            messages.append('你尚未參加此活動')
    # If group activit is not exist
    else:
        messages.append('活動已過期或無此活動')

    return messages

def check_group_activity_is_end(group_activity_id):
    """check_group_activity_is_end function.

    Check group activity is end or not

    :param group_activity_id: string for group activity id
    :return: boolean for result
    """
    now = datetime.datetime.now()
    result = GroupActivity.query.filter(
        GroupActivity.id == group_activity_id,
        GroupActivity.deleted_at == None,
        GroupActivity.end_at > now
    ).first()
    result = False
    if result:
        return True
    return result
