from app import db, create_app
from app.models import Admin
import json, unittest
from app.chatbot.admin import admin_door_message

class AdminDoorMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        admin = Admin(
            line_user_id='line_user_id',
            deleted_at=None
        )

        db.session.add_all([admin])
        db.session.commit()
         #if posrback card.id=1
        self.result_message = admin_door_message("line_user_id")
        self.expected_message = {
            "altText": "管理員安安",
            "contents": {
                "body": {
                    "contents": [
                        {
                            "color": "#1DB446",
                            "size": "lg",
                            "text": "Dashboard",
                            "type": "text",
                            "weight": "bold",
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
                                "label": "OPEN",
                                "type": "uri",
                                "uri": "?line_user_id=line_user_id"
                            },
                            "height": "sm",
                            "style": "link",
                            "type": "button"
                        }
                    ],
                    "layout": "vertical",
                    "spacing": "sm",
                    "type": "box"
                },
                "type": "bubble"
            },
            "type": "flex"
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

class NotAdminDoorMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        admin = Admin(
            line_user_id=None,
            deleted_at=None
        )

        db.session.add_all([admin])
        db.session.commit()
         #if posrback card.id=1
        self.result_message = admin_door_message("line_user_id")
        self.expected_message = {
            "type": "text",
            "text": "咪卡也發大財！"
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_not_admin_door_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
