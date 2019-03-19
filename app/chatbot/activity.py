import datetime
import json
import urllib

from flask import Flask
from linebot import LineBotApi
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage, ImageComponent,
                            PostbackAction, SeparatorComponent, TextComponent,
                            TextSendMessage, URIAction)
from sqlalchemy import func

from .. import db
from ..models import Activity, User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])


def my_activity_message(line_user_id):
    user = User.query.filter(
        User.line_user_id==line_user_id,
        User.deleted_at==None
    ).first()
    now = datetime.datetime.now()
    activitys = Activity.query.filter(
        Activity.user_id==user.id,
        Activity.deleted_at==None,
        Activity.end_at>now
    ).order_by(
        Activity.start_at.asc()
    ).limit(9).all()

    if activitys:
        carousel_template_columns = []
        for activity in activitys:
            button_list = []

            if activity.rel_link != "":
                item = ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='相關連結',
                        uri=activity.rel_link
                        )
                    )
                button_list.append(item)
            item = ButtonComponent(
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
            button_list.append(item)
            item = ButtonComponent(
                style='link',
                height='sm',
                action=PostbackAction(
                    label='刪除活動',
                    data=','.join(
                        [
                            'delete_my_activity',
                            str(activity.id)
                        ]
                    )
                ),
            )
            button_list.append(item)



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
                                    text='開始日期',
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
                    contents=button_list
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

def delete_my_activity(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    activity.deleted_at = datetime.datetime.now()
    message = TextSendMessage(text='刪除失敗！')
    if activity:
        try:
            db.session.commit()
            message = TextSendMessage(text='刪除成功！')
        except:
            pass
    return message
