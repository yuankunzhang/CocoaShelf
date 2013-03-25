# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, \
        flash, redirect, url_for, abort, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _
from flask.ext.principal import Permission, UserNeed

from cocoa.permissions import moderator
from .models import Post
from .forms import PostNewForm
from ..account.models import User
from ..book.models import Book

mod = Blueprint('blog', __name__)

@mod.route('/')
def home():

    posts = Post.query.filter_by(author=current_user) \
            .order_by(Post.id.desc()).all()
    return render_template('blog/index.html', posts=posts)


@mod.route('/new/', methods=['GET', 'POST'])
@mod.route('/new/<ref_book_id>/', methods=['GET', 'POST'])
@login_required
def new(ref_book_id=None):

    form = PostNewForm(request.form)
    if ref_book_id is not None:
        form.ref_books.data = (ref_book_id,)

    if form.validate_on_submit():
        post = Post(form.type.data, form.title.data, 
                    form.content.data, form.ref_books.data,
                    form.keywords.data)
        post.save()

        flash(_(u'Published new post.'))
        return redirect(url_for('blog.home'))

    return render_template('blog/new.html', form=form)


@mod.route('/prepare_ref_books/', methods=['POST'])
def prepare_ref_books():

    book_ids = request.form.getlist('book_ids[]')
    books = []

    for id in book_ids:
        book = Book.query.filter_by(isbn13=id).first()
        if book:
            books.append(book)

    books = [
        {
            'title':    b.title,
            'id':       b.id,
            'isbn13':   b.isbn13,
            'author':   ', '.join(b.author),
        } for b in books
    ]

    return jsonify(books=books)


@mod.route('/<int:user_id>/')
def item(user_id):

    user = User.query.get_or_404(user_id)

    perms = {
        'edit_perm':    Permission(UserNeed(user_id)),
        'delete_perm':  Permission(UserNeed(user_id)) & moderator,
    }

    return render_template('blog/item.html', user=user, perms=perms)


@mod.route('/<int:user_id>/<string:slug>/')
@mod.route('/<int:user_id>/entry/<int:post_id>/')
def entry(user_id, slug):

    post = Post.get_by_slug(user_id, slug)
    if post is None:
        abort(404)

    perms = {
        'edit_perm':    Permission(UserNeed(user_id)),
        'delete_perm':  Permission(UserNeed(user_id)) & moderator,
    }

    post.previous = Post.query.filter(Post.id<post.id).\
                    order_by(Post.id.desc()).limit(1).first()
    post.next = Post.query.filter(Post.id>post.id).\
                order_by(Post.id).limit(1).first()

    return render_template('blog/entry.html', post=post,
                            perms=perms)
