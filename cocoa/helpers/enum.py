# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

class EnumInteger(object):
    """在枚举类型中使用的整型"""

    def __init__(self, val=0, name=None):
        self._val = int(val)
        self._name = name

    def __index__(self):
        return self._val

    def value(self):
        return self._val

    def name(self):
        return self._name

    def __str__(self):
        return _(self._name.lower())


def Enum(*sequential, **named):
    """伪枚举类型"""

    data = dict(zip(sequential, range(len(sequential))), **named)
    enums = dict((k, EnumInteger(v, k)) for (k, v) in data.iteritems())
    return type('Enum', (), enums)
