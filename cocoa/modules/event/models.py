# -*- coding: utf-8 -*-
import json
from time import time

from cocoa.extensions import db
from cocoa.helpers.sql import JSONEncodedDict
from .consts import EventType

class EventRecord(db.Model):

    __tablename__ = 'event_record'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.SmallInteger)
    who = db.Column(db.Integer, db.ForeignKey('user.id'))
    what = db.Column(JSONEncodedDict(255))
    timestamp = db.Column(db.Integer, default=int(time()))

    def __init__(self, type, event):
        self.type = type
        self.who = event.who
        self.what = event.__dict__

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_event(self):
        return Event.get(self.type, self.what, self.timestamp)

    @staticmethod
    def get_records(type, num=10):
        return EventRecord.query.filter_by(type=type).\
               order_by(EventRecord.timestamp.desc()).\
               limit(10).all()


class Event(object):

    @staticmethod
    def get(type, attrs, timestamp):
        if type == EventType.SIGN_UP.value:
            return SignUpEvent(attrs['user_id'], timestamp)
        elif type == EventType.ADD_BOOK_TO_SHELF.value:
            return AddBookToShelfEvent(
                attrs['user_id'],
                attrs['column_name'],
                attrs['book_id'],
                timestamp)

    def save(self):
        type = self.__type__.value
        EventRecord(type, self).save()


class SignUpEvent(Event):

    __type__ = EventType.SIGN_UP

    def __init__(self, user_id, timestamp=None):
        self.user_id = user_id
        self.who = user_id
        self.timestamp=timestamp


class AddBookToShelfEvent(Event):

    __type__ = EventType.ADD_BOOK_TO_SHELF

    def __init__(self, user_id, column_name, book_id, timestamp=None):
        self.user_id = user_id
        self.who = user_id
        self.column_name = column_name
        self.book_id = book_id
        self.timestamp=timestamp
