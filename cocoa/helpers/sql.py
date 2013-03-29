# -*- coding: utf-8 -*-
"""
    对SQLAlchemy的扩展
    2013.03.04
"""
from sqlalchemy.types import TypeDecorator, VARCHAR, TEXT
import json

class JSONEncodedDict(TypeDecorator):

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        return _dumps(value)

    def process_result_value(self, value, dialect):
        return _loads(value)


class JSONEncodedDictText(TypeDecorator):

    impl = TEXT

    def process_bind_param(self, value, dialect):
        return _dumps(value)

    def process_result_value(self, value, dialect):
        return _loads(value)


def _dumps(value):

    if value is not None:
        value = json.dumps(value)
    return value


def _loads(value):

    if value is not None:
        value = json.loads(value)
    return value
