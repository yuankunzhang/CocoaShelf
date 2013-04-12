# -*- coding: utf-8 -*-
from flask.ext.login import current_user
#from flask.ext.babel import gettext as _
from flask.ext.wtf import TextField, TextAreaField, \
     BooleanField, PasswordField, HiddenField, FileField, \
     RadioField, Required, Email, EqualTo, ValidationError, \
     Length, RecaptchaField, Recaptcha

from cocoa.helpers.wtf import Form
from .models import User
from .consts import Gender

class SigninForm(Form):

    email = TextField(u'邮箱', [
        Required(message=u'必填'),
        Email(message=u'请使用正确的邮箱地址'),
    ], id=u'signin-email')

    password = PasswordField(u'密码', [
        Required(message=u'必填'),
    ], id=u'signin-password')

    remember = BooleanField(u'记住我', [
    ], id=u'signin-remember')


def user_not_exist():

    message = u'该邮箱地址已被注册'

    def _check(form, field):
        u = User.query.filter_by(email=field.data).first()
        if u is not None:
            raise ValidationError(message)

    return _check


class SignupForm(Form):

    email = TextField(u'邮箱', [
        Required(message=u'必填'),
        Email(message=u'请使用正确的邮箱地址'),
        user_not_exist(),
    ], id=u'signup-email')

    password = PasswordField(u'密码', [
        Required(message=u'必填'),
        Length(min=6, message=u'密码长度不少于6位'),
    ], id=u'signup-password')

    confirm = PasswordField(u'确认密码', [
        Required(message=u'必填'),
        EqualTo('password', message=u'两次输入的密码不匹配'),
    ], id=u'signup-confirm')

    city_id = HiddenField()

    recaptcha = RecaptchaField('', [
        Recaptcha(message=u'验证码不正确'),
    ])


class SettingsForm(Form):

    penname = TextField(u'笔名', [
        Required(message=u'必填'),
        Length(min=6, message=u'长度不少于6位'),
    ], id=u'settings-penname')

    intro = TextAreaField(u'个人简介', [
    ], id=u'settings-intro')

    gender = RadioField(u'性别',
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

    message = u'密码错误'

    def _check(form, field):
        if not current_user.check_password(field.data):
            raise ValidationError(message)

    return _check


class PasswordChangeForm(Form):

    old = PasswordField(u'原密码', [
        Required(message=u'必填'),
        Length(min=6, message=u'密码长度不少于6位'),
        old_password_ok()
    ], id=u'old-password')

    new = PasswordField(u'新密码', [
        Required(message=u'必填'),
        Length(min=6, message=u'长度不少于6位'),
    ], id=u'new-password')

    confirm = PasswordField(u'确认密码', [
        Required(message=u'必填'),
        EqualTo(u'new', message=u'两次输入不匹配'),
    ], id=u'confirm')
