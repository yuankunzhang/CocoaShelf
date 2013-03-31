# -*- coding: utf-8 -*-
from flask import Blueprint

from .book import book_similarity

mod = Blueprint('recsys', __name__)

@mod.route('/book_similarity')
def calc_book_similarity():

    book_similarity()

    return 'Done!'
