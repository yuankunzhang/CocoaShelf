# -*- coding: utf-8 -*-
"""
    cocoa/__init__.py
    ~~~~~~~~~~~~~~~~~

    应用实例
    2013.03.01
"""
activate_this = '/var/www/cocoa/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from .application import create_app
