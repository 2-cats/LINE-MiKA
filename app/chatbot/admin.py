from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage, ImageComponent,
                            MessageAction, PostbackAction, TextComponent,
                            TextSendMessage, URIAction)

from .. import db
from ..models import Admin

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def admin_door_message(line_user_id):
    admin = Admin.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    if admin is None:
        message = TextSendMessage(text='咪卡也發大財！')
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='Dashboard',
                        wrap=True,
                        color='#1DB446',
                        weight= 'bold',
                        size='lg',
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
                            label='OPEN',
                            uri=''.join(
                                [
                                    app.config['ADMIN_LINE_LIFF_URL'],
                                    '?line_user_id=',
                                    str(line_user_id)
                                ]
                            )
                        )
                    )
                ]
            )
        )
        message = FlexSendMessage(
            alt_text='管理員安安', contents=bubble_template)
    return message
