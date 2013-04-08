# -*- coding: utf-8 -*-
from time import time
from datetime import datetime

from flask.ext.login import current_user

from cocoa.extensions import db
from cocoa.helpers.html import safe_html

class Mail(db.Model):

    __tablename__ = 'mail'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('mail.id'))
    timestamp = db.Column(db.Integer, default=int(time()))

    from_user = db.relationship('User', foreign_keys=[from_user_id],
        primaryjoin='Mail.from_user_id==User.id',
        backref=db.backref('sent_mails', cascade='all, delete-orphan'))
    to_user = db.relationship('User', foreign_keys=[to_user_id],
        primaryjoin='Mail.to_user_id==User.id',
        backref=db.backref('received_mails', cascade='all, delete-orphan'))
    child_mail = db.relationship('Mail',
        backref=db.backref('parent_mail', remote_side=id))

    def __init__(self, to_user, parent_id, title,
                 content, from_user=None):
        self.to_user = to_user
        self.title = title
        self.content = safe_html(content, safe_tags=[])
        self.parent_id = parent_id
        self.from_user = from_user

    @staticmethod
    def send(from_user, to_user, parent_id, title, content):
        mail = Mail(to_user, parent_id, title, content, from_user)
        db.session.add(mail)
        db.session.commit()

        to_user.inbox.append(MailInbox(from_user, mail))
        db.session.commit()
               

class MailInbox(db.Model):

    __tablename__ = 'mail_inbox'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mail_id = db.Column(db.Integer, db.ForeignKey('mail.id'))
    unread = db.Column(db.Boolean, default=True)

    user = db.relationship('User', foreign_keys=[user_id],
        primaryjoin='MailInbox.user_id==User.id',
        backref=db.backref('inbox', cascade='all, delete-orphan'))
    from_user = db.relationship('User', foreign_keys=[from_user_id],
        primaryjoin='MailInbox.from_user_id==User.id')
    mail = db.relationship('Mail',
        backref=db.backref('mail_thumb', uselist=False))

    def __init__(self, from_user, mail, user=None):
        self.from_user = from_user
        self.mail = mail
        self.user = user

    def read(self):
        self.unread = False
        db.session.commit()
