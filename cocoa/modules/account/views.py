# -*- coding: utf-8 -*-
import json

from PIL import Image

import flask_sijax
from flask import Blueprint, request, render_template, \
        redirect, url_for, flash, g, jsonify
from flask.ext.login import login_required, login_user, \
        logout_user, current_user
from flask.ext.babel import gettext as _

from .models import User
from .forms import SigninForm, SignupForm, SettingsForm, \
        PasswordChangeForm
from .helpers import save_avatar, update_thumbnail
from .ajax import AjaxActions

mod = Blueprint('account', __name__)

@mod.route('/')
def home():

    return 'home'


@mod.route('/signup/', methods=['GET', 'POST'])
def signup():

    form = SignupForm(request.form)

    if current_user.is_authenticated():
        return redirect(url_for('frontend.home'))

    if form.validate_on_submit():
        user = User(form.email.data,
                    form.password.data,
                    form.city_id.data)

        user.save()
        
        login_user(user)
        flash(_(u'Successfully signed up.'))
        return redirect(url_for('account.settings', user_id=user.id))

    return render_template('account/signup.html', form=form)


@mod.route('/signin/', methods=['GET', 'POST'])
def signin(next=None):

    form = SigninForm(request.form)
    if request.args.has_key('next'):
        next = request.args['next']

    if current_user.is_authenticated():
        return redirect(url_for('frontend.home'))

    if form.validate_on_submit():
        user, ok = User.authenticate(form.email.data, form.password.data)

        if ok:
            login_user(user, form.remember.data)
            flash(_('Successfully signed in.'))
            next = url_for('shelf.item', shelf_id=user.shelf.id)
            return redirect(next)

    return render_template('account/signin.html', form=form, next=next)


@mod.route('/signout/')
@login_required
def signout():

    logout_user()
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

        flash(_(u'Settings updated'))
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
            'file': {
                'name':     '1.jpg',
                'size':     1000,
                'url':      '/static/upload/avatar/' + current_user.avatar,
                'delete_url':       '',
                'delete_type':      'DELETE',
                'thumbnail_box':    current_user.thumbnail_box,
            },
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
