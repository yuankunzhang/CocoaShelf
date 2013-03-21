# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from .models import Tag

mod = Blueprint('tag', __name__)

@mod.route('/')
def home():

    return render_template('index.html')


@mod.route('/<int:tag_id>/')
def item(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag/item.html', tag=tag)
