import datetime

from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, ImageComponent, PostbackAction,
                            TextComponent, URIAction, VideoSendMessage)

from .. import db
from ..models import Activity, GroupActivityLog, User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def follow_message(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id, deleted_at=None).first()
    if user is None:
        user = User(
                line_user_id=line_user_id
            )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            pass
    message_list = []
    bubble_template = BubbleContainer(
        hero=ImageComponent(
            url='https://i.imgur.com/AOCMVKP.jpg',
            size='full',
            aspect_ratio='5:4',
            aspect_mode='cover'
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='歡迎加入',
                    wrap=True,
                    weight= 'bold',
                    size='lg',
                    color='#1DB446'
                ),
                TextComponent(
                    text='嗨，我是 MiKA ，也可以叫我咪卡，我可以幫你找名片、遞名片、辦活動！\n\n先來試試看搜尋名片吧！',
                    wrap=True,
                    size='md',
                    margin='md'
                )
            ]
        )
    )
    message = FlexSendMessage(
        alt_text='歡迎加入',
        contents=bubble_template
    )
    message_list.append(message)
    message = VideoSendMessage(
        original_content_url=''.join(
            [
                app.config['APP_URL'],
                'static/video/follow.mp4'
            ]
        ),
        preview_image_url='https://i.imgur.com/N1Hpitz.jpg'
    )
    message_list.append(message)
    return message_list

def unfollow(line_user_id):
    now = datetime.datetime.now()
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    user.deleted_at = now
    db.session.add(user)
    
    activitys = Activity.query.filter_by(
        user_id=user.id,
        deleted_at=None
    ).all()
    for activity in activitys:
        activity.deleted_at = now
        db.session.add(activity)
    
    group_activity_logs = GroupActivityLog.query.filter_by(
        user_id=user.id,
        deleted_at=None
    ).all()

    for group_activity_log in group_activity_logs:
        group_activity_log.deleted_at = now
        db.session.add(group_activity_log)
    
    try:
        db.session.commit()
    except:
        pass
