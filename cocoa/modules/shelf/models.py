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

    def get_column(self, column_type):
        if column_type == ColumnType.HAVE.value():
            return self.have_books
        elif column_type == ColumnType.READ.value():
            return self.read_books
        elif column_type == ColumnType.READING.value():
            return self.reading_books
        elif column_type == ColumnType.WISH.value():
            return self.wish_books
        elif column_type == ColumnType.LIKE.value():
            return self.like_books
        else:
            return None

    def add_book_to_shelf(self, book, column_types):
        for column_type in column_types:
            column = self.get_column(int(column_type))
            if column is not None and book not in column:
                column.append(book)
        db.session.commit()

    def get_book_status(self, book):
        have_flag = book in self.have_books
        read_flag = book in self.read_books
        reading_flag = book in self.reading_books
        wish_flag = book in self.wish_books
        like_flag = book in self.like_books

        whole_flag = have_flag and read_flag and \
                     reading_flag and wish_flag and \
                     like_flag

        return {
            'have':     have_flag,
            'read':     read_flag,
            'reading':  reading_flag,
            'wish':     wish_flag,
            'like':     like_flag,
            'whole':    whole_flag,
        }
