# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from flask.ext.babel import gettext as _

from ..bookrate.models import BookRate
from ..tag.models import Tag
from ..colist.models import Colist
from ..blog.models import Post
from ..shelf.models import Shelf
from ..book.models import Book
from ..group.models import Group
from ..vitality.models import UserVitality
from .consts import SearchType

mod = Blueprint('frontend', __name__)

@mod.route('/')
def home():

    books_top_10 = BookRate.top_list(10)
    tags_top_20 = Tag.top_list(20)
    new_colists = Colist.query.order_by(Colist.timestamp.desc()).all()
    recommended_posts = Post.query.get_recommended_posts(num=5)
    active_users = UserVitality.query.active_users()
    active_groups = Group.query.active_groups()

    # 一些数量的统计
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
                            active_users=active_users,
                            active_groups=active_groups,
                            amount=amount)


@mod.route('/search/', methods=['POST'])
def search():

    q = request.form['q'].strip()
    if q == '':
        raise ValueError(_(u'No query string.'))
    q_str = '%' + q + '%'

    type = SearchType.BOOK
    if 'type' in request.form:
        try:
            type = SearchType.from_int(int(request.form['type']))
        except:
            raise ValueError(_(u'Search type not recognized.'))

    results = []

    if type == SearchType.BOOK:
        results = Book.query.search(q_str)
        template = 'search_book.html'

    return render_template('frontend/'+template, results=results, q=q)
