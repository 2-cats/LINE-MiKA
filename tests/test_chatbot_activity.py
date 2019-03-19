from app import db, create_app
from app.models import Activity, User
import datetime, json, unittest
from app.chatbot.activity import (my_activity_message, delete_my_activity)

class MyActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

      # Create fake User data
        user = User(
            line_user_id='line_user_id',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()
        now = datetime.datetime.now()
        activity = Activity(
            user_id=user.id,
            title='員工旅遊',
            description='谷林發大財',
            organizer='谷林運算',
            address='鹿兒島',
            lat='31.5969',
            lng='130.557',
            rel_link='',
            session_limit='10',
            session_count='3',
            group_link='',
            public=True,
            start_at=now + datetime.timedelta(hours=5),
            end_at=now + datetime.timedelta(hours=8),
            deleted_at=None
        )

        db.session.add_all([activity])
        db.session.commit()
        self.result_message = my_activity_message(user.line_user_id)
        self.expected_message = {
            "altText": "我的活動清單",
            "contents": {
                "type": "carousel",
                "contents": [
                    {
                        "body": {
                            "contents": [
                                {
                                    "color": "#1DB446",
                                    "size": "md",
                                    "text": "員工旅遊",
                                    "type": "text",
                                    "weight": "bold",
                                    "wrap": True
                                },
                                {
                                    "color": "#666666",
                                    "margin": "md",
                                    "size": "sm",
                                    "text": "谷林發大財",
                                    "type": "text",
                                    "wrap": True
                                },
                                {
                                    "contents": [
                                        {
                                            "color": "#666666",
                                            "flex": 2,
                                            "size": "md",
                                            "text": "開始日期",
                                            "type": "text",
                                            "wrap": True
                                        },
                                        {
                                            "color": "#333333",
                                            "flex": 5,
                                            "margin": "sm",
                                            "size": "sm",
                                            "text": activity.start_at.strftime("%Y/%m/%d %H:%M"),
                                            "type": "text"
                                        }
                                    ],
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "type": "box"
                                },
                                {
                                    "contents": [
                                        {
                                            "color": "#666666",
                                            "flex": 2,
                                            "size": "md",
                                            "text": "結束日期",
                                            "type": "text",
                                            "wrap": True
                                        },
                                        {
                                            "color": "#333333",
                                            "flex": 5,
                                            "margin": "sm",
                                            "size": "sm",
                                            "text": activity.end_at.strftime("%Y/%m/%d %H:%M"),
                                            "type": "text"
                                        }
                                    ],
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "type": "box"
                                },
                                {
                                    "contents": [
                                        {
                                            "color": "#666666",
                                            "flex": 2,
                                            "size": "md",
                                            "text": "位置",
                                            "type": "text"
                                        },
                                        {
                                            "color": "#333333",
                                            "flex": 5,
                                            "margin": "sm",
                                            "size": "sm",
                                            "text": "鹿兒島",
                                            "type": "text",
                                            "wrap": True
                                        }
                                    ],
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "type": "box"
                                }
                            ],
                            "layout": "vertical",
                            "type": "box"
                        },
                        "footer": {
                            "contents": [
                                {
                                    "action": {
                                        "label": "位置導航",
                                        "type": "uri",
                                        "uri": "https://www.google.com/maps/search/?api="
                                               "1&query=31.5969,130.557"
                                    },
                                    "height": "sm",
                                    "style": "link",
                                    "type": "button"
                                },
                                {
                                    "action": {
                                        "data": "delete_my_activity,1",
                                        "label": "刪除活動",
                                        "type": "postback"
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
                    {
                        "body": {
                            "contents": [
                                {
                                    "color": "#1DB446",
                                    "size": "md",
                                    "text": "新增活動",
                                    "type": "text",
                                    "weight": "bold"
                                },
                                {
                                    "color": "#666666",
                                    "margin": "md",
                                    "size": "sm",
                                    "text": "請點我，新增活動唷！",
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
                                        "label": "新增活動",
                                        "type": "uri",
                                        "uri": "line://app/1615255233-GWBxWODB"
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
                    }
                ]
            },
            "type": "flex"
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_my_activity_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )

class MyActivityHaveRellinkMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

      # Create fake User data
        user = User(
            line_user_id='line_user_id',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()
        now = datetime.datetime.now()
        activity = Activity(
            user_id=user.id,
            title='員工旅遊',
            description='谷林發大財',
            organizer='谷林運算',
            address='鹿兒島',
            lat='31.5969',
            lng='130.557',
            rel_link='https://tw.yahoo.com/',
            session_limit='10',
            session_count='3',
            group_link='',
            public=True,
            start_at=now + datetime.timedelta(hours=5),
            end_at=now + datetime.timedelta(hours=8),
            deleted_at=None
        )

        db.session.add_all([activity])
        db.session.commit()
        self.result_message = my_activity_message(user.line_user_id)
        self.expected_message = {
            "altText": "我的活動清單",
            "contents": {
                "type": "carousel",
                "contents": [
                    {
                        "body": {
                            "contents": [
                                {
                                    "color": "#1DB446",
                                    "size": "md",
                                    "text": "員工旅遊",
                                    "type": "text",
                                    "weight": "bold",
                                    "wrap": True
                                },
                                {
                                    "color": "#666666",
                                    "margin": "md",
                                    "size": "sm",
                                    "text": "谷林發大財",
                                    "type": "text",
                                    "wrap": True
                                },
                                {
                                    "contents": [
                                        {
                                            "color": "#666666",
                                            "flex": 2,
                                            "size": "md",
                                            "text": "開始日期",
                                            "type": "text",
                                            "wrap": True
                                        },
                                        {
                                            "color": "#333333",
                                            "flex": 5,
                                            "margin": "sm",
                                            "size": "sm",
                                            "text": activity.start_at.strftime("%Y/%m/%d %H:%M"),
                                            "type": "text"
                                        }
                                    ],
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "type": "box"
                                },
                                {
                                    "contents": [
                                        {
                                            "color": "#666666",
                                            "flex": 2,
                                            "size": "md",
                                            "text": "結束日期",
                                            "type": "text",
                                            "wrap": True
                                        },
                                        {
                                            "color": "#333333",
                                            "flex": 5,
                                            "margin": "sm",
                                            "size": "sm",
                                            "text": activity.end_at.strftime("%Y/%m/%d %H:%M"),
                                            "type": "text"
                                        }
                                    ],
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "type": "box"
                                },
                                {
                                    "contents": [
                                        {
                                            "color": "#666666",
                                            "flex": 2,
                                            "size": "md",
                                            "text": "位置",
                                            "type": "text"
                                        },
                                        {
                                            "color": "#333333",
                                            "flex": 5,
                                            "margin": "sm",
                                            "size": "sm",
                                            "text": "鹿兒島",
                                            "type": "text",
                                            "wrap": True
                                        }
                                    ],
                                    "layout": "horizontal",
                                    "margin": "md",
                                    "type": "box"
                                }
                            ],
                            "layout": "vertical",
                            "type": "box"
                        },
                        "footer": {
                            "contents": [
                                {
                                    "action": {
                                        "label": "相關連結",
                                        "type": "uri",
                                        "uri": "https://tw.yahoo.com/"
                                    },
                                    "height": "sm",
                                    "style": "link",
                                    "type": "button"
                                },
                                {
                                    "action": {
                                        "label": "位置導航",
                                        "type": "uri",
                                        "uri": "https://www.google.com/maps/search/?api="
                                               "1&query=31.5969,130.557"
                                    },
                                    "height": "sm",
                                    "style": "link",
                                    "type": "button"
                                },
                                {
                                    "action": {
                                        "data": "delete_my_activity,1",
                                        "label": "刪除活動",
                                        "type": "postback"
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
                    {
                        "body": {
                            "contents": [
                                {
                                    "color": "#1DB446",
                                    "size": "md",
                                    "text": "新增活動",
                                    "type": "text",
                                    "weight": "bold"
                                },
                                {
                                    "color": "#666666",
                                    "margin": "md",
                                    "size": "sm",
                                    "text": "請點我，新增活動唷！",
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
                                        "label": "新增活動",
                                        "type": "uri",
                                        "uri": "line://app/1615255233-GWBxWODB"
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
                    }
                ]
            },
            "type": "flex"
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_my_activity_message_with_rellink(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )

class NoMyActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

      # Create fake User data
        user = User(
            line_user_id='line_user_id',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()
        now = datetime.datetime.now()
        activity = Activity(
            user_id=None,
            title='員工旅遊',
            description='谷林發大財',
            organizer='谷林運算',
            address='鹿兒島',
            lat='31.5969',
            lng='130.557',
            rel_link='',
            session_limit='10',
            session_count='3',
            group_link='',
            public=True,
            start_at=now + datetime.timedelta(hours=5),
            end_at=now + datetime.timedelta(hours=8),
            deleted_at=None
        )

        db.session.add_all([activity])
        db.session.commit()
        self.result_message = my_activity_message(user.line_user_id)
        self.expected_message = {
            "altText": "新增活動",
            "contents": {
                "body": {
                    "contents": [
                        {
                            "color": "#1DB446",
                            "size": "md",
                            "text": "您尚未有任何活動！",
                            "type": "text",
                            "weight": "bold"
                        },
                        {
                            "color": "#666666",
                            "margin": "md",
                            "size": "sm",
                            "text": "請點我，新增活動唷！",
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
                                "label": "新增活動",
                                "type": "uri",
                                "uri": "line://app/1615255233-GWBxWODB"
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

    def test_no_my_activity_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )

class DeleteMyActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

      # Create fake User data
        user = User(
            line_user_id='line_user_id',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()
        now = datetime.datetime.now()
        activity = Activity(
            user_id=user.id,
            title='員工旅遊',
            description='谷林發大財',
            organizer='谷林運算',
            address='鹿兒島',
            lat='31.5969',
            lng='130.557',
            rel_link='',
            session_limit='10',
            session_count='3',
            group_link='',
            public=True,
            start_at=now + datetime.timedelta(hours=5),
            end_at=now + datetime.timedelta(hours=8),
            deleted_at=None
        )

        db.session.add_all([activity])
        db.session.commit()
        self.result_message = delete_my_activity('1')
        self.expected_message = {
            "type": "text",
            "text": "刪除成功！"
        }
    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_delete_my_activity_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
