# -*- coding: utf-8 -*-
from datetime import datetime

import flask_sijax
from flask import Blueprint, request, render_template, \
    g, redirect, url_for, flash, jsonify, abort
from flask.ext.login import current_user, login_required

from .models import Shelf, ColumnReading
from .consts import ColumnType
from .ajax import AjaxActions
from ..book.models import Book

mod = Blueprint('shelf', __name__)

@mod.route('/')
def home():

    return 'Shelf index page.'


@mod.route('/<int:shelf_id>/')
def item(shelf_id):

    shelf = _get_shelf(shelf_id)
    return render_template('shelf/details.html', shelf=shelf)


@flask_sijax.route(mod, '/<int:shelf_id>/<string:column_name>/')
def column(shelf_id, column_name):

    if g.sijax.is_sijax_request:
        g.sijax.register_object(AjaxActions)
        return g.sijax.process_request()

    shelf = _get_shelf(shelf_id)
    column = ColumnType.from_name(column_name)
    books = column.class_.get_books(shelf)

    return render_template('shelf/' + column_name + '.html',
                           shelf=shelf, column=column, books=books)


@mod.route('/<int:shelf_id>/<string:column_name>/addbooks/',
    methods=['GET', 'POST'])
def add_books(shelf_id, column_name):

    shelf = _get_shelf(shelf_id)
    column = ColumnType.from_name(column_name)

    if request.method == 'POST':
        book_ids = request.form.getlist('book_ids')
        for b_id in book_ids:
            book = Book.query.filter_by(isbn13=b_id).first()
            if book is not None:
                shelf.add_book(book, (column_name,))

        flash(u'Added books to shelf.')
        return redirect(url_for('shelf.column', shelf_id=shelf_id,
                                column_name=column_name))

    return render_template('shelf/add_books.html',
                           shelf=shelf, column=column)


@mod.route('/<int:shelf_id>/readingplan/')
def reading_plan(shelf_id):

    shelf = _get_shelf(shelf_id)
    return render_template('shelf/reading_plan.html', shelf=shelf)


@mod.route('/<int:shelf_id>/readingplan_data/')
def reading_plan_data(shelf_id):

    shelf = _get_shelf(shelf_id)

    books = ColumnReading.get_finished_books(shelf)
    data = [{
        'startDate':    datetime.fromtimestamp(int(book['timestamp'])) \
                        .strftime('%Y,%m,%d'),
        'endDate':      datetime.fromtimestamp(int(
                        book['finished_timestamp'])).strftime('%Y,%m,%d'),
        'headline':     book['title'],
        'text':         book['summary'],
        'assert':       {
            'media':    '/static/upload/cover/' + book['cover'],
            'credit':   '',
            'caption':  '',
        },
    } for book in books]

    timeline = {
        'timeline': {
            'type': 'default',
            'date': data,
        },
    }

    return jsonify(timeline)


def _get_shelf(shelf_id):

    if shelf_id is not None:
        shelf = Shelf.query.get_or_404(shelf_id)
    else:
        abort(404)

    return shelf
