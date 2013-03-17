# -*- coding: utf-8 -*-
from flask import Blueprint

mod = Blueprint('bookstore', __name__)

@mod.route('/')
def home():

    return 'Bookstore index page.'
