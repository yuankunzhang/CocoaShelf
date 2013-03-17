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
        return self._name.lower()

    def text(self):
        return self._text

    def set_text(self, text):
        self._text = text


class Enum(object):

    def __init__(self, *seq, **named):
        self._items = dict(zip(seq, range(len(seq))), **named).items()
        d = dict((k, EnumInteger(k, v)) for (k, v) in self._items)
        self.__dict__.update(d)

    def from_int(self, value):
        for k, v in self._items:
            if v == value:
                return self.__dict__[k]
        raise ValueError(_(u'Wrong value'))

    def from_name(self, name):
        for k, v in self._items:
            if k == name.upper():
                return self.__dict__[k]
        raise ValueError(_(u'Wrong key'))

    def items(self):
        return self._items

    def __iter__(self):
        for k, v in sorted(self._items, key=lambda o: o[1]):
            yield self.__dict__[k]
