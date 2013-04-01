# -*- coding: utf-8 -*-
# 用户活跃度
from flask import Blueprint
from flask.ext.login import current_user

mod = Blueprint('vitality', __name__)

@mod.route('/')
def home():

    current_user.vitality.update(2)

    return 'abc'
