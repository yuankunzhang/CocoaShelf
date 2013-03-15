# -*- coding: utf-8 -*-
from datetime import datetime
from time import time

from flask.ext.babel import gettext as _

from cocoa.extensions import db
from .consts import ColumnType
from .query import ShelfQuery
from ..book.models import Book, BookExtra

class ColumnBase(object):

    @classmethod
    def get_books(cls, shelf):
        query = cls.query.outerjoin(Book).\
               filter(cls.shelf==shelf)
        if cls == ColumnReading:
            query = query.filter(cls.finished_timestamp==None)
        rows = query.all()
        return [r.book for r in rows]

    @classmethod
    def contains(cls, shelf, book):
        query = cls.query.filter(cls.shelf==shelf).filter(cls.book==book)
        if cls == ColumnReading:
            query = query.filter(cls.finished_timestamp==None)

        result = query.first()
        if result is None:
            return False
        else:
            return True

    @classmethod
    def add_book(cls, shelf, book):
        if not cls.contains(shelf, book):
            b = cls(book, shelf)
            db.session.add(b)
            db.session.commit()


class ColumnHave(db.Model, ColumnBase):
    """我有"""

    __tablename__ = 'column_have'

    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class ColumnRead(db.Model, ColumnBase):
    """读过"""

    __tablename__ = 'column_read'

    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class ColumnReading(db.Model, ColumnBase):
    """在读"""

    __tablename__ = 'column_reading'

    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    timestamp = db.Column(db.Integer, default=int(time()))
    finished_timestamp = db.Column(db.Integer)

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf

    @classmethod
    def get_finished_books(cls, shelf):
        rows = db.session.query(
                Book.title, Book.cover, BookExtra.summary,
                cls.timestamp, cls.finished_timestamp).\
               outerjoin(BookExtra).\
               outerjoin(cls).\
               filter(cls.finished_timestamp!=None).\
               filter(cls.shelf==shelf).all()

        books = [{
            'title': r.title,
            'cover': r.cover,
            'summary': r.summary,
            'timestamp': r.timestamp,
            'finished_timestamp': r.finished_timestamp,
        } for r in rows]

        return books


class ColumnWish(db.Model, ColumnBase):
    """想读"""

    __tablename__ = 'column_wish'

    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class ColumnLike(db.Model, ColumnBase):
    """喜欢"""

    __tablename__ = 'column_like'

    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref(__tablename__, cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, shelf=None):
        self.book = book
        self.shelf = shelf


class Shelf(db.Model):

    __tablename__ = 'shelf'

    query_class = ShelfQuery

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User',
        backref=db.backref('shelf', uselist=False))

    def __init__(self, user=None):
        self.user = user

    def __repr__(self):
        return u'<Shelf for %r>' % self.user.email

    def add_book(self, book, column_names):
        for column_name in column_names:
            column = _get_column(column_name)

            if column is not None:
                column.add_book(self, book)

    def finish_reading(self, book):
        reading_book = ColumnReading.query.filter_by(shelf=self,
            book=book, finished_timestamp=None).first()
        if reading_book is not None:
            reading_book.finished_timestamp = int(time())
            ColumnRead.add_book(self, book)
            db.session.commit()


def _get_column(column_name):
    if column_name in ['have', 'read', 'reading', 'wish', 'like']:
        return ColumnType.from_name(column_name).class_
    else:
        return None


ColumnType.HAVE.class_ = ColumnHave
ColumnType.READ.class_ = ColumnRead
ColumnType.READING.class_ = ColumnReading
ColumnType.WISH.class_ = ColumnWish
ColumnType.LIKE.class_ = ColumnLike