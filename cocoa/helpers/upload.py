# -*- coding: utf-8 -*-
import os
from time import time

from flask import current_app

def mkdir(basedir):

    if not os.path.exists(basedir):
        os.makedirs(basedir)

    FILES_PER_DIR = current_app.config['FILES_PER_DIR']
    sub_dirs = [x for x in os.listdir(basedir) \
                if os.path.isdir(os.path.join(basedir, x))]
    folder = None
    path = None

    if len(sub_dirs) != 0:
        sub_dirs.sort()
        folder = sub_dirs[-1]
        path = os.path.join(basedir, folder)
        file_num = len(os.listdir(path))

    if len(sub_dirs) == 0 or file_num >= FILES_PER_DIR:
        folder = str(int(time()))
        path = os.path.join(basedir, folder)

        os.makedirs(path)

    return folder
