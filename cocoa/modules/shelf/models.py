# -*- coding: utf-8 -*-
from datetime import datetime
from time import time

from sqlalchemy.ext.associationproxy import association_proxy

from cocoa.extensions import db
from cocoa.helpers.common import timesince
from .consts import ColumnType

class IHave(db.Model):
    """我有"""

    __tablename__ = 'i_have'

    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class IRead(db.Model):
    """读过"""

    __tablename__ = 'i_read'

    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class IReading(db.Model):
    """在读"""

    __tablename__ = 'i_reading'

    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))
    finish_timestamp = db.Column(db.Integer)

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class IWish(db.Model):
    """想读"""

    __tablename__ = 'i_wish'

    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class ILike(db.Model):
    """喜欢"""

    __tablename__ = 'i_like'

    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class Shelf(db.Model):

    __tablename__ = 'shelf'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    have_books = association_proxy('i_have', 'book')
    read_books = association_proxy('i_read', 'book')
    reading_books = association_proxy('i_reading', 'book')
    wish_books = association_proxy('i_wish', 'book')
    like_books = association_proxy('i_like', 'book')

    user = db.relationship('User',
        backref=db.backref('shelf', uselist=False))

    def __init__(self, user=None):
        self.user = user

    def __repr__(self):
        return u'<Shelf (user: %r)>' % self.user.email
