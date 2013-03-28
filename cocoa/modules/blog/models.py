# -*- coding: utf-8 -*-
from time import time

from sqlalchemy import func

from sqlalchemy.ext.associationproxy import association_proxy

from flask.ext.sqlalchemy import BaseQuery
from flask.ext.login import current_user
from flask.ext.principal import Permission, UserNeed

from cocoa.extensions import db
from cocoa.helpers.sql import JSONEncodedDict
from cocoa.helpers.common import slugify
from cocoa.permissions import moderator
from .consts import PostType, PostStatus
from ..book.models import Book
from ..permissions import Permissions

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
        return keyword

    @staticmethod
    def from_name(name):
        return Keyword.query.filter_by(name=name).first()


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


class PostQuery(BaseQuery):

    def get_published(self, user_id):
        return Post.query.filter_by(user_id=user_id).\
               filter_by(status=PostStatus.PUBLISHED.value).\
               all()

    def get_by_slug(self, user_id, slug):
        return Post.query.filter_by(user_id=user_id).\
                filter_by(slug=slug).first()


class Post(db.Model):

    __tablename__ = 'post'

    query_class = PostQuery

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Integer, default=int(time()))
    type = db.Column(db.SmallInteger, default=PostType.ARTICAL.value)
    slug = db.Column(db.String(100))

    title = db.Column(db.Text)
    content = db.Column(db.Text)
    ref_books = db.Column(JSONEncodedDict(255))
    status = db.Column(db.SmallInteger, default=PostStatus.DRAFT.value)

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

    class _Permissions(Permissions):

        def default(self):
            return Permission(UserNeed(self.user_id)) & moderator

        def delete(self):
            return self.default()

        def edit(self):
            return Permission(UserNeed(self.user_id))

    def permissions(self):
        return self._Permissions(self)

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

    def update(self, type, title, content, ref_books, keywords):
        self.type = type
        self.title = title
        self.content = content

        self.ref_books = ref_books

        kws = [kw.name for kw in self.keywords]
        for name in kws:
            if name not in keywords:
                self.keywords.remove(Keyword.from_name(name))
        for name in keywords:
            if name not in kws:
                self.keywords.append(Keyword.create_or_increase(name))

        db.session.commit()

    def delete(self):
        self.status = PostStatus.DROPPED.value
        db.session.commit()

    @staticmethod
    def get_keywords(user_id):
        return db.session.query(Keyword.id, Keyword.name,
                    func.count(Keyword.id).label('count')).\
                outerjoin(PostKeywords,
                    PostKeywords.keyword_id==Keyword.id).\
                outerjoin(Post,
                    Post.id==PostKeywords.post_id).\
                filter(Post.user_id==user_id).\
                order_by(func.count(Keyword.id).desc()).\
                group_by(Keyword.id).all()

    @staticmethod
    def get_keyword_posts(user_id, keyword_id):
        return Post.query.outerjoin(PostKeywords).outerjoin(Keyword).\
                filter(Post.user_id==user_id, Keyword.id==keyword_id).\
                all()
