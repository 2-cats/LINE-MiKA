import unittest

from app.chatbot.bind import check_bind
from app.liff.bind import (bind_line_user_id, check_line_user_id_exist,
                           check_username_exist, query_user_data)


class BindTestCase(unittest.TestCase):
    def setUp(self):
        self.bind_user_lind_id = "Ud70573ef58ee136041925101bc130d72"
        self.unbind_user_lind_id = "line_user_id"

        self.bind_aws_user_name = "e2ab6bae-834f-4a6b-b295-dfb6304b76c6"
        self.unbind_aws_user_name= "aws_user_name"

        self.bind_phone= "+886981263972"
        self.unbind_phone= "aws_user_name"

        self.bind_email= "smart032410@gmail.com"
        self.unbind_email= "unknow@goodlinker.io"

    def test_check_bind(self):
        self.assertEquals(check_bind(self.bind_user_lind_id), True)
        self.assertEquals(check_bind(self.unbind_user_lind_id), False)
    
    def test_query_user_data(self):
        self.assertEquals(query_user_data(self.unbind_email, self.unbind_phone, self.bind_user_lind_id), 'fail: LINE account has been bind.')
        self.assertEquals(query_user_data(self.bind_email, self.bind_phone, self.unbind_user_lind_id), 'fail: User has been bind.')
        self.assertEquals(query_user_data('email', 'bind_phone', 'user_lind_id'), 'fail: User not found')
        return 0

    def test_check_username_exist(self):
        self.assertEquals(check_username_exist(self.bind_aws_user_name), True)
        self.assertEquals(check_username_exist(self.unbind_aws_user_name), False)
        return 0

    def test_check_line_user_id_exist(self):
        self.assertEquals(check_line_user_id_exist(self.bind_user_lind_id), True)
        self.assertEquals(check_line_user_id_exist(self.unbind_user_lind_id), False)
        return 0
