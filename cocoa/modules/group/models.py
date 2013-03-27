# -*- coding: utf-8 -*-
from time import time

from sqlalchemy.ext.associationproxy import association_proxy

from flask import current_app
from flask.ext.login import current_user
from flask.ext.babel import gettext as _

from cocoa.extensions import db

class GroupTopicReplies(db.Model):

    __tablename__ = 'm_group_topic_replies'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('m_group_topics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.Integer, default=int(time()))

    topic = db.relationship('GroupTopics',
        backref=db.backref('replies', cascade='all, delete-orphan'))
    user = db.relationship('User')

    def __init__(self, content, user, topic=None):
        self.content = content
        self.user = user
        self.topic = topic


class GroupTopics(db.Model):

    __tablename__ = 'm_group_topics'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255))
    timestamp = db.Column(db.Integer, default=int(time()))

    group = db.relationship('Group',
        backref=db.backref('topics', cascade='all, delete-orphan'))
    user = db.relationship('User')

    def __init__(self, title, user, group=None):
        self.title = title
        self.user = user
        self.group = group

    def reply(self, content):
        rep = GroupTopicReplies(content, current_user)
        self.replies.append(rep)
        db.session.commit()


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
    name = db.Column(db.String(255), unique=True)
    intro = db.Column(db.Text)
    totem = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.Integer, default=int(time()))

    owner = db.relationship('User', backref='groups')
    users = association_proxy('group_users', 'user')

    def __init__(self, name, intro, owner=None):
        self.name = name
        self.intro = intro
        self.owner = owner

    def save(self):
        group = Group.query.filter_by(name=self.name).first()
        if group is not None:
            raise ValueError(_(u'This group name has been used.'))
        self.users.append(self.owner)
        db.session.add(self)
        db.session.commit()

    def applied(self, applier, intro):
        """申请加入"""

        if applier in self.users:
            raise ValueError(_(u'You\'ve already in this group'))
        else:
            appler = GroupAppliers(applier, intro, self)
            appler.save()

    def new_topic(self, title):
        topic = GroupTopics(title, current_user)
        self.topics.append(topic)
        db.session.commit()

    def get_totem_path(self):
        if self.totem:
            return current_app.config['TOTEM_STATIC_PATH'] + self.totem
        else:
            return None


class GroupAppliers(db.Model):
    """成员申请加入小组的临时表"""

    __tablename__ = 'group_appliers'

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'),
        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        primary_key=True)
    intro = db.Column(db.String(255))    # 申请理由
    timestamp = db.Column(db.Integer, default=int(time()))

    group = db.relationship('Group',
        backref=db.backref('appliers', cascade='all, delete-orphan'))
    applier = db.relationship('User',
        backref=db.backref('applied_groups',
                            cascade='all, delete-orphan'))

    def __init__(self, applier, intro, group=None):
        self.applier = applier
        self.intro = intro
        self.group = group

    def save(self):
        applier = GroupAppliers.query.filter_by(group=self.group).\
                    filter_by(applier=self.applier).first()
        if applier is not None:
            raise ValueError(_(u'You\'ve already applied to join.'))
        else:
            db.session.add(self)
            db.session.commit()
