# -*- coding: utf-8 -*-
import json

from flask import Blueprint, render_template, flash, \
    url_for, redirect
from flask.ext.babel import gettext as _

from cocoa.permissions import moderator
from ..book.models import Book
from .models import Category

mod = Blueprint('category', __name__)

@mod.route('/')
@moderator.require(403)
def home():

    return render_template('index.html')

@mod.route('/change_category/<int:book_id>/')
@mod.route('/change_category/<int:book_id>/<int:category_id>')
def change_category(book_id, category_id=None):

    book = Book.query.get(book_id)

    if category_id is not None:
        category = Category.query.get_or_404(category_id)
        book.set_category(category)
        flash(_(u'Changed book category'))
        return redirect(url_for('book.item', book_id=book_id))

    categories = Category.as_list(parent_id=category_id)
    return render_template('category/change_category.html',
                           book=book, categories=categories)


@mod.route('/categories/<int:parent_id>/', methods=['POST'])
@moderator.require(403)
def categories(parent_id):
    print parent_id

    return json.dumps(Category.as_list(parent_id))
