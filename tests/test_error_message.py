import json
import unittest

import responses
from linebot import LineBotApi

from app.chatbot.error_message import (alert_no_action_message,
                                       alert_to_bind_message)


class NoActionMessageTestCase(unittest.TestCase):
    '''
    Test error message
    '''
    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data

        self.result_message = alert_no_action_message('line_user_id')
        self.expected_message = [
            {
                "packageId":2,
                "stickerId":149,
                "type":"sticker"
            },
            {
                "type":"flex",
                "altText":"抱歉，我聽不懂指令",
                "contents":{
                    "body":{
                        "contents":[
                            {
                                "size":"lg",
                                "text":"我聽不懂你的指令",
                                "type":"text",
                                "weight":"bold",
                                "wrap":True
                            },
                            {
                                "margin":"md",
                                "size":"md",
                                "text":"抱歉，我還在學習中，聽不懂你的指令，如果有使用上的問題，歡迎聯繫我們",
                                "type":"text",
                                "wrap":True
                            }
                        ],
                        "layout":"vertical",
                        "type":"box"
                    },
                    "footer":{
                        "contents":[
                            {
                            "action":{
                                "label":"聯絡我們",
                                "text":"聯絡我們",
                                "type":"message"
                            },
                            "height":"sm",
                            "style":"link",
                            "type":"button"
                            }
                        ],
                        "layout":"vertical",
                        "type":"box"
                    },
                    "type":"bubble"
                },
            }
        ]

    @responses.activate
    def test_no_action_message(self):
        '''
        Test reply message
        '''
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            json={}, status=200
        )

        self.tested.reply_message('replyToken', self.result_message)
        
        request = responses.calls[0].request
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            json.loads(request.body),
            {
                'replyToken': 'replyToken',
                'messages': self.expected_message
            }
        )

class NoBindMessageTestCase(unittest.TestCase):
    '''
    Test error message
    '''
    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data

        self.result_message = alert_to_bind_message('line_user_id')
        self.expected_message = [
            {
                "type":"template",
                "altText":"綁定帳號",
                "template":{
                    "actions":[
                        {
                            "label":"點我進行綁定",
                            "type":"uri",
                            "uri":"line://app/1633151989-5BJ0B9EZ"
                        }
                    ],
                    "text":"您好，我是 Lassie！第一次使用嗎？完成簡單的綁定只需要三分鐘，就可以享用完整的服務！",
                    "title":"綁定服務",
                    "type":"buttons"
                }
            }
        ]

    @responses.activate
    def test_to_bind_message(self):
        '''
        Test reply to bind message
        '''
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            json={}, status=200
        )

        self.tested.reply_message('replyToken', self.result_message)
        
        request = responses.calls[0].request
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            json.loads(request.body),
            {
                'replyToken': 'replyToken',
                'messages': self.expected_message
            }
        )
