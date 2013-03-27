# -*- coding: utf-8 -*-
"""
    cocoa/config.py
    ~~~~~~~~~~~~~~~

    配置文件
    2013.03.01
"""
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig(object):

    # 测试模式，在线上环境中务必关闭
    DEBUG = True

    DEBUG_LOG = os.path.join(_basedir, 'logs/debug.log')
    ERROR_LOG = os.path.join(_basedir, 'logs/error.log')

    ADMINS = frozenset(['feber007@gmail.com'])
    SECRET_KEY = 'set_a_secret_key_here'
    
    SQLALCHEMY_DATABASE_URI = 'mysql://root:900307@localhost/cocoa_dev_3'
    SQLALCHEMY_ECHO = False

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'set_a_session_key_here'

    SIJAX_STATIC_PATH = os.path.join(_basedir, 'static/js/sijax')
    SIJAX_JSON_URI = os.path.join(_basedir, 'static/js/sijax/json2.js')

    ACCEPT_LANGUAGES = ['en', 'zh_CN']
    BABEL_DEFAULT_LOCALE = 'zh_CN'

    THEME = 'cocoa'

    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

    # 路径设置
    # 用户头像
    AVATAR_STATIC_PATH = '/static/upload/avatar/'
    AVATAR_BASE_DIR = os.path.join(_basedir, 'static/upload/avatar')
    # 图书封面
    COVER_STATIC_PATH = '/static/upload/cover/'
    COVER_BASE_DIR = os.path.join(_basedir, 'static/upload/cover')
    # 小组图腾
    TOTEM_STATIC_PATH = '/static/upload/totem/'
    TOTEM_BASE_DIR = os.path.join(_basedir, 'static/upload/totem')

    FILES_PER_DIR = 1000
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024


class TestConfig(object):

    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/cocoa.db'
    SQLALCHEMY_ECHO = False
