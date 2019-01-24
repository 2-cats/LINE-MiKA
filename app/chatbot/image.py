import urllib

from flask import Flask
from linebot import LineBotApi
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, TextComponent, URIAction)

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])

def scan_card_image_message(image_id):
    image_file = line_bot_api.get_message_content(image_id)
    name = '李存恩'
    nickname = '永和金城武'
    title = '業務'
    summary = '原價屋'
    company_name = '原價屋電腦有限公司'
    email = 'aaaaaaaaaaaaaa321@gmail.com'
    tel_number = '035725183'
    fax_number = '035725183'
    tax_number = '035725183'
    phone_number = '0988777666'
    line_id = '123123'
    address = '123123'
    bubble_template = BubbleContainer(
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='最後一個步驟',
                    weight='bold',
                    color='#1DB446',
                    size='md',
                ),
                TextComponent(
                    text='我已經將您的名片分析完成，請確認一下有沒有問題',
                    margin='md',
                    wrap=True,
                    color='#666666',
                    size='sm',
                )
            ]
        ),
        footer=BoxComponent(
            layout='vertical',
            contents=[
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(
                        label='下一步驟',
                        uri=''.join(
                            [
                                app.config["ADD_CARD_LINE_LIFF_URL"],
                                '?',
                                'name=', urllib.parse.quote_plus(str(name)),
                                '&nickname=', urllib.parse.quote_plus(str(nickname)),
                                '&title=', urllib.parse.quote_plus(str(title)),
                                '&summary=', urllib.parse.quote_plus(str(summary)),
                                '&company_name=', urllib.parse.quote_plus(str(company_name)),
                                '&email=', urllib.parse.quote_plus(str(email)),
                                '&tel_number=', urllib.parse.quote_plus(str(tel_number)),
                                '&fax_number=', urllib.parse.quote_plus(str(fax_number)),
                                '&tax_number=', urllib.parse.quote_plus(str(tax_number)),
                                '&phone_number=', urllib.parse.quote_plus(str(phone_number)),
                                '&line_id=', urllib.parse.quote_plus(str(line_id)),
                                '&address=', urllib.parse.quote_plus(str(address))
                            ]
                        )
                    )
                )
            ]
        )
    )
    
    message = FlexSendMessage(
        alt_text='名片掃描完成！', contents=bubble_template)
    return message
