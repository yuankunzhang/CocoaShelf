# -*- coding: utf-8 -*-
"""
    cocoa/extensions.py
    ~~~~~~~~~~~~~~~~~~~

    扩展
    2013.03.01
"""
import flask_sijax
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.cache import Cache
from flask.ext.babel import Babel

__all__ = ['db', 'sijax', 'login_manager', 'cache', 'babel', 'misaka']

db = SQLAlchemy()
sijax = flask_sijax.Sijax()
login_manager = LoginManager()
cache = Cache()
babel = Babel()
