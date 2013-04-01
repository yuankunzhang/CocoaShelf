# -*- coding: utf-8 -*-
from time import time
from datetime import datetime, timedelta

from flask.ext.sqlalchemy import BaseQuery
from flask.ext.babel import gettext as _

from cocoa.extensions import db
from cocoa.helpers.sql import JSONEncodedDict

from .consts import Weekdays

class UserVitalityQuery(BaseQuery):

    def active_users(self, num=10):
        from ..account.models import User

        return User.query.outerjoin(UserVitality).\
               filter(UserVitality.total>0).\
               order_by(UserVitality.timestamp.desc()).\
               order_by(UserVitality.total.desc()).\
               limit(num).all()


class UserVitality(db.Model):
    """用户活跃度"""

    __tablename__ = 'user_vitality'

    query_class = UserVitalityQuery

    today = datetime.today()
    deadline = today - timedelta(days=7)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        primary_key=True)
    sun = db.Column(JSONEncodedDict(100))
    mon = db.Column(JSONEncodedDict(100))
    tue = db.Column(JSONEncodedDict(100))
    wed = db.Column(JSONEncodedDict(100))
    thu = db.Column(JSONEncodedDict(100))
    fri = db.Column(JSONEncodedDict(100))
    sat = db.Column(JSONEncodedDict(100))
    total = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.Integer)

    user = db.relationship('User',
        backref=db.backref('vitality', cascade='all, delete-orphan',
                            uselist=False))

    def __init__(self, user=None):
        self.user = user

    def update(self, amount):
        column = Weekdays.from_int(self.today.weekday()).name
        vitality = getattr(self, column)

        if vitality is None:
            vitality = [0] * 2
        else:
            last_date = datetime.fromtimestamp(vitality[0])
            if last_date < self.deadline:
                self.total -= vitality[1]
                vitality[1] = 0

        vitality = [int(time()), vitality[1] + amount]
        self.__setattr__(column, vitality)
        self.total += amount
        db.session.commit()
