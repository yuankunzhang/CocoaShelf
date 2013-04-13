# -*- coding: utf-8 -*-
import os
import time

from PIL import Image

from flask import current_app

from cocoa.extensions import db
from cocoa.helpers.upload import mkdir

FORMAT = 'JPEG'
EXTENSION = '.jpg'

def isbn10_to_13(isbn10):

    isbn13 = '978' + isbn10[:-1]
    r = sum(int(x) * weight for x, weight in zip(isbn13, (1, 3) * 6))
    chksum = (10 - r % 10) % 10
    return isbn13 + str(chksum)


def isbn13_to_10(isbn13):

    isbn10 = isbn13[3:12]
    r = sum((10 - i) * (int(x) if x != 'X' else 10) \
        for i, x in enumerate(isbn10) if i != 9)
    chksum = (11 - r % 11) % 11
    return isbn10 + str(chksum)


def save_cover(img, book):

    basedir = current_app.config['COVER_BASE_DIR']
    folder = mkdir(basedir)

    basename = 'b' + str(book.id) + '_' + str(int(time.time()))
    cover_name = basename + EXTENSION
    cover_path = os.path.join(folder, cover_name)

    img.save(os.path.join(basedir, cover_path), FORMAT, quality=100)

    book.cover = cover_path
    db.session.commit()
