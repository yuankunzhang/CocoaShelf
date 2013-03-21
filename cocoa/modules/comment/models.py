# -*- coding: utf-8 -*-
from time import time

from flask.ext.babel import gettext as _

from cocoa.extensions import db
from cocoa.helpers.html import safe_html

class ShelfComments(db.Model):
    """书架留言"""

    __tablename__ = 'shelf_comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.Integer, default=int(time()))

    shelf = db.relationship('Shelf',
        backref=db.backref('comments', cascade='all, delete-orphan'))
    user = db.relationship('User',
        backref=db.backref('shelf_comments', cascade='all, delete-orphan'))

    def __init__(self, content, user, shelf=None):
        self.content = content
        self.user = user
        self.shelf = shelf

    def save(self):
        db.session.add(self)
        db.session.commit()


class BookShortReview(db.Model):
    """图书短评"""

    __tablename__ = 'book_short_review'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.Integer, default=int(time()))

    book = db.relationship('Book',
        backref=db.backref('short_reviews', cascade='all, delete-orphan'))
    user = db.relationship('User',
        backref=db.backref('book_short_reviews',
                            cascade='all, delete-orphan'))

    def __init__(self, content, book, user=None):
        self.content = safe_html(content, safe_tags=[])
        self.book = book
        self.user = user

    def save(self):
        s_review = BookShortReview.query.filter_by(user=self.user).\
                    filter_by(book=self.book).first()
        if s_review is not None:
            raise ValueError(_(u'You\'ve already comment this book.'))
        else:
            db.session.add(self)
            db.session.commit()
