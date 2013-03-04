# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

from cocoa.helpers.enum import Enum

Currency = Enum('CNY', 'USD')
Binding = Enum('PAPERBACK', 'HARDCOVER')
Language = Enum('CHINESE', 'ENGLISH')
