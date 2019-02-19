import datetime

from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, ImageComponent, PostbackAction,
                            TextComponent, URIAction)

from .. import db
from ..models import User

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
                ),
                TextComponent(
                    text='您好，我是 MiKA！你可以叫我咪卡，我的任務是努力為大家整理、搜尋名片、連結群組上的每位朋友！第一次使用，不妨先傳一張名片讓我認識你吧！',
                    wrap=True,
                    size='md',
                    margin='md'
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
                    action=PostbackAction(
                        label='智慧新增名片',
                        data='scan_card_confirm,'
                    ),
                ),
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='手動新增名片', uri=app.config['ADD_CARD_LINE_LIFF_URL']),
                )
            ]
        )
    )
    message = FlexSendMessage(
        alt_text='歡迎加入', contents=bubble_template)
    return message

def unfollow(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id, deleted_at=None).first()
    user.deleted_at = datetime.datetime.now()
    try:
        db.session.commit()
    except:
        pass
