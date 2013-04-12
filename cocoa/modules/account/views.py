# -*- coding: utf-8 -*-
import json

from PIL import Image

import flask_sijax
from flask import Blueprint, request, render_template, session, \
     redirect, url_for, flash, g, jsonify, current_app, abort
from flask.ext.login import login_required, login_user, \
     logout_user, current_user
from flask.ext.babel import gettext as _
from flask.ext.principal import Identity, AnonymousIdentity, \
     identity_changed

from cocoa.permissions import moderator
from .models import User, SignupConfirm
from .forms import SigninForm, SignupForm, SettingsForm, \
        PasswordChangeForm
from .helpers import save_avatar, update_thumbnail, send_confirm_mail
from ..vitality.consts import VitalityTable

mod = Blueprint('account', __name__)

@mod.route('/')
def home():

    return 'home'


@mod.route('/signup/', methods=['GET', 'POST'])
def signup():

    form = SignupForm(request.form)

    # 已登入用户：重定向至首页
    if current_user.is_authenticated():
        return redirect(url_for('frontend.home'))

    if form.validate_on_submit():
        user = User(form.email.data,
                    form.password.data,
                    form.city_id.data)

        user.save()

        # 发送帐号确认邮件
        send_confirm_mail(user)
        return redirect(url_for('account.activate_user', user_id=user.id))

    return render_template('account/signup.html', form=form)


@mod.route('/signin/', methods=['GET', 'POST'])
def signin(next=None):

    form = SigninForm(request.form)
    if request.args.has_key('next'):
        next = request.args['next']

    # 已登入用户：重定向至首页
    if current_user.is_authenticated():
        return redirect(url_for('frontend.home'))

    if form.validate_on_submit():
        user, ok = User.authenticate(form.email.data, form.password.data)

        if ok:
            login_user(user, form.remember.data)
            user.vitality.update(VitalityTable['SIGNIN'])
            # Tell flask-principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            flash(u'登入成功!')
            if next is None:
                next = url_for('shelf.item', shelf_id=user.shelf.id)
            return redirect(next)
        else:
            form.password.errors = (u'密码不正确',)

    return render_template('account/signin.html', form=form, next=next)


@mod.route('/activate/<int:user_id>/')
@mod.route('/activate/<int:user_id>/<string:hashstr>/')
def activate_user(user_id, hashstr=None):

    user = User.query.get_inactive_user(user_id)
    if user is None:
        abort(404)

    if hashstr is None:
        confirm = SignupConfirm.query.get(user_id)
        if confirm is None:
            abort(404)
        else:
            return render_template('account/activate_user.html', user=user)
    else:
        if user.account_confirm(hashstr):
            flash(u'您的帐号已经被激活，请从这里登入.')
            return redirect(url_for('account.signin'))
        else:
            abort(404)


@mod.route('/signout/')
@login_required
def signout():

    logout_user()

    # Remove session keys set by flask-principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    # Tell flask-principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('frontend.home'))


@mod.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():

    form = SettingsForm(request.form, current_user)

    if form.validate_on_submit():
        current_user.update(form.penname.data,
                            form.intro.data,
                            form.gender.data,
                            form.city_id.data)

        flash(u'帐号设置已更新')
        return redirect(url_for('shelf.item',
                                shelf_id=current_user.shelf.id))

    return render_template('account/settings.html', form=form)


@mod.route('/upload_avatar/', methods=['GET', 'POST'])
@login_required
def upload_avatar():

    if request.method == 'POST':
        if 'avatar' not in request.files:
            raise ValueError(_(u'bad request'))

        save_avatar(Image.open(request.files['avatar']))

        file = {
            'files': [{
                'name':     '1.jpg', # TODO
                'size':     1000,    # TODO
                'url':      '/static/upload/avatar/' + current_user.avatar,
                'delete_url':       '',
                'delete_type':      'DELETE',
                'thumbnail_box':    current_user.thumbnail_box,
            }]
        }

        return jsonify(file)

    return render_template('account/upload_avatar.html')


@mod.route('/edit_thumbnail/', methods=['POST'])
@login_required
def edit_thumbnail():

    x1 = int(request.form['x1'])
    y1 = int(request.form['y1'])
    x2 = int(request.form['x2'])
    y2 = int(request.form['y2'])

    box = (x1, y1, x2, y2)
    update_thumbnail(box)

    flash(_(u'Thumbnail updated.'))
    return redirect(url_for('account.settings'))


@mod.route('/change_password/', methods=['GET', 'POST'])
@login_required
def change_password():

    form = PasswordChangeForm(request.form)

    if form.validate_on_submit():
        current_user.update_password(form.old.data, form.new.data)

        flash(_(u'Password changed'))
        return redirect(url_for('account.settings'))

    return render_template('account/change_password.html', form=form)
