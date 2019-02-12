import datetime
import json
import urllib

import boto3
import requests
from flask import Flask
from linebot import LineBotApi
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, TextComponent, URIAction)

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])

BUCKET_NAME = 'lassie-image'
SCAN_CARD_TMP_PATH = 'app/static/tmp/card_tmp.png'

def scan_card_image_message(image_id, line_user_id):
    image_file = line_bot_api.get_message_content(image_id)
    img_data = image_file.content

    # Download image to local
    with open(SCAN_CARD_TMP_PATH, 'wb') as handler:
        handler.write(img_data)

    file_name = ''.join(['mika/', line_user_id, '-', datetime.datetime.today().strftime('%Y-%m-%d-%H-%M'), '.png'])

    # Upload image to s3
    client = boto3.client('s3', region_name='ap-southeast-1')
    client.upload_file(SCAN_CARD_TMP_PATH, BUCKET_NAME, file_name)

    # Post to OCR API
    data = {
        "image_url": ''.join([app.config['OCR_SCAN_CARD_RESOURCE'], file_name]),
    }

    response = requests.post(
        app.config['OCR_SCAN_CARD_API_PATH'],
        json = data
    )

    response_json = json.loads(response.text)

    if response_json['status'] == 'success':
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
                                    'name=', urllib.parse.quote_plus(response_json['card']['personal']['name']),
                                    '&nickname=', urllib.parse.quote_plus(response_json['card']['personal']['nickname']),
                                    '&title=', urllib.parse.quote_plus(response_json['card']['personal']['title']),
                                    '&summary=', urllib.parse.quote_plus(response_json['card']['office']['summary']),
                                    '&company_name=', urllib.parse.quote_plus(response_json['card']['office']['name']),
                                    '&email=', urllib.parse.quote_plus(response_json['card']['office']['email']),
                                    '&tel_number=', urllib.parse.quote_plus(response_json['card']['office']['tel_number']),
                                    '&fax_number=', urllib.parse.quote_plus(response_json['card']['office']['fax_number']),
                                    '&tax_number=', urllib.parse.quote_plus(response_json['card']['office']['tax_number']),
                                    '&phone_number=', urllib.parse.quote_plus(response_json['card']['personal']['phone_number']),
                                    '&line_id=', urllib.parse.quote_plus(response_json['card']['office']['line_id']),
                                    '&address=', urllib.parse.quote_plus(response_json['card']['office']['address'])
                                ]
                            )
                        )
                    )
                ]
            )
        )
    else:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='錯誤',
                        weight='bold',
                        size='md',
                    ),
                    TextComponent(
                        text='發生了一些不可預期的錯誤，請稍後再嘗試使用此功能',
                        margin='md',
                        wrap=True,
                        color='#666666',
                        size='sm',
                    )
                ]
            )
        )
    message = FlexSendMessage(
        alt_text='名片掃描完成！', contents=bubble_template)
    return message
