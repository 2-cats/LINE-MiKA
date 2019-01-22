import json
import unittest

import responses
from linebot import LineBotApi

from app.models import User


class UserTestCase(unittest.TestCase):
    '''
    Test contact
    '''
    def setUp(self):
        self.user1 = User.query.filter_by(line_user_id='Ud70573ef58ee136041925101bc130d72').first()
        self.expected_user_name = 'e2ab6bae-834f-4a6b-b295-dfb6304b76c6'

        self.user2 = User.query.filter_by(aws_user_name='e2ab6bae-834f-4a6b-b295-dfb6304b76c6').first()
        self.expected_line_user_id = 'Ud70573ef58ee136041925101bc130d72'
    
    def test_aws_user_name(self):
        self.assertEquals(self.expected_user_name, self.user1.aws_user_name)
    
    def test_line_user_id(self):
        self.assertEquals(self.expected_line_user_id, self.user2.line_user_id)

