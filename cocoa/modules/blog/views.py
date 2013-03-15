# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, \
    flash, redirect, url_for
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from .models import Post
from .forms import PostNewForm

mod = Blueprint('blog', __name__)

@mod.route('/')
def home():

    posts = Post.query.filter_by(author=current_user) \
            .order_by(Post.id.desc()).all()
    return render_template('blog/index.html', posts=posts)


@mod.route('/new/', methods=['GET', 'POST'])
@mod.route('/new/<ref_book_id>', methods=['GET', 'POST'])
@login_required
def new(ref_book_id=None):

    form = PostNewForm(request.form)
    if ref_book_id is not None:
        form.ref_books.data = (ref_book_id,)

    if form.validate_on_submit():
        post = Post(form.type.data, form.title.data, 
                    form.content.data, form.ref_books.data)
        post.save()

        flash(_(u'Published new post.'))
        return redirect(url_for('blog.home'))

    return render_template('blog/new.html', form=form)
