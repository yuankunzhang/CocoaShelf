# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template

mod = Blueprint('mail', __name__)

@mod.route('/')
def home():

    return 'mail index page.'
