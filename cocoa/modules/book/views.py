# -*- coding: utf-8 -*-
import flask_sijax
from flask import Blueprint, request, render_template, g, \
    redirect, url_for, flash
from flask.ext.login import current_user, login_required

from .models import Book
from ..tag.models import BookTags

mod = Blueprint('book', __name__)

@mod.route('/')
def home():

    books = Book.query.order_by(Book.pubdate.desc()).all()
    return render_template('book/index.html', books=books)


@flask_sijax.route(mod, '/<book_id>/')
def item(book_id):

    book = Book.query.get_or_404(book_id)
    print book.extra.summary.__repr__()
    return render_template('book/item.html', book=book)
