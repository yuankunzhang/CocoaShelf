# -*- coding: utf-8 -*-
from datetime import datetime

from jinja2 import Markup
from flask import Blueprint, request, render_template, \
        flash, redirect, url_for, abort, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

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
@mod.route('/prepare_ref_books/<string:id_type>/', methods=['POST'])
def prepare_ref_books(id_type=None):

    book_ids = request.form.getlist('book_ids[]')
    books = []

    for id in book_ids:
        if id_type == 'id':
            book = Book.query.filter_by(id=id).first()
        else:
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
    posts = Post.query.get_published(user_id)

    return render_template('blog/item.html', user=user, posts=posts)


@mod.route('/<int:user_id>/<string:slug>/')
@mod.route('/<int:user_id>/entry/<int:post_id>/')
def entry(user_id, slug):

    post = Post.query.get_by_slug(user_id, slug)
    if post is None:
        abort(404)

    post.previous = Post.query.filter(Post.id<post.id).\
                    order_by(Post.id.desc()).limit(1).first()
    post.next = Post.query.filter(Post.id>post.id).\
                order_by(Post.id).limit(1).first()

    return render_template('blog/entry.html', post=post)


@mod.route('/delete/<int:post_id>/')
@login_required
def delete(post_id):

    post = Post.query.get_or_404(post_id)

    if post.permissions().delete().can():
        post.delete()
        return redirect(url_for('blog.item', user_id=current_user.id))
    else:
        abort(403)


@mod.route('/edit/<int:user_id>/<string:slug>/', methods=['GET', 'POST'])
@login_required
def edit(user_id, slug):

    post = Post.query.get_by_slug(user_id, slug)
    form = PostNewForm(request.form, post)

    if form.validate_on_submit():
        post.update(form.type.data, form.title.data, 
                    form.content.data, form.ref_books.data,
                    form.keywords.data)
        return redirect(url_for('blog.entry', user_id=user_id, slug=slug))

    form.keywords.data = [n.name for n in post.keywords]
    return render_template('blog/edit.html', post=post, form=form)


@mod.route('/keywords/<int:user_id>/')
def keywords(user_id):

    user = User.query.get_or_404(user_id)
    keywords = Post.get_keywords(user_id)

    return render_template('blog/keywords.html', user=user,
                            keywords=keywords)


@mod.route('/keywordposts/<int:user_id>/', methods=['POST'])
def keyword_posts(user_id):

    user = User.query.get_or_404(user_id)
    keyword_id = request.form['keyword_id']
    data = Post.get_keyword_posts(user_id, keyword_id)

    posts = [{
                'id':       p.id,
                'title':    p.title,
                'author':   p.author.get_display_name(),
                'content':  p.content,
                'keywords': [n.name for n in p.keywords],
                'timestamp':datetime.fromtimestamp(p.timestamp).\
                            strftime('%Y-%m-%d %H:%M:%S')
            } for p in data]

    return jsonify(posts=posts)
