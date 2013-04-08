# -*- coding: utf-8 -*-
from time import time

from flask.ext.babel import gettext as _

from cocoa.extensions import db

class Follower(db.Model):

    __tablename__ = 'follower'

    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        primary_key=True)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    from_user = db.relationship('User', foreign_keys=[from_user_id],
        primaryjoin='Follower.from_user_id==User.id',
        backref=db.backref('u_followings', cascade='all, delete-orphan'))
    to_user = db.relationship('User', foreign_keys=[to_user_id],
        primaryjoin='Follower.to_user_id==User.id',
        backref=db.backref('u_followers', cascade='all, delete-orphan'))
    
    def __init__(self, to_user, from_user=None):
        self.to_user = to_user
        self.from_user = from_user

    def save(self):
        f = Follower.query.filter_by(from_user=self.from_user,
                to_user=self.to_user).first()
        if f is not None:
            raise ValueError(_(u'You\'ve already followed this user.'))
        else:
            db.session.add(self)
            db.session.commit()
