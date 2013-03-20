# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, \
        abort, redirect, url_for
from flask.ext.login import current_user, login_required

from .models import Mail, MailInbox
from .forms import MailNewForm
from ..account.models import User

mod = Blueprint('mail', __name__)

@mod.route('/')
def home():

    return 'mail index page.'


@mod.route('/new/<int:to_user_id>/', methods=['GET', 'POST'])
@mod.route('/new/<int:to_user_id>/<int:parent_id>/',
        methods=['GET', 'POST'])
@login_required
def new(to_user_id, parent_id=None):

    # 不能给自己写信
    if to_user_id == current_user.id:
        abort(404)

    to_user = User.query.get_or_404(to_user_id)
    form = MailNewForm(request.form)
    if parent_id is not None:
        form.parent_id.data = parent_id

    if form.validate_on_submit():
        Mail.send(current_user, to_user, form.parent_id.data,
                  form.title.data, form.content.data)
        return redirect(url_for('mail.home'))

    return render_template('mail/new.html', form=form, to_user=to_user)


@mod.route('/inbox/')
@login_required
def inbox():

    mail_thumb = current_user.inbox
    return render_template('mail/inbox.html', mail_thumb=mail_thumb)

@mod.route('/<int:mail_thumb_id>/')
@login_required
def item(mail_thumb_id):

    mail_thumb = MailInbox.query.get_or_404(mail_thumb_id)
    if mail_thumb.user.id != current_user.id:
        abort(404)

    if mail_thumb.unread:
        mail_thumb.read()

    mail = mail_thumb.mail
    return render_template('mail/item.html', mail=mail)
