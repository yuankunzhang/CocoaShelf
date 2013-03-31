# -*- coding: utf-8 -*-
import math

import flask_sijax
from flask import Blueprint, request, render_template, g, \
    redirect, url_for, flash
from flask.ext.login import current_user, login_required
from flask.ext.principal import Permission

from cocoa.permissions import moderator
from cocoa.extensions import cache
from .models import Book
from .ajax import AjaxActions
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
@cache.cached(timeout=60)
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
