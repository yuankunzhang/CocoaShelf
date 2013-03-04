# -*- coding: utf-8 -*-
import re
import json
from time import time

from werkzeug import generate_password_hash, check_password_hash

from flask.ext.babel import gettext as _

from cocoa.extensions import db, login_manager
from .consts import Role, Gender

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)  # 用户名
    penname = db.Column(db.String(100))                # 笔名
    intro = db.Column(db.Text)
    gender = db.Column(db.SmallInteger, default=Gender.SECRET.value())
    avatar = db.Column(db.String(100))
    thumbnail_box = db.Column(db.String(100))
    city_id = db.Column(db.String(20), db.ForeignKey('geo_city.city_id'))
    role = db.Column(db.SmallInteger, default=Role.MEMBER.value())
    active = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.Integer, default=int(time()))

    city = db.relationship('City', backref='users')

    def __init__(self, email, password, city_id=None, username=None):
        self.email = email.lower()
        self.password = generate_password_hash(password)
        self.city_id = city_id
        self.username = username

        # TODO
        # check if email address is valid.

        if self.username is None:
            email_name = re.match('^([\d\w.-]+)@', self.email).group(1)
            if User.query.filter_by(username=email_name).first() is None:
                self.username = email_name
            else:
                sn = 2
                username = email_name + str(sn)
                while User.query.filter_by(username=username).first() \
                        is not None:
                    sn += 1
                    username = email_name + str(sn)
                self.username = username

    def __repr__(self):
        return '<User %r>' % self.email

    def save(self):
        u = User.query.filter_by(email=self.email).first()
        if u is None:
            db.session.add(self)
            db.session.commit()
        else:
            raise ValueError(_('This email has been signed up.'))
    
    def update(self, penname, intro, gender, city_id):
        self.penname = penname
        self.intro = intro
        self.gender = gender
        self.city_id = city_id

        db.session.commit()

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def update_password(self, old, new):
        if not self.check_password(old):
            raise ValueError(_('Wrong previous password.'))
        else:
            self.password = generate_password_hash(new)
            db.session.commit()

    @staticmethod
    def authenticate(email, password):
        u = User.query.filter_by(email=email).first()
        if u is None or \
                not check_password_hash(u.password, password):
            return None, False
        else:
            return u, True

    # functions that are required by Flask-Login
    def is_authenticated(self):
        return True

    def is_active(self):
        # TODO
        #return self.active = True
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    # end

    def get_location(self):
        """获取用户所在地，格式： '江苏 无锡市'"""

        if self.city is None:
            return None

        province_name = self.city.province.get_short_name()
        city_name = self.city.name
        return u'%r %r' % (province_name, city_name)

    def set_thumbnail_box(self, box):
        box = dict(zip(('x1', 'y1', 'x2', 'y2'), box))
        self.thumbnail_box = json.dumps(box)

    def get_thumbnail(self):
        if self.avatar is None:
            return None
        else:
            slices = self.avatar.split('.')
            return slices[0] + '_t.' + slices[1]
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id)
