# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, \
        redirect, url_for
from flask.ext.login import current_user, login_required

from .forms import GroupNewForm, TopicNewForm, ReplyForm
from .models import Group, GroupTopics

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


@mod.route('/<int:group_id>/')
def item(group_id):

    group = Group.query.get_or_404(group_id)
    return render_template('group/item.html', group=group)


@mod.route('/<int:group_id>/newtopic/', methods=['GET', 'POST'])
@login_required
def new_topic(group_id):

    group = Group.query.get_or_404(group_id)
    form = TopicNewForm(request.form)

    if form.validate_on_submit():
        group.new_topic(form.title.data)

        return redirect(url_for('group.item', group_id=group_id))

    return render_template('group/new_topic.html',
                           group=group, form=form)


@mod.route('/<int:group_id>/topic/<int:topic_id>/')
def topic(group_id, topic_id):

    group = Group.query.get_or_404(group_id)
    topic = GroupTopics.query.get_or_404(topic_id)
    form = ReplyForm(request.form)

    return render_template('group/topic.html',
                           group=group, topic=topic, form=form)


@mod.route('/<int:group_id>/replytopic/<int:topic_id>/', methods=['POST'])
@login_required
def reply_topic(group_id, topic_id):

    topic = GroupTopics.query.get_or_404(topic_id)
    form = ReplyForm(request.form)

    if form.validate_on_submit():
        topic.reply(form.content.data)

        return redirect(url_for('group.topic',
                                group_id=group_id,
                                topic_id=topic_id))
