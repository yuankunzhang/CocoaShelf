# -*- coding: utf-8 -*-
from sqlalchemy.ext.associationproxy import association_proxy

from flask import url_for
from flask.ext.sqlalchemy import BaseQuery

from cocoa.extensions import db

class CategoryQuery(BaseQuery):

    def roots(self):
        """第一级分类"""

        return Category.query.filter_by(parent_id=None).all()


class Category(db.Model):
    """图书分类"""

    __tablename__ = 'category'

    query_class = CategoryQuery

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(100))

    sub_categories = db.relationship('Category',
        backref=db.backref('parent_category', remote_side=id))
    books = association_proxy('category_books', 'book')
    
    def __init__(self, name, parent_id=None):
        self.name = name
        self.parent_id = parent_id

    def __repr__(self):
        return '<Category %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def as_tree(self, hyper_link=True):
        node = self
        # 如果是末端分类，设置超链接
        if node.parent_id and node.parent_category.parent_id \
                and hyper_link:
            tree_str = '<a href="' + \
                url_for('book.category_view',
                         category_id=self.id) + \
                '">' + self.name + '</a>'
        else:
            tree_str = self.name

        while node.parent_id is not None:
            node = node.parent_category
            tree_str = node.name + ' &gt; ' + tree_str
        return tree_str

    @staticmethod
    def as_list(parent_id=None):

        data = db.session.query(Category.id, Category.name,
               Category.parent_id).filter_by(parent_id=parent_id).all()

        results = [{'id': x.id, 'name': x.name, 'parent_id': x.parent_id} \
                  for x in data]
        return results


class BookCategory(db.Model):

    __tablename__ = 'm_book_category'

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        primary_key=True)

    book = db.relationship('Book',
        backref=db.backref('book_category',
            cascade='all, delete-orphan', uselist=False))
    category = db.relationship('Category',
        backref=db.backref('category_books', cascade='all, delete-orphan'))

    def __init__(self, category, book=None):
        self.category = category
        self.book = book
