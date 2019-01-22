import json
import unittest

import responses
from linebot import LineBotApi

from app.mqtt.report import lassie_report_message


class MQTTTestCase(unittest.TestCase):
    def setUp(self):
        self.tested = LineBotApi('channel_secret')

        self.user_lind_id = "13a9cf07-b1c9-498d-80b3-47b95b6671c4"

        self.result_lassie_report_message = lassie_report_message("\"thing01 - 一號溫度機\",5")
        self.expected_lassie_report_message = [
            {
                "type":"flex",
                "altText":"今日報表",
                "contents":{
                    'type': 'bubble',
                    "body":{
                        "flex":1,
                        "layout":"vertical",
                        "margin":"md",
                        "spacing":"md",
                        "type":"box",
                        "contents":[
                            {
                                "color":"#1DB446",
                                "size":"lg",
                                "text":"今日報表",
                                "type":"text",
                                "weight":"bold"
                            },
                            {
                                "size":"md",
                                "text":"我已經幫你把今日報表整理完成了，請點擊檢視",
                                "type":"text",
                                "wrap":True
                            }
                        ]
                    },
                    "footer":{
                        "flex":1,
                        "layout":"vertical",
                        "margin":"md",
                        "spacing":"md",
                        "type":"box",
                        "contents":[
                            {
                                "action":{
                                    "label":"檢視報表",
                                    "type":"uri",
                                    "uri":"line://app/1633151989-ovydbgML?data=%22thing01+-+%E4%B8%80%E8%99%9F%E6%BA%AB%E5%BA%A6%E6%A9%9F%22%2C5"
                                },
                                "style":"link",
                                "type":"button"
                            }
                        ],
                        
                    },
                }
            }
        ]

    @responses.activate
    def test_lassie_report_message(self):
        '''
        Test reply lassie report message
        '''
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            json={}, status=200
        )

        self.tested.reply_message('replyToken', self.result_lassie_report_message)
        
        request = responses.calls[0].request
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            json.loads(request.body),
            {
                'replyToken': 'replyToken',
                'messages': self.expected_lassie_report_message
            }
        )
