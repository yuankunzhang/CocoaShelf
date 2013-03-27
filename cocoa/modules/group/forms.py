# -*- coding: utf-8 -*-
from flask.ext.wtf import TextField, TextAreaField, FileField, \
        Required, ValidationError
from flask.ext.babel import gettext as _

from cocoa.helpers.wtf import Form
from .models import Group

def group_not_exist():

    message = _(u'This group name has been used.')

    def _check(form, field):
        group =Group.query.filter_by(name=field.data).first()
        if group is not None:
            raise ValidationError(message)

    return _check


class GroupNewForm(Form):

    name = TextField(_(u'Group Name'), [
        Required(message=_(u'Required')),
        group_not_exist()
    ], id=u'group-name')

    intro = TextAreaField(_(u'Group Introduction'), [
        Required(message=_(u'Required'))
    ], id='group-intro')

    totem = FileField(_(u'Totem'), [
    ], id='group-totem')


class TopicNewForm(Form):

    title = TextField(_(u'Topic title'), [
        Required(message=_(u'Required'))
    ], id=u'topic-title')


class ReplyForm(Form):

    content = TextAreaField(_(u'Reply'), [
        Required(message=_(u'Required'))
    ], id=u'reply-content')
