# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from ..bookrate.models import BookRate
from ..tag.models import Tag
from ..colist.models import Colist

mod = Blueprint('frontend', __name__)

@mod.route('/')
def home():

    from ..recsys.tag import tag_similarity
    tag_similarity()

    books_top_10 = BookRate.top_list(10)
    tags_top_20 = Tag.top_list(20)
    new_colists = Colist.query.order_by(Colist.timestamp.desc()).all()

    return render_template('frontend/index.html',
                            books_top_10=books_top_10,
                            tags_top_20=tags_top_20,
                            new_colists=new_colists)
