# -*- coding: utf-8 -*-
import os

from flask import Blueprint, current_app, render_template, \
     send_from_directory

from sphinx.websupport import WebSupport

mod = Blueprint('docs', __name__)

@mod.route('/')
@mod.route('/<string:docname>/')
def home(docname='index'):

    support = WebSupport(datadir=current_app.config['DOCS_DATA_DIR'])
    doc = support.get_document(docname)
    print doc['sidebar']

    return render_template('/docs/doc.html', doc=doc)


@mod.route('/static/')
@mod.route('/static/<path:filename>/')
def custom_static(filename=None):

    static_dir = os.path.join(current_app.config['DOCS_DIR'], 'static')
    return send_from_directory(static_dir, filename)
