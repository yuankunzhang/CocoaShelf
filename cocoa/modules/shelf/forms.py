# -*- coding: utf-8 -*-
from flask.ext.wtf import TextAreaField, Required
from flask.ext.babel import gettext as _

from cocoa.helpers.wtf import Form

class CommentForm(Form):

    content = TextAreaField(_(u'Comment this shelf'), [
        Required(message=_(u'Required')),
    ], id=u'comment-content')
