# -*- coding: utf-8 -*-
from cocoa.extensions import db
from cocoa.helpers.sql import JSONEncodedDictText
from ..tag.models import Tag

class SimilarityTags(db.Model):
    """相似标签数据表"""

    __tablename__ = 'rec_similarity_tags'

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'),
        primary_key=True)

    # 与其他标签的相似性
    # Format: [[12, 4], [7, 3], [16, 1]]
    # 12 => tag_id, 4 => relationship distance.
    # 相关距离越大，相似性越高
    similarity = db.Column(JSONEncodedDictText)

    tag = db.relationship('Tag',
        backref=db.backref('similar_tags', uselist=False))

    def __init__(self, similarity, tag=None):
        self.similarity = similarity
        self.tag = tag


def tag_similarity():

    all_tags = Tag.query.useful_tags()

    for target_tag in all_tags:
        related_tags = {}
        for book in target_tag.books:
            for book_tag in book.tags:
                id = book_tag.id

                if id == target_tag.id:
                    continue
                if not related_tags.has_key(id):
                    related_tags[id] = 1
                else:
                    related_tags[id] += 1

        related_tags = sorted(related_tags.iteritems(),
            key=lambda (k, v): (v, k), reverse=True)

        if target_tag.similar_tags is None:
            target_tag.similar_tags = SimilarityTags(related_tags)
        else:
            target_tag.similar_tags.similarity = related_tags
        db.session.commit()
