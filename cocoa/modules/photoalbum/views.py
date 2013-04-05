# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, current_app, \
     render_template
from flask.ext.login import login_required
from flask.ext.babel import gettext as _
from flask.ext.uploads import UploadSet, IMAGES

from cocoa.helpers.upload import mkdir
from cocoa.extensions import album

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

        folder = mkdir(album.config.destination)

        filename = album.save(request.files['photo'], folder)
        print filename

        return 'Photo upload.'

    return render_template('photoalbum/upload.html')
