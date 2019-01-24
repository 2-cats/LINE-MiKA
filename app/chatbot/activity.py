
import datetime
import json

from flask import Flask
from linebot import LineBotApi
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage, PostbackAction,
                            TextComponent, TextSendMessage, URIAction)

from .. import db
from ..models import Activity, ActivityLog, Card, User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])


def add_group_activity_message(line_user_id):
    return 0

def group_activity_message(source_id):
    activitys =  Activity.query.filter_by(source_id=source_id).order_by(Activity.created_at.desc()).all()
    carousel_template_columns = []
    for activity in activitys:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text=activity.title,
                        wrap=True,
                        weight= 'bold',
                        size='md',
                        color='#1DB446'
                    ),
                    TextComponent(
                        text=activity.description,
                        size='sm',
                        wrap=True,
                        margin='md',
                        color='#666666'
                    ),
                    BoxComponent(
                        layout='horizontal',
                        margin='md',
                        contents=[
                            TextComponent(
                                text='時間',
                                wrap=True,
                                flex=2,
                                size='md',
                                color='#666666'
                            ),
                            TextComponent(
                                text=activity.activity_time.strftime("%Y年%m月%d日 %H:%M"),
                                size='sm',
                                flex=5,
                                margin='sm',
                                color='#333333'
                            )
                        ]
                    ),
                    BoxComponent(
                        layout='horizontal',
                        margin='md',
                        contents=[
                            TextComponent(
                                text='人數',
                                wrap=True,
                                flex=2,
                                size='md',
                                color='#666666'
                            ),
                            TextComponent(
                                text=''.join(
                                    [
                                        str(activity.session_count),
                                        '/',
                                        str(activity.session_limit)
                                    ]
                                ),
                                size='sm',
                                flex=5,
                                margin='sm',
                                color='#333333'
                            )
                        ]
                    ),
                    BoxComponent(
                        layout='horizontal',
                        margin='md',
                        contents=[
                            TextComponent(
                                text='位置',
                                flex=2,
                                size='md',
                                color='#666666'
                            ),
                            TextComponent(
                                text=activity.address,
                                size='sm',
                                wrap=True,
                                flex=5,
                                margin='sm',
                                color='#333333'
                            )
                        ]
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(
                            label='位置導航',
                            uri=''.join(
                                [
                                    'https://www.google.com/maps/search/?api=1&query=',
                                    str(activity.lat),
                                    ',',
                                    str(activity.lng)
                                ]
                            )
                        ),
                    ),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(
                            label='有誰參加',
                            data=','.join(
                                [
                                    'who_join_group_activity',
                                    str(activity.id)
                                ]
                            )
                        )
                    ),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(
                            label='加一',
                            data=','.join(
                                [
                                    'join_group_activity',
                                    str(activity.id)
                                ]
                            )
                        ),
                    ),
                ]
            )
        )
        carousel_template_columns.append(bubble_template)
    message = FlexSendMessage(
        alt_text='群組活動清單',
        contents=CarouselContainer(
            contents=carousel_template_columns
        )
    )
    return message

def join_group_activity_message(line_user_id):
    return 0

def who_join_group_activity_message(activity_id):
    activity_logs = User.query.join(ActivityLog, User.id==ActivityLog.user_id).filter(ActivityLog.activity_id==str(activity_id))

    join_users = []
    for activity_log in activity_logs:
        user = line_bot_api.get_profile(activity_log.line_user_id)
        user_dict = json.loads(str(user))
        join_users.append(user_dict['displayName'])
    user = '、'.join(join_users)

    activity = Activity.query.filter_by(id=str(activity_id)).first()
    return TextSendMessage(
            text=''.join([user ,' 參加了 ', activity.title])
        )

def my_activity_message(line_user_id):
    return 0
