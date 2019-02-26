from datetime import datetime

from flask import Flask
from linebot import LineBotApi
from sqlalchemy.orm import backref

import config

from . import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    line_user_id = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

    cards = db.relationship("Card", lazy='dynamic')
    issues = db.relationship("Issue", lazy='dynamic')
    activity_logs = db.relationship("GroupActivityLog", lazy='dynamic')
    send_picture_logs = db.relationship("SendPictureLog", lazy='dynamic')
    orders = db.relationship("Order", lazy='dynamic')
    def __repr__(self):
        return '<User %r>' % self.id

class PicLog(db.Model):
    __tablename__ = 'pic_logs'
    id = db.Column(db.Integer, primary_key = True)
    result = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key = True)
    group_id = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

    group_activity = db.relationship("GroupActivity", lazy='dynamic')
    def __repr__(self):
        return '<Group %r>' % self.id

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key = True)
    line_user_id = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Admin %r>' % self.id

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64))
    nickname =  db.Column(db.String(64))
    line_id = db.Column(db.String(64))
    title = db.Column(db.String(64))
    title_en = db.Column(db.String(64))
    company_name = db.Column(db.String(64))
    department = db.Column(db.String(64))
    industry = db.Column(db.String(64))
    summary = db.Column(db.String(64))
    email = db.Column(db.String(64))
    fax_number = db.Column(db.String(64))
    tax_number = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    tel_number = db.Column(db.String(64))
    address = db.Column(db.String(64))
    address_en = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    rel_link = db.Column(db.String(64))
    image_path = db.Column(db.String(64))
    anime_path = db.Column(db.String(64), default="img/card/anime/default.gif")
    cosplay_path = db.Column(db.String(64), default="img/card/cosplay/default.png")
    public = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(128))
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

    issues = db.relationship("Issue", lazy='dynamic')

    def __repr__(self):
        return '<Card %r>' % self.id

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    content = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Issues %r>' % self.id

class GroupActivityLog(db.Model):
    __tablename__ = 'group_activity_logs'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    group_activity_id = db.Column(db.Integer, db.ForeignKey('group_activitys.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<GroupActivityLog %r>' % self.id

class Activity(db.Model):
    __tablename__ = 'activitys'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(64))
    description = db.Column(db.String(64))
    organizer = db.Column(db.String(64))
    address = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    rel_link = db.Column(db.String(64))
    session_limit = db.Column(db.Integer)
    session_count = db.Column(db.Integer)
    group_link = db.Column(db.String(64))
    public = db.Column(db.Boolean, default=True)
    start_at = db.Column(db.DateTime, default=datetime.now)
    end_at = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)
    def __repr__(self):
        return '<Activity %r>' % self.id

class GroupActivity(db.Model):
    __tablename__ = 'group_activitys'
    id = db.Column(db.Integer, primary_key = True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    title = db.Column(db.String(64))
    description = db.Column(db.String(64))
    organizer = db.Column(db.String(64))
    address = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    rel_link = db.Column(db.String(64))
    session_limit = db.Column(db.Integer)
    session_count = db.Column(db.Integer)
    group_link = db.Column(db.String(64))
    public = db.Column(db.Boolean, default=True)
    start_at = db.Column(db.DateTime, default=datetime.now)
    end_at = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

    activity_logs = db.relationship("GroupActivityLog", lazy='dynamic')

    def __repr__(self):
        return '<Activity %r>' % self.id

class SendPictureLog(db.Model):
    __tablename__ = 'send_picture_logs'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<SendPictureLog %r>' % self.id

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    product_type = db.Column(db.String(64))
    description = db.Column(db.String(64))
    product_code = db.Column(db.String(64))
    price= db.Column(db.Integer)
    recommend = db.Column(db.Boolean, default=False)
    author = db.Column(db.String(64))
    image_path = db.Column(db.String(64))
    demo_image_path = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime)

    orders = db.relationship("Order", lazy='dynamic')
    order = db.relationship("Order", backref="product")

    def __repr__(self):
        return '<Product %r>' % self.id

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    order_number = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    currency = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    canceled_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    

    def __repr__(self):
        return '<Order %r>' % self.id
