# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template

mod = Blueprint('shelf', __name__)

@mod.route('/')
def home():

    return 'library index page.'
