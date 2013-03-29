# -*- coding: utf-8 -*-
from cocoa.extensions import db
from cocoa.helpers.sql import JSONEncodedDictText
from ..book.models import Book

class SimilarityBooks(db.Model):
    """相似图书数据表"""

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)

    similarity = db.Column(JSONEncodedDictText)

    book = db.relationship('Book',
        backref=db.backref('similar_books', uselist=False))

    def __init__(self, similarity, book=None):
        self.similarity = similarity
        self.book = book

def book_similarity():

    all_books = Book.query.all()

    for target_book in all_books:
        book_tags = target_book.tags

        for tag in book_tags:
            secondly_books = tag.books

            for compare_book in secondly_books:
                distance = 0
                secondly_book_tags = compare_book.tags

                for t in secondly_book_tags:
                    if t in book_tags:
                        distance += 1
