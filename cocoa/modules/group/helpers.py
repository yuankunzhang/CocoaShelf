# -*- coding: utf-8 -*-
import os
import time

from PIL import Image

from flask import current_app

from cocoa.extensions import db
from cocoa.helpers.upload import mkdir

FORMAT = 'JPEG'
EXTENSION = '.jpg'
TOTEM_SIDE_LEN = 60

def save_totem(img, group):

    basedir = current_app.config['TOTEM_BASE_DIR']
    folder = None

    # 如果是更新图腾，则使用原图腾的目录
    # 否则，获取新目录
    if group.totem is not None:
        folder = group.totem.split('/')[0]
    else:
        folder = mkdir(basedir)

    basename = 'g' + str(group.id) + '_' + str(int(time.time()))
    totem_name = basename + EXTENSION
    totem_path = os.path.join(folder, totem_name)

    totem_img = _crop_and_resize(img)

    totem_img.save(os.path.join(basedir, totem_path),
        FORMAT, quality=100)

    if group.totem is not None:
        old_totem = os.path.join(basedir, group.totem)

        if os.path.isfile(old_totem):
            os.remove(old_totem)

    group.totem = totem_path
    db.session.commit()


def _crop_and_resize(img):

    img = img.resize((TOTEM_SIDE_LEN, TOTEM_SIDE_LEN), Image.ANTIALIAS)

    origin_w, origin_h = img.size
    x = y =0

    # square it!
    ruler = min(TOTEM_SIDE_LEN, origin_w, origin_h)

    x = origin_w / 2 - ruler / 2;
    y = origin_h / 2 - ruler / 2;

    box = (x, y, x + ruler, y + ruler)
    return img.crop(box)
