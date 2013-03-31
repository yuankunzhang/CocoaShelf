# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from ..bookrate.models import BookRate
from ..tag.models import Tag
from ..colist.models import Colist
from ..blog.models import Post
from ..shelf.models import Shelf
from ..book.models import Book

mod = Blueprint('frontend', __name__)

@mod.route('/')
def home():

    books_top_10 = BookRate.top_list(10)
    tags_top_20 = Tag.top_list(20)
    new_colists = Colist.query.order_by(Colist.timestamp.desc()).all()
    recommended_posts = Post.query.get_recommended_posts(num=5)

    amount = {
        'shelf':    Shelf.query.count(),
        'book':     Book.query.count(),
        'tag':      Tag.query.count(), 
        'colist':   Colist.query.count(),
    }

    return render_template('frontend/index.html',
                            books_top_10=books_top_10,
                            tags_top_20=tags_top_20,
                            new_colists=new_colists,
                            recommended_posts=recommended_posts,
                            amount=amount)
