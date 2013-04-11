# -*- coding: utf-8 -*-
"""
    cocoa/application.py
    ~~~~~~~~~~~~~~~~~~~~

    初始化脚本
    2013.03.01
"""
import re
import logging
import re
from datetime import datetime

from logging.handlers import RotatingFileHandler

import markdown as md

from jinja2 import evalcontextfilter, Markup, escape
from flask import Flask, request, jsonify, render_template, \
     g, render_template, Markup
from flask.ext.babel import gettext as _
from flask.ext.principal import Principal, identity_loaded
from flask.ext.uploads import configure_uploads

from .config import DefaultConfig
from .extensions import db, sijax, login_manager, cache, babel, \
      sys_mail, album
from .admin import admin
from .helpers.common import timesince as _timesince
from .modules import frontend, location, account, book, shelf, \
      category, blog, colist, group, bookstore, mail, tag, \
      recsys, vitality, docs, photoalbum

__all__ = ['create_app']

DEFAULT_APP_NAME = 'cocoa'

DEFAULT_MODULES = (
    (frontend.mod, ''),
    (location.mod, '/location'),
    (account.mod, '/u'),
    (book.mod, '/book'),
    (shelf.mod, '/shelf'),
    (category.mod, '/category'),
    (blog.mod, '/blog'),
    (colist.mod, '/colist'),
    (group.mod, '/group'),
    (bookstore.mod, '/bookstore'),
    (mail.mod, '/mail'),
    (tag.mod, '/tag'),
    (recsys.mod, '/recsys'),
    (vitality.mod, '/vitality'),
    (docs.mod, '/docs'),
    (photoalbum.mod, '/photoalbum'),
)

def create_app(config=None, app_name=None, modules=None):

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(app_name)

    configure_app(app, config)
    configure_extensions(app)
    configure_errorhandlers(app)
    configure_modules(app, modules)
    configure_identity(app)
    configure_logging(app)
    configure_template_filters(app)

    return app


def configure_app(app, config):

    app.config.from_object(DefaultConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('COCOA_CONFIG', silent=True)


def configure_modules(app, modules):

    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)

    if app.debug:
        from cocoa.utils.book import mod as bookutils
        from cocoa.utils.db import mod as dbutils
        app.register_blueprint(bookutils, url_prefix='/bookutils')
        app.register_blueprint(dbutils, url_prefix='/dbutils')


def configure_template_filters(app):

    _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

    @app.template_filter()
    @evalcontextfilter
    def nl2br(eval_ctx, value):
        if value is None:
            return ''
        result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', \
            Markup('</p>\n<p>')) for p in _paragraph_re.split(value))
        if eval_ctx.autoescape:
            result = Markup(result)
        return result

    @app.template_filter()
    def timesince(timestamp):
        dt = datetime.fromtimestamp(timestamp)
        return _timesince(dt)

    @app.template_filter()
    def dt(timestamp):
        dt = datetime.fromtimestamp(timestamp)
        return dt

    @app.template_filter()
    def markdown(stream):
        """
            处理markdown格式文本
            img标签：
                ![Alt](/path/to/img, 'Optional Title')@width
            或：
                ![Alt](/path/to/img, 'Optional Title')@width@height
        """

        result = md.markdown(stream, safe_mode='remove')
        re_img = r'(<img)(\s[^>]*\ssrc=".*?".*>)@(\d+)'
        result = re.sub(re_img, r'\1 width="\3"\2', result)
        return Markup(result) 


def configure_errorhandlers(app):

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('404 page not found'))
        return render_template('errors/404.html', error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('403 forbidden'))
        return render_template('errors/403.html', error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('500 server error'))
        return render_template('errors/500.html', error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(error=_('401 unauthorized'))
        return render_template('errors/401.html', error=error)


def configure_extensions(app):

    db.init_app(app)
    sijax.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'account.signin'
    sys_mail.init_app(app)
    cache.init_app(app)

    admin.init_app(app)

    configure_i18n(app)
    configure_uploads(app, album)


def configure_i18n(app):

    babel.init_app(app)


def configure_identity(app):

    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = account.models.User.query.from_identity(identity)


def configure_logging(app):

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    # Level: debug
    debug_log = app.config['DEBUG_LOG']
    debug_file_handler = \
        RotatingFileHandler(debug_log,
                            maxBytes=100000,
                            backupCount=10)
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    # Level: warning
    warning_log = app.config['WARNING_LOG']
    warning_file_handler = \
        RotatingFileHandler(warning_log,
                            maxBytes=100000,
                            backupCount=10)
    warning_file_handler.setLevel(logging.WARNING)
    warning_file_handler.setFormatter(formatter)
    app.logger.addHandler(warning_file_handler)

    # Level: error
    error_log = app.config['ERROR_LOG']
    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)
