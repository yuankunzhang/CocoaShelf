# -*- coding: utf-8 -*-
import re
import requests
import time
from datetime import datetime
from os.path import join, dirname
from PIL import Image
from StringIO import StringIO

from flask import Blueprint

from cocoa.modules.book.models import Book, BookExtra

mod = Blueprint('bookutils', __name__)

_basedir = dirname(__file__)

@mod.route('/grab_douban/')
def grab_douban():
    """从豆瓣抓取数据"""

    SLEEP_TIME = 11

    # 计数器文件
    counter_file = open(join(_basedir, 'counter.txt'), 'r+')
    counter = int(counter_file.readline()) or 1
    # 索引文件
    index_file = open(join(_basedir, 'records.txt'), 'r')

    douban_api_url_base = 'https://api.douban.com/v2/book/isbn/'

    line = 1
    while (True):
        if line == counter: break
        index_file.readline()
        line += 1

    for line in iter(index_file.readline, b''):
        # 从Amazon获取isbn13
        re_isbn13 = '.*(978\d{10}).*'
        req = requests.get(line)
        if req.status_code != requests.codes.ok:
            counter += 1
            continue

        html_amazon = req.text
        m = re.search(re_isbn13, html_amazon)
        if m is None:
            counter += 1
            continue
        else:
            isbn13 = m.group(1)

        book = Book.query.filter_by(isbn13=isbn13).first()
        if book is not None:
            counter += 1
            continue

        douban_api_url = douban_api_url_base + isbn13
        print douban_api_url

        req = requests.get(douban_api_url)
        if req.status_code != requests.codes.ok:
            counter += 1
            continue

        data = req.json()
        if 'code' in data and data['code'] == 6000:
            counter += 1
            continue

        isbn = data['isbn13']
        title = data['title']
        subtitle = data['subtitle']
        orititle = data['origin_title']

        author = data['author']
        translator = data['translator']
        publisher = data['publisher']
        pubdate = data['pubdate']
        price = data['price']
        binding = data['binding']

        pages = data['pages']

        author_intro = data['author_intro']
        summary = data['summary']

        book = Book(isbn, title, author, publisher,
                    price, subtitle, orititle,
                    translator, pubdate=pubdate,
                    pages=pages, binding=binding)
        book.extra = BookExtra(summary, author_intro)

        try:
            book.save()
        except ValueError:
            counter += 1
            continue

        # 抓取封面
        img_src = data['images']['large'].replace('\\', '')
        img = requests.get(img_src)

        if img.status_code == requests.codes.ok:
            book.save_cover(Image.open(StringIO(img.content)))

        counter += 1
        counter_file.seek(0)
        counter_file.write(str(counter) + '\n')

        time.sleep(SLEEP_TIME)

    counter_file.close()
    index_file.close()
    return 'Done!'
