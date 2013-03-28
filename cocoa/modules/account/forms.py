# -*- coding: utf-8 -*-
from flask.ext.login import current_user
from flask.ext.babel import gettext as _
#from flask.ext.uploads import UploadSet, IMAGES
from flask.ext.wtf import TextField, TextAreaField, \
    BooleanField, PasswordField, HiddenField, FileField, \
    RadioField, Required, Email, EqualTo, ValidationError

from cocoa.helpers.wtf import Form
from .models import User
from .consts import Gender

class SigninForm(Form):

    email = TextField(_(u'Email'), [
        Required(message=_(u'Required')),
        Email(message=_(u'Invalid email address')),
    ], id=u'signin-email')

    password = PasswordField(_(u'Password'), [
        Required(message=_(u'Required')),
    ], id=u'signin-password')

    remember = BooleanField(_(u'Remember me'), [
    ], id=u'signin-remember')


def user_not_exist():

    message = _(u'This email address has been signed up.')

    def _check(form, field):
        u = User.query.filter_by(email=field.data).first()
        if u is not None:
            raise ValidationError(message)

    return _check


class SignupForm(Form):

    email = TextField(_(u'Email'), [
        Required(message=_(u'Required')),
        Email(message=_(u'Invalid email address')),
        user_not_exist(),
    ], id=u'signup-email')

    password = PasswordField(_(u'Password'), [
        Required(message=_(u'Required')),
        # TODO length check
    ], id=u'signup-password')

    confirm = PasswordField(_(u'Confirm Password'), [
        Required(message=_(u'Required')),
        EqualTo('password', message=_(u'Doesn\'t match to your password')),
    ], id=u'signup-confirm')

    city_id = HiddenField()


class SettingsForm(Form):

    penname = TextField(_(u'Pen name'), [
        Required(message=_(u'Required')),
        # TODO
        # length requirements
    ], id=u'settings-penname')

    intro = TextAreaField(_(u'Introduction'), [
    ], id=u'settings-intro')

    gender = RadioField(_(u'Gender'),
        choices=[
            (Gender.SECRET.value, Gender.SECRET.text),
            (Gender.MALE.value, Gender.MALE.text),
            (Gender.FEMALE.value, Gender.FEMALE.text),
        ],
        coerce=int, id=u'settings-gender'
    )

    city_id = HiddenField()


"""
class AvatarUploadForm(Form):

    avatar = FileField(_(u'Upload avatar'), [
        FileRequired(message=_(u'No file')),
        FileAllowed(UploadSet('images', IMAGES), _(u'Images only!'))
    ], id=u'avatar')
"""


def old_password_ok():

    message = _(u'Wrong password')

    def _check(form, field):
        if not current_user.check_password(field.data):
            raise ValidationError(message)

    return _check


class PasswordChangeForm(Form):

    old = PasswordField(_(u'Old password'), [
        Required(message=_(u'Required')),
        # TODO
        #Length(min=6, message=u'长度最少6位'),
        old_password_ok()
    ], id=u'old-password')

    new = PasswordField(_(u'New password'), [
        Required(message=_(u'Required')),
        # TODO
        #Length(min=5, messsage=u'长度最少6位'),
    ], id=u'new-password')

    confirm = PasswordField(_(u'Confirm'), [
        Required(message=_(u'Required')),
        EqualTo(u'new', message=_(u'Not match')),
    ], id=u'confirm')
