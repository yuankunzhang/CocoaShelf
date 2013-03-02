# -*- coding: utf-8 -*-
import json

from PIL import Image

from flask import Blueprint, request, render_template, \
    redirect, url_for, flash
from flask.ext.login import login_required, login_user, \
    current_user

mod = Blueprint('account', __name__)

@mod.route('/')
def home():

    return 'home'


@mod.route('/signin/')
def signin(next=None):

    return 'signin'


@mod.route('/signup/')
def signup(next=None):

    return 'signup'


@mod.route('/signout/')
@login_required
def signout():

    return 'signout'
