# -*- coding: utf-8 -*-
from flask import Blueprint, request

mod = Blueprint('group', __name__)

@mod.route('/')
def home():

    return 'Group index page.'
