from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage, ImageComponent,
                            MessageAction, PostbackAction, TextComponent,
                            URIAction,SeparatorComponent,MessageAction)
import urllib
from .. import db
from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


def group_helper_message(source_id):
    carousel_template = CarouselContainer(
        contents=[
            BubbleContainer(
                hero=ImageComponent(
                    url='https://i.imgur.com/XICiMgE.jpg',
                    size='full',
                    aspect_ratio='5:4',
                    aspect_mode='cover'
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='我是 MiKA',
                            wrap=True,
                            weight= 'bold',
                            color='#1DB446',
                            size='lg',
                        ),
                        TextComponent(
                            text='我可以幫你打理群組裡頭的大小活動喔！',
                            wrap=True,
                            size='md',
                            margin='md'
                        )
                    ]
                ),
                footer=BoxComponent(
                            layout='horizontal',
                            spacing='sm',
                            contents=[
                                ButtonComponent(
                                    style='link',
                                    height='sm',
                                    action=MessageAction(label='近期活動', text='近期活動')
                                ),
                                SeparatorComponent(

                                ),
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
                                )
                            ]
                        )



            ),
            BubbleContainer(
                hero=ImageComponent(
                    url='https://i.imgur.com/JpX9kt6.jpg',
                    size='full',
                    aspect_ratio='5:4',
                    aspect_mode='cover'
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='也可以叫我咪卡',
                            wrap=True,
                            weight= 'bold',
                            color='#1DB446',
                            size='lg',
                        ),
                        TextComponent(
                            text='想讓大家認識你嗎？在群組遞上名片也不是問題喔！',
                            wrap=True,
                            size='md',
                            margin='md'
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    contents=[
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(label='我的名片', text='我的名片'),
                            )
                        ]
                    )
                )
            ]
        )
        
    message = FlexSendMessage(
        alt_text='蹦蹦！蹦～找我嗎？', contents=carousel_template)
    return message


def store_helper_message(line_user_id):
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
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
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                     text='MiKA STORE',
                    wrap=True,
                    color='#1DB446',
                    weight= 'bold',
                    size='lg',
                ),
                TextComponent(
                    text='你可以在這裏更換名片角色或者是遞名片的動畫，妝點你的卡片！',
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
                    action=URIAction(
                        label='打開',
                        uri=''.join(
                            [
                                app.config['EDIT_CARD_STYLE_LINE_LIFF_URL'],
                                '?user_id=',
                                str(user.id)
                            ]
                        )
                    )
                )
            ]
        )
    )
    message = FlexSendMessage(
        alt_text='MiKA STORE！', contents=bubble_template)
    return message
