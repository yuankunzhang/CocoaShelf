# -*- coding: utf-8 -*-
import json
from time import time

from cocoa.extensions import db
from .consts import Event_type

class EventRecord(db.Model):

    __tablename__ = 'event_record'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.SmallInteger)
    what = db.Column(db.Text)
    timestamp = db.Column(db.Integer, default=int(time()))

    def __init__(self, type, event, timestamp=None):
        self.type = type
        self.what = event.to_json()
        self.timestamp = timestamp

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_event(self):
        return Event.from_json(self.type, self.what)


class Event(object):

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def from_json(type, json_str):
        return json.loads(json_str, object_hook=_object_decoder(type))


def  _object_decoder(type):

    def _decoder(obj):
        if type == Event_type.NEW_SHELF.value():
            return NewShelfEvent(obj['shelf_id'])
        elif type == Event_type.ADD_BOOK_TO_SHELF.value():
            return AddBookToShelfEvent(
                obj['shelf_id'],
                obj['shelf_type'],
                obj['book_id']
            )

    return _decoder


class NewShelfEvent(Event):

    def __init__(self, shelf_id):
        self.shelf_id = shelf_id


class AddBookToShelfEvent(Event):

    def __init__(self, shelf_id, shelf_type, book_id):
        self.shelf_id = shelf_id
        self.shelf_type = shelf_type
        self.book_id = book_id
