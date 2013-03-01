# -*- coding: utf-8 -*-
"""
    通用帮助函数
    2013.03.01
"""
from datetime import datetime

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
