# -*- coding: utf-8 -*-
"""
    对SQLAlchemy的扩展
    2013.03.04
"""
from sqlalchemy.types import TypeDecorator, Text
import json

class JSONEncodedDict(TypeDecorator):

    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
