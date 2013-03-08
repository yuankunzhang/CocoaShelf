# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

from cocoa.helpers.enum import Enum

Currency = Enum('CNY', 'USD')
Currency.CNY.set_text(u'元')
Currency.USD.set_text(u'美元')

Binding = Enum('PAPERBACK', 'HARDCOVER')
Binding.PAPERBACK.set_text(u'平装')
Binding.HARDCOVER.set_text(u'精装')

Language = Enum('CHINESE', 'ENGLISH')
