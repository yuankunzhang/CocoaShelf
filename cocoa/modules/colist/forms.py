# -*- coding: utf-8 -*-
from flask.ext.wtf import TextField, TextAreaField, Required
from flask.ext.babel import gettext as _

from cocoa.helpers.wtf import Form

class ColistNewForm(Form):

    name = TextField(_(u'Colist Name'), [
        Required(message=_(u'Required'))
    ], id=u'colist-name')

    intro = TextAreaField(_(u'Colist Introduction'), [
        Required(message=_(u'Required'))
    ], id=u'colist-intro')
