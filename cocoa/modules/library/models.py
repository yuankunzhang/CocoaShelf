# -*- coding: utf-8 -*-
from datetime import datetime
from time import time

from sqlalchemy.ext.associationproxy import association_proxy

from cocoa.extensions import db
from cocoa.helpers.common import timesince
from .consts import ShelfType

class ShelfHave(db.Model):
    """我有"""

    __tablename__ = ShelfType.HAVE.text()

    library_id = db.Column(db.Integer, db.ForeignKey('library.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    library = db.relationship('Library',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class ShelfRead(db.Model):
    """读过"""

    __tablename__ = ShelfType.READ.text()

    library_id = db.Column(db.Integer, db.ForeignKey('library.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    library = db.relationship('Library',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class ShelfReading(db.Model):
    """在读"""

    __tablename__ = ShelfType.READING.text()

    library_id = db.Column(db.Integer, db.ForeignKey('library.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    library = db.relationship('Library',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class ShelfWish(db.Model):
    """想读"""

    __tablename__ = ShelfType.WISH.text()

    library_id = db.Column(db.Integer, db.ForeignKey('library.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    library = db.relationship('Library',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class ShelfLike(db.Model):
    """喜欢"""

    __tablename__ = ShelfType.LIKE.text()

    library_id = db.Column(db.Integer, db.ForeignKey('library.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    library = db.relationship('Library',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class Library(db.Model):

    __tablename__ = 'library'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    have_books = association_proxy(ShelfType.HAVE.text(), 'book')
    read_books = association_proxy(ShelfType.READ.text(), 'book')
    reading_books = association_proxy(ShelfType.READING.text(), 'book')
    wish_books = association_proxy(ShelfType.WISH.text(), 'book')
    like_books = association_proxy(ShelfType.LIKE.text(), 'book')

    def __init__(self, user=None):
        self.user = user

    def __repr__(self):
        return u'<Shelf (user: %r)>' % self.user.email
