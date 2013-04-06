# -*- coding: utf-8 -*-
import os

from flask import Blueprint, request, jsonify, current_app, \
     render_template
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from cocoa.extensions import album as album_set
from .models import Album

mod = Blueprint('photoalbum', __name__)

@mod.route('/')
def home():

    return 'Photo album index.'


@mod.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():

    if request.method == 'POST':
        if 'photo' not in request.files:
            raise ValueError(_(u'bad request'))
        file = request.files['photo']

        default_album = Album.query.user_default_album(current_user)
        folder = default_album.folder

        src = album_set.save(request.files['photo'], folder)
        filename = src.split('/')[-1]

        default_album.add_photo(filename)

        file = {
            'files': [{
                'name':         filename, # TODO
                'size':         100,      # TODO
                'url':          '/static/upload/album/' + src,
                'delete_url':   '',
                'delete_type':  'DELETE',
            }]
        }

        return jsonify(file)

    return render_template('photoalbum/upload.html')
