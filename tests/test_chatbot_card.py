import datetime
import json
import unittest

from app import create_app, db
from app.chatbot.card import (card_management_message,delete_my_card_message,nearby_card_message,search_card_message,show_my_card_message)
from app.models import User,Card



class CardManagementMessageTestCase(unittest.TestCase):
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

       card = Card(
           user_id=user.id,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()

       self.result_message = card_management_message(user.line_user_id)
       self.expected_message = [
                  {
                    "altText": "我的名片",
                    "contents": {
                      "body": {
                        "contents": [
                          {
                            "color": "#1DB446",
                            "size": "md",
                            "text": "test公司",
                            "type": "text",
                            "weight": "bold",
                            "wrap": True
                          },
                          {
                            "color": "#666666",
                            "margin": "md",
                            "size": "sm",
                            "text": "test內容",
                            "type": "text",
                            "wrap": True
                          },
                          {
                            "contents": [
                              {
                                "color": "#666666",
                                "flex": 2,
                                "size": "md",
                                "text": "姓名",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test 87",
                                "type": "text",
                                "wrap": True
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
                                "text": "職稱",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test",
                                "type": "text",
                                "wrap": True
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
                                "text": "地址",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test",
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
                              "data": "delete_my_card,1",
                              "label": "刪除名片",
                              "type": "postback"
                            },
                            "height": "sm",
                            "style": "link",
                            "type": "button"
                          },
                          {
                            "action": {
                              "label": "更新名片",
                              "type": "uri",
                              "uri": "line://app/1615255233-wn5EjnJ5?id=1"
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
                        "url": "https://i.imgur.com/Hn6lBtg.jpgstatic/img/card/cosplay/default.png"
                      },
                      "type": "bubble"
                    },
                    "type": "flex"
                  }
                ]

   def tearDown(self):
       db.session.remove()  # Remove database session
       db.drop_all()  # Drop database
       self.app_context.pop()

   def test_card_management_message(self):

       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )


class CardManagementMessageNoCardTestCase(unittest.TestCase):
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

       card = Card(
           user_id=None,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()

       self.result_message = card_management_message(user.line_user_id)
       self.expected_message = {
                  "type": "flex",
                  "altText": "新增名片",
                  "contents": {
                    "body": {
                      "contents": [
                        {
                          "size": "lg",
                          "text": "找不到你的名片",
                          "type": "text",
                          "weight": "bold",
                          "wrap": True
                        },
                        {
                          "margin": "md",
                          "size": "md",
                          "text": "找不到你的名片，試著新增一張名片吧",
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
                            "data": "scan_card_confirm,",
                            "label": "智慧新增名片",
                            "type": "postback"
                          },
                          "height": "sm",
                          "style": "link",
                          "type": "button"
                        },
                        {
                          "action": {
                            "label": "手動新增名片",
                            "type": "uri",
                            "uri": "line://app/1615255233-18kbn2ak"
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

   def test_no_card_management_message(self):
        #for no card
       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )


class CardManagementMessageHaveImgurlTestCase(unittest.TestCase):
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

       card = Card(
           user_id=user.id,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='https://i.imgur.com/Hn6lBtg.jpg',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()

       self.result_message = card_management_message(user.line_user_id)
       self.expected_message = [
                  {
                    "type": "flex",
                    "altText": "我的名片",
                    "contents": {
                      "body": {
                        "contents": [
                          {
                            "color": "#1DB446",
                            "size": "md",
                            "text": "test公司",
                            "type": "text",
                            "weight": "bold",
                            "wrap": True
                          },
                          {
                            "color": "#666666",
                            "margin": "md",
                            "size": "sm",
                            "text": "test內容",
                            "type": "text",
                            "wrap": True
                          },
                          {
                            "contents": [
                              {
                                "color": "#666666",
                                "flex": 2,
                                "size": "md",
                                "text": "姓名",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test 87",
                                "type": "text",
                                "wrap": True
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
                                "text": "職稱",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test",
                                "type": "text",
                                "wrap": True
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
                                "text": "地址",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test",
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
                              "data": "delete_my_card,1",
                              "label": "刪除名片",
                              "type": "postback"
                            },
                            "height": "sm",
                            "style": "link",
                            "type": "button"
                          },
                          {
                            "action": {
                              "label": "更新名片",
                              "type": "uri",
                              "uri": "line://app/1615255233-wn5EjnJ5?id=1"
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
                        "action": {
                          "type": "uri",
                          "uri": "?card_id=1"
                        },
                        "aspectMode": "cover",
                        "aspectRatio": "5:4",
                        "size": "full",
                        "type": "image",
                        "url": "https://i.imgur.com/Hn6lBtg.jpgstatic/img/card/cosplay/default.png"
                      },
                      "type": "bubble"
                    }
                  }
                ]

   def tearDown(self):
       db.session.remove()  # Remove database session
       db.drop_all()  # Drop database
       self.app_context.pop()

   def test_card_management_have_imgurl_message(self):

       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )

class DeleteMyCardMessageTestCase(unittest.TestCase):
   def setUp(self):
       self.app = create_app('testing')
       self.app_context = self.app.app_context()
       self.app_context.push()
       db.create_all()




       card = Card(
           user_id='1',
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()
        #if posrback card.id=1
       self.result_message = delete_my_card_message("1")
       self.expected_message = {
                  "type": "text",
                  "text": "刪除成功！"
                }

   def tearDown(self):
       db.session.remove()  # Remove database session
       db.drop_all()  # Drop database
       self.app_context.pop()

   def test_delete_my_card_message(self):

       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )



class NearByCardMessageTestCase(unittest.TestCase):
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

       card = Card(
           user_id=user.id,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()

       self.result_message = nearby_card_message(38.7,78.8,'line_user_id')
       self.expected_message = {
                  "type": "flex",
                  "altText": "搜尋名片清單",
                  "contents": {
                    "type": "carousel",
                    "contents": [
                      {
                        "body": {
                          "contents": [
                            {
                              "color": "#1DB446",
                              "size": "md",
                              "text": "test公司",
                              "type": "text",
                              "weight": "bold",
                              "wrap": True
                            },
                            {
                              "color": "#666666",
                              "margin": "md",
                              "size": "sm",
                              "text": "test內容",
                              "type": "text",
                              "wrap": True
                            },
                            {
                              "contents": [
                                {
                                  "color": "#666666",
                                  "flex": 2,
                                  "size": "md",
                                  "text": "姓名",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test 87",
                                  "type": "text",
                                  "wrap": True
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
                                  "text": "職稱",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test",
                                  "type": "text",
                                  "wrap": True
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
                                  "text": "地址",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test",
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
                                "label": "電話",
                                "type": "uri",
                                "uri": "tel:0987654321"
                              },
                              "height": "sm",
                              "style": "link",
                              "type": "button"
                            },
                            {
                              "action": {
                                "label": "LINE",
                                "type": "uri",
                                "uri": "line://ti/p/line_user_id"
                              },
                              "height": "sm",
                              "style": "link",
                              "type": "button"
                            },
                            {
                              "action": {
                                "label": "e-mail",
                                "type": "uri",
                                "uri": "mailto:8740@gmail.com"
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
                          "aspectRatio": "20:13",
                          "size": "full",
                          "type": "image",
                          "url": "https://i.imgur.com/Hn6lBtg.jpgstatic/img/card/cosplay/default.png"
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

   def test_nearby_card_message(self):
       # test bearby for one card
       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )


class NearByCardMessageForNoCardTestCase(unittest.TestCase):
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

       card = Card(
           user_id=user.id,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()

       self.result_message = nearby_card_message(100.7,100.8,'line_user_id')
       self.expected_message = {
                  "type": "flex",
                  "altText": "新增名片",
                  "contents": {
                    "body": {
                      "contents": [
                        {
                          "size": "lg",
                          "text": "沒有名片",
                          "type": "text",
                          "weight": "bold",
                          "wrap": True,
                          "color": "#1DB446"
                        },
                        {
                          "margin": "md",
                          "size": "md",
                          "text": "抱歉，我找不到你想要找的名片",
                          "type": "text",
                          "wrap": True
                        }
                      ],
                      "layout": "vertical",
                      "type": "box"
                    },
                    "type": "bubble"
                  }
                }

   def tearDown(self):
       db.session.remove()  # Remove database session
       db.drop_all()  # Drop database
       self.app_context.pop()

   def test_nearby_no_card_message(self):
       # test bearby for one card
       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )


class NearByCardMessageTestCase2(unittest.TestCase):
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

       card = Card(
           user_id=user.id,
           name='test',
           nickname='87',
           line_id='',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='https://i.imgur.com/Hn6lBtg.jpg',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()
       self.result_message = nearby_card_message(38.7,78.8,'line_user_id')
       self.expected_message = {
                  "type": "flex",
                  "altText": "搜尋名片清單",
                  "contents": {
                    "type": "carousel",
                    "contents": [
                      {
                        "body": {
                          "contents": [
                            {
                              "color": "#1DB446",
                              "size": "md",
                              "text": "test公司",
                              "type": "text",
                              "weight": "bold",
                              "wrap": True
                            },
                            {
                              "color": "#666666",
                              "margin": "md",
                              "size": "sm",
                              "text": "test內容",
                              "type": "text",
                              "wrap": True
                            },
                            {
                              "contents": [
                                {
                                  "color": "#666666",
                                  "flex": 2,
                                  "size": "md",
                                  "text": "姓名",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test 87",
                                  "type": "text",
                                  "wrap": True
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
                                  "text": "職稱",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test",
                                  "type": "text",
                                  "wrap": True
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
                                  "text": "地址",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test",
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
                                "label": "電話",
                                "type": "uri",
                                "uri": "tel:0987654321"
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
                          "action": {
                            "type": "uri",
                            "uri": "?card_id=1"
                          },
                          "aspectMode": "cover",
                          "aspectRatio": "20:13",
                          "size": "full",
                          "type": "image",
                          "url": "https://i.imgur.com/Hn6lBtg.jpgstatic/img/card/cosplay/default.png"
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

   def test_nearby_card_message2(self):
       # test bearby for one card
       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )

class SearchCardMessageTestCase(unittest.TestCase):
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

       card = Card(
           user_id=user.id,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()
       self.result_message = search_card_message('test','line_user_id')
       self.expected_message =  {
                  "type": "flex",
                  "altText": "搜尋名片清單",
                  "contents": {
                    "type": "carousel",
                    "contents": [
                      {
                        "body": {
                          "contents": [
                            {
                              "color": "#1DB446",
                              "size": "md",
                              "text": "test公司",
                              "type": "text",
                              "weight": "bold",
                              "wrap": True
                            },
                            {
                              "color": "#666666",
                              "margin": "md",
                              "size": "sm",
                              "text": "test內容",
                              "type": "text",
                              "wrap": True
                            },
                            {
                              "contents": [
                                {
                                  "color": "#666666",
                                  "flex": 2,
                                  "size": "md",
                                  "text": "姓名",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test 87",
                                  "type": "text",
                                  "wrap": True
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
                                  "text": "職稱",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test",
                                  "type": "text",
                                  "wrap": True
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
                                  "text": "地址",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test",
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
                                "label": "電話",
                                "type": "uri",
                                "uri": "tel:0987654321"
                              },
                              "height": "sm",
                              "style": "link",
                              "type": "button"
                            },
                            {
                              "action": {
                                "label": "e-mail",
                                "type": "uri",
                                "uri": "mailto:8740@gmail.com"
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
                          "url": "https://i.imgur.com/Hn6lBtg.jpgstatic/img/card/cosplay/default.png"
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

   def test_search_card_message(self):
       # test search for one card
       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )


class SearchNoCardMessageTestCase(unittest.TestCase):
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

       card = Card(
           user_id = None,
           name='test',
           nickname ='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()
       self.result_message = search_card_message(None,'line_user_id')
       self.expected_message =  {
                  "type": "flex",
                  "altText": "新增名片",
                  "contents": {
                    "type": "bubble",
                    "body": {
                      "contents": [
                        {
                          "color": "#1DB446",
                          "size": "lg",
                          "text": "沒有名片",
                          "type": "text",
                          "weight": "bold",
                          "wrap": True
                        },
                        {
                          "margin": "md",
                          "size": "md",
                          "text": "抱歉，我找不到你想要找的名片",
                          "type": "text",
                          "wrap": True
                        }
                      ],
                      "layout": "vertical",
                      "type": "box"
                    }
                  }
                }
   def tearDown(self):
       db.session.remove()  # Remove database session
       db.drop_all()  # Drop database
       self.app_context.pop()

   def test_search_no_card_message(self):
       # test search for one card
       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )


class SearchCardMessageForNoLinkTestCase(unittest.TestCase):
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

       card = Card(
           user_id = None,
           name='test',
           nickname ='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='https://tw.yahoo.com/',
           image_path='https://i.imgur.com/Hn6lBtg.jpg',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()
       self.result_message = search_card_message('test','line_user_id')
       self.expected_message =  {
                  "type": "flex",
                  "altText": "搜尋名片清單",
                  "contents": {
                    "type": "carousel",
                    "contents": [
                      {
                        "body": {
                          "contents": [
                            {
                              "color": "#1DB446",
                              "size": "md",
                              "text": "test公司",
                              "type": "text",
                              "weight": "bold",
                              "wrap": True
                            },
                            {
                              "color": "#666666",
                              "margin": "md",
                              "size": "sm",
                              "text": "test內容",
                              "type": "text",
                              "wrap": True
                            },
                            {
                              "contents": [
                                {
                                  "color": "#666666",
                                  "flex": 2,
                                  "size": "md",
                                  "text": "姓名",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test 87",
                                  "type": "text",
                                  "wrap": True
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
                                  "text": "職稱",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test",
                                  "type": "text",
                                  "wrap": True
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
                                  "text": "地址",
                                  "type": "text"
                                },
                                {
                                  "color": "#333333",
                                  "flex": 5,
                                  "size": "md",
                                  "text": "test",
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
                                "label": "電話",
                                "type": "uri",
                                "uri": "tel:0987654321"
                              },
                              "height": "sm",
                              "style": "link",
                              "type": "button"
                            },
                            {
                              "action": {
                                "label": "相關連結",
                                "type": "uri",
                                "uri": "https://tw.yahoo.com/"
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
                          "action": {
                            "type": "uri",
                            "uri": "?card_id=1"
                          },
                          "aspectMode": "cover",
                          "aspectRatio": "5:4",
                          "size": "full",
                          "type": "image",
                          "url": "https://i.imgur.com/Hn6lBtg.jpgstatic/img/card/cosplay/default.png"
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

   def test_search_card_foe_none_line_message(self):
       # test search for one card
       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )

class ShowMyCardMessageTestCase(unittest.TestCase):
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

       card = Card(
           user_id=user.id,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()
       self.result_message = show_my_card_message('line_user_id')
       self.expected_message =  [
                  {
                    "text": "這是 test 的名片",
                    "type": "text"
                  },
                  {
                    "altText": "我的名片",
                    "contents": {
                      "body": {
                        "contents": [
                          {
                            "color": "#1DB446",
                            "size": "md",
                            "text": "test公司",
                            "type": "text",
                            "weight": "bold",
                            "wrap": True
                          },
                          {
                            "color": "#666666",
                            "margin": "md",
                            "size": "sm",
                            "text": "test內容",
                            "type": "text",
                            "wrap": True
                          },
                          {
                            "contents": [
                              {
                                "color": "#666666",
                                "flex": 2,
                                "size": "md",
                                "text": "姓名",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test 87",
                                "type": "text",
                                "wrap": True
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
                                "text": "職稱",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test",
                                "type": "text",
                                "wrap": True
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
                                "text": "地址",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test",
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
                              "label": "電話",
                              "type": "uri",
                              "uri": "tel:0987654321"
                            },
                            "height": "sm",
                            "style": "link",
                            "type": "button"
                          },
                          {
                            "action": {
                              "label": "e-mail",
                              "type": "uri",
                              "uri": "mailto:8740@gmail.com"
                            },
                            "height": "sm",
                            "style": "link",
                            "type": "button"
                          },
                          {
                            "action": {
                              "label": "導航至公司",
                              "type": "uri",
                              "uri": "https://www.google.com/maps/search/?api=1&query=38.777,78.888"
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
                        "url": "https://i.imgur.com/Hn6lBtg.jpgstatic/img/card/cosplay/default.png"
                      },
                      "type": "bubble"
                    },
                    "type": "flex"
                  }
                ]

   def tearDown(self):
       db.session.remove()  # Remove database session
       db.drop_all()  # Drop database
       self.app_context.pop()

   def test_show_my_card_message(self):

       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )

class ShowMyCardMessageForNoCardTestCase(unittest.TestCase):
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

       card = Card(
           user_id=None,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )
       db.session.add_all([card])
       db.session.commit()
       self.result_message = show_my_card_message('line_user_id')
       self.expected_message =[
                  {
                    "type": "flex",
                    "altText": "找不到名片",
                    "contents": {
                      "body": {
                        "contents": [
                          {
                            "color": "#1DB446",
                            "size": "md",
                            "text": "找不到名片",
                            "type": "text",
                            "weight": "bold"
                          },
                          {
                            "color": "#666666",
                            "margin": "md",
                            "size": "sm",
                            "text": "請先跟咪卡新增一張名片，下次你就可以在群組秀名片囉！",
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
                ]

   def tearDown(self):
       db.session.remove()  # Remove database session
       db.drop_all()  # Drop database
       self.app_context.pop()

   def test_show_my_card_for_no_card_message(self):

       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )

class ShowMyCardMessageForNoUserTestCase(unittest.TestCase):
   def setUp(self):
       self.app = create_app('testing')
       self.app_context = self.app.app_context()
       self.app_context.push()
       db.create_all()

     # Create fake User data
       user = User(
           line_user_id='line_user_id',
           deleted_at= datetime.datetime.now()
       )


       db.session.add_all([user])
       db.session.commit()

       card = Card(
           user_id=None,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='8740@gmail.com',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='',
           image_path='',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )
       db.session.add_all([card])
       db.session.commit()
       self.result_message = show_my_card_message('line_user_id')
       self.expected_message = [
                  {
                    "type": "flex",
                    "altText": "找不到名片",
                    "contents": {
                      "body": {
                        "contents": [
                          {
                            "color": "#1DB446",
                            "size": "md",
                            "text": "找不到名片",
                            "type": "text",
                            "weight": "bold"
                          },
                          {
                            "color": "#666666",
                            "margin": "md",
                            "size": "sm",
                            "text": "請先跟咪卡我成為好友並且新增名片，下次你也可以在群組秀名片囉！",
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
                ]

   def tearDown(self):
       db.session.remove()  # Remove database session
       db.drop_all()  # Drop database
       self.app_context.pop()

   def test_show_my_card_for_no_user_message(self):

       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )

class ShowMyCardMessageTestCase2(unittest.TestCase):
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

       card = Card(
           user_id=user.id,
           name='test',
           nickname='87',
           line_id='line_user_id',
           title='test',
           title_en='test',
           company_name='test公司',
           department='test',
           industry='test產業',
           summary='test內容',
           email='',
           fax_number='02-345678',
           tax_number='02-87654321',
           phone_number='0987654321',
           tel_number='02-78407840',
           address='test',
           address_en='test',
           lat='38.777',
           lng='78.888',
           rel_link='https://tw.yahoo.com/',
           image_path='https://i.imgur.com/Hn6lBtg.jpg',
           anime_path='img/card/anime/default.gif',
           cosplay_path='img/card/cosplay/default.png',
           public=True,
           description='test',
           view_count='0',
           deleted_at=None
       )

       db.session.add_all([card])
       db.session.commit()
       self.result_message = show_my_card_message('line_user_id')
       self.expected_message = [
                  {
                    "text": "這是 test 的名片",
                    "type": "text"
                  },
                  {
                    "altText": "我的名片",
                    "contents": {
                      "body": {
                        "contents": [
                          {
                            "color": "#1DB446",
                            "size": "md",
                            "text": "test公司",
                            "type": "text",
                            "weight": "bold",
                            "wrap": True
                          },
                          {
                            "color": "#666666",
                            "margin": "md",
                            "size": "sm",
                            "text": "test內容",
                            "type": "text",
                            "wrap": True
                          },
                          {
                            "contents": [
                              {
                                "color": "#666666",
                                "flex": 2,
                                "size": "md",
                                "text": "姓名",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test 87",
                                "type": "text",
                                "wrap": True
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
                                "text": "職稱",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test",
                                "type": "text",
                                "wrap": True
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
                                "text": "地址",
                                "type": "text"
                              },
                              {
                                "color": "#333333",
                                "flex": 5,
                                "size": "md",
                                "text": "test",
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
                              "label": "電話",
                              "type": "uri",
                              "uri": "tel:0987654321"
                            },
                            "height": "sm",
                            "style": "link",
                            "type": "button"
                          },
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
                              "label": "導航至公司",
                              "type": "uri",
                              "uri": "https://www.google.com/maps/search/?api=1&query=38.777,78.888"
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
                        "action": {
                          "type": "uri",
                          "uri": "?card_id=1"
                        },
                        "aspectMode": "cover",
                        "aspectRatio": "5:4",
                        "size": "full",
                        "type": "image",
                        "url": "https://i.imgur.com/Hn6lBtg.jpgstatic/img/card/cosplay/default.png"
                      },
                      "type": "bubble"
                    },
                    "type": "flex"
                  }
                ]

   def tearDown(self):
       db.session.remove()  # Remove database session
       db.drop_all()  # Drop database
       self.app_context.pop()

   def test_show_my_card_message2(self):

       self.assertEqual(
           json.loads(str(self.result_message)),
           self.expected_message
       )