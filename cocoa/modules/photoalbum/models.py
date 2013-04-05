# -*- coding: utf-8 -*-
from time import time

from cocoa.extensions import db

class PhotoAlbum(db.Model):

    __tablename__ = 'photo_album'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey='user.id')
    photo_src = db.Column(db.String(100))
    timestamp = db.Column(db.Integer, default=int(time()))

    user = db.relationship('User',
        backref=db.backref('photo_album', cascade='all, delete-orphan'))

    def __init__(self, photo_src, user=None):
        self.photo_src = photo_src
        self.user = user
