import json
import unittest

import responses
from linebot import LineBotApi

from app.chatbot.device import (get_device_list_data, have_device_message,
                                no_device_message)


class DeviceDataTestCase(unittest.TestCase):
    '''
    Test device
    '''
    def setUp(self):
        '''
        Set up test
        '''
        # test data
        self.result_message = get_device_list_data('line_user_id')
        self.expected_message = [
           
        ]
        self.assertEquals(self.result_message, self.expected_message)

class HaveDeviceMessageTestCase(unittest.TestCase):
    '''
    Test device
    '''
    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data
        self.result_message = have_device_message(
            'line_user_id', 
            [
                {
                    'name': 'Thing01',
                    'device_status': '連接中',
                    'text_color': '#1DB446'
                },
                {
                    'name': 'Thing02',
                    'device_status': '離線',
                    'text_color': '#FF3333'
                },

            ]
            
        )
        self.expected_message = [
           {
                "type":"flex",
                "altText":"您的設備清單",
                "contents":{
                    "type":"carousel",
                    "contents":[
                        {
                            "type":"bubble",
                            "body":{
                                "layout":"vertical",
                                "type":"box",
                                "contents":[
                                    {
                                        "size":"lg",
                                        "text":"Thing01",
                                        "type":"text",
                                        "weight":"bold",
                                        "wrap":True
                                    },
                                    {
                                        "color":"#1DB446",
                                        "margin":"md",
                                        "size":"sm",
                                        "text":"連接中",
                                        "type":"text",
                                        "wrap":True
                                    }
                                ]
                            }
                        },
                        {
                        "body":{
                            "layout":"vertical",
                            "type":"box",
                            "contents":[
                                {
                                    "size":"lg",
                                    "text":"Thing02",
                                    "type":"text",
                                    "weight":"bold",
                                    "wrap":True
                                },
                                {
                                    "color":"#FF3333",
                                    "margin":"md",
                                    "size":"sm",
                                    "text":"離線",
                                    "type":"text",
                                    "wrap":True
                                }
                            ]
                        },
                        "type":"bubble"
                        }
                    ],
                    
                }
            }
        ]

    @responses.activate
    def test_have_device_message(self):
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

class NoDeviceMessageTestCase(unittest.TestCase):
    '''
    Test device
    '''
    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data
        self.result_message = no_device_message('line_user_id')
        self.expected_message = [
           {
                "text":"您尚未使用任何萊西！",
                "type":"text"
            }
        ]

    @responses.activate
    def test_no_device_message(self):
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
