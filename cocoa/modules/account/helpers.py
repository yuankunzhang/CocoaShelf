# -*- coding: utf-8 -*-
import os
import time

from PIL import Image

from flask import current_app, url_for
from flask.ext.login import current_user
from flask.ext.mail import Message

from cocoa.extensions import db, sys_mail
from cocoa.helpers.upload import mkdir
from .models import SignupConfirm

FORMAT = 'JPEG'
EXTENSION = '.jpg'
AVATAR_MAX_SIDE_LEN = 200
THUMBNAIL_SIDE_LEN = 60

def save_avatar(img):

    basedir = current_app.config['AVATAR_BASE_DIR']
    folder = None

    # 如果是更新头像，则使用原头像的目录
    # 否则，获取新目录
    if current_user.avatar is not None:
        folder = current_user.avatar.split('/')[0]
    else:
        folder = mkdir(basedir)

    basename = 'u' + str(current_user.id) + '_' + str(int(time.time()))
    avatar_name = basename + EXTENSION
    avatar_path = os.path.join(folder, avatar_name)
    thumbnail_name = basename + '_t' + EXTENSION
    thumbnail_path = os.path.join(folder, thumbnail_name)

    avatar_img = _resize(img)
    thumbnail_img = avatar_img.copy()

    # save avatar image
    avatar_img.save(os.path.join(basedir, avatar_path),
        FORMAT, quality=100)
    #save thumbnail image
    thumbnail_box = _save_thumbnail(thumbnail_img,
        os.path.join(basedir, thumbnail_path))
    
    # delete old avatar
    if current_user.avatar is not None:
        old_avatar = os.path.join(basedir, current_user.avatar)
        old_thumbnail = os.path.join(basedir, current_user.thumbnail)

        if os.path.isfile(old_avatar):
            os.remove(old_avatar)
        if os.path.isfile(old_thumbnail):
            os.remove(old_thumbnail)

    current_user.avatar = avatar_path
    current_user.set_thumbnail_box(thumbnail_box)

    db.session.commit()


def update_thumbnail(thumbnail_box):

    basedir = current_app.config['AVATAR_BASE_DIR']

    if current_user.avatar is None:
        raise ValueError('Action forbidden')

    avatar = os.path.join(basedir, current_user.avatar)
    thumbnail = os.path.join(basedir, current_user.thumbnail)

    img = Image.open(avatar).crop(thumbnail_box)
    _save_thumbnail(img, thumbnail)

    current_user.set_thumbnail_box(thumbnail_box)
    db.session.commit()


def _resize(img):
    """Resize an image"""

    LEN = AVATAR_MAX_SIDE_LEN
    origin_w, origin_h = img.size
    target_w, target_h = img.size

    ratio_w = 1.0 * origin_w / LEN
    ratio_h = 1.0 * origin_h / LEN

    if ratio_w > ratio_h:
        if ratio_w > 1:
            target_w = LEN
            target_h = 1.0 * origin_h // ratio_w
    else:
        if ratio_h > 1:
            target_h = LEN
            target_w = 1.0 * origin_w // ratio_h

    return img.resize((target_w, target_h), Image.ANTIALIAS)


def _save_thumbnail(img, out):
    """Save thumbnail image"""
    
    origin_w, origin_h = img.size
    x = y = 0
    
    # square it!
    ruler = min(AVATAR_MAX_SIDE_LEN, origin_w, origin_h)

    x = origin_w / 2 - ruler / 2;
    y = origin_h / 2 - ruler / 2;

    thumbnail_box = (x, y, x + ruler, y + ruler)

    img.crop(thumbnail_box).\
        resize((THUMBNAIL_SIDE_LEN, THUMBNAIL_SIDE_LEN), Image.ANTIALIAS).\
        save(out, FORMAT, quality=100)

    return thumbnail_box


def send_confirm_mail(user):

    subject = u'确认你的可可帐号!'
    msg = Message(subject=subject,
                  sender=('Cocoa', 'fmcocoa@gmail.com'),
                  recipients=[user.email])

    confirm = SignupConfirm(user)
    confirm.save()
    # 发送确认邮件
    confirm_url = url_for('account.activate_user',
        user_id=user.id, hashstr=confirm.hashstr, _external=True)
    msg.body = u'亲爱的%s, 点击这里确认您的帐号：%s' % \
        (user.display_name, confirm_url)

    sys_mail.send(msg)
