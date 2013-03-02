# -*- coding: utf-8 -*-
import json

from flask.ext.babel import gettext as _

from cocoa.extensions import db

class IpSection(db.Model):

    __tablename__ = 'geo_ip'

    start = db.Column(db.BigInteger, primary_key=True)
    end = db.Column(db.BigInteger)
    city_id = db.Column(db.String(20), db.ForeignKey('geo_city.city_id'))

    city = db.relationship('City')

    def __repr__(self):
        return '<IP for %r>' % self.city.name


class City(db.Model):

    __tablename__ = 'geo_city'

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))
    province_id = db.Column(db.String(20),
        db.ForeignKey('geo_province.province_id'))

    province = db.relationship('Province', backref='cities')

    def __repr__(self):
        return '<City %r>' % self.name


class Province(db.Model):

    __tablename__ = 'geo_province'

    id = db.Column(db.Integer, primary_key=True)
    province_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Province %r>' % self.name

    def get_short_name(self):
        return province_short_name(self.name)
        return json.dumps(provinces)


def _str2ip(ip_str):

    sections = map(int, ip_str.split('.'))

    if len(sections) != 4:
        raise ValueError(_('Not a valid IP address.'))

    return (arr[0] << 24) | \
           (arr[1] << 16) | \
           (arr[2] << 8)  | \
           (arr[3] << 0)


def ip2city(ip_str):

    ip = _str2ip(ip_str)
    belongs_to = IpSection.query.filter(
        IpSection.start<=ip, IpSection.end>=ip).first()

    if belongs_to is None:
        return None
    else:
        return belongs_to.city

def province_short_name(name):

    if name[-1:] == u'省' or name[-1:] == u'市':
        return name[:-1]
    elif name[:2] in (u'新疆', u'西藏', u'广西',
                      u'宁夏', u'香港', u'澳门',):
        return name[:2]
    elif name[:3] == u'内蒙古':
        return name[:3]


def provinces():
    data = db.session.query(Province.province_id, Province.name).all()
    provinces = [{'province_id': x, 'name': province_short_name(y)} \
        for x, y in data]


def cities(province_id):
    data = db.session.query(City.city_id, City.name) \
             .filter(City.province_id==province_id).all()
    cities = [{'city_id': x, 'name': y} for x, y in cities]

    return json.dumps(cities)
