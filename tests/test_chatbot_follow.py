from app import db, create_app
import json, unittest
from app.chatbot.follow import follow_message

class FollowMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.result_message = follow_message("line_user_id")
        self.expected_message = [
            {
                "altText": "歡迎加入",
                "contents": {
                    "body": {
                        "contents": [
                            {
                                "color": "#1DB446",
                                "size": "lg",
                                "text": "歡迎加入",
                                "type": "text",
                                "weight": "bold",
                                "wrap": True
                            },
                            {
                                "margin": "md",
                                "size": "md",
                                "text": "嗨，我是 MiKA ，也可以叫我咪卡，我可以幫你找名片、遞名片、辦活動！\n\n先來試試看搜尋名片吧！",
                                "type": "text",
                                "wrap": True
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
                        "url": "https://i.imgur.com/AOCMVKP.jpg"
                    },
                    "type": "bubble"
                },
                "type": "flex"
            },
            {
                "originalContentUrl": "https://i.imgur.com/Hn6lBtg.jpgstatic/video/follow.mp4",
                "previewImageUrl": "https://i.imgur.com/N1Hpitz.jpg",
                "type": "video"
            }
        ]

    def test_follow_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
