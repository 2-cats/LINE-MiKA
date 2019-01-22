import json
import unittest

import responses
from linebot import LineBotApi

from app.chatbot.report import make_report_message


class ReportTestCase(unittest.TestCase):
    '''
    Test report
    '''
    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data
        self.result_message = make_report_message()
        self.expected_message = [
            {
                "text":"好的，我正在為您準備報表，請稍候！",
                "type":"text"
            }
        ]

    @responses.activate
    def test_report_message(self):
        '''
        Test reply report message
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