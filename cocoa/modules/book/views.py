# -*- coding: utf-8 -*-
import math

from PIL import Image

import flask_sijax
from flask import Blueprint, request, render_template, g, \
    redirect, url_for, flash
from flask.ext.login import current_user, login_required
from flask.ext.principal import Permission

from cocoa.permissions import moderator
from .models import Book, BookExtra
from .forms import BookAddForm
from .ajax import AjaxActions
from .helpers import save_cover
from ..tag.models import BookTags
from ..shelf.consts import ColumnType
from ..bookrate.models import BookRate
from ..tag.models import Tag
from ..category.models import Category

mod = Blueprint('book', __name__)

@mod.route('/')
def home():

    recent_books = Book.query.get_recent_books()
    popular_books = BookRate.top_list(10)

    return render_template('book/index.html',
                            recent_books=recent_books,
                            popular_books=popular_books)


@mod.route('/add/', methods=['GET', 'POST'])
@login_required
def add():

    form = BookAddForm(request.form)

    if form.validate_on_submit():
        book = Book(
            form.isbn.data,
            form.title.data,
            form.author.data,
            form.publisher.data,
            form.price.data,
            form.subtitle.data,
            form.orititle.data,
            form.translator.data,
            None,
            form.pubdate.data,
            form.currency.data,
            form.pages.data,
            form.binding.data
        )

        book.extra = BookExtra(form.summary.data, form.author_intro.data)
        book.save()

        # 保存封面图片
        if 'cover' in request.files:
            save_cover(Image.open(request.files['cover']), book)

        return redirect(url_for('book.item', book_id=book.id))

    return render_template('book/add.html', form=form)


BOOKS_PER_PAGE = 10


@mod.route('/all/')
@mod.route('/all/<int:page>/')
def all(page=1):

    total = Book.query.count()

    books = Book.query.paginate(page, BOOKS_PER_PAGE, False).items

    paginate = {
        'total':    int(math.ceil(float(total) / BOOKS_PER_PAGE)),
        'current':  page,
    }

    return render_template('book/all.html', books=books,
                            paginate=paginate)


@mod.route('/categoryview/')
@mod.route('/categoryview/<int:category_id>')
def category_view(category_id=None):
    """按分类展示图书"""

    categories = Category.query.roots()
    target_category = None
    
    if category_id:
        target_category = Category.query.get(category_id)
    return render_template('book/category_view.html',
                            categories=categories,
                            target_category=target_category)


@flask_sijax.route(mod, '/<int:book_id>/')
def item(book_id):

    if g.sijax.is_sijax_request:
        g.sijax.register_object(AjaxActions)
        return g.sijax.process_request()

    book = Book.query.get_or_404(book_id)

    edit_category_perm = Permission(moderator)

    if book.rate:
        book.score = book.rate.total / book.rate.count

    if current_user.is_authenticated():
        book.in_columns, book.not_in_columns = \
            current_user.shelf.query.check_columns(book)

    return render_template('book/item.html', book=book,
                           edit_category_perm=edit_category_perm)
