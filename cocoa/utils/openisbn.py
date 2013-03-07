# -*- coding: utf-8 -*-
import re
from os.path import join, dirname
from urllib2 import urlopen, URLError

from bs4 import BeautifulSoup

from cocoa.extensions import db
from cocoa.helpers.html import safe_html
from cocoa.helpers.common import str2list
from cocoa.modules.book.models import Book, BookExtra

_basedir = dirname(__file__)

def _get_attr(name, content, mod=None):

    re_author = 'Author:(.*)'
    re_publisher = 'Publisher:(.*)'
    re_pages = 'Pages:(.*)'
    re_published = 'Published:(.*)'
    re_language = 'Language:\n.*\n(.*)'
    re_binding = 'Binding:(.*)'
    re_price = 'List Price:(.*)'

    if mod is None:
        m = re.search(eval('re_' + name), content)
    else:
        m = re.search(eval('re_' + name), content, mod)

    if m is not None:
        return m.group(1).strip()
    else:
        return None


def grab():

    # 计数器文件
    counter_file = open(join(_basedir, 'counter.txt'), 'r+')
    counter = int(counter_file.readline()) or 1
    # 索引文件
    index_file = open(join(_basedir, 'records.txt'), 'r')

    line = 1
    while (True):
        if line == counter: break
        index_file.readline()
        line += 1

    for line in iter(index_file.readline, b''):
        # retrieve the isbn13 number
        re_isbn13 =  '.*(978\d{10}).*'
        try:
            amazon_doc = urlopen(line).read()
            m = re.search(re_isbn13, amazon_doc)
            
            if m is None:
                continue
            else:
                isbn13 = m.group(1)
        except URLError:
            print URLError
            continue

        # get html doc
        url = 'http://www.openisbn.com/isbn/%s' % isbn13
        print url
        try:
            html_doc = urlopen(url).read()
        except URLError:
            print URLError
            continue

        soup = BeautifulSoup(html_doc, 'html5lib')
        title = soup.find('div', class_='PostHead').string.strip()

        content = soup.find('div', class_='PostContent').prettify()

        author = str2list(_get_attr('author', content))
        publisher = _get_attr('publisher', content)
        pages = _get_attr('pages', content)
        language = _get_attr('language', content, re.M)
        binding = _get_attr('binding', content)
        price, currency = _get_attr('price', content).split(' ')

        book = Book(isbn13, title, author, publisher,
                    price, pages=pages)
        book.set_language(language)
        book.set_binding(binding)
        book.set_currency(currency)

        intro = soup.find('div', class_='div')
        if intro.font is not None:
            intro.font.extract()
        intro = safe_html(intro.prettify())
        if intro[-3:] == u'海报：':
            intro = intro[:-3].strip()

        book.extra = BookExtra(intro)
        book.save()
        break

        # update counter and the counter file
        counter += 1
        counter_file.seek(0)
        counter_file.write(str(counter) + '\n')
    # end for

    counter_file.close()
    index_file.close()
