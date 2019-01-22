from datetime import datetime

from flask import Flask
from linebot import LineBotApi

import config

from . import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    line_user_id = db.Column(db.String(64), unique=True)
    aws_user_name = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    members = db.relationship("Member", back_populates="user", lazy='noload')

    def __repr__(self):
        return '<User %r>' % self.line_user_id

    def link_rm_to_guest(self):
        '''
        Link rich menu to guest
        '''
        try:
            line_bot_api.link_rich_menu_to_user(self.line_user_id, app.config['GUEST_RICH_MENU_ID'])
        except:
            pass

    def link_rm_to_user(self):
        '''
        Link rich menu to user
        '''
        try:
            line_bot_api.link_rich_menu_to_user(self.line_user_id, app.config['USER_RICH_MENU_ID'])
        except:
            pass

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key = True)
    source_id = db.Column(db.String(64))
    source_type = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    arn = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="members", lazy='noload')

    def __repr__(self):
        return '<Member %r>' % self.source_id
