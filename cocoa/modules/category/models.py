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

    def as_tree(self):
        tree_str = self.name
        node = self
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
    category = db.relationship('Category')

    def __init__(self, category, book=None):
        self.category = category
        self.book = book
