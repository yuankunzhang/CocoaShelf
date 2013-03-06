# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser

class HTMLStripper(HTMLParser):

    def __init__(self, safe_tags=None):
        self.reset()
        self.fed = []
        self.safe_tags = safe_tags or []

    def handle_starttag(self, tag, attrs):
        if tag in self.safe_tags:
            self.fed.append('<' + tag + '>')

    def handle_endtag(self, tag):
        if tag in self.safe_tags:
            self.fed.append('<' + tag + '>')

    def handle_startendtag(self, tag, attrs):
        if tag in self.safe_tags:
            self.fed.append('<' + tag + '>')

    def handle_data(self, data):
        self.fed.append(data)

    def get(self):
        return ''.join(self.fed)


def strip_tags(content, safe_tags=None):

    s = HTMLStripper(safe_tags=safe_tags)
    s.feed(content)
    return s.get()


def nl2br(content):

    return '<br>'.join(content.split('\n'))


def safe_html(content, safe_tags=None):

    if content == None:
        return ''

    safe_tags = safe_tags or ('b', 'i', 'u', 'a')
    return strip_tags(content, safe_tags).strip()
