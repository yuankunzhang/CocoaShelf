# -*- coding: utf-8 -*-
"""
    数据库操作脚本
"""
from flask import Blueprint

from cocoa.extensions import db
from cocoa.modules.account.models import User
from cocoa.modules.vitality.models import UserVitality

mod = Blueprint('dbutils', __name__)

@mod.route('/map_user_to_vitality/')
def map_user_to_vitality():

    users = User.query.all()
    for u in users:
        u.vitality = UserVitality()
    db.session.commit()

    return 'Done!'
