# -*- coding: utf-8 -*-
from time import time

from werkzeug import cached_property

from sqlalchemy import func
from sqlalchemy.ext.associationproxy import association_proxy

from flask import current_app, abort, url_for
from flask.ext.sqlalchemy import BaseQuery
from flask.ext.login import current_user
from flask.ext.babel import gettext as _
from flask.ext.principal import Permission, UserNeed

from cocoa.extensions import db
from ..permissions import Permissions
from .consts import ApplicantStatus

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


class GroupQuery(BaseQuery):

    def user_joined(self, user_id):
        """给定的用户在哪些小组中"""

        return Group.query.outerjoin(GroupUsers).\
                filter(GroupUsers.user_id==user_id).\
                filter(Group.user_id!=user_id).all()

    def active_groups(self, num=10):
        return Group.query.outerjoin(GroupUsers).\
               order_by(func.count(GroupUsers.user_id).desc()).\
               group_by(Group.id).all()


class Group(db.Model):

    __tablename__ = 'group'

    query_class = GroupQuery

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255), unique=True)
    intro = db.Column(db.Text)
    totem = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.Integer, default=int(time()))

    owner = db.relationship('User', backref='groups')
    users = association_proxy('group_users', 'user')
    appliers = association_proxy('applicants', 'applier')

    def __init__(self, name, intro, owner=None):
        self.name = name
        self.intro = intro
        self.owner = owner

    def __repr__(self):
        return '<Group %r>' % self.name

    class _Permissions(Permissions):

        def default(self):
            return Permission(UserNeed(self.owner.id))

        def add_user(self):
            return self.default()

    def permissions(self):
        return self._Permissions(self)

    @cached_property
    def url(self):
        return url_for('group.item', group_id=self.id)

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
        elif applier in self.appliers:
            raise ValueError(_(u'You\'ve post your applicant'))
        else:
            appler = GroupApplicant(applier, intro, self)
            appler.save()

    def untreated_applicants(self):
        return GroupApplicant.query.filter_by(
            status=ApplicantStatus.UNTREATED.value).all()

    def add_user(self, user):
        if self.permissions().add_user().can():
            if user in self.users:
                raise ValueError(_(u'This user is group member'))
            else:
                self.users.append(user)
                db.session.commit()

    def new_topic(self, title):
        topic = GroupTopics(title, current_user)
        self.topics.append(topic)
        db.session.commit()

    @cached_property
    def totem_path(self):
        if self.totem:
            return current_app.config['TOTEM_STATIC_PATH'] + self.totem
        else:
            return ''

    def get_totem_path(self):
        if self.totem:
            return current_app.config['TOTEM_STATIC_PATH'] + self.totem
        else:
            return ''


class GroupApplicant(db.Model):
    """成员申请加入小组的临时表"""

    __tablename__ = 'group_applicants'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    intro = db.Column(db.String(255))    # 申请理由
    status = db.Column(db.SmallInteger,
        default=ApplicantStatus.UNTREATED.value)
    timestamp = db.Column(db.Integer, default=int(time()))

    group = db.relationship('Group',
        backref=db.backref('applicants', cascade='all, delete-orphan'))
    applier = db.relationship('User',
        backref=db.backref('applied_groups',
                            cascade='all, delete-orphan'))

    def __init__(self, applier, intro, group=None):
        self.applier = applier
        self.intro = intro
        self.group = group

    def save(self):
        applier = GroupApplicant.query.filter_by(group=self.group).\
                    filter_by(applier=self.applier).first()
        if applier is not None:
            raise ValueError(_(u'You\'ve already applied to join.'))
        else:
            db.session.add(self)
            db.session.commit()

    def accepted(self):
        if self.group.permissions().add_user().can():
            self.group.add_user(self.applier)
            self.status = ApplicantStatus.ACCEPTED.value
            db.session.commit()
        else:
            abort(403)

    def declined(self):
        if self.group.permissions().add_user().can():
            self.status = ApplicantStatus.DECLINED.value
            db.session.commit()
        else:
            abort(403)
