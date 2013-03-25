# -*- coding: utf-8 -*-
from time import time

from sqlalchemy.ext.associationproxy import association_proxy

from flask.ext.login import current_user

from cocoa.extensions import db
from cocoa.helpers.sql import JSONEncodedDict
from cocoa.helpers.common import slugify
from .consts import PostType, PostStatus
from ..book.models import Book

class Keyword(db.Model):

    __tablename__ = 'post_keyword'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    count = db.Column(db.Integer, default=1)
    disabled = db.Column(db.Boolean, default=False)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Keyword %r>' % self.name

    @staticmethod
    def create_or_increase(name):
        keyword = Keyword.query.filter_by(name=name).first()

        if keyword is None:
            keyword = Keyword(name)
            db.session.add(keyword)
        else:
            keyword.count += 1

        db.session.commit()


class PostKeywords(db.Model):

    __tablename__ = 'm_post_keywords'

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),
        primary_key=True)
    keyword_id = db.Column(db.Integer, db.ForeignKey('post_keyword.id'),
        primary_key=True)

    post = db.relationship('Post',
        backref=db.backref('post_keywords', cascade='all, delete-orphan'))
    keyword = db.relationship('Keyword',
        backref=db.backref('keyword_posts', cascade='all, delete-orphan'))

    def __init__(self, keyword=None, post=None):
        self.keyword = keyword
        self.post = post


class Post(db.Model):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Integer, default=int(time()))
    type = db.Column(db.SmallInteger, default=PostType.ARTICAL.value())
    slug = db.Column(db.String(100))

    title = db.Column(db.Text)
    content = db.Column(db.Text)
    ref_books = db.Column(JSONEncodedDict(255))
    status = db.Column(db.SmallInteger, default=PostStatus.DRAFT.value())

    author = db.relationship('User',
        backref=db.backref('posts', cascade='all, delete-orphan'))

    keywords = association_proxy('post_keywords', 'keyword')

    def __init__(self, type, title, content, ref_books=None,
                 keywords=None, status=None, author=None):
        self.type = type
        self.title = title
        self.content = content

        self.ref_books = ref_books
        for k in keywords:
            self.keywords.append(Keyword.create_or_increase(k))

        self.status = status
        self.author = author

    def __repr__(self):
        return '<Post %r>' % self.title

    def get_ref_books(self):
        return [Book.query.get(i) for i in self.ref_books]

    def save(self):
        slug = slugify(self.title)
        if Post.query.filter_by(slug=slug).first() is None:
            self.slug = slug
        else:
            sn = 2
            self.slug = slug + u'-' + str(sn)
            while Post.query.filter_by(slug=self.slug).first() \
                    is not None:
                sn += 1
                self.slug = slug + u'-' + str(sn)

        current_user.posts.append(self)
        db.session.commit()

    @staticmethod
    def get_by_slug(user_id, slug):
        return Post.query.filter_by(user_id=user_id).\
                filter_by(slug=slug).first()
