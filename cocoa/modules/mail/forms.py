# -*- coding: utf-8 -*-
from flask.ext.wtf import TextField, TextAreaField, HiddenField, \
        Required
from flask.ext.babel import gettext as _

from cocoa.helpers.wtf import Form

class MailNewForm(Form):

    parent_id = HiddenField()

    title = TextField(_(u'Title'), [
        Required(_(u'Required')),
    ], id=u'mail-title')

    content = TextAreaField(_(u'Content'), [
        Required(_(u'Required')),
    ], id=u'mail-content')
