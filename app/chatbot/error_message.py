from flask import Flask
from linebot.models import (FlexSendMessage, BoxComponent, BubbleContainer, ButtonComponent,
                            ButtonsTemplate, StickerSendMessage,
                            TemplateSendMessage, TextComponent, URIAction,MessageAction)

import config

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def alert_to_bind_message(line_user_id):
    buttons_template = ButtonsTemplate(
        title='綁定服務',
        text='您好，我是 Lassie！第一次使用嗎？完成簡單的綁定只需要三分鐘，就可以享用完整的服務！',
        actions=[
            URIAction(
                label='點我進行綁定',
                uri=app.config['BIND_LINE_LIFF_URL']
            )
        ])
    template_message = TemplateSendMessage(
        alt_text='綁定帳號',
        template=buttons_template
    )
    return template_message

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
