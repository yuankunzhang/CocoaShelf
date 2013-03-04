# -*- coding: utf-8 -*-
from time import time

from sqlalchemy.ext.associationproxy import association_proxy

from flask.ext.babel import gettext as _
from flask.ext.login import current_user

from cocoa.extensions import db
from cocoa.helpers.sqlalchemy import JSONEncodedDict
from cocoa.helpers.html import safe_html
from .consts import Currency, Binding, Language
from .helpers import isbn10_to_13, isbn13_to_10

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


class BookExtra(db.Model):
    """内容简介，作者简介"""

    __tablename__ = 'book_extra'

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    summary = db.Column(db.Text)
    author_intro = db.Column(db.Text)

    book = db.relationship('Book',
        backref=db.backref('extra', cascade='all, delete-orphan'))

    def __init__(self, summary=None, author_intro=None, book=None):
        self.summary = safe_html(summary)
        self.author_intro = safe_html(author_intro)
        self.book = book


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


def categories(parent_id=None):

    if parent_id is not None:   # second or third level
        return Category.query.filter_by(parent_id=parent_id).all()
    else:                       # first level
        return Category.query.filter_by(parent_id=None).all()


class BookCategory(db.Model):

    __tablename__ = 'm_book_category'

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category_id'),
        primary_key=True)

    book = db.relationship('Book',
        backref=db.backref('book_category',
        cascade='all, delete-orphan' uselist=False))
    category = db.relationship('Category')

    def __init__(self, category, book=None);
        self.category = category
        self.book = book
    

class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    isbn10 = db.Column(db.String(30), unique=True)
    isbn13 = db.Column(db.String(30), unique=True)

    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    orititle = db.Column(db.String(100))

    size = db.Column(db.SmallInteger)
    cover = db.Column(db.String(255))
    authors = db.Column(JSONEncodedDict)
    translators = db.Column(JSONEncodedDict)
    publisher = db.Column(db.String(100))
    pubdate = db.Column(db.Date)

    price = db.Column(db.Integer)
    currency = db.Column(db.SmallInteger, default=Currency.CNY.value())
    pages = db.Column(db.Integer)
    binding = db.Column(db.SmallInteger, default=Binding.PAPERBACK.value())
    language = db.Column(db.SmallInteger, default=Language.CHINESE.value())

    timestamp = db.Column(db.Integer, default=int(time()))
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))

    tags = association_proxy('book_tags', 'tag')

    def __init__(self, isbn, title, authors, publisher, price,
                 subtitle=None, orititle=None, translators=None,
                 size=None, pubdate=None, currency=None
                 pages=None, binding=None, language=None):
        if len(isbn) == 10:
            self.isbn10 = isbn
            self.isbn13 = isbn
        elif len(isbn) == 13:
            self.isbn13 = isbn
            self.isbn10 = isbn13_to10(isbn)
        else:
            raise ValueError(_(u'Invalid isbn number'))

        self.title = title
        self.subtitle = subtitle
        self.orititle = orititle

        self.authors = authors
        self.translators = translators

        self.publisher = publisher
        self.pubdate = pubdate
        self.size = size
        
        self.price = price
        self.currency = currency
        self.pages = pages
        self.binding = binding
        self.language = language

        self.creator = current_user.id

    def __repr__(self):
        return '<Book %r>' % self.title

    def save(self):
        book = Book.query.filter_by(isbn13=self.isbn13).first()
        if book is not None:
            raise ValueError(_(u'We\'ve already have this book'
                               u'in our database')
        else:
            db.session.add(self)
            db.session.commit()

    def add_tags(self, tag_list):
        for name in tag_list:
            tag = Tag.create_or_increase(name)
            if tag in self.tags:
                book_tag = BookTags.query \
                           .filter_by(book=self, tag=tag).first()
                book_tag.increase()
            else:
                self.tags.append(tag)
                db.session.commit()

    def get_pubdate(self):
        return self.pubdate.strftime('%Y-%m')
