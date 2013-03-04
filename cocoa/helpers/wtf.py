# -*- coding: utf-8 -*-
"""
    对WTForms的扩展
    2013.03.03
"""
from flask.ext.wtf import Form as Base

class Form(Base):

    filters = [lambda x: x.strip()]
