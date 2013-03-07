# -*- coding: utf-8 -*-

from cocoa.extensions import db

class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(100))

    sub_categories = db.relationship('Category',
        backref=db.backref('parent_category', remote_side=id))

    def __init__(self, name, parent_id=None):
        self.name = name
        self.parent_id = parent_id

    def __repr__(self):
        return '<Category %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class BookCategory(db.Model):

    __tablename__ = 'm_book_category'

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        primary_key=True)

    book = db.relationship('Book',
        backref=db.backref('book_category',
        cascade='all, delete-orphan', uselist=False))
    category = db.relationship('Category')

    def __init__(self, category, book=None):
        self.category = category
        self.book = book


def categories(parent_id=None):

    if parent_id is not None:   # second or third level
        return Category.query.filter_by(parent_id=parent_id).all()
    else:                       # first level
        return Category.query.filter_by(parent_id=None).all()


