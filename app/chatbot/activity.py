import datetime
import json
import urllib

from flask import Flask
from linebot import LineBotApi
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage, ImageComponent,
                            PostbackAction, TextComponent, TextSendMessage,
                            URIAction)
from sqlalchemy import func

from .. import db
from ..models import Activity, ActivityLog, Card, User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])


def group_activity_message(source_id):
    activitys =  Activity.query.filter_by(source_id=source_id).order_by(Activity.created_at.desc()).limit(9)
    carousel_template_columns = []
    if activitys:
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
                                    text='開始時間',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.start_at.strftime("%Y/%m/%d %H:%M"),
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
                                    text='結束時間',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.end_at.strftime("%Y/%m/%d %H:%M"),
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
                            action=URIAction(
                                label='有誰參加',
                                uri=''.join(
                                    [
                                        app.config['WHO_JOIN_ACTIVITY_LIFF_URL'],
                                        '?activity_id=',
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
    bubble_template = BubbleContainer(
        hero=ImageComponent(
            url='https://i.imgur.com/EsVTFD6.png',
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover'
        ),
        footer=BoxComponent(
            layout='vertical',
            spacing='sm',
            contents=[
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='新增活動',
                        uri=''.join(
                            [
                                app.config['ADD_GROUP_ACTIVITY_LIFF_URL'],
                                '?',
                                'source_id=',
                                urllib.parse.quote_plus(str(source_id))
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

def join_group_activity_message(activity_id, line_user_id):
    user = User.query.filter_by(line_user_id=str(line_user_id)).first()

    # Check is user or not
    if user is None:
        user = User(
                line_user_id=line_user_id
            )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            pass

    # Query model activity
    activity = Activity.query.filter_by(id=activity_id).first()
    
    # Get user data
    user_profile = line_bot_api.get_profile(line_user_id)
    user_dict = json.loads(str(user_profile))
    # Check now time is can join activity
    if check_time_can_join(activity.start_at):

        # Check activity session limit can join
        if activity.session_limit > activity.session_count:
            activity.session_count = activity.session_count + 1
            try:
                db.session.commit()
                content = ''.join(
                    [
                        user_dict['displayName'],
                        ' 您重複參加活動 ',
                        activity.title,
                        ' 囉！'
                    ]
                )

                # Logging user activity
                activity_log = ActivityLog.query.filter_by(
                    activity_id=str(activity_id),
                    user_id=user.id
                ).first()
    
                if activity_log is None:
                    activity_log = ActivityLog(
                        activity_id=activity_id,
                        user_id=user.id
                    )
                    db.session.add(activity_log)
                    try:
                        db.session.commit()
                        content = ''.join(
                            [
                                user_dict['displayName'],
                                ' 成功參加活動 ',
                                activity.title,
                                ' 囉！'
                            ]
                        )
                    except:
                        pass
            except:
                pass
        else:
            content = ''.join(
                [
                    user_dict['displayName'],
                    ' 想參加活動 ',
                    activity.title,
                    ' ，但是人數已經超過上限'
                ]
            )
    else:
        content = ''.join(
            [
                user_dict['displayName'],
                ' 想參加活動 ',
                activity.title,
                ' ，但是活動時間已經開始或是結束'
            ]
        )

    return TextSendMessage(
        text=content
    )
    return 0

def check_time_can_join(start_at):
    now = datetime.datetime.now()
    if start_at >= now:
        return True
    return False

def add_activity_message(line_user_id):

    bubble_template = BubbleContainer(
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='新增活動',
                    weight='bold',
                    color='#1DB446',
                    size='md',
                ),
                TextComponent(
                    text='請點我，新增活動唷！',
                    margin='md',
                    wrap=True,
                    color='#666666',
                    size='sm',
                )
            ]
        ),
        footer=BoxComponent(
            layout='vertical',
            spacing="sm",
            contents=[

                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='新增活動', uri=app.config['ADD_ACTIVITY_LIFF_URL']),
                )
            ]
        )
    )


    message = FlexSendMessage(
        alt_text='新增活動！', contents=bubble_template)
    return message

def my_activity_message(line_user_id):
    activitys = Activity.query.filter_by(source_id=line_user_id).order_by(Activity.created_at.desc()).limit(9).all()

    if activitys:
        carousel_template_columns = []
        for activity in activitys:
            bubble_template = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text=activity.title,
                            wrap=True,
                            weight='bold',
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
                                    text='開始時間',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.start_at.strftime("%Y/%m/%d %H:%M"),
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
                                    text='結束時間',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.start_at.strftime("%Y/%m/%d %H:%M"),
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
                                    text='結束日期',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.end_at.strftime('%Y{y}%m{m}%d{d} %H{h}:%M{M}').format(y='年',
                                                                                                          m='月',
                                                                                                          d='日',
                                                                                                          h='時',
                                                                                                          M='分'),
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
                        )
                    ]
                )
            )
            carousel_template_columns.append(bubble_template)
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='新增活動',
                        weight='bold',
                        color='#1DB446',
                        size='md',
                    ),
                    TextComponent(
                        text='請點我，新增活動唷！',
                        margin='md',
                        wrap=True,
                        color='#666666',
                        size='sm',
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing="sm",
                contents=[

                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='新增活動', uri=app.config['ADD_ACTIVITY_LIFF_URL']),
                    )
                ]
            )
        )
        carousel_template_columns.append(bubble_template)
        message = FlexSendMessage(
            alt_text='我的活動清單',
            contents=CarouselContainer(
                contents=carousel_template_columns
            )
        )
        return message
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='您尚未有任何活動！',
                        weight='bold',
                        color='#1DB446',
                        size='md',
                    ),
                    TextComponent(
                        text='請點我，新增活動唷！',
                        margin='md',
                        wrap=True,
                        color='#666666',
                        size='sm',
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing="sm",
                contents=[

                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='新增活動', uri=app.config['ADD_ACTIVITY_LIFF_URL']),
                    )
                ]
            )
        )
        message = FlexSendMessage(
            alt_text='新增活動', contents=bubble_template)

        return message

def search_activity_message(keyword ,source_id):
    activitys = Activity.query.filter(Activity.title.like('%{}%'.format(keyword)) ,Activity.public == 1,Activity.deleted_at == None).order_by(func.random()).limit(3).all()

    carousel_template_columns = []
    
    if activitys:
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
                                    text='開始時間',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.start_at.strftime("%Y/%m/%d %H:%M"),
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
                                    text='結束時間',
                                    wrap=True,
                                    flex=2,
                                    size='md',
                                    color='#666666'
                                ),
                                TextComponent(
                                    text=activity.end_at.strftime("%Y/%m/%d %H:%M"),
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
                                label='前往活動群組',
                                uri=str(activity.group_link)
                            )
                        )
                    ]
                )
            )
            carousel_template_columns.append(bubble_template)
        message = FlexSendMessage(
            alt_text='搜尋活動結果',
            contents=CarouselContainer(
                contents=carousel_template_columns
            )
        )
        return message
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='沒有結果',
                        wrap=True,
                        weight='bold',
                        size='md',
                        color='#1DB446',
                    ),
                    TextComponent(
                        text=''.join(['抱歉，找不到有關 ', keyword, ' 的活動']),
                        wrap=True,
                        size='sm',
                    )
                ]
            ),
        )
        message = FlexSendMessage(
            alt_text='新增活動', contents=bubble_template)

    return message
