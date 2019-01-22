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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    cards = db.relationship("Card", back_populates="user", lazy='noload')
    issues = db.relationship("Issue", back_populates="user", lazy='noload')

    def __repr__(self):
        return '<User %r>' % self.line_user_id

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64))
    nickname =  db.Column(db.String(64))
    line_id = db.Column(db.String(64))
    title = db.Column(db.String(64))
    title_en = db.Column(db.String(64))
    department = db.Column(db.String(64))
    industry = db.Column(db.String(64))
    summary = db.Column(db.String(64))
    email = db.Column(db.String(64))
    fax_number = db.Column(db.String(64))
    tax_number = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    tel_number = db.Column(db.String(64))
    address = db.Column(db.String(64))
    address_cn = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    rel_link = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="cards", lazy='noload')
    issue = db.relationship("Issue", back_populates="cards", lazy='noload')
    def __repr__(self):
        return '<Card %r>' % self.id

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    content = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="Issues", lazy='noload')
    card = db.relationship("Card", back_populates="Issues", lazy='noload')
    def __repr__(self):
        return '<Issues %r>' % self.source_id

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activitys.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="activity_logs", lazy='noload')
    activity = db.relationship("Activity", back_populates="activity_logs", lazy='noload')
    def __repr__(self):
        return '<ActivityLog %r>' % self.source_id

class Activity(db.Model):
    __tablename__ = 'activitys'
    id = db.Column(db.Integer, primary_key = True)
    source_type = db.Column(db.String(64))
    source_id = db.Column(db.String(64))
    title = db.Column(db.String(64))
    description = db.Column(db.String(64))
    activity_time = db.Column(db.DateTime)
    organizer = db.Column(db.String(64))
    address = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    rel_link = db.Column(db.String(64))
    session_limit = db.Column(db.Integer)
    session_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    activity_logs = db.relationship("ActivityLog", back_populates="activitys", lazy='noload')

    def __repr__(self):
        return '<Activity %r>' % self.source_id