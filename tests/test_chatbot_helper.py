from app import db, create_app
import json, unittest
from app.models import User
from app.chatbot.helper import group_helper_message, store_helper_message




class GroupHelperMessageTestCase(unittest.TestCase):
    def setUp(self):

        self.result_message = group_helper_message("line_user_id")
        self.expected_message = {
            "type": "flex",
            "altText": "蹦蹦！蹦～找我嗎？",
            "contents": {
                "contents": [
                    {
                        "body": {
                            "contents": [
                                {
                                    "color": "#1DB446",
                                    "size": "lg",
                                    "text": "我是 MiKA",
                                    "type": "text",
                                    "weight": "bold",
                                    "wrap": True
                                },
                                {
                                    "margin": "md",
                                    "size": "md",
                                    "text": "我可以幫你打理群組裡頭的大小活動喔！",
                                    "type": "text",
                                    "wrap": True
                                }
                            ],
                            "layout": "vertical",
                            "type": "box"
                        },
                        "footer": {
                            "contents": [
                                {
                                    "action": {
                                        "label": "近期活動",
                                        "text": "近期活動",
                                        "type": "message"
                                    },
                                    "height": "sm",
                                    "style": "link",
                                    "type": "button"
                                },
                                {
                                    "type": "separator"
                                },
                                {
                                    "action": {
                                        "label": "新增活動",
                                        "type": "uri",
                                        "uri": "line://app/1615255233-ZpK3k8JK?source_id=line_user_id"
                                    },
                                    "height": "sm",
                                    "style": "link",
                                    "type": "button"
                                }
                            ],
                            "layout": "horizontal",
                            "spacing": "sm",
                            "type": "box"
                        },
                        "hero": {
                            "aspectMode": "cover",
                            "aspectRatio": "5:4",
                            "size": "full",
                            "type": "image",
                            "url": "https://i.imgur.com/XICiMgE.jpg"
                        },
                        "type": "bubble"
                    },
                    {
                        "body": {
                            "contents": [
                                {
                                    "color": "#1DB446",
                                    "size": "lg",
                                    "text": "也可以叫我咪卡",
                                    "type": "text",
                                    "weight": "bold",
                                    "wrap": True
                                },
                                {
                                    "margin": "md",
                                    "size": "md",
                                    "text": "想讓大家認識你嗎？在群組遞上名片也不是問題喔！",
                                    "type": "text",
                                    "wrap": True
                                }
                            ],
                            "layout": "vertical",
                            "type": "box"
                        },
                        "footer": {
                            "contents": [
                                {
                                    "action": {
                                        "label": "我的名片",
                                        "text": "我的名片",
                                        "type": "message"
                                    },
                                    "height": "sm",
                                    "style": "link",
                                    "type": "button"
                                }
                            ],
                            "layout": "vertical",
                            "type": "box"
                        },
                        "hero": {
                            "aspectMode": "cover",
                            "aspectRatio": "5:4",
                            "size": "full",
                            "type": "image",
                            "url": "https://i.imgur.com/JpX9kt6.jpg"
                        },
                        "type": "bubble"
                    }
                ],
                "type": "carousel"
            }
        }

    def test_group_helper_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )


class AdminDoorMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        user = User(
            line_user_id='line_user_id',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()
         #if posrback card.id=1
        self.result_message = store_helper_message("line_user_id")
        self.expected_message = {
            "type": "flex",
            "altText": "MiKA STORE！",
            "contents": {
                "type": "bubble",
                "body": {
                    "contents": [
                        {
                            "color": "#1DB446",
                            "size": "lg",
                            "text": "MiKA STORE",
                            "type": "text",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "margin": "md",
                            "size": "md",
                            "text": "你可以在這裏更換名片角色或者是遞名片的動畫，妝點你的卡片！",
                            "type": "text",
                            "wrap": True
                        }
                    ],
                    "layout": "vertical",
                    "type": "box"
                },
                "footer": {
                    "contents": [
                        {
                            "action": {
                                "label": "打開",
                                "type": "uri",
                                "uri": "line://app/1615255233-eXg8l0Yg?user_id=1"
                            },
                            "height": "sm",
                            "style": "link",
                            "type": "button"
                        }
                    ],
                    "layout": "vertical",
                    "spacing": "sm",
                    "type": "box"
                }
            }
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_admin_door_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )