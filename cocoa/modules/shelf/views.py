# -*- coding: utf-8 -*-
import flask_sijax
from flask import Blueprint, request, render_template, abort, g
from flask.ext.login import current_user, login_required

from .models import Shelf
from .ajax import AjaxActions

mod = Blueprint('shelf', __name__)

@mod.route('/')
def home():

    return 'Shelf index page.'


@mod.route('/<int:shelf_id>/')
def item(shelf_id=None):

    shelf = _get_shelf(shelf_id)
    return render_template('shelf/details.html', shelf=shelf)


@flask_sijax.route(mod, '/<int:shelf_id>/<string:column_type>/')
def column(column_type, shelf_id=None):

    if g.sijax.is_sijax_request:
        g.sijax.register_object(AjaxActions)
        return g.sijax.process_request()

    shelf = _get_shelf(shelf_id)
    if column_type not in ('have', 'read', 'reading', 'wish', 'like'):
        abort(404)
    return render_template('shelf/'+column_type+'.html', shelf=shelf)


def _get_shelf(shelf_id=None):

    if shelf_id is None and current_user.is_authenticated():
        shelf = current_user.shelf
    elif shelf_id is not None:
        shelf = Shelf.query.get_or_404(shelf_id)
    else:
        abort(404)

    return shelf
