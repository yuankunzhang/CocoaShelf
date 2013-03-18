# -*- coding: utf-8 -*-
from flask.ext.wtf import TextField, TextAreaField, Required
from flask.ext.babel import gettext as _

from cocoa.helpers.wtf import Form

class GroupNewForm(Form):

    name = TextField(_(u'Group Name'), [
        Required(message=_(u'Required'))
    ], id=u'group-name')

    intro = TextAreaField(_(u'Group Introduction'), [
        Required(message=_(u'Required'))
    ], id='add-intro')
