# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template

from .models import Bookstore
from ..location.models import City, ip2city

mod = Blueprint('bookstore', __name__)

@mod.route('/')
def home():

    # testcase
    ip = '114.225.152.111'
    #ip = request.remote_addr

    city = ip2city(ip)
    if city:
        bookstores = city.bookstores
    else:
        bookstores = Bookstore.query.all()

    return render_template('bookstore/index.html',
                            bookstores=bookstores,
                            city=city)
