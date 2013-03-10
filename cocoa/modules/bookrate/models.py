# -*- coding: utf-8 -*-
from time import time

from cocoa.extensions import db

class BookRateDetail(db.Model):

    __tablename__ = 'book_rate_detail'

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        primary_key=True)
    score = db.Column(db.SmallInteger)
    timestamp = db.Column(db.Integer, default=int(time()))

    book = db.relationship('Book',
        backref=db.backref('rate_details', cascade='all, delete-orphan'))
    user = db.relationship('User')

    def __init__(self, score=0, user=None, book=None):
        self.score = score
        self.user = user
        self.book = book

    def save(self):
        rate_detail = BookRateDetail.query.filter_by(book=self.book,
            user=self.user).first()
        if rate_detail is not None:
            raise ValueError('We already have this record')
        else:
            db.session.add(self)
            db.session.commit()

            BookRate.create_or_update(self.score, self.book)


class BookRate(db.Model):

    __tablename__ = 'book_rate'

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    max = db.Column(db.Integer, default=0)
    min = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=1)

    book = db.relationship('Book',
        backref=db.backref('rate', cascade='all, delete-orphan',
            uselist=False))

    def __init__(self, score=0, book=None):
        self.max = self.min = self.total = score
        self.count = 1
        self.book = book

    @staticmethod
    def create_or_update(score, book):
        rate = BookRate.query.filter_by(book=book).first()
        if rate is None:
            rate = BookRate(score, book)
            db.session.add(rate)
            db.session.commit()
        else:
            rate.update(score)
        
        return rate

    def update(self, score):
        if self.max < score:
            self.max = score
        elif self.min > score:
            self.min = score

        self.total += score
        self.count += 1
