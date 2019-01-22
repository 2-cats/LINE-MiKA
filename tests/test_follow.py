import json
import unittest

import responses
from linebot import LineBotApi

from app.chatbot.follow import follow_message, unfollow


class FollowTestCase(unittest.TestCase):
    '''
    Test follow
    '''
    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data
        self.result_message = follow_message('line_user_id')
        self.expected_message = [
            {
                "type":"flex",
                "altText":"歡迎您的加入",
                "contents":{
                    "type":"bubble",
                    "body":{
                        "contents":[
                            {
                                "size":"lg",
                                "text":"歡迎加入",
                                "type":"text",
                                "weight":"bold",
                                "wrap":True
                            },
                            {
                                "margin":"md",
                                "size":"md",
                                "text":"您好，我是 Lassie！我致力於打造一個連結各種設備與用戶之間聰明、可靠、友善的互動系統，讓用戶能隨時掌握設備狀況建立連結！第一次使用請先完成綁定喔！",
                                "type":"text",
                                "wrap":True
                            }
                        ],
                        "layout":"vertical",
                        "type":"box"
                    }
                }
            }
        ]

    @responses.activate
    def test_follow_message(self):
        '''
        Test reply follow event message
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
    
class UnfollowTestCase(unittest.TestCase):

    def test_unfollow(self):
        '''
        Test reply unfollow
        '''
        unfollow('line_user_id')
