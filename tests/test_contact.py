import json
import unittest

import responses
from linebot import LineBotApi

from app.chatbot.contact import contact_us


class ContactTestCase(unittest.TestCase):
    '''
    Test contact
    '''
    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data
        self.result_message = contact_us('line_user_id')
        self.expected_message = [
            {
                "altText":"遇到問題",
                "type":"flex",
                "contents":{
                    "body":{
                        "contents":[
                            {
                                "color":"#17c950",
                                "size":"xl",
                                "text":"遇到問題？",
                                "type":"text",
                                "weight":"bold",
                                "wrap":True
                            },
                            {
                                "margin":"md",
                                "size":"lg",
                                "text":"如果在使用上遇到問題，歡迎直接聯繫我們的客服！",
                                "type":"text",
                                "wrap":True
                            }
                        ],
                        "flex":1,
                        "layout":"vertical",
                        "margin":"md",
                        "spacing":"sm",
                        "type":"box"
                    },
                    "direction":"ltr",
                    "type":"bubble",
                    "footer":{
                        "contents":[
                            {
                                "action":{
                                    "label":"LINE@ 客服",
                                    "type":"uri",
                                    "uri":"line://ti/p/@gtb6688a"
                                },
                                "style":"link",
                                "type":"button"
                            },
                            {
                                "action":{
                                    "label":"電話客服",
                                    "type":"uri",
                                    "uri":"tel:02-82315949"
                                },
                                "style":"link",
                                "type":"button"
                            }
                        ],
                        "layout":"vertical",
                        "margin":"md",
                        "type":"box"
                    }
                }
            }
        ]

    @responses.activate
    def test_contact_message(self):
        '''
        Test reply contact event message
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
    