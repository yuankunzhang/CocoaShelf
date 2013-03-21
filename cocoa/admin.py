# -*- coding: utf-8 -*-
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

from .extensions import db
from .modules.location.models import City
from .modules.account.models import User

__all__ = ['admin']

admin = Admin(name='Cocoa')
admin.add_view(ModelView(User, db.session))
