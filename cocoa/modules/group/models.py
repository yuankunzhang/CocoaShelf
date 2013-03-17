# -*- coding: utf-8 -*-
from time import time

from sqlalchemy.ext.associationproxy import association_proxy

from cocoa.extensions import db

class GroupUsers(db.Model):

    __tablename__ = 'm_group_users'

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'),
        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    group = db.relationship('Group',
        backref=db.backref('group_users', cascade='all, delete-orphan'))
    user = db.relationship('User')

    def __init__(self, user, group=None):
        self.user = user
        self.group = group


class Group(db.Model):

    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255))
    intro = db.Column(db.Text)
    active = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.Integer, default=int(time()))

    owner = db.relationship('User', backref='groups')
    users = association_proxy('group_users', 'user')

    def __init__(self, name, intro, owner=None):
        self.name = name
        self.intro = intro
        self.owner = owner
