# -*- coding: utf-8 -*-
from time import time
from datetime import datetime

from flask.ext.login import current_user

from cocoa.extensions import db
from cocoa.helpers.sql import JSONEncodedDict
from cocoa.helpers.html import safe_html

class Mail(db.Model):

    __tablename__ = 'mail'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_users = db.Column(JSONEncodedDict(255))
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    timestamp = db.Column(db.Integer, default=int(time()))

    from_user = db.relationship('User',
        backref=db.backref('sent_mails', cascade='all, delete-orphan'))

    def __init__(self, to_users, title, content, from_user=None):
        self.to_users = to_users
        self.title = title
        self.content = safe_html(content, safe_tags=[])
        self.from_user = from_user

    @staticmethod
    def send(from_user, to_users, title, content):
        mail = Mail(to_users, title, content, from_user)
        db.session.add(mail)
        db.session.commit()

        for to_user in to_users:
            user = User.query.get(to_user)
            user.inbox.append(MailInbox(from_user, mail))
        db.session.commit()

    def get_datetime(self, format):
        return datetime.fromtimestamp(int(self.timestamp)).\
               strftime(format)
               

class MailInbox(db.Model):

    __tablename__ = 'mail_inbox'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mail_id = db.Column(db.Integer, db.ForeignKey('mail.id'))

    user = db.relationship('User', foreign_keys=[user_id],
        backref=db.backref('inbox', cascade='all, delete-orphan'))
    from_user = db.relationship('User', foreign_keys=[from_user_id])
    mail = db.relationship('Mail')

    def __init__(self, from_user, mail, user=None):
        self.from_user = from_user
        self.mail = mail
        self.user = user
