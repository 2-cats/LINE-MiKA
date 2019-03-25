from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            ButtonsTemplate, FlexSendMessage, MessageAction,
                            StickerSendMessage, TemplateSendMessage,
                            TextComponent, URIAction)

import config

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def alert_no_action_message(line_user_id):
    message = []
    message_item = StickerSendMessage(
        package_id=2,
        sticker_id=149
    )
    message.append(message_item)
    bubble_template = BubbleContainer(
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='我聽不懂你的指令',
                    wrap=True,
                    weight= 'bold',
                    size='lg',
                ),
                TextComponent(
                    text='抱歉，我還在學習中，聽不懂你的指令，如果有使用上的問題，歡迎聯繫我們',
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
                    action=MessageAction(label='聯絡我們', text='聯絡我們'),
                )
            ]
        )
    )
    message_item = FlexSendMessage(
        alt_text='抱歉，我聽不懂指令', contents=bubble_template)
    message.append(message_item)
    return message
