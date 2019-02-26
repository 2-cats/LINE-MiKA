from .. import db
from ..models import Activity, Card, Group, GroupActivity, User


def dashboard_index():
    users = User.query.all()
    groups = Group.query.all()
    cards = Card.query.all()
    activitys = Activity.query.all()
    groupActivitys = GroupActivity.query.all()

    follow_count = 0
    unfollow_count = 0
    join_group = 0
    leave_group = 0
    card_num = 0
    del_card_num = 0
    activity_num = 0
    cancel_activity_num = 0
    g_activity_num = 0
    cancel_g_activity_num = 0

    for user in users:
        if user.deleted_at == None:
            follow_count += 1
        else:
            unfollow_count += 1
    
    for group in groups:
        if group.deleted_at == None:
            join_group += 1
        else:
            leave_group += 1
        
    for card in cards:
        if card.deleted_at == None:
            card_num += 1
        else:
            del_card_num +=1

    for activity in activitys:
        if activity.deleted_at == None:
            activity_num += 1
        else:
            cancel_activity_num += 1
    
    for groupActivity in groupActivitys:
        if groupActivity.deleted_at == None:
            g_activity_num += 1
        else:
            cancel_g_activity_num  += 1

    data = {
        'follow_count': follow_count,
        'unfollow_count': unfollow_count,
        'join_group': join_group,
        'leave_group': leave_group,
        'card_num': card_num,
        'del_card_num': del_card_num,
        'activity_num': activity_num,
        'cancel_activity_num': cancel_activity_num,
        'g_activity_num': g_activity_num,
        'cancel_g_activity_num': cancel_g_activity_num
    }

    return data
