# -*- coding: utf-8 -*-
from time import time

from flask.ext.login import current_user

from cocoa.extensions import db
from cocoa.helpers.sql import JSONEncodedDict
from cocoa.helpers.common import slugify
from .consts import PostType, PostStatus
from ..book.models import Book

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

    def __init__(self, type, title, content, ref_books=None,
                 status=None, author=None):
        self.type = type
        self.title = title
        self.content = content

        self.ref_books = ref_books

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
        return Post.query.filter(user_id==user_id).\
                filter(slug==slug).first()
