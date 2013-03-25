# -*- coding: utf-8 -*-
from flask.ext.wtf import TextField, TextAreaField, \
    SelectField, Required
from flask.ext.babel import gettext as _

from cocoa.helpers.wtf import Form, DictField
from .consts import PostType

class PostNewForm(Form):

    title = TextField(_(u'Title'), [
        Required(message=_(u'Required')),
    ], id=u'post-title')

    content = TextAreaField(_(u'Content'), [
    ], id=u'post-content')

    type = SelectField(_(u'Type'), choices=[
        (PostType.ARTICAL.value(), PostType.ARTICAL.text()),
        (PostType.REVIEW.value(), PostType.REVIEW.text()),
        (PostType.NOTE.value(), PostType.NOTE.text()),
    ], coerce=int, id=u'post-type')

    ref_books = DictField(_(u'References'), [
    ], id=u'post-ref-books')

    keywords =DictField(_(u'Keywords'), [
    ], id=u'post-keywords')
