# -*- coding: utf-8 -*-
import flask_sijax
from flask import Blueprint, request, render_template, g, \
    redirect, url_for, flash
from flask.ext.login import current_user, login_required

from .models import Book
from .ajax import AjaxActions
from ..tag.models import BookTags
from ..shelf.consts import ColumnType

mod = Blueprint('book', __name__)

@mod.route('/')
def home():

    books = Book.query.order_by(Book.pubdate.desc()).all()
    return render_template('book/index.html', books=books)


@flask_sijax.route(mod, '/<book_id>/')
def item(book_id):

    if g.sijax.is_sijax_request:
        g.sijax.register_object(AjaxActions)
        return g.sijax.process_request()

    book = Book.query.get_or_404(book_id)

    if book.rate:
        book.score = book.rate.total / book.rate.count

    if current_user.is_authenticated():
        book.in_columns, book.not_in_columns = \
            current_user.shelf.query.check_columns(book)

    return render_template('book/item.html', book=book)
