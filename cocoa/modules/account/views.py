# -*- coding: utf-8 -*-
import json

from PIL import Image

from flask import Blueprint, request, render_template, \
    redirect, url_for, flash
from flask.ext.login import login_required, login_user, \
    logout_user, current_user
from flask.ext.babel import gettext as _

from .models import User
from .forms import SigninForm, SignupForm, SettingsForm, \
    AvatarUploadForm, PasswordChangeForm
from .helpers import save_avatar, update_thumbnail

mod = Blueprint('account', __name__)

@mod.route('/')
def home():

    return 'home'


@mod.route('/signup/', methods=['GET', 'POST'])
def signup(next=None):

    form = SignupForm(request.form)
    next = next or url_for('account.home')

    if current_user.is_authenticated():
        return redirect(next)

    if form.validate_on_submit():
        user = User(form.email.data,
                    form.password.data,
                    form.city_id.data)

        user.save()
        
        login_user(user)
        flash(_(u'Successfully signed up.'))
        return redirect(next)

    return render_template('account/signup.html', form=form)


@mod.route('/signin/', methods=['GET', 'POST'])
def signin(next=None):

    form = SigninForm(request.form)
    next = next or url_for('account.home')

    if current_user.is_authenticated():
        return redirect(next)

    if form.validate_on_submit():
        user, flag = User.authenticate(form.email.data, form.password.data)

        if flag:
            login_user(user, form.remember.data)
            flash(_('Successfully signed in.'))
            return redirect(next)

    return render_template('account/signin.html', form=form)


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
        return redirect(url_for('account.settings'))

    return render_template('account/settings.html', form=form)


@mod.route('/upload_avatar/', methods=['GET', 'POST'])
@login_required
def upload_avatar():

    form = AvatarUploadForm(request.form)

    if form.validate_on_submit():
        save_avatar(Image.open(request.files['avatar']))
        flash(_(u'Avatar uploaded successfully.'))

    return render_template('account/upload_avatar.html', form=form)


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
