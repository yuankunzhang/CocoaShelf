# -*- coding: utf-8 -*-
"""
    cocoa/application.py
    ~~~~~~~~~~~~~~~~~~~~

    初始化脚本
    2013.03.01
"""
from flask import Flask, request, jsonify, render_template, g
from flask.ext.babel import gettext as _
from flask.ext.themes import setup_themes

from .config import DefaultConfig
from .extensions import db, sijax, login_manager, cache, babel
from .modules import frontend

__all__ = ['create_app']

DEFAULT_APP_NAME = 'cocoa'

DEFAULT_MODULES = (
    (frontend.mod, ''),
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


def configure_template_filters(app):

    pass


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
    setup_themes(app)

    configure_i18n(app)


def configure_i18n(app):

    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.configure.get('ACCEPT_LANGUAGES',
                                            ['zh_CN'])
        return request.accept_languages.best_match(accept_languages)


def configure_logging(app):

    # TODO
    pass
