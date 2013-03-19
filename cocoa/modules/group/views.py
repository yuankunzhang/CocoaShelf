# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, \
        redirect, url_for
from flask.ext.login import current_user, login_required

from .forms import GroupNewForm
from .models import Group

mod = Blueprint('group', __name__)

@mod.route('/')
def home():

    groups = current_user.groups
    return render_template('group/index.html', groups=groups)


@mod.route('/new/', methods=['GET', 'POST'])
@login_required
def new():

    form = GroupNewForm(request.form)

    if form.validate_on_submit():
        group = Group(form.name.data, form.intro.data, current_user)
        group.save()

        return redirect(url_for('group.home'))

    return render_template('group/new.html', form=form)


@mod.route('/<group_id>/')
def item(group_id):

    group = Group.query.get(group_id)
    return render_template('group/item.html', group=group)
