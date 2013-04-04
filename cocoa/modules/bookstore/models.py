# -*- coding: utf-8 -*-
from time import time

from cocoa.extensions import db

class Bookstore(db.Model):

    __tablename__ = 'bookstore'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(30))
    intro = db.Column(db.Text)
    city_id = db.Column(db.String(20), db.ForeignKey('geo_city.city_id'))
    timestamp = db.Column(db.Integer, default=int(time()))

    city = db.relationship('City', backref='bookstores')

    def __init__(self, name=None, address=None, intro=None, city_id=None):
        #TODO
        """
            为了妥协flask-admin,将参数默认值均改为None
            请改回
        """

        self.name = name
        self.address = address
        self.intro = intro
        self.city_id = city_id
