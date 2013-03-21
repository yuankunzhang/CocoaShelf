# -*- coding: utf-8 -*-
"""
    通用帮助函数
    2013.03.01
"""
import re

from datetime import datetime

from unidecode import unidecode

from flask.ext.babel import gettext, ngettext

def timesince(dt, default=None):

    if default is None:
        default = gettext('just now')

    now = datetime.now()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue
        if period < 0:
            break

        singular = u'%%(num)d %s ago' % singular
        plural = u'%%(num)d %s ago' % plural

        return ngettext(singular, plural, num=period)

    return default


def str2list(valuelist, seperator=',', remove_duplicates=True):

    data = []

    if valuelist:
        data = [x.strip() for x in valuelist.split(seperator)]

    if remove_duplicates:
        data = list(_remove_duplicates(data))

    return data

def _remove_duplicates(seq):

    d = {}
    for item in seq:
        if item.lower() not in d:
            d[item.lower()] = True
            yield item


def slugify(text, delim=u'-'):

    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    max_len = 10

    result = []
    text = text[:max_len]
    for word in _punct_re.split(text.lower()):
        if unidecode(word).split() != u'[?]':
            result.extend(unidecode(word).split())
    return unicode(delim.join(result))
