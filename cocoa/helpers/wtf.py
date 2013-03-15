# -*- coding: utf-8 -*-
"""
    对WTForms的扩展
    2013.03.03
"""
from flask.ext.wtf import Form as Base, Field, TextInput

from .common import str2list

class Form(Base):

    filters = [lambda x: x.strip()]


class DictField(Field):

    widget = TextInput()

    def __init__(self, label='', validators=None,
                 remove_duplicates=True, **kwargs):
        super(DictField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = str2list(valuelist[0],
                                 self.remove_duplicates)
        else:
            self.data = []
