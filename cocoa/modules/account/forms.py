# -*- coding: utf-8 -*-
from flask.ext.login import current_user
from flask.ext.babel import gettext as _
from flask.ext.wtf import TextField, TextAreaField, \
    BooleanField, PasswordField, HiddenField, FileField,  \
    RadioField, Required, Email, EqualTo, Regexp, Length, \
    ValidationError

from cocoa.helpers.form import Form
from .consts import UserConst as C
from .models import User

class SigninForm(Form):

    email = TextField(_('Email'), [
        Required(message=_('Required')),
        Email(message=_('Invalid email address')),
    ], id='signin-email')

    password = PasswordField(_('Password'), [
        Required(message=_('Required')),
    ], id='signin-password')

    remember = BooleanField(_('Remember me'),
        id='signin-remember')


def user_not_exist():

    message = _('This email address has been signed up.')

    def _check(form, field):
        u = User.query.filter_by(email=field.data).first()
        if u is not None:
            raise ValidationError(message)

    return _check


class SignupForm(Form):

    email = TextField(_('Email'), [
        Required(message=_('Required')),
        Email(message=_('Invalid email address')),
        user_not_exist(),
    ], id='signup-email')

    password = PasswordField(_('Password'), [
        Required(message=_('Required')),
        # TODO length check
    ], id='signup-password')

    confirm = PasswordField(_('Confirm Password'), [
        Required(message=_('Required')),
        EqualTo('password', message=_('Doesn\'t match to your password')),
    ], id='signup-confirm')

    city_id = HiddenField()
