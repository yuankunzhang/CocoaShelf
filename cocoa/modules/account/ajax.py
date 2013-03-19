# -*- coding: utf-8 -*-
from PIL import Image

from werkzeug import FileStorage

from flask.ext.uploads import UploadSet, IMAGES

from .helpers import save_avatar

images = UploadSet(u'images', IMAGES)

class AjaxActions(object):

    @staticmethod
    def upload_avatar(obj_response, files, form_values):

        if 'avatar' not in files:
            return u'bad upload'

        avatar = files['avatar']

        if not isinstance(avatar, FileStorage):
            return u'bad upload'

        return

        save_avatar(Image.open(avatar))
