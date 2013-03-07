# -*- coding: utf-8 -*-
from cocoa.extensions import db

class Tag(db.Model):

    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique=True)
    count = db.Column(db.Integer, default=1)
    disabled = db.Column(db.Boolean, default=False)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Tag %r(%d total)>' % (self.name, self.count)

    @staticmethod
    def create_or_increase(name):
        tag = Tag.query.filter_by(name=name).first()
        if tag is None:
            tag = Tag(name)
            db.session.add(tag)
            db.session.commit()
        else:
            tag.increase()

        return tag

    def increase(self):
        self.count += 1
        db.session.commit()


class BookTags(db.Model):

    __tablename__ = 'm_book_tags'

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'),
        primary_key=True)
    count = db.Column(db.Integer, default=1)

    book = db.relationship('Book',
        backref=db.backref('book_tags', cascade='all, delete-orphan'))
    tag = db.relationship('Tag')

    def __init__(self, tag=None, book=None):
        self.tag = tag
        self.book = book

    def increase(self):
        self.count += 1
        db.session.commit()
