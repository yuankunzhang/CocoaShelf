# -*- coding: utf-8 -*-
from time import time

from cocoa.extensions import db

class ShelfComments(db.Model):
    """书架留言"""

    __tablename__ = 'm_shelf_comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref('comments', cascade='all, delete-orphan'))
    user = db.relationship('User',
        backref=db.backref('comments', cascade='all, delete-orphan'))

    def __init__(self, content, user, shelf=None):
        self.content = content
        self.user = user
        self.shelf = shelf

    def save(self):
        db.session.add(self)
        db.session.commit()
