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
    ], id='group-intro')


class TopicNewForm(Form):

    title = TextField(_(u'Topic title'), [
        Required(message=_(u'Required'))
    ], id=u'topic-title')


class ReplyForm(Form):

    content = TextAreaField(_(u'Reply'), [
        Required(message=_(u'Required'))
    ], id=u'reply-content')
