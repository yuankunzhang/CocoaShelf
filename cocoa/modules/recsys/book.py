# -*- coding: utf-8 -*-
import math
import time

from cocoa.extensions import db
from cocoa.helpers.sql import JSONEncodedDictText

TOP_COUNT = 10  # 保存相似度最高的10本图书

class SimilarBooks(db.Model):
    """相似图书数据表"""

    __tablename__ = 'rec_similar_books'

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        primary_key=True)

    similarity = db.Column(JSONEncodedDictText)

    book = db.relationship('Book',
        backref=db.backref('similar_books', uselist=False))

    def __init__(self, similarity, book=None):
        self.similarity = similarity
        self.book = book

def book_similarity(book_id=None):
    from ..book.models import Book

    time_start = time.time()

    if book_id:
        ids = [book_id]
    else:
        ids = [b.id for b in Book.query.all()]

    for id in ids:
        book = Book.query.get(id)
        tags = [x.tag for x in book.book_tags if x.tag.useless == False]
        tag_set = {}
        for x in book.book_tags:
            if x.tag.useless == False:
                tag_set.update({x.tag_id: x.count})
        topN = []

        for tag in tags:
            similar_book_ids = [b.id for b in tag.books if b.id != id]

            for sb_id in similar_book_ids:
                if sb_id in [x[0] for x in topN]:
                    continue

                sb = Book.query.get(sb_id)
                sb_tag_set = {}
                for x in sb.book_tags:
                    if x.tag.useless == False:
                        sb_tag_set.update({x.tag_id: x.count})
                distance = 0

                for t, c in sb_tag_set.items():
                    if tag_set.has_key(t):
                        c2 = tag_set[t]
                        distance += math.sqrt((c - c2)**2 / float(c + c2))

                if not topN or len(topN) < TOP_COUNT:
                    topN.append((sb_id, distance))
                elif distance < topN[-1][1]:
                    topN[-1] = (sb_id, distance)
                topN = sorted(topN, key=lambda x: x[1])

        if book.similar_books is None:
            book.similar_books = SimilarityBooks(topN)
        else:
            book.similar_books.similarity = topN
        db.session.commit()

    time_execution = time.time() - time_start
    print 'Program execution time: ', time_execution, 's'
