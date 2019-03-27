from app import db, create_app
from app.models import Group, GroupActivity, GroupActivityLog, User
import datetime, json, unittest
from app.chatbot.group_activity import (group_activity_message, join_group_activity_message, leave_group_activity_message)
#in this test , we used true line_user_id to get user_profile

class GroupActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

      # Create fake User data
        group = Group(
            group_id='group_id',
            deleted_at=None
        )

        db.session.add_all([group])
        db.session.commit()

        now = datetime.datetime.now()

        activitys = GroupActivity(
            group_id=group.id,
            activity_type='體育',
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

        db.session.add_all([activitys])
        db.session.commit()

        self.result_message = group_activity_message(group.group_id)
        self.expected_message = {
            "type": "flex",
            "altText": "群組活動清單",
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
                                    "text": "體育",
                                    "type": "text",
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
                                            "text": "開始時間",
                                            "type": "text",
                                            "wrap": True
                                        },
                                        {
                                            "color": "#333333",
                                            "flex": 5,
                                            "margin": "sm",
                                            "size": "sm",
                                            "text": activitys.start_at.strftime("%Y/%m/%d %H:%M"),
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
                                            "text": "結束時間",
                                            "type": "text",
                                            "wrap": True
                                        },
                                        {
                                            "color": "#333333",
                                            "flex": 5,
                                            "margin": "sm",
                                            "size": "sm",
                                            "text": activitys.end_at.strftime("%Y/%m/%d %H:%M"),
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
                                            "text": "人數",
                                            "type": "text",
                                            "wrap": True
                                        },
                                        {
                                            "color": "#333333",
                                            "flex": 5,
                                            "margin": "sm",
                                            "size": "sm",
                                            "text": "3/10",
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
                                    "contents": [
                                        {
                                            "action": {
                                                "data": "join_group_activity,1",
                                                "label": "加一",
                                                "type": "postback"
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
                                                "data": "leave_group_activity,1",
                                                "label": "減一",
                                                "type": "postback"
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
                                {
                                    "action": {
                                        "label": "位置導航",
                                        "type": "uri",
                                        "uri": "https://www.google.com/maps/search/?api=1&query=31.5969,130.557"
                                    },
                                    "height": "sm",
                                    "style": "link",
                                    "type": "button"
                                },
                                {
                                    "action": {
                                        "label": "有誰參加",
                                        "type": "uri",
                                        "uri": "line://app/1615255233-dkO3Vw9O?activity_id=1"
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
                        "footer": {
                            "contents": [
                                {
                                    "action": {
                                        "label": "新增活動",
                                        "type": "uri",
                                        "uri": "line://app/1615255233-ZpK3k8JK?source_id=group_id"
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
                        "hero": {
                            "aspectMode": "cover",
                            "aspectRatio": "5:4",
                            "size": "full",
                            "type": "image",
                            "url": "https://i.imgur.com/Gtj8dTV.jpg"
                        },
                        "type": "bubble"
                    }
                ]
            }
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_group_activity_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
#not friend
class NotFriendJoinGroupActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create fake User data
        user = User(
            #True line user id
            line_user_id='line_user_id',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()

        group = Group(
            group_id='group_id',
            deleted_at=None
        )

        db.session.add_all([group])
        db.session.commit()

        now = datetime.datetime.now()

        activitys = GroupActivity(
            group_id=group.id,
            activity_type='體育',
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

        db.session.add_all([activitys])
        db.session.commit()

        self.result_message = join_group_activity_message(activitys.id, 'no_line_user_id')
        self.expected_message = {
            "type": "flex",
            "altText": "加入失敗",
            "contents": {
                "body": {
                    "contents": [
                        {
                            "color": "#1DB446",
                            "size": "md",
                            "text": "加入失敗",
                            "type": "text",
                            "weight": "bold"
                        },
                        {
                            "color": "#666666",
                            "margin": "md",
                            "size": "sm",
                            "text": "請先跟咪卡我成為好友，才能加入活動，加我好友後，還可以快速方便的查詢群組活動喔！",
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
                                "label": "好！加好友！",
                                "type": "uri",
                                "uri": "https://line.me/ti/p/@zdc4653z"
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
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_join_group_activity_message_for_not_friend(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
#normalcase
class JoinGroupActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create fake User data
        user = User(
            #True line user id
            line_user_id='Ud739a32831d46aa18507233eb0a68e60',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()

        group = Group(
            group_id='group_id',
            deleted_at=None
        )

        db.session.add_all([group])
        db.session.commit()

        now = datetime.datetime.now()

        activitys = GroupActivity(
            group_id=group.id,
            activity_type='體育',
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

        db.session.add_all([activitys])
        db.session.commit()

        self.result_message = join_group_activity_message(activitys.id, user.line_user_id)
        self.expected_message = {
            'text': '小寶 成功參加活動 員工旅遊 囉！', 'type': 'text'}

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_join_group_activity_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
#normal case + too late to join
class TooLateToJoinGroupActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create fake User data
        user = User(
            #True line user id
            line_user_id='Ud739a32831d46aa18507233eb0a68e60',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()

        group = Group(
            group_id='group_id',
            deleted_at=None
        )

        db.session.add_all([group])
        db.session.commit()

        now = datetime.datetime.now()

        activitys = GroupActivity(
            group_id=group.id,
            activity_type='體育',
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
            start_at=now + datetime.timedelta(hours=-5),
            end_at=now + datetime.timedelta(hours=8),
            deleted_at=None
        )

        db.session.add_all([activitys])
        db.session.commit()

        self.result_message = join_group_activity_message(activitys.id, user.line_user_id)
        self.expected_message = {
            "type": "text",
            "text": "小寶 想參加活動 員工旅遊 ，但是活動時間已經開始或是結束"
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_join_group_activity_message_for_too_late(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
#normal case + ober limit
class OverLimitToJoinGroupActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create fake User data
        user = User(
            #True line user id
            line_user_id='Ud739a32831d46aa18507233eb0a68e60',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()

        group = Group(
            group_id='group_id',
            deleted_at=None
        )

        db.session.add_all([group])
        db.session.commit()

        now = datetime.datetime.now()

        activitys = GroupActivity(
            group_id=group.id,
            activity_type='體育',
            title='員工旅遊',
            description='谷林發大財',
            organizer='谷林運算',
            address='鹿兒島',
            lat='31.5969',
            lng='130.557',
            rel_link='',
            session_limit='10',
            session_count='10',
            group_link='',
            public=True,
            start_at=now + datetime.timedelta(hours=5),
            end_at=now + datetime.timedelta(hours=8),
            deleted_at=None
        )

        db.session.add_all([activitys])
        db.session.commit()

        activity_log = GroupActivityLog(
            group_activity_id=activitys.id,
            user_id=user.id,
            deleted_at=None
        )

        db.session.add_all([activity_log])
        db.session.commit()

        self.result_message = join_group_activity_message(activitys.id, user.line_user_id)
        self.expected_message = {
            "type": "text",
            "text": "小寶 想參加活動 員工旅遊 ，但是人數已經超過上限"
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_join_group_activity_message_for_over_limit(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
#normal case + double participation
class DoubleParticipationToJoinGroupActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create fake User data
        user = User(
            #True line user id
            line_user_id='Ud739a32831d46aa18507233eb0a68e60',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()

        group = Group(
            group_id='group_id',
            deleted_at=None
        )

        db.session.add_all([group])
        db.session.commit()

        now = datetime.datetime.now()

        activitys = GroupActivity(
            group_id=group.id,
            activity_type='體育',
            title='員工旅遊',
            description='谷林發大財',
            organizer='谷林運算',
            address='鹿兒島',
            lat='31.5969',
            lng='130.557',
            rel_link='',
            session_limit='50',
            session_count='1',
            group_link='',
            public=True,
            start_at=now + datetime.timedelta(hours=5),
            end_at=now + datetime.timedelta(hours=8),
            deleted_at=None
        )

        db.session.add_all([activitys])
        db.session.commit()

        activity_log = GroupActivityLog(
            group_activity_id=activitys.id,
            user_id=user.id,
            deleted_at=None
        )

        db.session.add_all([activity_log])
        db.session.commit()

        self.result_message = join_group_activity_message(activitys.id, user.line_user_id)
        self.expected_message = {
            "type": "text",
            "text": "小寶 您重複參加活動 員工旅遊 囉！"
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_join_group_activity_message_for_double_participation(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
#normal case
class LeaveGroupActivityMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create fake User data
        user = User(
            #True line user id
            line_user_id='Ud739a32831d46aa18507233eb0a68e60',
            deleted_at=None
        )

        db.session.add_all([user])
        db.session.commit()

        group = Group(
            group_id='group_id',
            deleted_at=None
        )

        db.session.add_all([group])
        db.session.commit()

        now = datetime.datetime.now()

        activity = GroupActivity(
            group_id=group.id,
            activity_type='體育',
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

        activity_log = GroupActivityLog(
            group_activity_id=activity.id,
            user_id=user.id,
            deleted_at=None
        )

        db.session.add_all([activity_log])
        db.session.commit()

        self.result_message = leave_group_activity_message(activity.id, user.line_user_id)
        self.expected_message = {
            "type": "text",
            "text": "小寶 退出活動 員工旅遊"
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_leave_group_activity_message(self):

        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
