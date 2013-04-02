# -*- coding: utf-8 -*-
from time import time

from cocoa.extensions import db

class Bookstore(db.Model):

    __tablename__ = 'bookstore'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(255))
    intro = db.Column(db.Text)
    city_id = db.Column(db.String(20), db.ForeignKey('geo_city.city_id'))
    timestamp = db.Column(db.Integer, default=int(time()))

    city = db.relationship('City', backref='bookstores')

    def __init__(self, name, address, intro=None, city_id=None):
        self.name = name
        self.address = address
        self.intro = intro
        self.city_id = city_id
