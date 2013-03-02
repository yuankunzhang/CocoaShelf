# -*- coding: utf-8 -*-
import json

from PIL import Image

from flask import Blueprint, request, render_template, \
    redirect, url_for, flash
from flask.ext.login import login_required, login_user, \
    logout_user, current_user
from flask.ext.babel import gettext as _

from .models import User
from .forms import SigninForm, SignupForm

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
