# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

class EnumInteger(object):
    """在枚举类型中使用的整型"""

    def __init__(self, name, val=0):
        self._name = name
        self._val = int(val)

    def __index__(self):
        return self._val

    def value(self):
        return self._val

    def name(self):
        return self._name

    def text(self):
        return self._text

    def set_text(self, text):
        self._text = text


class EnumBase(object):

    @classmethod
    def from_int(cls, value):
        for k in cls.items.keys():
            if cls.items[k] == value:
                return EnumInteger(k, value)

        return ValueError(_(u'Wrong value'))


def Enum(*sequential, **named):
    """伪枚举类型"""

    data = dict(zip(sequential, range(len(sequential))), **named)
    enums = dict((k, EnumInteger(k, v)) for (k, v) in data.iteritems())
    enums['items'] = data
    return type('Enum', (EnumBase,), enums)
