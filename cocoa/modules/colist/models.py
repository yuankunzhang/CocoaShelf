# -*- coding: utf-8 -*-
from time import time

from sqlalchemy.ext.associationproxy import association_proxy

from flask.ext.login import current_user

from cocoa.extensions import db
from ..book.models import Book

class ColistBooks(db.Model):

    __tablename__ = 'm_colist_books'

    colist_id = db.Column(db.Integer, db.ForeignKey('colist.id'),
        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    timestamp = db.Column(db.Integer, default=int(time()))

    colist = db.relationship('Colist',
        backref=db.backref('colist_books', cascade='all, delete-orphan'))
    book = db.relationship('Book')

    def __init__(self, book=None, colist=None):
        self.book = book
        self.colist = colist


class Colist(db.Model):

    __tablename__ = 'colist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255))
    intro = db.Column(db.Text)
    timestamp = db.Column(db.Integer, default=int(time()))

    books = association_proxy('colist_books', 'book')
    user = db.relationship('User', backref='colists')

    def __init__(self, name, intro, user=None):
        self.name = name
        self.intro = intro
        self.user = user

    def __repr__(self):
        return '<Colist %r>' % self.name

    def save(self):
        current_user.colists.append(self)
        db.session.commit()

    def add_book(self, book):
        if book not in self.books:
            self.books.append(book)
            db.session.commit()

    def add_books(self, book_ids):
        for bid in book_ids:
            book = Book.query.filter_by(isbn13=bid).first()
            if book not in self.books:
                self.books.append(book)

        db.session.commit()
